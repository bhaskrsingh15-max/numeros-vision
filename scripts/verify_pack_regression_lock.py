"""
NUMEROS VISION — Step 0/1 Build Safety & Report Pack Regression Lock
====================================================================
Enforces the non-negotiable Build Safety directive from the Logo Intelligence Audit:
1. The logo module only adds new files; it never edits or deletes anything in existing engines
   (`app/engine/` and `pdf_service/app/engine/`).
2. Before and after every build step, regenerate one canonical report of each existing pack
   (`report_basic`, `report_advanced`, `report_premium`, and `planner_2027`) and compare against
   the locked golden baseline (`tests/fixtures/pack_regression_lock_baseline.json`).
   Any structural, text, page-count, or engine-file hash difference exits non-zero and stops release.

Usage:
  python scripts/verify_pack_regression_lock.py --lock     # Create initial baseline (run once at Step 1 start)
  python scripts/verify_pack_regression_lock.py --verify   # Verify zero drift against locked baseline (default)
"""

import argparse
import datetime
import hashlib
import io
import json
import os
import sys
import tempfile
from typing import Any, Dict
from unittest.mock import patch

import pypdf

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASELINE_PATH = os.path.join(ROOT_DIR, "tests", "fixtures", "pack_regression_lock_baseline.json")

FIXED_TODAY = datetime.date(2026, 11, 13)


class _FixedDate(datetime.date):
    @classmethod
    def today(cls) -> "datetime.date":
        return FIXED_TODAY


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def collect_engine_file_hashes() -> Dict[str, str]:
    """Hashes every .py file in app/engine/ and pdf_service/app/engine/ after LF line-ending normalisation."""
    manifest: Dict[str, str] = {}
    for rel_dir in ("app/engine", "pdf_service/app/engine"):
        abs_dir = os.path.join(ROOT_DIR, *rel_dir.split("/"))
        if not os.path.isdir(abs_dir):
            continue
        for root, dirs, files in os.walk(abs_dir):
            dirs[:] = sorted(d for d in dirs if d != "__pycache__")
            for fname in sorted(files):
                if not fname.endswith(".py"):
                    continue
                fpath = os.path.join(root, fname)
                rel_path = os.path.relpath(fpath, ROOT_DIR).replace("\\", "/")
                with open(fpath, "rb") as f:
                    norm_bytes = f.read().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
                    manifest[rel_path] = sha256_bytes(norm_bytes)
    return dict(sorted(manifest.items()))


def build_canonical_view_payload(tier: str, pack_id: str) -> Dict[str, Any]:
    has_basic = tier in ("basic", "advanced", "premium")
    has_advanced = tier in ("advanced", "premium")
    has_premium = tier == "premium"
    return {
        "job_id": f"job_reglock_{tier}",
        "pack_id": pack_id,
        "view": {
            "user": {"userId": "usr_reglock_001"},
            "subject": {
                "id": "sbj_reglock_001",
                "name": "Aaditya Sharma",
                "dob": "1990-08-15",
                "created_at": 1700000000000,
            },
            "tier": tier,
            "entitlements": [pack_id],
            "calculation": {
                "driver": 6,
                "conductor": 6,
                "conductorRaw": 33,
                "conductorDisplay": "33/6",
                "driverPlanet": "Venus",
                "conductorPlanet": "Venus",
                "counts": {"1": 2, "2": 0, "3": 0, "4": 0, "5": 1, "6": 0, "7": 0, "8": 1, "9": 2},
                "presentDigits": [1, 5, 8, 9],
                "missingDigits": [2, 3, 4, 6, 7],
                "planes": [
                    {
                        "name": "Will Plane",
                        "digits": [9, 5, 1],
                        "presentCount": 3,
                        "percentage": 100,
                        "status": "COMPLETE",
                    }
                ],
            },
            "sections": {
                "grid": {"unlocked": True, "cells": []},
                "enabledDigits": {"unlocked": True, "items": []},
                "elementBalancing": {"unlocked": has_basic, "pageCount": 3},
                "enabledNumbersInDepth": {"unlocked": has_advanced, "pageCount": 12},
                "missingNumbersInDepth": {"unlocked": has_premium, "pageCount": 32},
                "remedies": {"unlocked": has_premium, "pageCount": 32},
                "predictions": {"unlocked": has_premium, "pageCount": 32},
            },
        },
    }


