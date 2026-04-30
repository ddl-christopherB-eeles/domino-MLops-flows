from pathlib import Path

metadata_path = Path("/workflow/inputs/metadata")
result_path = Path("/workflow/outputs/result")

# Read the declared input without assuming whether Flows encoded it as
# msgpack or JSON/Struct.
metadata_bytes = metadata_path.read_bytes()
print(f"Received metadata input with {len(metadata_bytes)} bytes")

result_path.parent.mkdir(parents=True, exist_ok=True)
result_path.write_text("ok")
