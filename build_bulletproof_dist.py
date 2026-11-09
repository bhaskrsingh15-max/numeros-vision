import os
import re
import json
import shutil
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_SRC = os.path.join(BASE_DIR, "app", "static")
PACKS_JSON_PATH = os.path.join(BASE_DIR, "app", "config", "packs.json")
DIST_DIR = os.path.join(BASE_DIR, "dist_cloudflare_pages")
LEGACY_ZIP = os.path.join(BASE_DIR, "cloudflare_pages_upload.zip")

# Load canonical packs.json at build time
with open(PACKS_JSON_PATH, "r", encoding="utf-8") as pf:
    PACKS_DATA = json.load(pf)

# 0. Remove legacy upload zip so only one deploy folder (dist_cloudflare_pages) exists
if os.path.exists(LEGACY_ZIP):
    os.remove(LEGACY_ZIP)

# 1. Clean and re-populate DIST_DIR from app/static
if os.path.exists(DIST_DIR):
    shutil.rmtree(DIST_DIR)

shutil.copytree(
    STATIC_SRC,
    DIST_DIR,
    ignore=shutil.ignore_patterns("*.backup", "*_backup", "*.log", ".git*", "reports")
)

# 1b. Enforce strict PDF exclusion: delete any PDF outside samples/*
for root, dirs, files in os.walk(DIST_DIR):
    for f in files:
        if f.lower().endswith(".pdf"):
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, DIST_DIR).replace("\\", "/")
            if not rel_path.startswith("samples/"):
                os.remove(full_path)
            else:
                with open(full_path, "rb") as pf:
                    if b"{{" in pf.read():
                        raise ValueError(f"BUILD BLOCKED: Public PDF '{rel_path}' contains unapproved placeholder '{{{{'")

# Ensure dist_cloudflare_pages/reports does not exist
reports_dir = os.path.join(DIST_DIR, "reports")
if os.path.exists(reports_dir):
    shutil.rmtree(reports_dir)

# 1c. Inject canonical packs.json into dist_cloudflare_pages/config/packs.json and sync HTML/JS tokens at build time
config_dest_dir = os.path.join(DIST_DIR, "config")
os.makedirs(config_dest_dir, exist_ok=True)
shutil.copy2(PACKS_JSON_PATH, os.path.join(config_dest_dir, "packs.json"))

basic_pack = PACKS_DATA["core_reports"]["report_basic"]
adv_pack = PACKS_DATA["core_reports"]["report_advanced"]
prem_pack = PACKS_DATA["core_reports"]["report_premium"]
BUILD_TOKENS = {
    "{{PACK_BASIC_NAME}}": str(basic_pack["name"]),
    "{{PACK_BASIC_PRICE_INR}}": f"{int(basic_pack['price_inr']):,}",
    "{{PACK_BASIC_PER_DAY_INR}}": f"{int(basic_pack['price_inr']) / 365:.2f}",
    "{{PACK_BASIC_PAGES}}": str(basic_pack["pages"]),
    "{{PACK_ADVANCED_NAME}}": str(adv_pack["name"]),
    "{{PACK_ADVANCED_PRICE_INR}}": f"{int(adv_pack['price_inr']):,}",
    "{{PACK_ADVANCED_PER_DAY_INR}}": f"{int(adv_pack['price_inr']) / 365:.2f}",
    "{{PACK_ADVANCED_PAGES}}": str(adv_pack["pages"]),
    "{{PACK_PREMIUM_NAME}}": str(prem_pack["name"]),
    "{{PACK_PREMIUM_PRICE_INR}}": f"{int(prem_pack['price_inr']):,}",
    "{{PACK_PREMIUM_PER_DAY_INR}}": f"{int(prem_pack['price_inr']) / 365:.2f}",
    "{{PACK_PREMIUM_PAGES}}": str(prem_pack["pages"]),
}
for root, _, files in os.walk(DIST_DIR):
    for f in files:
        if f.lower().endswith((".html", ".js")):
            fp = os.path.join(root, f)
            txt = open(fp, "r", encoding="utf-8", errors="ignore").read()
            updated = txt
            for k, v in BUILD_TOKENS.items():
                if k in updated:
                    updated = updated.replace(k, v)
            if updated != txt:
                open(fp, "w", encoding="utf-8").write(updated)