def extract_pdf_fingerprint(pdf_bytes: bytes) -> Dict[str, Any]:
    reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    page_hashes = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        # Normalize line endings for cross-platform stability
        norm_txt = "\n".join(line.rstrip() for line in txt.splitlines()).strip()
        page_hashes.append(sha256_text(norm_txt))
    return {
        "page_count": len(reader.pages),
        "page_text_sha256": page_hashes,
        "combined_text_sha256": sha256_text("|".join(page_hashes)),
    }


def generate_all_pack_fingerprints() -> Dict[str, Any]:
    from app.services.internal_pdf_worker_service import render_pdf_from_view
    from app.engine.planner_2027_engine import calculate_planner_2027
    from pdf_service.app.services.planner_2027_pdf_generator import generate_planner_2027_pdf

    packs: Dict[str, Any] = {}

    with patch("datetime.date", _FixedDate):
        for tier, pack_id, expected_pages in (
            ("basic", "report_basic", 3),
            ("advanced", "report_advanced", 12),
            ("premium", "report_premium", 32),
        ):
            payload = build_canonical_view_payload(tier, pack_id)
            pdf_bytes, render_meta = render_pdf_from_view(payload)
            fp = extract_pdf_fingerprint(pdf_bytes)
            if fp["page_count"] != expected_pages:
                raise RuntimeError(
                    f"Pack {pack_id} rendered {fp['page_count']} pages, expected {expected_pages}."
                )
            # Exclude wall-clock duration and OS/compression-sensitive pdf_size_bytes
            stable_meta = {
                k: v
                for k, v in render_meta.items()
                if k not in ("duration_ms", "generated_at", "timestamp", "pdf_size_bytes")
            }
            packs[pack_id] = {
                "render_meta": stable_meta,
                "pdf_fingerprint": fp,
            }

        # Planner 2027 engine + 24-page PDF
        planner_calc = calculate_planner_2027("Arun Sharma", "1981-11-28")
        planner_calc_json = json.dumps(planner_calc, sort_keys=True, ensure_ascii=False)
        with tempfile.TemporaryDirectory() as tmpdir:
            out_pdf = os.path.join(tmpdir, "reglock_arun_2027.pdf")
            planner_pdf_bytes = generate_planner_2027_pdf(
                "Arun Sharma", "1981-11-28", out_pdf, is_sample=True
            )
            planner_fp = extract_pdf_fingerprint(planner_pdf_bytes)
            if planner_fp["page_count"] != 24:
                raise RuntimeError(
                    f"Pack planner_2027 rendered {planner_fp['page_count']} pages, expected 24."
                )
            packs["planner_2027"] = {
                "engine_json_sha256": sha256_text(planner_calc_json),
                "pdf_fingerprint": planner_fp,
            }

    return {
        "schema_version": "1.1.0",
        "fixed_reference_date": FIXED_TODAY.isoformat(),
        "engine_files_sha256": collect_engine_file_hashes(),
        "packs": packs,
    }


def _strip_ignored_pack_fields(pack_entry: Dict[str, Any]) -> Dict[str, Any]:
    fp = pack_entry.get("pdf_fingerprint", {})
    norm: Dict[str, Any] = {
        "pdf_fingerprint": {
            "page_count": fp.get("page_count"),
            "page_text_sha256": fp.get("page_text_sha256", []),
            "combined_text_sha256": fp.get("combined_text_sha256"),
        }
    }
    if "engine_json_sha256" in pack_entry:
        norm["engine_json_sha256"] = pack_entry["engine_json_sha256"]
    if "render_meta" in pack_entry:
        norm["render_meta"] = {
            k: v
            for k, v in pack_entry["render_meta"].items()
            if k not in ("duration_ms", "generated_at", "timestamp", "pdf_size_bytes")
        }
    return norm


