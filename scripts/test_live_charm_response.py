import urllib.request
import json

payload = {
    "name": "Anjali Sharma",
    "day": 10,
    "month": 6,
    "year": 1990,
    "question": "Is 2026 better for my career prospects? and what how will it unfold?",
    "pob": "New Delhi",
    "tob": "10:30",
    "user_id": "test_user_anjali"
}

req = urllib.request.Request(
    "http://127.0.0.1:8000/api/v1/readings/ask",
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print("STATUS:", resp.status)
        print("DIRECT_ANSWER SNIPPET:")
        direct_ans = data.get("direct_answer", "")
        # print first 500 chars and last 500 chars
        print(direct_ans[:400].encode('ascii', errors='replace').decode('ascii'))
        print("...")
        print(direct_ans[-600:].encode('ascii', errors='replace').decode('ascii'))
except Exception as e:
    print("ERROR:", e)
