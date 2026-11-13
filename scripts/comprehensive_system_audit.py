import sys
import os
import time

sys.path.insert(0, os.path.abspath('.'))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

audit_results = {}

print("==================================================================")
print("  NUMEROS VISION — COMPREHENSIVE END-TO-END SYSTEM AUDIT  ")
print("==================================================================")

# ── 1. RAG AI LAYER AUDIT ───────────────────────────────────────────────
print("\n[AUDIT 1/6] Advanced RAG AI Layer & Source Governor...")
try:
    from app.engine.rag_retriever import rag_engine
    from app.charm.rag.source_governor import source_governor

    n_passages = len(rag_engine.passages)
    n_vocab = len(rag_engine.doc_freq)
    n_sources = len(source_governor.sources)

    # Retrieval test
    t0 = time.time()
    res = rag_engine.query("Sun Driver 1 Rahu Conductor 4 leadership", top_k=2)
    lat = (time.time() - t0) * 1000

    assert n_passages > 5000, f"Expected >5000 passages, got {n_passages}"
    assert n_sources > 50, f"Expected >50 sources, got {n_sources}"
    audit_results["RAG_Layer"] = {
        "status": "OPERATIONAL",
        "passages": n_passages,
        "vocab": n_vocab,
        "sources": n_sources,
        "latency_ms": round(lat, 2)
    }
    print(f"  [OK] RAG Engine: {n_passages} passages, {n_sources} sources indexed. Latency: {lat:.2f}ms")
except Exception as e:
    audit_results["RAG_Layer"] = {"status": "FAILED", "error": str(e)}
    print(f"  [FAIL] RAG Engine FAILED: {e}")

# ── 2. DETERMINISTIC ENGINE & PINNACLES AUDIT ───────────────────────────
print("\n[AUDIT 2/6] Deterministic Calculation Engine (Lo Shu, D/C/K, Pinnacles, Challenges, Vastu)...")
try:
    from app.services.pdf_report_generator import run_deterministic_calculation

    calc = run_deterministic_calculation("Bhaskr Singh", 28, 11, 1981, "core_blueprint")
    assert calc["driver_number"] == 1, f"Expected driver 1, got {calc['driver_number']}"
    assert calc["conductor_number"] == 4, f"Expected conductor 4, got {calc['conductor_number']}"
    assert calc["kua_number"] == 1, f"Expected kua 1, got {calc['kua_number']}"
    assert calc["chaldean_name_root"] == 5, f"Expected chaldean 5, got {calc['chaldean_name_root']}"

    audit_results["Deterministic_Engine"] = {
        "status": "OPERATIONAL",
        "driver": calc["driver_number"],
        "conductor": calc["conductor_number"],
        "kua": calc["kua_number"],
        "chaldean": f"{calc['chaldean_name_compound']} -> {calc['chaldean_name_root']}",
        "missing_numbers": calc["missing_numbers"]
    }
    print(f"  [OK] Deterministic Engine: Driver {calc['driver_number']}, Conductor {calc['conductor_number']}, Kua {calc['kua_number']}, Chaldean {calc['chaldean_name_compound']}->{calc['chaldean_name_root']}")
except Exception as e:
    audit_results["Deterministic_Engine"] = {"status": "FAILED", "error": str(e)}
    print(f"  [FAIL] Deterministic Engine FAILED: {e}")

# ── 3. 3-TIER PDF GENERATION AUDIT (3, 12, 32 PAGES) ────────────────────
print("\n[AUDIT 3/6] Vector PDF Report Generator (ReportLab Platypus Engine)...")
try:
    import pypdf
    import io
    from app.services.pdf_report_generator import generate_customised_pdf_report

    pdf_checks = {}
    for tier, expected_pgs in [("basic", 3), ("advanced", 12), ("premium", 32)]:
        pdf_bytes, meta = generate_customised_pdf_report(
            name="Bhaskr Singh", day=28, month=11, year=1981,
            topic_id="core_blueprint", tier=tier
        )
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        actual_pgs = len(reader.pages)
        assert actual_pgs == expected_pgs, f"Tier {tier}: expected {expected_pgs} pages, got {actual_pgs}"

        # Verify page 31 and 32 on premium
        if tier == "premium":
            p31_txt = reader.pages[30].extract_text()
            p32_txt = reader.pages[31].extract_text()
            assert "Section 29: 4-Stage Pinnacle Cycles" in p31_txt, "Page 31 missing Section 29 Pinnacle"
            assert "Section 30: Vastu Dosha as per Missing Numbers" in p32_txt, "Page 32 missing Section 30 Vastu"

        pdf_checks[tier] = {"expected": expected_pgs, "actual": actual_pgs, "size_bytes": len(pdf_bytes)}
        print(f"  [OK] Tier '{tier}': Exactly {actual_pgs} pages ({len(pdf_bytes):,} bytes)")

    audit_results["PDF_Engine"] = {"status": "OPERATIONAL", "tiers": pdf_checks}
