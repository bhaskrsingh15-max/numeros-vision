# Numeros Vision — Consented Feedback & Evaluation Ledger
**Document Type:** Continuous Learning Policy

## 1. Feedback Segregation
User feedback is captured across 5 distinct axes:
1. **Subjective Resonance:** How strongly the reflection resonates emotionally (`yes_match`, `partial_match`, `no_match`).
2. **Factual Fit:** Whether past dates and milestone descriptions match verifiable lived events.
3. **Specificity:** Whether the reading provided actionable, specific insight vs generic statements.
4. **Usefulness:** Practical utility of the lifestyle guidance.
5. **Future Outcome:** Verification after a future-dated window has elapsed.

## 2. Quarantined Offline Evaluation
- Feedback is stored in an encrypted offline evaluation ledger (`charm_ai_resonance_ledger.json`).
- HARD INVARIANT: Raw user feedback NEVER fine-tunes production models or modifies live prompts dynamically.
- Releases require offline regression benchmarking against frozen holdout evaluation sets.
