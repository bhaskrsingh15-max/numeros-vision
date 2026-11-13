# Numeros Vision — Chaldean Name Engine & Balancing
**Document Type:** Engine Specification
**Engine Module:** `app/engine/cheiro_engine.py` & `app/engine/name_balancing_engine.py`

## 1. Canonical Letter Vibration Map
- **1:** A, I, J, Q, Y
- **2:** B, K, R
- **3:** C, G, L, S
- **4:** D, M, T
- **5:** E, H, N, X
- **6:** U, V, W
- **7:** O, Z
- **8:** F, P
- **9:** Sacred Vibration (not assigned to single letters; appears only as compound sum or reduced total).

## 2. Name Balancing Flow
1. Compute exact compound sum from character trace.
2. Reduce compound sum to single root number (1-9).
3. Evaluate compatibility between single root and native Driver/Conductor.
4. If friction exists, generate candidate variations (adding or substituting letters) strictly preserving phonetic elegance.
5. Rank candidates by compound auspiciousness and driver harmony. Disclose calculations; user selects preference.
