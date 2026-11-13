import json

transcript_path = r'C:\Users\Bhaskr Singh\.gemini\antigravity\brain\c1ea3ed7-b9d2-437a-b7aa-f0cb4004681b\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get('step_index')
        if idx in [40506, 40559, 40644]:
            print(f"=== STEP {idx} ===")
            print(obj.get('content'))
