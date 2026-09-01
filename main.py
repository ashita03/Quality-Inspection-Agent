import sys
from agent.db import init_db
from agent.graph import build_graph


def run_inspection(image_path: str, part_id: str):
    init_db()
    graph = build_graph()

    initial_state = {
        "image_path": image_path,
        "part_id": part_id,
        "reasoning_trace": [],
    }

    result = graph.invoke(initial_state)

    print("\n=== INSPECTION RESULT ===")
    print(f"Part ID:  {result['part_id']}")
    print(f"Verdict:  {result['verdict'].upper()}")
    print(f"Defect:   {result.get('defect_type')} (confidence: {result.get('confidence')})")
    print("\n--- Agent reasoning trace ---")
    for line in result["reasoning_trace"]:
        print(f"  - {line}")
    print()

    return result


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <image_path> <part_id>")
        sys.exit(1)

    run_inspection(sys.argv[1], sys.argv[2])