# 1d. Inject build-time JSON-LD for 2027 Year Ahead Planner derived from planner_2027_pricing.json
try:
    from app.config.planner_2027_jsonld import generate_planner_2027_jsonld
    planner_pricing_file = os.path.join(BASE_DIR, "app", "config", "planner_2027_pricing.json")
    with open(planner_pricing_file, "r", encoding="utf-8") as ppf:
        p_cfg = json.load(ppf)
    jsonld_obj = generate_planner_2027_jsonld(p_cfg)
    jsonld_str = json.dumps(jsonld_obj, indent=2)

    dist_y2027 = os.path.join(DIST_DIR, "year_2027.html")
    if os.path.exists(dist_y2027):
        with open(dist_y2027, "r", encoding="utf-8") as yf:
            y_content = yf.read()
        # Replace script tag content
        new_y_content = re.sub(
            r'<script type="application/ld\+json">.*?</script>',
            f'<script type="application/ld+json">\n{jsonld_str}\n  </script>',
            y_content,
            flags=re.DOTALL
        )
        with open(dist_y2027, "w", encoding="utf-8") as yf:
            yf.write(new_y_content)
        print("PASS: Injected build-time JSON-LD into dist_cloudflare_pages/year_2027.html")
except Exception as e:
    print(f"Warning: could not inject build-time JSON-LD: {e}")

# 2. Mirror essential static assets into dist/static/ (css, js, icons) for FastAPI path parity
static_mirror = os.path.join(DIST_DIR, "static")
os.makedirs(static_mirror, exist_ok=True)
for item in ["css", "js", "icons"]:
    src_item = os.path.join(DIST_DIR, item)
    if os.path.exists(src_item) and os.path.isdir(src_item):
        dest_item = os.path.join(static_mirror, item)
        if os.path.exists(dest_item):
            shutil.rmtree(dest_item)
        shutil.copytree(src_item, dest_item)

# Also mirror favicon, manifest, sitemap, llms, and verification files into static/
for fname in [
    "favicon.ico", "apple-touch-icon.png", "manifest.json", "manifest.webmanifest",
    "sitemap.xml", "robots.txt", "BingSiteAuth.xml", "llms.txt", "llms-full.txt",
    "49bf97a1d74343ce951918a3a0e676d4.txt", "sitemap.html"
]:
    fsrc = os.path.join(DIST_DIR, fname)
    if os.path.exists(fsrc):
        shutil.copy2(fsrc, os.path.join(static_mirror, fname))

