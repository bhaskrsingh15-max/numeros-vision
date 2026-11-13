# NUMEROS VISION / CHARM AI — REGRESSION TEST REPORT
**Version:** 1.0.0  
**Execution Date:** 2026-10-29  
**Execution Environment:** Windows Server / Python 3.14 / Antigravity Sandbox  
**Overall Status:** ALL SUITES PASSING (100% SUCCESS RATE)

---

## 1. Test Suite Summary

| Suite Name | Target Module | Tests Run | Pass | Fail | Execution Time |
| :--- | :--- | :---: | :---: | :---: | :---: |
| `test_nadi_event_engine.py` | `app/engine/nadi_event_engine.py` | 7 | 7 | 0 | 0.002s |
| `test_professional_engine.py` | `app/engine/professional_numerology_engine.py` | 3 | 3 | 0 | 0.004s |
| `test_evidence_prediction_engine.py` | `app/engine/prediction_orchestrator.py` | 3 | 3 | 0 | 0.003s |
| `test_day8_rag_and_twin_paradox.py` | `app/engine/rag_retriever.py` & `twin_paradox_engine.py` | 2 | 2 | 0 | 0.002s |
| **TOTAL** | **Core Prediction & Retrieval Architecture** | **15** | **15** | **0** | **0.011s** |

---

## 2. Granular Test Case Results

### Suite A: `tests/test_nadi_event_engine.py`
1. `test_career_event_evaluation`: Verifies career query matches Numeros Vision Classical Archive Ch. 8, PDF p. 110, Group A hierarchy. **PASSED**.
2. `test_business_event_evaluation`: Verifies business query matches houses 2, 7, 10, 11 with Mercury significator. **PASSED**.
3. `test_property_event_evaluation`: Verifies property query matches houses 4, 11, 12 with Mars significator. **PASSED**.
4. `test_missing_dob_input`: Verifies missing DOB cleanly returns `MISSING_REQUIRED_INPUT`. **PASSED**.
5. `test_milestone_calibration_flow`: Verifies multi-milestone calibration returns `CALIBRATED_WITH_MILESTONES`. **PASSED**.
6. `test_pcpndt_statutory_circuit_breaker`: Verifies fetal sex inquiry triggers statutory block. **PASSED**.
7. `test_public_output_neutrality`: Verifies zero developer jargon and zero competitor leaks in public payload. **PASSED**.

### Suite B: `tests/test_professional_engine.py`
1. `test_driver_conductor_81_combinations`: Verifies deterministic 81 Driver-Conductor matrix calculations. **PASSED**.
2. `test_cheiro_chaldean_compound`: Verifies Cheiro compound number reductions. **PASSED**.
3. `test_lo_shu_grid_planes`: Verifies 3x3 Lo Shu magic square plane evaluations. **PASSED**.

### Suite C: `tests/test_evidence_prediction_engine.py`
1. `test_evidence_tier_separation`: Verifies E1 (Deterministic) through E4 (Empirical) classification. **PASSED**.
2. `test_abstention_standard`: Verifies system abstains rather than inventing dates when inputs are insufficient. **PASSED**.
3. `test_non_fatalistic_remedies`: Verifies remedies are non-coercive and safe. **PASSED**.

### Suite D: `tests/test_day8_rag_and_twin_paradox.py`
1. `test_bm25_retrieval_integrity`: Verifies BM25 corpus index loads 10,939 passages and returns relevant chunks. **PASSED**.
2. `test_twin_paradox_engine`: Verifies minute-level sub-lord differentiation for twin births (Classical Nadi Ch. 17). **PASSED**.
