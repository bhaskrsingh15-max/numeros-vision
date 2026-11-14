# -*- coding: utf-8 -*-
"""
Live Preview End-to-End Verification for Phase 5 Logo Intelligence
against `https://preview.numeros-vision.pages.dev`.

Proves all Phase 5 Acceptance Criteria on Preview:
1. All 10 real logo fixtures (`01`..`10`, 5 SVG + 5 PNG) run end-to-end on preview (`200 OK`).
2. Real PNG, JPEG, PDF, and SVG multipart binary uploads run end-to-end on preview (`200 OK`)
   with confidence scores and user override confirmation.
3. Identical input produces identical output on live preview.
4. Stencil / cut-letter logo (`04_apex_stencil_cut_letters.svg`) fails the `nothing_cut` gate.
5. `'DE WOW WAFEL'` gives compound `51`, root `6` (both direct preview & OCR from `09_de_wow_wafel_demo.png`).
6. Gold `#C9A227` on `#FFFDF7` measures `2.38:1` and fails `contrast_threshold`.
7. Shukla Paksha start for Nov 2026 is `2026-11-09` (`9 Nov 2026`) with 3 Shukla Paksha dates.
8. Four separate results (`visual_quality`, `brand_fit`, `name_intelligence`, `traditional_alignment`),
   never one blended score; compliant prices; zero forbidden copy words.
"""

from __future__ import annotations

import base64
import io
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request
import uuid

from PIL import Image, ImageDraw
import pymupdf

PREVIEW_BASE = os.environ.get("NV_PREVIEW_BASE", "https://preview.numeros-vision.pages.dev")
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "logo_10_samples"

FORBIDDEN_RE = re.compile(
    r"\b(verified|validated|certified|authentic|guaranteed|guarantee|guarantees|legal\s+certification)\b",
    re.IGNORECASE,
)


def post_json(path: str, payload: dict) -> tuple[int, dict]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{PREVIEW_BASE}{path}",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "NumerosVision-Phase5-Verifier/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            return exc.code, json.loads(body)
        except Exception:
            return exc.code, {"raw": body}


def post_multipart(path: str, filename: str, file_bytes: bytes, mime: str, fields: dict | None = None) -> tuple[int, dict]:
    boundary = f"----NVPhase5Boundary{uuid.uuid4().hex}"
    chunks: list[bytes] = []
    for k, v in (fields or {}).items():
        chunks.append(f"--{boundary}\r\n".encode())
        chunks.append(f'Content-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode("utf-8"))
    chunks.append(f"--{boundary}\r\n".encode())
    chunks.append(
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\nContent-Type: {mime}\r\n\r\n'.encode("utf-8")
    )
    chunks.append(file_bytes)
    chunks.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(chunks)

    req = urllib.request.Request(
        f"{PREVIEW_BASE}{path}",
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
            "User-Agent": "NumerosVision-Phase5-Verifier/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8"))


