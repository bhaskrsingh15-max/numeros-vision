# NUMEROS VISION & CHARM AI — ROLLBACK & DISASTER RECOVERY PROTOCOL
**Document Version**: 2.0.0  
**Effective Date**: 2026-10-29  
**Master Standard**: `Numeros_Vision_Google_Antigravity_Master_Implementation_v2.md`

---

## 1. Rollback Policy & Safety Guarantees

All changes introduced in Release 2.0.0 are strictly **additive and non-destructive**. No existing calculation engines, database models, or legacy API endpoints were deleted or replaced.

If a rollback is required for operational or verification reasons, follow the step-by-step procedure below to restore the repository to its baseline state.

---

## 2. Step-by-Step Rollback Instructions

### Step 1: Revert Modified Python & Static Files
If reverting engine hardening or UI tweaks, execute the following file restorations:

1. **Revert `app/engine/rag_retriever.py`**:
   Remove the provenance filtering block added to `_load_and_index_corpus()` at line 100:
   ```python
   # Remove:
   status = (p.get("status") or "").lower()
   if status in ("needs_review", "pending_ocr", "draft", "unapproved", "rejected"):
       continue
   if any(marker in str(raw_prov).lower() for marker in ("pending", "draft", "needs_review", "unapproved")):
       continue
   ```

2. **Revert `app/charm/chat/response_composer.py`**:
   Restore `timing_status` at line 313 to its previous formatting:
   ```python
   timing_status=(
       f"Cycle Status: {'Verified Temporal Window' if 'VERIFIED' in consensus.verification_status else 'Temporal Baseline'} · "
       f"Momentum: {'Favorable Alignment' if 'ACCELERATED' in consensus.event_assessment else 'Steady Rhythm'} · "
       f"Planning Horizon: {intent.requested_horizon.replace('_', ' ')}"
   ),
   ```

3. **Revert `app/static/js/nv_profile_sync.js`**:
   Restore modal heading `<h3 id="nv-modal-heading">` to previous inline text if necessary.

---

### Step 2: Remove Additive Knowledge and Registry Deliverables
To remove newly created registries without affecting runtime execution:

1. Remove formula registry:
   - `data/knowledge_base/formula_registry.json`
2. Remove knowledge analysis files:
   - `knowledge/analysis/consensus_matrix.csv`
   - `knowledge/analysis/unique_methods.csv`
   - `knowledge/analysis/conflict_register.csv`
   - `knowledge/analysis/gap_register.csv`
   - `knowledge/analysis/method_authority_registry.yaml`
3. Remove per-book review registers:
   - `knowledge/books/B1_you_and_your_name/`
   - `knowledge/books/B2_chaldean_numerology/`
   - `knowledge/books/B3_chinese_numerology/`
   - `knowledge/books/B4_numbers_meaning_magic/`
   - `knowledge/books/B5_numerology_magic_numbers/`
   - `knowledge/books/B6_understanding_numerology/`
4. Remove test fixtures:
   - `tests/test_formula_registry.py`

---

### Step 3: Restart ASGI Server
After performing file adjustments, restart Uvicorn:
```powershell
# Kill running task or process on port 8000
# Restart server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

---

## 3. Verification Post-Rollback
Verify that core calculations remain functional by running:
```powershell
python -m unittest tests/test_cheiro_engine.py
```
Ensure that `Ran 7 tests ... OK` is achieved.
