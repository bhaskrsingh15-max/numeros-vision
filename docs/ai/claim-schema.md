# Numeros Vision — Structured Claim Schema
**Document Type:** AI & Evidence Contract

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NumerosVisionClaim",
  "type": "object",
  "properties": {
    "claim_id": {"type": "string"},
    "reading_id": {"type": "string"},
    "system_id": {"type": "string", "enum": ["loshu", "chaldean", "cheiro", "pythagorean", "vedic_numerology", "kp_astrology", "bnn_astrology", "vedic_astrology", "lal_kitab"]},
    "system_family_id": {"type": "string", "enum": ["numerology_core", "acoustics", "numerology_comparative", "astrology_classical", "astrology_nadi", "astrology_remedial"]},
    "theme_ids": {"type": "array", "items": {"type": "string"}},
    "time_window": {
      "type": "object",
      "properties": {
        "start": {"type": ["string", "null"]},
        "end": {"type": ["string", "null"]},
        "is_timeless": {"type": "boolean"}
      }
    },
    "direction": {"type": "string", "enum": ["positive", "challenging", "mixed", "neutral"]},
    "support_type": {"type": "string", "enum": ["deterministic_result", "traditional_interpretation", "retrieved_source", "lifestyle_guidance"]},
    "source_refs": {"type": "array", "items": {"type": "string"}},
    "mapping_status": {"type": "string", "enum": ["reviewed", "direct", "ambiguous"]},
    "conflict_status": {"type": "string", "enum": ["none", "convergent", "conflicted"]}
  },
  "required": ["claim_id", "system_id", "system_family_id", "theme_ids", "direction", "support_type"]
}
```