# 3. Create physical directory/index.html for every canonical route
ROUTING_MAP = {
    # Roadmap & Sample Reports
    "sample_roadmap": "sample_roadmap.html",
    "sample-roadmap": "sample_roadmap.html",
    "roadmap-preview": "sample_roadmap.html",
    "sample": "sample.html",
    "sample-report": "sample.html",
    "sample_report": "sample.html",
    "sample2": "sample2.html",

    # Catalogue & Pricing
    "reports_catalogue": "reports_catalogue.html",
    "pricing": "pricing.html",

    # Calculators Hub
    "calculators": "calculator_hub.html",
    "numerology-calculators": "calculator_hub.html",
    "insights": "insights_hub.html",

    # Company & Legal
    "about": "about.html",
    "contact": "contact.html",
    "consultation": "consultation.html",
    "practitioner": "practitioner.html",
    "privacy": "privacy.html",
    "privacy-policy": "privacy.html",
    "terms": "terms.html",
    "refund": "refund.html",
    "refund-policy": "refund.html",
    "cancel": "cancel.html",
    "cancellation": "cancel.html",
    "disclaimer": "disclaimer.html",
    "accessibility": "accessibility.html",
    "cookie_policy": "cookie_policy.html",
    "cookie-policy": "cookie_policy.html",

    # App & Tools
    "login": "login.html",
    "signup": "signup.html",
    "register": "signup.html",
    "dashboard": "dashboard.html",
    "charm-ai": "charm_ai.html",

    # Dedicated Tools
    "tools/lo-shu-grid": "tools/lo-shu-grid.html",
    "tools/name-numerology": "tools/name-numerology.html",
    "tools/name-balancing": "tools/name-balancing.html",
    "tools/mobile-numerology": "tools/mobile-numerology.html",
    "tools/life-path-calculator": "tools/life-path-calculator.html",
    "tools/compatibility-calculator": "tools/compatibility-calculator.html",
    "tools/business-alignment": "tools/business-alignment.html",
    "tools/business-numerology": "tools/business-alignment.html",
    "tools/baby-naming": "tools/baby-naming.html",
    "tools/property-numerology": "tools/property-numerology.html",
    "tools/vehicle-numerology": "tools/vehicle-numerology.html",
    "tools/blessing-years": "tools/blessing-years.html",
    "tools/profession-calculator": "tools/profession-calculator.html",
    "tools/lucky-number": "tools/lucky-number.html",
    "tools/logo-intelligence": "tools/logo-intelligence.html",
    "tools/logo-studio": "tools/logo-intelligence.html",

    # Knowledge, Methodology & Sitemap
    "your-reading": "your-reading.html",
    "sitemap": "sitemap.html",
    "methodology": "methodology.html",
    "numerology_overview": "numerology_overview.html",
    "numerology-overview": "numerology_overview.html",
    "faq": "faq.html",
    "compare": "compare_hub.html",
    "learn": "learn.html",

    # Specialised Calculator Directories
    "calculators/birth-number": "birth_number_calculator.html",
    "calculators/lo-shu-grid": "tools/lo-shu-grid.html",
    "calculators/pythagorean": "pythagorean_calculator.html",
    "calculators/personal-year": "tools/blessing-years.html",
    "calculators/life-path-number": "tools/life-path-calculator.html",
    "calculators/name-numerology": "tools/name-balancing.html",
    "calculators/chaldean-name-numerology": "tools/name-balancing.html",
    "calculators/mobile-number-numerology": "tools/mobile-numerology.html",
    "calculators/numerology-compatibility": "tools/compatibility-calculator.html",

    # Regional City Hubs
    "local": "local_hub.html",
    "local/delhi": "local_delhi.html",
    "local/mumbai": "local_mumbai.html",
    "local/bangalore": "local_bangalore.html",
    "local/dubai": "local_dubai.html",
}

for route_name, src_file in ROUTING_MAP.items():
    source_path = os.path.join(DIST_DIR, src_file)
    if os.path.exists(source_path):
        target_file = os.path.join(DIST_DIR, f"{route_name}.html")
        if os.path.normpath(target_file) != os.path.normpath(source_path):
            os.makedirs(os.path.dirname(target_file), exist_ok=True)
            shutil.copy2(source_path, target_file)
        target_index = os.path.join(DIST_DIR, route_name, "index.html")
        if os.path.normpath(target_index) != os.path.normpath(source_path):
            os.makedirs(os.path.dirname(target_index), exist_ok=True)
            shutil.copy2(source_path, target_index)

# 4. Standard Cloudflare _headers file
headers_content = """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), camera=(), microphone=()

/sw.js
  Cache-Control: no-cache, no-store, must-revalidate
  Pragma: no-cache

/*.html
  Cache-Control: public, max-age=0, must-revalidate

/static/*
  Cache-Control: public, max-age=31536000, immutable

/logos/*
  Cache-Control: public, max-age=31536000, immutable

/icons/*
  Cache-Control: public, max-age=31536000, immutable

/css/*
  Cache-Control: public, max-age=31536000, immutable

/js/*
  Cache-Control: public, max-age=31536000, immutable

/fonts/*
  Cache-Control: public, max-age=31536000, immutable
"""
with open(os.path.join(DIST_DIR, "_headers"), "w", encoding="utf-8") as f:
    f.write(headers_content)

