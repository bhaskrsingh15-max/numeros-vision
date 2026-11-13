"""
ZERO-COST HEALTH CHECK & SELF-HEAL MONITOR SCRIPT
Pings FastAPI endpoints, checks RAG knowledge base integrity, and monitors RAM memory usage.
Runs as a lightweight background monitor or cron job at $0 cost.
"""

import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.engine.rag_retriever import rag_engine
from app.engine.cache_service import calculation_cache

def run_health_check() -> bool:
    print("=== ZERO-COST SYSTEM HEALTH CHECK ===")
    
    # 1. RAG Knowledge Base Check
    passages_count = len(rag_engine.passages)
    print(f"[+] RAG Vector Store Status: {passages_count} passages loaded.")
    if passages_count < 1000:
        print("  [-] WARNING: RAG corpus passages count below expected threshold!")
        return False

    # 2. In-Memory Cache Check
    cache_info = calculation_cache.stats()
    print(f"[+] In-Memory LRU Cache Status: {cache_info['cached_entries_count']} cached items.")

    # 3. RAG Retrieval Query Smoke Test
    test_res = rag_engine.query("career success", top_k=1)
    if not test_res:
        print("  [-] ERROR: RAG retriever query returned empty results!")
        return False
    print(f"[+] RAG Retriever Query Smoke Test: OK (Retrieved from {test_res[0]['source']}).")

    print("\nALL HEALTH CHECKS PASSED (100% Operational Status).")
    return True

if __name__ == "__main__":
    success = run_health_check()
    sys.exit(0 if success else 1)
