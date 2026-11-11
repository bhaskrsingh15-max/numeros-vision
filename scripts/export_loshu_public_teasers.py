"""
Deterministic Public Teaser Compiler for Lo Shu Curiosity Block (Mockup A)
==========================================================================
Reads ONLY `topics.loshu_curiosity_teasers` from `app/data/basic_report_content_library.json`
and writes a sanitized, public-safe JSON slice to `app/static/data/loshu_public_teasers.json`.

Security & IP Protection Gate:
- NEVER exports `depth_1_basic`, `depth_2_advanced`, `depth_3_premium`, `ninety_day_plan`,
  `driver_conductor` 81-pair prose, or `elements.*.states.*.remedy` paid report text.
- Fails hard if any paid paragraph substring (`>= 45` chars) from paid report keys appears
  anywhere in the exported browser JSON.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_LIB_PATH = ROOT / "app" / "data" / "basic_report_content_library.json"
PUBLIC_OUT_PATH = ROOT / "app" / "static" / "data" / "loshu_public_teasers.json"


def collect_paid_prose_fragments(lib: dict) -> list[str]:
    """Collects all paid report prose strings from depth_1/2/3, remedies, and 90-day plans."""
    paid_strings: list[str] = []
    topics = lib.get("topics", {})
    for topic_key, topic_val in topics.items():
        if topic_key == "loshu_curiosity_teasers":
            continue
        _walk_paid(topic_val, paid_strings)
    return [s.strip() for s in paid_strings if len(s.strip()) >= 40]


def _walk_paid(node, acc: list[str]) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("text", "remedy", "days_1_30", "days_31_60", "days_61_90") and isinstance(v, str):
                acc.append(v)
            else:
                _walk_paid(v, acc)
    elif isinstance(node, list):
        for item in node:
            _walk_paid(item, acc)


def export_public_teasers() -> dict:
    lib = json.loads(CONTENT_LIB_PATH.read_text(encoding="utf-8"))
    teasers = lib.get("topics", {}).get("loshu_curiosity_teasers")
    if not teasers or not teasers.get("public_browser_safe"):
        raise RuntimeError("Missing or unapproved `topics.loshu_curiosity_teasers` in content library.")

    payload = {
        "schema_version": "1.0.0",
        "source_library_version": lib.get("version", "2.0.0"),
        "status": teasers.get("status", "DRAFT"),
        "public_browser_safe": True,
        "default_overview": teasers["default_overview"],
        "digits": teasers["digits"],
        "planes": teasers["planes"],
    }

    serialized = json.dumps(payload, indent=2, ensure_ascii=False)

    # Strict IP / Paid-Content Non-Leakage Gate
    forbidden_keys = ("depth_1_basic", "depth_2_advanced", "depth_3_premium", "ninety_day_plan")
    for fk in forbidden_keys:
        if fk in serialized:
            raise AssertionError(f"Paid report structure key '{fk}' leaked into public teasers!")

    paid_fragments = collect_paid_prose_fragments(lib)
    for frag in paid_fragments:
        if frag in serialized:
            raise AssertionError(f"Paid report prose leaked into public teasers: {frag[:60]}...")

    PUBLIC_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_OUT_PATH.write_text(serialized + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    out = export_public_teasers()
    print(
        f"Exported loshu_public_teasers.json ({PUBLIC_OUT_PATH.stat().st_size} bytes): "
        f"{len(out['digits'])} digits, {len(out['planes'])} planes."
    )
