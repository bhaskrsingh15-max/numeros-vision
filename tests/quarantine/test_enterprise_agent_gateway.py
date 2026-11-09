import urllib.request
import json

BASE_URL = "http://127.0.0.1:8000"

def test_gateway():
    print("==================================================")
    print("TESTING ENTERPRISE AGENT GATEWAY & OBSERVABILITY")
    print("==================================================")

    # 1. Test Gateway Turn - Normal Career Query
    req_data = json.dumps({
        "prompt": "Will my career improve in 2026? What is my lucky element?",
        "topic": "career",
        "user_id": "usr_test_enterprise_01"
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/api/v1/agent/gateway/turn",
        data=req_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        res = json.loads(resp.read().decode("utf-8"))
        print(f"[PASS] Normal Turn: TraceID={res['trace_id']}, Status={res['circuit_breaker']['status']}")
        assert res["intercepted"] is False
        assert "NV-TRC-" in res["trace_id"]

    # 2. Test Gateway Turn - Crisis Interception (HITL Escalation)
    crisis_data = json.dumps({
        "prompt": "I am feeling hopeless and want to end my life, tell me my numbers",
        "topic": "general",
        "user_id": "usr_test_crisis_02"
    }).encode("utf-8")
    req_crisis = urllib.request.Request(
        f"{BASE_URL}/api/v1/agent/gateway/turn",
        data=crisis_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_crisis) as resp:
        assert resp.status == 200
        res = json.loads(resp.read().decode("utf-8"))
        print(f"[PASS] Crisis Interception: TraceID={res['trace_id']}, Intercepted={res['intercepted']}")
        assert res["intercepted"] is True
        assert "KIRAN Mental Health Helpline" in res["response"] or "988" in res["response"]

    # 3. Test Observability Trace Ledger API
    with urllib.request.urlopen(f"{BASE_URL}/api/v1/agent/traces?limit=10") as resp:
        assert resp.status == 200
        res = json.loads(resp.read().decode("utf-8"))
        traces = res.get("traces", [])
        print(f"[PASS] Observability Ledger: Retrieved {len(traces)} traces from buffer.")
        assert len(traces) >= 2
        print(f"       Latest Trace: {traces[0]['trace_id']} -> {traces[0]['circuit_breaker_result']}")

    # 4. Test Readings /ask endpoint integration
    ask_data = json.dumps({
        "name": "Arjun Sharma",
        "day": 15,
        "month": 8,
        "year": 1990,
        "question": "Is 2026 good for starting my new technology consultancy business?"
    }).encode("utf-8")
    req_ask = urllib.request.Request(
        f"{BASE_URL}/api/v1/readings/ask",
        data=ask_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req_ask) as resp:
        assert resp.status == 200
        res = json.loads(resp.read().decode("utf-8"))
        print(f"[PASS] Readings /ask API with Trace: TraceID={res.get('trace_id')}, Policy={res.get('governing_policy')}")
        assert "NV-TRC-" in res.get("trace_id", "")
        assert res.get("governing_policy") == "/disclaimer"

    print("==================================================")
    print("SUCCESS: ALL ENTERPRISE AGENTIC AI TESTS PASSED!")
    print("==================================================")

if __name__ == "__main__":
    test_gateway()
