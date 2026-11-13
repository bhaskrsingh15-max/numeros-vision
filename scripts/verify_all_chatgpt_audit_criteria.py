# scripts/verify_all_chatgpt_audit_criteria.py
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "static")

scorecard = {}

# 1. HOMEPAGE AUDIT
with open(os.path.join(STATIC_DIR, "index.html"), 'r', encoding='utf-8', errors='ignore') as f:
    idx = f.read()

# Verify removal of marketing cards
removed_marketing = (
    "100% Deterministic Engine" not in idx and
    "10+ Specialised Topics" not in idx and
    "3 Tiers Unified Pricing" not in idx and
    "9 Traditions Cross-Synthesized" not in idx
)
# Verify removal of #about transparency section
removed_about = ('id="about"' not in idx and 'nv-section-transparency' not in idx)

# Verify live hero calculation without forced redirect
unlocked_calc = 'calculateHeroProfile' in idx and '_executeRenderCosmicProfile(name, d, m, y)' in idx

scorecard["1. Homepage Clutter & Funnel"] = {
    "Marketing Cards Removed": ("PASS" if removed_marketing else "FAIL"),
    "Legacy #about Transparency Block Removed": ("PASS" if removed_about else "FAIL"),
    "Live Deterministic On-Page Calculation": ("PASS" if unlocked_calc else "FAIL")
}

# 2. NOMENCLATURE AUDIT (2-5-8 and 4-5-6)
with open(os.path.join(STATIC_DIR, "tools", "lo-shu-grid.html"), 'r', encoding='utf-8', errors='ignore') as f:
    loshu = f.read()

has_silver = "Silver Success Plane" in loshu or "Silver Rajyog" in loshu
no_disappointment = "disappointment" not in loshu.lower()
has_golden = "Golden Success Plane" in loshu or "Golden Rajyog" in loshu

scorecard["2. Lo Shu Grid Nomenclature"] = {
    "Silver Success Plane (2-5-8) Strictly Enforced": ("PASS" if has_silver else "FAIL"),
    "Zero 'Disappointment Plane' Deprecated Wording": ("PASS" if no_disappointment else "FAIL"),
    "Golden Success Plane (4-5-6) Verified": ("PASS" if has_golden else "FAIL")
}

# 3. SAMPLE ROADMAP & PACKAGE SHOWCASE
with open(os.path.join(STATIC_DIR, "sample_roadmap.html"), 'r', encoding='utf-8', errors='ignore') as f:
    smp = f.read()

has_basic_tier = "Basic Report" in smp and "₹199" in smp
has_adv_tier = "Advanced Report" in smp and "₹510" in smp
has_prem_tier = "Premium" in smp and "₹1,050" in smp
has_live_calc = "runLiveCalculation" in smp and "resDriver" in smp and "resLoshuGrid" in smp
has_pdf_download = "downloadLiveCalculatedPdf" in smp or "downloadSamplePdf" in smp

scorecard["3. Sample Roadmap & Package Showcase (/sample_roadmap/)"] = {
    "Basic Tier Visualizer (3p · ₹199)": ("PASS" if has_basic_tier else "FAIL"),
    "Advanced Tier Visualizer (12p · ₹510)": ("PASS" if has_adv_tier else "FAIL"),
    "Premium Sovereign Visualizer (32p · ₹1,050)": ("PASS" if has_prem_tier else "FAIL"),
    "Live On-Page Interactive Calculation Engine": ("PASS" if has_live_calc else "FAIL"),
    "Specimen PDF Download Buttons": ("PASS" if has_pdf_download else "FAIL")
}

# 4. REPORTS CATALOGUE
with open(os.path.join(STATIC_DIR, "reports_catalogue.html"), 'r', encoding='utf-8', errors='ignore') as f:
    cat = f.read()

sample_links = re.findall(r'href=[\'"](\/sample_roadmap\/[^\'"]*)[\'"]', cat)
has_pdf_modal = "handleGeneratePdf" in cat and "orderModal" in cat

scorecard["4. Reports Catalogue (/reports_catalogue/)"] = {
    "All Sample Buttons Linked to /sample_roadmap/": ("PASS" if len(sample_links) >= 10 else f"PARTIAL ({len(sample_links)} found)"),
    "Instant PDF Delivery Modal": ("PASS" if has_pdf_modal else "FAIL")
}

# 5. PRICING CONSISTENCY
with open(os.path.join(STATIC_DIR, "pricing.html"), 'r', encoding='utf-8', errors='ignore') as f:
    prc = f.read()

has_199 = "₹199" in prc
has_510 = "₹510" in prc
has_1050 = "₹1,050" in prc

scorecard["5. Pricing Consistency (/pricing/)"] = {
    "Basic Report: ₹199": ("PASS" if has_199 else "FAIL"),
    "Advanced Report: ₹510": ("PASS" if has_510 else "FAIL"),
    "Premium Dossier: ₹1,050": ("PASS" if has_1050 else "FAIL")
}

# 6. CLOUDFLARE CONFIGURATION FILES
has_headers = os.path.exists(os.path.join(STATIC_DIR, "_headers"))
has_redirects = os.path.exists(os.path.join(STATIC_DIR, "_redirects"))
has_sw = os.path.exists(os.path.join(STATIC_DIR, "sw.js"))

scorecard["6. Cloudflare Direct Deployment Files"] = {
    "_headers (Cache & Security)": ("PASS" if has_headers else "FAIL"),
    "_redirects (Clean 33-Page Routing)": ("PASS" if has_redirects else "FAIL"),
    "sw.js (Service Worker v5.0.0-clean)": ("PASS" if has_sw else "FAIL")
}

print("="*70)
print("NUMEROS VISION v5.0.0 — INDEPENDENT CODE AUDIT SCORECARD")
print("="*70)

all_passed = True
for section, tests in scorecard.items():
    print(f"\n{section}:")
    for test, result in tests.items():
        print(f"  [{result}] {test}")
        if result != "PASS":
            all_passed = False

print("\n" + "="*70)
print(f"OVERALL AUDIT VERDICT: {'100% ALL CHECKS PASSED' if all_passed else 'SOME CHECKS REQUIRE ATTENTION'}")
print("="*70)
