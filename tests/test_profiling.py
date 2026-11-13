import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time
from app.engine.consensus import generate_consensus_reading
from app.engine.enterprise_agent_gateway import EnterpriseAgentGateway
from app.engine.question_explanation_engine import generate_simple_explanation_and_remedies
from app.engine.rag_retriever import rag_engine
from orchestrator import handle_question

q = "Is 2026 favorable for my career progression and new ventures?"
name = "Arjun Sharma"
day, month, year = 15, 8, 1990

print("Profiling sub-steps...")

t0 = time.time()
gw = EnterpriseAgentGateway.process_turn(q, "career", "test_user")
t1 = time.time()
print(f"1. EnterpriseAgentGateway: {(t1-t0)*1000:.2f} ms")

t0 = time.time()
cr = generate_consensus_reading(name, day, month, year)
t1 = time.time()
print(f"2. generate_consensus_reading: {(t1-t0)*1000:.2f} ms")

t0 = time.time()
expl = generate_simple_explanation_and_remedies(q, 6, 6, name=name, day=day, month=month, year=year)
t1 = time.time()
print(f"3. generate_simple_explanation_and_remedies: {(t1-t0)*1000:.2f} ms")

t0 = time.time()
rag = rag_engine.query(q, top_k=3)
t1 = time.time()
print(f"4. rag_engine.query: {(t1-t0)*1000:.2f} ms")

t0 = time.time()
user_profile = {
    "phase1_result": {"driver": 6, "conductor": 6},
    "phase2_result": {"rashi_vs_driver": "neutral"}
}
orch = handle_question(q, user_profile, current_age=35, day=day, month=month, year=year)
t1 = time.time()
print(f"5. orchestrator handle_question: {(t1-t0)*1000:.2f} ms")
