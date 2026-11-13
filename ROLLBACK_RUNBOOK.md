# NUMEROS VISION & CHARM AI — ROLLBACK RUNBOOK
**Version:** 1.0.0  
**Effective Date:** 2026-10-29  
**Target:** Safe, instant reversion of changes without data loss or downtime.

---

## 1. Quick Disabling via Feature Flags

### A. Disable Nadi Event Intelligence Engine Instantly
If the Nadi Event Engine must be disabled without restarting or redeploying code:
1. Set the environment variable:
   ```powershell
   $env:NADI_EVENT_ENGINE_ENABLED = "False"
   ```
2. Or in `.env`:
   ```ini
   NADI_EVENT_ENGINE_ENABLED=False
   ```
3. When disabled, `app/engine/nadi_event_engine.py` immediately returns `{"status": "ENGINE_DISABLED"}` and routes standard queries exclusively to the baseline numerology engine.

---

## 2. Reverting Frontend Content Changes

If any public HTML file or template needs to be restored:
1. Previous versions are tracked in Git / conversation history.
2. The static distribution package is maintained at `dist_cloudflare_pages/`.
3. To rebuild the distribution at any time:
   ```powershell
   python build_bulletproof_dist.py
   ```
4. To test locally:
   ```powershell
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

---

## 3. Knowledge Registries Rollback

If any JSON registry needs to be rolled back:
- Registries are isolated JSON files in `data/knowledge_base/`:
  - `nadi_event_rules.json`
  - `nadi_profession_rules.json`
  - `nadi_remedy_rules.json`
- Deleting or renaming any file reverts the engine to the hard-coded baseline defaults with zero crashes.

---

## 4. Verification Checkpoint

After any rollback, execute the regression test suite to ensure system integrity:
```powershell
python -m unittest tests/test_nadi_event_engine.py tests/test_professional_engine.py tests/test_evidence_prediction_engine.py tests/test_day8_rag_and_twin_paradox.py
```
All 15 tests must report `OK`.
