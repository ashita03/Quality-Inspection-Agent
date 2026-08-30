from langgraph.graph import StateGraph, END
from agent.state import InspectionState
from agent.tools import inspect_image_node
from agent import db


# --- Node: check history -------------------------------------------------

def check_history_node(state: dict) -> dict:
    defect_type = state.get("defect_type", "none")
    recent_count = db.count_recent_defects(defect_type)

    # simple spike rule: 3+ of the same defect in the recent window = flag it
    history_flag = recent_count >= 3

    trace_line = (
        f"check_history: '{defect_type}' seen {recent_count}x recently "
        f"-> history_flag={history_flag}"
    )

    return {
        "recent_defect_count": recent_count,
        "history_flag": history_flag,
        "reasoning_trace": state.get("reasoning_trace", []) + [trace_line],
    }


# --- Conditional edge: the actual decision --------------------------------

def route_after_history(state: dict) -> str:
    if not state.get("defect_detected"):
        return "pass_node"
    return "escalate_node"


# --- Terminal nodes --------------------------------------------------------

def escalate_node(state: dict) -> dict:
    if state.get("confidence", 0.0) < 0.55:
        why = "low confidence defect call -> needs human review"
    elif state.get("history_flag"):
        why = f"'{state.get('defect_type')}' is spiking recently -> possible process issue"
    else:
        why = "confident defect detection -> failing part"

    reasoning = state.get("reasoning_trace", []) + [f"escalate_node: {why}"]
    final_state = {**state, "verdict": "escalate", "reasoning_trace": reasoning}
    db.insert_inspection(final_state)
    return {"verdict": "escalate", "reasoning_trace": reasoning}


def pass_node(state: dict) -> dict:
    reasoning = state.get("reasoning_trace", []) + [
        "pass_node: no significant defect found, part passes."
    ]
    final_state = {**state, "verdict": "pass", "reasoning_trace": reasoning}
    db.insert_inspection(final_state)
    return {"verdict": "pass", "reasoning_trace": reasoning}


# --- Build the graph ---------------------------------------------------

def build_graph():
    graph = StateGraph(InspectionState)

    graph.add_node("inspect_image", inspect_image_node)
    graph.add_node("check_history", check_history_node)
    graph.add_node("escalate_node", escalate_node)
    graph.add_node("pass_node", pass_node)

    graph.set_entry_point("inspect_image")
    graph.add_edge("inspect_image", "check_history")

    graph.add_conditional_edges(
        "check_history",
        route_after_history,
        {
            "escalate_node": "escalate_node",
            "pass_node": "pass_node",
        },
    )

    graph.add_edge("escalate_node", END)
    graph.add_edge("pass_node", END)

    return graph.compile()