import base64
import json
from langchain_ollama import ChatOllama

# Change this if you pulled a different model, e.g. "qwen2-vl"
VISION_MODEL = "llava"

_llm = ChatOllama(model=VISION_MODEL, temperature=0)


def _encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


INSPECTION_PROMPT = """You are a quality control inspector examining a product image
from a manufacturing line. Look carefully for any visible defects: scratches,
cracks, dents, discoloration, missing parts, misalignment, or contamination.

Respond ONLY with a JSON object, no other text, in this exact format:
{
  "defect_detected": true or false,
  "defect_type": "scratch" | "crack" | "dent" | "discoloration" | "contamination" | "none",
  "confidence": a number between 0.0 and 1.0,
  "notes": "one short sentence describing what you see"
}
"""


def inspect_image_node(state: dict) -> dict:
    image_b64 = _encode_image(state["image_path"])

    message = {
        "role": "user",
        "content": INSPECTION_PROMPT,
        "images": [image_b64],
    }

    response = _llm.invoke([message])
    raw_text = response.content

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
        "reasoning_trace": state.get("reasoning_trace", []) + [trace_line],
    }