# 5. Clean _redirects file (synced from app/static/_redirects)
src_redirects = os.path.join(STATIC_SRC, "_redirects")
if os.path.exists(src_redirects):
    shutil.copy2(src_redirects, os.path.join(DIST_DIR, "_redirects"))

# 5b. Cloudflare Pages _routes.json (limits Worker invocations to /api/* only)
src_routes = os.path.join(STATIC_SRC, "_routes.json")
if os.path.exists(src_routes):
    shutil.copy2(src_routes, os.path.join(DIST_DIR, "_routes.json"))

# 6. Synchronize isolated pdf_service directory
try:
    from scripts.sync_pdf_service import sync_pdf_service
    sync_pdf_service()
except Exception as e:
    print(f"Warning: could not sync pdf_service: {e}")

total_files = sum(len(files) for _, _, files in os.walk(DIST_DIR))
print(f"Successfully generated canonical Cloudflare Pages build in {DIST_DIR}")
print(f"Total physical files generated: {total_files}")


def verify_production_html_no_placeholders(dist_dir: str) -> None:
    """
    Production-deploy guard:
    Scans every built HTML file in dist_dir and fails if any {{...}} placeholder remains.
    On preview or development environments, placeholders (e.g. {{CONSENT_TEXT_PENDING}}) are permitted.
    """
    import re
    placeholder_pattern = re.compile(r"\{\{[A-Za-z0-9_]+\}\}")
    violations = []
    for dirpath, _, filenames in os.walk(dist_dir):
        for fn in filenames:
            if fn.lower().endswith(".html"):
                full_path = os.path.join(dirpath, fn)
                rel_path = os.path.relpath(full_path, dist_dir).replace("\\", "/")
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    matches = placeholder_pattern.findall(content)
                    if matches:
                        unique_matches = sorted(set(matches))
                        violations.append(f"{rel_path}: {unique_matches}")
    if violations:
        raise ValueError(
            "PRODUCTION DEPLOY BLOCKED: Built HTML contains unrendered template placeholders:\n"
            + "\n".join(violations[:20])
        )


if os.environ.get("ENVIRONMENT") == "production" or os.environ.get("BUILD_ENV") == "production":
    verify_production_html_no_placeholders(DIST_DIR)
    print("PASS: Production HTML verified with 0 unrendered {{...}} placeholders.")


def verify_wrangler_no_placeholders(toml_content: str) -> None:
    """Refuses to deploy while any placeholder database_id (e.g. 00000000-...) remains in wrangler.toml."""
    import re
    ids = re.findall(r'database_id\s*=\s*"([^"]*)"', toml_content)
    if not ids:
        raise ValueError("No database_id entries found in wrangler.toml.")
    for db_id in ids:
        clean = db_id.strip()
        if (
            not clean
            or clean.startswith("00000000-0000-0000-0000-")
            or "REPLACE" in clean.upper()
            or "PLACEHOLDER" in clean.upper()
            or "TODO" in clean.upper()
        ):
            raise ValueError(
                f"DEPLOYMENT BLOCKED: wrangler.toml contains placeholder database_id '{clean}'. "
                "Replace both production and preview database_ids with real D1 UUIDs before deploying."
            )


if __name__ == "__main__":
    import sys
    if "--verify-deploy" in sys.argv:
        wrangler_path = os.path.join(BASE_DIR, "wrangler.toml")
        with open(wrangler_path, "r", encoding="utf-8") as wf:
            verify_wrangler_no_placeholders(wf.read())
        print("PASS: wrangler.toml verified with real non-placeholder D1 database_ids.")
    if "--verify-production" in sys.argv:
        verify_production_html_no_placeholders(DIST_DIR)
        print("PASS: Production HTML verified with 0 unrendered {{...}} placeholders.")