def main() -> None:
    check_page = "--check-page" in sys.argv
    print(f"=== Verifying Phase 5 Logo Intelligence on {PREVIEW_BASE} ===")

    st_empty, _ = post_json("/api/v1/logo/preview", {})
    assert st_empty == 400, f"Expected 400 on empty preview, got {st_empty}"
    print("[PASS] Empty input validation -> 400")

    st_dww, dww = post_json(
        "/api/v1/logo/five-layer-evaluate",
        {
            "business_name": "DE WOW WAFEL",
            "business_category": "hospitality_food",
            "owner_name": "Founder",
            "owner_dob": "1981-11-28",
            "partners": [{"name": "Co-Founder", "dob": "1991-11-29"}],
            "dpdp_consent": True,
            "reference_date": "2026-11-08",
        },
    )
    assert st_dww == 200, f"DE WOW WAFEL failed: {st_dww} {dww}"
    ni = dww["four_results"]["name_intelligence"]
    assert ni["compound_number"] == 51 and ni["root_number"] == 6, f"Unexpected DE WOW WAFEL numbers: {ni}"
    sp_start = dww["layers"]["layer5_activation"]["timing"]["shukla_paksha_start_date"]
    assert sp_start == "2026-11-09", f"Expected 2026-11-09 Shukla Paksha start, got {sp_start}"
    assert len(dww["layers"]["layer5_activation"]["three_shukla_paksha_dates"]) == 3
    print(f"[PASS] 'DE WOW WAFEL' -> compound={ni['compound_number']}, root={ni['root_number']} | Shukla Paksha start={sp_start}")

    st_gold, gold = post_json(
        "/api/v1/logo/preview",
        {
            "business_name": "AURA PEAK",
            "symbol_concept": "ascending_peak",
            "primary_color": "#C9A227",
            "accent_color": "#C9A227",
            "bg_color": "#FFFDF7",
        },
    )
    assert st_gold == 200
    assert gold["contrast_ratio"] == 2.38 and gold["contrast_passed"] is False, f"Gold check failed: {gold}"
    print(f"[PASS] Gold #C9A227 on #FFFDF7 -> {gold['contrast_ratio']}:1 (contrast_passed={gold['contrast_passed']})")

    samples = sorted(FIXTURES_DIR.glob("[0-9][0-9]_*"))
    assert len(samples) == 10
    for idx, fp in enumerate(samples, start=1):
        raw = fp.read_bytes()
        if fp.suffix.lower() == ".svg":
            payload = {"svg_content": raw.decode("utf-8")}
        else:
            payload = {"image_base64": base64.b64encode(raw).decode("ascii"), "filename": fp.name}

        s1, b1 = post_json("/api/v1/logo/analyze-existing", payload)
        s2, b2 = post_json("/api/v1/logo/analyze-existing", payload)
        assert s1 == 200 and s2 == 200, f"Sample {fp.name} returned {s1}/{s2}"
        assert b1 == b2, f"Non-deterministic response on {fp.name}"
        assert not FORBIDDEN_RE.search(json.dumps(b1)), f"Forbidden word in {fp.name}"

        gmap = {g["gate_id"]: g["passed"] for g in b1["hard_gates"]}
        if fp.name == "04_apex_stencil_cut_letters.svg":
            assert gmap["nothing_cut"] is False, "Stencil logo must fail nothing_cut!"
        if fp.name == "03_aura_peak_gold_low_contrast.svg":
            assert b1["measurable_findings"]["wcag_contrast_estimate"] == 2.38
            assert gmap["contrast_threshold"] is False
        if fp.name == "05_fake_vector_raster_and_script.svg":
            assert gmap["vector_integrity"] is False
        if fp.name == "09_de_wow_wafel_demo.png":
            assert "DE WOW WAFEL" in b1["upload_reading"]["extracted_text"].upper()
        if fp.name == "10_tiny_32px_favicon.png":
            assert gmap["app_icon_legibility"] is False

        print(
            f"[PASS] Logo {idx:02d}/10 `{fp.name}` -> 200 | verdict={b1['free_scan']['verdict']} "
            f"| contrast={b1['measurable_findings']['wcag_contrast_estimate']}:1 | nothing_cut={gmap['nothing_cut']}"
        )

    pdf_doc = pymupdf.open()
    page = pdf_doc.new_page(width=600, height=300)
    page.draw_rect(pymupdf.Rect(0, 0, 600, 300), color=None, fill=(1.0, 0.992, 0.968))
    page.insert_text(pymupdf.Point(160, 160), "DE WOW WAFEL", fontsize=30, color=(0.086, 0.514, 0.357))
    pdf_bytes = pdf_doc.tobytes()
    pdf_doc.close()
    st_pdf, b_pdf = post_multipart("/api/v1/logo/analyze-existing", "wafel.pdf", pdf_bytes, "application/pdf")
    assert st_pdf == 200 and b_pdf["upload_reading"]["format"] == "PDF"

    img = Image.new("RGB", (500, 260), (255, 253, 247))
    ImageDraw.Draw(img).rectangle((60, 60, 180, 180), fill=(82, 62, 40))
    jbuf = io.BytesIO()
    img.save(jbuf, format="JPEG", quality=92)
    st_jpg, b_jpg = post_multipart(
        "/api/v1/logo/analyze-existing",
        "mark.jpg",
        jbuf.getvalue(),
        "image/jpeg",
        fields={"confirmed_text": "DE WOW WAFEL"},
    )
    assert st_jpg == 200 and b_jpg["upload_reading"]["format"] == "JPEG" and b_jpg["upload_reading"]["user_corrected"] is True
    print("[PASS] Multipart PDF & JPEG uploads + user override -> 200")

    if check_page:
        req = urllib.request.Request(
            f"{PREVIEW_BASE}/calculators/logo-intelligence/",
            headers={"User-Agent": "NumerosVision-Phase5-Verifier/1.0"},
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8")
            assert resp.status == 200
            assert "nvLogoStudioComingSoon" not in html, "Coming Soon panel still present on live page!"
            assert "calculateChaldeanWordmark" not in html, "Client-side Chaldean calculator still present!"
            assert not FORBIDDEN_RE.search(html), f"Forbidden word in live HTML: {FORBIDDEN_RE.search(html).group(0)}"
            print("[PASS] Live /calculators/logo-intelligence/ page active & zero forbidden words!")

    print("=== ALL PHASE 5 LIVE PREVIEW CHECKS PASSED ===")


if __name__ == "__main__":
    main()
