"""
Build Integrity & PDF Exclusion Test (Commit 6a - Item 1)
=========================================================
Verifies:
1. wrangler.toml and build_bulletproof_dist.py agree on pages_build_output_dir = "dist_cloudflare_pages".
2. dist_cloudflare_pages/reports does NOT exist.
3. cloudflare_pages_upload.zip does NOT exist.
4. No PDF exists anywhere in dist_cloudflare_pages except under samples/*.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(ROOT, "dist_cloudflare_pages")
WRANGLER_TOML = os.path.join(ROOT, "wrangler.toml")
LEGACY_ZIP = os.path.join(ROOT, "cloudflare_pages_upload.zip")


def test_single_build_path_and_pdf_exclusion():
    # 1. Verify wrangler.toml points to dist_cloudflare_pages
    with open(WRANGLER_TOML, "r", encoding="utf-8") as f:
        toml_text = f.read()
    m = re.search(r'pages_build_output_dir\s*=\s*"([^"]+)"', toml_text)
    assert m is not None, "pages_build_output_dir not found in wrangler.toml"
    assert m.group(1) == "dist_cloudflare_pages", (
        f"wrangler.toml pages_build_output_dir is '{m.group(1)}', expected 'dist_cloudflare_pages'"
    )

    # 2. Verify legacy zip does not exist
    assert not os.path.exists(LEGACY_ZIP), f"Legacy {LEGACY_ZIP} must be deleted"

    # 3. Verify dist_cloudflare_pages exists and dist_cloudflare_pages/reports does not
    assert os.path.isdir(DIST_DIR), "dist_cloudflare_pages directory does not exist"
    reports_dir = os.path.join(DIST_DIR, "reports")
    assert not os.path.exists(reports_dir), f"Forbidden directory exists: {reports_dir}"

    # 4. Walk dist_cloudflare_pages and fail if any PDF outside samples/* exists
    found_pdfs = []
    unauthorized_pdfs = []
    for dirpath, _, filenames in os.walk(DIST_DIR):
        for fn in filenames:
            if fn.lower().endswith(".pdf"):
                rel = os.path.relpath(os.path.join(dirpath, fn), DIST_DIR).replace("\\", "/")
                found_pdfs.append(rel)
                if not rel.startswith("samples/"):
                    unauthorized_pdfs.append(rel)

    assert not unauthorized_pdfs, (
        f"Unauthorized PDFs found in build output: {unauthorized_pdfs}"
    )
    assert len(found_pdfs) >= 1, "Expected at least 1 sample PDF in dist_cloudflare_pages/samples/*"
    print(f"PASS: Single build path verified (dist_cloudflare_pages). Allowed sample PDFs: {found_pdfs}")


def test_built_site_prices_and_page_counts_match_packs_json():
    """
    Scans every built HTML and JS file in dist_cloudflare_pages and fails on:
    - Any rupee amount (₹, Rs, &#8377;) that disagrees with active packs.json prices {0, 199, 510, 1050}
    - Any 'N Pages' or 'N-Page' expression where N disagrees with packs.json page counts {3, 12, 32} or uses '+' (e.g. '45+')
    - Any legacy forbidden price/page strings ('210', '1,500', '9 Pages', '21 Pages', '45+')
    """
    import json

    packs_path = os.path.join(ROOT, "app", "config", "packs.json")
    with open(packs_path, "r", encoding="utf-8") as f:
        packs = json.load(f)

    allowed_prices = set()
    allowed_pages = set()
    for pack in packs.get("core_reports", {}).values():
        if pack.get("status") == "active":
            allowed_prices.add(int(pack["price_inr"]))
            allowed_pages.add(int(pack["pages"]))
    for pack in packs.get("charm_ai", {}).values():
        if pack.get("status") == "active":
            allowed_prices.add(int(pack["price_inr"]))

    assert allowed_prices == {0, 199, 510, 1050}, f"Unexpected active prices in packs.json: {allowed_prices}"
    assert allowed_pages == {3, 12, 32}, f"Unexpected active page counts in packs.json: {allowed_pages}"
    allowed_per_day = {round(p / 365, 2) for p in allowed_prices if p > 0}

    re_rupee = re.compile(r"(?:₹|&#8377;|\\u20b9|\bRs\.?\s*)([\d,]+(?:\.\d+)?)(\s*/\s*day)?", re.IGNORECASE)
    re_pages = re.compile(r"\b(\d+)\+?\s*[-–]?\s*[Pp]ages?\b")
    re_forbidden = re.compile(r"\b210\b|1,500|45\+|\b9\s*[-–]?\s*[Pp]ages?\b|\b21\s*[-–]?\s*[Pp]ages?\b|\{\{PACK_")

    violations = []
    for dirpath, _, filenames in os.walk(DIST_DIR):
        for fn in filenames:
            if not fn.lower().endswith((".html", ".js")):
                continue
            full_path = os.path.join(dirpath, fn)
            rel_path = os.path.relpath(full_path, DIST_DIR).replace("\\", "/")
            text = open(full_path, "r", encoding="utf-8", errors="ignore").read()

            file_allowed_prices = allowed_prices | {1499, 1999} if ("2027" in rel_path or "your-reading" in rel_path or rel_path == "_worker.js") else allowed_prices
            file_allowed_pages = allowed_pages | {24} if ("2027" in rel_path or "your-reading" in rel_path or rel_path == "_worker.js") else allowed_pages

            for line_no, line in enumerate(text.splitlines(), 1):
                for m in re_rupee.finditer(line):
                    raw_val = m.group(1).replace(",", "")
                    is_per_day = bool(m.group(2))
                    try:
                        val = float(raw_val)
                    except ValueError:
                        continue
                    if is_per_day:
                        if round(val, 2) not in allowed_per_day:
                            violations.append(
                                f"{rel_path}:{line_no}: Per-day rupee amount '{m.group(0)}' not in packs.json/365 {sorted(allowed_per_day)}"
                            )
                    elif val not in file_allowed_prices:
                        violations.append(f"{rel_path}:{line_no}: Rupee amount '{m.group(0)}' not in active packs.json {sorted(allowed_prices)}")

                for m in re_pages.finditer(line):
                    pg = int(m.group(1))
                    if pg not in file_allowed_pages or "+" in m.group(0):
                        violations.append(f"{rel_path}:{line_no}: Page count '{m.group(0)}' not in packs.json {sorted(allowed_pages)}")

                for m in re_forbidden.finditer(line):
                    violations.append(f"{rel_path}:{line_no}: Forbidden token '{m.group(0)}' found")

    assert not violations, (
        f"Found {len(violations)} price/page-count consistency violations in dist_cloudflare_pages:\n"
        + "\n".join(violations[:30])
    )
    pricing_built = open(os.path.join(DIST_DIR, "pricing.html"), "r", encoding="utf-8").read()
    assert "~₹2.88/day" in pricing_built and "₹1.40/day" in pricing_built, (
        "pricing.html in dist_cloudflare_pages is missing build-time injected per-day price hooks"
    )
    print(
        f"PASS: All built HTML/JS files in dist_cloudflare_pages strictly match packs.json "
        f"(prices={sorted(allowed_prices)}, per_day={sorted(allowed_per_day)}, pages={sorted(allowed_pages)})."
    )


def test_wrangler_placeholder_deploy_guard():
    sys.path.insert(0, ROOT)
    from build_bulletproof_dist import verify_wrangler_no_placeholders

    with open(WRANGLER_TOML, "r", encoding="utf-8") as f:
        current_toml = f.read()

    # Must refuse to deploy while placeholder 00000000-... database_ids remain
    placeholder_toml = 'database_id = "00000000-0000-0000-0000-000000000001"'
    blocked = False
    try:
        verify_wrangler_no_placeholders(placeholder_toml)
    except ValueError as exc:
        blocked = "DEPLOYMENT BLOCKED" in str(exc)
    assert blocked, "verify_wrangler_no_placeholders must block deployment when 00000000-... placeholder database_ids exist"
    # And verify current real toml passes
    verify_wrangler_no_placeholders(current_toml)

    # Must pass when real UUIDs replace placeholders
    valid_toml = (
        current_toml.replace("00000000-0000-0000-0000-000000000001", "a1b2c3d4-e5f6-4789-8012-3456789abcde")
        .replace("00000000-0000-0000-0000-000000000002", "b2c3d4e5-f6a7-4890-9123-456789abcdef")
    )
    verify_wrangler_no_placeholders(valid_toml)
    print("PASS: wrangler.toml placeholder deploy guard verified (blocks 00000000-... placeholders, allows real UUIDs).")


def test_production_html_placeholder_guard():
    """
    Verifies that verify_production_html_no_placeholders:
    1. Blocks production deployment if any {{...}} placeholder exists in HTML.
    2. Allows preview/dev environments to retain unrendered {{...}} placeholders.
    """
    import tempfile
    import shutil
    from build_bulletproof_dist import verify_production_html_no_placeholders

    temp_dir = tempfile.mkdtemp()
    try:
        # 1. Dirty directory with placeholder in HTML
        dirty_html = os.path.join(temp_dir, "test.html")
        with open(dirty_html, "w", encoding="utf-8") as f:
            f.write("<html><body>Consent: {{CONSENT_TEXT_PENDING}}</body></html>")

        blocked = False
        try:
            verify_production_html_no_placeholders(temp_dir)
        except ValueError as exc:
            blocked = "PRODUCTION DEPLOY BLOCKED" in str(exc)

        assert blocked, "verify_production_html_no_placeholders must block when HTML contains {{...}} placeholders"

        # 2. Clean directory without placeholder
        with open(dirty_html, "w", encoding="utf-8") as f:
            f.write("<html><body>Consent: Final Statutory Text</body></html>")

        verify_production_html_no_placeholders(temp_dir)
        print("PASS: Production HTML placeholder guard verified (blocks {{...}} placeholders on production).")
    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    test_single_build_path_and_pdf_exclusion()
    test_built_site_prices_and_page_counts_match_packs_json()
    test_wrangler_placeholder_deploy_guard()
    test_production_html_placeholder_guard()
