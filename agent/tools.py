"""
This module holds the actual work-functions the agent calls: looking at
an image, checking history, and writing to the DB.

Note on terminology: in a "ReAct-style" LangChain agent, these would be
wrapped with @tool and the LLM would freely choose which to call and when.
In LangGraph, we're being more explicit: each of these becomes a NODE in
the graph, and WE decide the wiring (which is more predictable and easier
to debug for a pipeline like this). The LLM still does the actual
reasoning/decision-making inside the inspect_image node and inside the
conditional edge — it's just that the *shape* of the pipeline is fixed
by us, not improvised by the model. This is a deliberate design choice
worth explaining in your README.
"""

import base64
import json
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

# Change this if you pulled a different model, e.g. "qwen2-vl"
VISION_MODEL = "llava"

_llm = ChatOllama(model=VISION_MODEL, temperature=0)


def _encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


INSPECTION_PROMPT = """You are a strict quality control inspector examining a product image
from a manufacturing line. Your job is to catch defects that a careless inspector would
miss - not just dramatic breaks.

Look carefully for ANY of the following, however subtle:
- Cracks or fractures, even hairline ones
- Scratches or surface marks
- Dents or deformation
- Rust, corrosion, oxidation, or discoloration
- Thread damage, stripping, or irregular thread spacing (for screws/bolts)
- Contamination, dust, debris, or foreign material stuck to the part
- Missing components or misalignment
- Any wear that looks inconsistent with a brand-new, unused part

Do NOT default to "no defect" just because nothing is catastrophically broken. A used,
worn, rusted, or dusty part is still a defect for QC purposes - manufacturing QC should
catch even minor deviations from a pristine part. Only say "none" if the part genuinely
looks flawless and new.

First, briefly think through what you observe in 1-2 sentences. Then, on a new line,
respond with ONLY a JSON object, no other text, in this exact format:
{
  "defect_detected": true or false,
  "defect_type": "scratch" | "crack" | "dent" | "discoloration" | "contamination" | "corrosion" | "thread_damage" | "none",
  "confidence": a number between 0.0 and 1.0,
  "notes": "one short sentence describing what you see"
}
"""


def inspect_image_node(state: dict) -> dict:
    """
    LangGraph node: sends the image to the local vision model and parses
    its verdict into the state.
    """
    image_b64 = _encode_image(state["image_path"])

    message = HumanMessage(
        content=[
            {"type": "text", "text": INSPECTION_PROMPT},
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{image_b64}",
            },
        ]
    )

    response = _llm.invoke([message])
    raw_text = response.content

    # Vision models are inconsistent about sticking to pure JSON, so we
    # defensively extract the {...} block rather than assuming clean output.
    try:
        start = raw_text.index("{")
        end = raw_text.rindex("}") + 1
        parsed = json.loads(raw_text[start:end])
    except (ValueError, json.JSONDecodeError):
        parsed = {
            "defect_detected": False,
            "defect_type": "none",
            "confidence": 0.0,
            "notes": "Could not parse model output.",
        }

    trace_line = (
        f"inspect_image: defect_detected={parsed.get('defect_detected')}, "
        f"type={parsed.get('defect_type')}, confidence={parsed.get('confidence')} "
        f"-> {parsed.get('notes')}"
    )

    return {
        "defect_detected": parsed.get("defect_detected", False),
        "defect_type": parsed.get("defect_type", "none"),
        "confidence": float(parsed.get("confidence", 0.0)),
        "raw_model_output": raw_text,
        "notes": parsed.get("notes", ""),
        "reasoning_trace": state.get("reasoning_trace", []) + [trace_line],
    }