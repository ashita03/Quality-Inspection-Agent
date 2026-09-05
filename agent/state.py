from typing import TypedDict, Optional, List


class InspectionState(TypedDict):
    # --- inputs (set before the graph runs) ---
    image_path: str
    part_id: str

    # --- filled in by the inspect_image node ---
    defect_detected: Optional[bool]
    defect_type: Optional[str]        # e.g. "scratch", "crack", "none"
    confidence: Optional[float]       # 0.0 - 1.0
    raw_model_output: Optional[str]   # full text response, useful for debugging
    equipment_type: Optional[str]     # e.g. "screw", "bolt", "bottle cap"
    notes: Optional[str]              # plain-language description of what the model saw

    # --- filled in by the check_history node ---
    recent_defect_count: Optional[int]   # how many similar defects recently
    history_flag: Optional[bool]         # True if this defect type is spiking

    # --- filled in by the decision / terminal nodes ---
    verdict: Optional[str]            # "pass", "fail", "escalate"
    reasoning_trace: List[str]        # human-readable log of what the agent did/d