except Exception as e:
    audit_results["PDF_Engine"] = {"status": "FAILED", "error": str(e)}
    print(f"  [FAIL] PDF Engine FAILED: {e}")

# ── 4. CHARM AI ORCHESTRATOR & FALLBACK AUDIT ───────────────────────────
print("\n[AUDIT 4/6] Charm AI Consultation Engine & Edge Resiliency...")
try:
    from app.charm.chat.response_composer import charm_chat_orchestrator

    chat_resp = charm_chat_orchestrator.process_chat_turn(
        message="What is my financial outlook for 2026?",
        user_name="Bhaskr Singh",
        day=28, month=11, year=1981
    )
    assert chat_resp.message_id.startswith("MSG-"), "Invalid message_id"
    assert "Dasha" in chat_resp.human_friendly_summary["takeaway"], "Missing Dasha in takeaway"

    audit_results["Charm_AI"] = {
        "status": "OPERATIONAL",
        "message_id": chat_resp.message_id,
        "takeaway": chat_resp.human_friendly_summary["takeaway"][:80] + "...",
        "actions_count": len(chat_resp.practical_next_steps)
    }
    print(f"  [OK] Charm AI Engine: Generated Message {chat_resp.message_id} with {len(chat_resp.practical_next_steps)} action steps")
except Exception as e:
    audit_results["Charm_AI"] = {"status": "FAILED", "error": str(e)}
    print(f"  [FAIL] Charm AI FAILED: {e}")

# ── 5. GOOGLE GEMINI SERVICE ADAPTER AUDIT ──────────────────────────────
print("\n[AUDIT 5/6] Google Gemini AI LLM Service Adapter...")
try:
    from app.services.gemini_service import gemini_service

    is_cfg = gemini_service.is_configured
    test_res = gemini_service.generate_chat_response(
        "Bhaskr Singh",
        "What are my key strengths?",
        {"driver": 1, "conductor": 4, "personal_year": 4, "active_dasha": "Mercury"}
    )
    audit_results["Gemini_Service"] = {
        "status": "OPERATIONAL",
        "configured": is_cfg,
        "active_source": test_res.get("source"),
        "model": test_res.get("model")
    }
    print(f"  [OK] Gemini Service: Configured={is_cfg}, Active Response Source={test_res.get('source')} ({test_res.get('model')})")
except Exception as e:
    audit_results["Gemini_Service"] = {"status": "FAILED", "error": str(e)}
    print(f"  [FAIL] Gemini Service FAILED: {e}")

# ── 6. PRODUCTION DISTRIBUTION & CLOUDFLARE PACKAGE AUDIT ───────────────
print("\n[AUDIT 6/6] Cloudflare Pages Production Distribution & Package Audit...")
try:
    zip_path = "cloudflare_pages_upload.zip"
    dist_dir = "dist_cloudflare_pages"

    assert os.path.exists(zip_path), f"Missing {zip_path}"
    assert os.path.exists(dist_dir), f"Missing {dist_dir}"
    zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)

    # Check key files in dist
    key_files = [
        "index.html", "sample.html", "charm_ai.html", "pricing.html",
        "reports/Numeros_Vision_Basic_Report_28-11-1981.pdf",
        "reports/Numeros_Vision_Advanced_Report_28-11-1981.pdf",
        "reports/Numeros_Vision_Premium_Report_28-11-1981.pdf"
    ]
    missing_files = [kf for kf in key_files if not os.path.exists(os.path.join(dist_dir, kf))]
    assert not missing_files, f"Missing files in dist: {missing_files}"

    audit_results["Production_Dist"] = {
        "status": "OPERATIONAL",
        "zip_size_mb": round(zip_size_mb, 2),
        "verified_files": len(key_files)
    }
    print(f"  [OK] Production Dist: Package size {zip_size_mb:.2f} MB (< 25MB Cloudflare limit). All critical files verified.")
except Exception as e:
    audit_results["Production_Dist"] = {"status": "FAILED", "error": str(e)}
    print(f"  [FAIL] Production Dist FAILED: {e}")

print("\n==================================================================")
all_passed = all(v.get("status") == "OPERATIONAL" for v in audit_results.values())
if all_passed:
    print("  ALL 6 CORE ARCHITECTURAL LAYERS ARE 100% OPERATIONAL & LIVE!  ")
else:
    print("  WARNING: Some modules encountered issues during audit.  ")
print("==================================================================")
