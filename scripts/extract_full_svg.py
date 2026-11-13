import json

transcript_path = r"C:\Users\Bhaskr Singh\.gemini\antigravity\brain\c1ea3ed7-b9d2-437a-b7aa-f0cb4004681b\.system_generated\logs\transcript_full.jsonl"

with open(transcript_path, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        obj = json.loads(line)
        if obj.get("step_index") == 1796:
            tc = obj["tool_calls"][0]
            content = tc["args"]["CodeContent"]
            with open("scratch/charm_sketch_full.svg", "w", encoding="utf-8") as out:
                out.write(content)
            print("Wrote scratch/charm_sketch_full.svg, length:", len(content))
            break
