import sys
from agent.tools import inspect_image_node

if len(sys.argv) != 2:
    print("Usage: python3 debug_vision.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

result = inspect_image_node({"image_path": image_path, "reasoning_trace": []})

print("\n=== RAW MODEL OUTPUT (unparsed) ===")
print(result["raw_model_output"])
print("\n=== PARSED RESULT ===")
print(f"defect_detected: {result['defect_detected']}")
print(f"defect_type:     {result['defect_type']}")
print(f"confidence:       {result['confidence']}")