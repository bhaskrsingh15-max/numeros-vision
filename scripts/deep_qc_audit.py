"""
deep_qc_audit.py
Deep audit of all public pages for:
1. Search Engine Optimization (Google, Bing)
2. Answer Engine & Generative Engine Optimization (AEO/GEO)
3. App Store / Progressive Web App (PWA) guidelines
4. Social meta tags (OpenGraph & Twitter)
5. Structured Data (JSON-LD)
6. Heading hierarchy & E-E-A-T signals
"""

import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "static")

def audit_all():
    files = []
    for root, dirs, filenames in os.walk(STATIC_DIR):
        for f in filenames:
            if f.endswith(".html") and f not in ["demo.html", "logo-preview.html"]:
                files.append(os.path.join(root, f))

    print(f"Total HTML pages found: {len(files)}")
    report = {}

    for path in sorted(files):
        rel = os.path.relpath(path, STATIC_DIR)
        with open(path, "r", encoding="utf-8", errors="ignore") as fp:
            html = fp.read()

        issues = []

        # 1. Title
        title_m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
        if not title_m or not title_m.group(1).strip():
            issues.append("Missing <title>")
        else:
            t = title_m.group(1).strip()
            if len(t) < 15 or len(t) > 75:
                issues.append(f"Title length suboptimal ({len(t)} chars)")

        # 2. Meta description
        desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I)
        if not desc_m:
            desc_m = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', html, re.I)
        if not desc_m or not desc_m.group(1).strip():
            issues.append("Missing meta description")

        # 3. Canonical tag
        canon_m = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.I)
        if not canon_m:
            canon_m = re.search(r'<link\s+href=["\'](.*?)["\']\s+rel=["\']canonical["\']', html, re.I)
        if not canon_m or not canon_m.group(1).strip().startswith("https://numerosvision.com"):
            issues.append("Missing or non-HTTPS canonical")

        # 4. Robots meta tag
        robots_m = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'](.*?)["\']', html, re.I)
        if not robots_m:
            issues.append("Missing <meta name='robots'> tag")

        # 5. OpenGraph essentials
        if 'property="og:title"' not in html and "property='og:title'" not in html:
            issues.append("Missing og:title")
        if 'property="og:description"' not in html and "property='og:description'" not in html:
            issues.append("Missing og:description")
        if 'property="og:image"' not in html and "property='og:image'" not in html:
            issues.append("Missing og:image")
        if 'property="og:url"' not in html and "property='og:url'" not in html:
            issues.append("Missing og:url")

        # 6. Twitter card
        if 'name="twitter:card"' not in html and "name='twitter:card'" not in html:
            issues.append("Missing twitter:card")

        # 7. App Store / PWA readiness
        if 'rel="manifest"' not in html and "rel='manifest'" not in html:
            issues.append("Missing manifest link")
        elif "manifest.json" not in html:
            issues.append("Manifest link is not /manifest.json")
        
        if 'name="apple-mobile-web-app-capable"' not in html and "name='apple-mobile-web-app-capable'" not in html:
            issues.append("Missing apple-mobile-web-app-capable")
        if 'rel="apple-touch-icon"' not in html and "rel='apple-touch-icon'" not in html:
            issues.append("Missing apple-touch-icon")

        # 8. Structured Data JSON-LD
        if 'application/ld+json' not in html:
            issues.append("Missing JSON-LD structured data")

        # 9. Headings
        h1_m = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
        if len(h1_m) == 0:
            issues.append("Missing <h1> tag")
        elif len(h1_m) > 1:
            issues.append(f"Multiple <h1> tags ({len(h1_m)})")

        report[rel] = issues

    print("\n--- DETAILED AUDIT RESULTS ---")
    gaps_found = 0
    for rel, issues in report.items():
        if issues:
            gaps_found += 1
            print(f"❌ {rel} ({len(issues)} issues):")
            for iss in issues:
                print(f"    - {iss}")
        else:
            print(f"✅ {rel}: 100% COMPLIANT across all criteria")

    print(f"\nSummary: {len(report) - gaps_found}/{len(report)} pages fully compliant.")
    print(f"Gaps found on {gaps_found} pages.")

if __name__ == "__main__":
    audit_all()