def compare_snapshots(baseline: Dict[str, Any], current: Dict[str, Any]) -> list[str]:
    diffs: list[str] = []

    base_engines = baseline.get("engine_files_sha256", {})
    curr_engines = current.get("engine_files_sha256", {})

    for path, b_hash in base_engines.items():
        if path not in curr_engines:
            diffs.append(f"[ENGINE DELETED] {path} was deleted!")
        elif curr_engines[path] != b_hash:
            diffs.append(f"[ENGINE MODIFIED] {path} SHA-256 changed: {b_hash[:12]} -> {curr_engines[path][:12]}")

    for path in curr_engines:
        if path not in base_engines:
            diffs.append(
                f"[UNEXPECTED FILE IN ENGINE DIR] {path} added inside protected engine directory "
                "(new logo files belong in app/logo_intelligence/ and pdf_service/app/logo_intelligence/)."
            )

    base_packs = baseline.get("packs", {})
    curr_packs = current.get("packs", {})
    for pack_id, b_pack_raw in base_packs.items():
        c_pack_raw = curr_packs.get(pack_id)
        if not c_pack_raw:
            diffs.append(f"[PACK MISSING] {pack_id} missing from current run.")
            continue
        b_pack = _strip_ignored_pack_fields(b_pack_raw)
        c_pack = _strip_ignored_pack_fields(c_pack_raw)
        if json.dumps(b_pack, sort_keys=True) != json.dumps(c_pack, sort_keys=True):
            diffs.append(f"[PACK DRIFT] {pack_id} output differs from locked baseline!")
            b_fp = b_pack["pdf_fingerprint"]
            c_fp = c_pack["pdf_fingerprint"]
            if b_fp.get("page_count") != c_fp.get("page_count"):
                diffs.append(
                    f"  - Page count changed: {b_fp.get('page_count')} -> {c_fp.get('page_count')}"
                )
            b_pages = b_fp.get("page_text_sha256", [])
            c_pages = c_fp.get("page_text_sha256", [])
            for idx, (bp, cp) in enumerate(zip(b_pages, c_pages), start=1):
                if bp != cp:
                    diffs.append(f"  - Page {idx} text SHA-256 changed: {bp[:12]} -> {cp[:12]}")

    return diffs


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify or lock report pack regression baseline.")
    parser.add_argument("--lock", action="store_true", help="Write golden baseline snapshot.")
    parser.add_argument("--verify", action="store_true", help="Verify current state against golden baseline.")
    args = parser.parse_args()

    snapshot = generate_all_pack_fingerprints()

    if args.lock:
        os.makedirs(os.path.dirname(BASELINE_PATH), exist_ok=True)
        with open(BASELINE_PATH, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2, sort_keys=True)
        print(f"[LOCKED] Baseline written to {BASELINE_PATH}")
        print(f"  Protected engine files hashed: {len(snapshot['engine_files_sha256'])}")
        for pack_id, pdata in snapshot["packs"].items():
            pages = pdata["pdf_fingerprint"]["page_count"]
            comb = pdata["pdf_fingerprint"]["combined_text_sha256"][:16]
            print(f"  Pack {pack_id:16s} -> {pages:2d} pages | text_sha256={comb}...")
        return 0

    if not os.path.isfile(BASELINE_PATH):
        print(f"[ERROR] Baseline file not found at {BASELINE_PATH}. Run with --lock first.", file=sys.stderr)
        return 1

    with open(BASELINE_PATH, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    diffs = compare_snapshots(baseline, snapshot)
    if diffs:
        print("[FAIL] REGRESSION LOCK VIOLATION DETECTED:", file=sys.stderr)
        for d in diffs:
            print(f"  {d}", file=sys.stderr)
        return 1

    print("[PASS] Build Safety Regression Lock verified: ZERO diffs across all engine files and 4 report packs.")
    print(f"  Verified {len(snapshot['engine_files_sha256'])} protected engine files.")
    for pack_id, pdata in snapshot["packs"].items():
        pages = pdata["pdf_fingerprint"]["page_count"]
        comb = pdata["pdf_fingerprint"]["combined_text_sha256"][:16]
        print(f"  Verified {pack_id:16s} -> {pages:2d} pages | text_sha256={comb}...")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
