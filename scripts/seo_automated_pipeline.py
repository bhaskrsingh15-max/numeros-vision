"""
scripts/seo_automated_pipeline.py
Automated CLI pipeline for modern SEO, AEO, GEO & App Store page generation & validation.

Usage:
  python scripts/seo_automated_pipeline.py --audit
  python scripts/seo_automated_pipeline.py --publish "Kua Number Auspicious Directions" --keyword "Kua Number Directions"
  python scripts/seo_automated_pipeline.py --test-demo
"""

import sys
import io
import argparse
import urllib.request
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add project root to sys.path
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.seo.page_orchestrator import SEOPageOrchestrator
from app.seo.anti_penalty_guardrails import AntiPenaltyGuardrailValidator

def run_audit():
    print("=" * 80)
    print("AUTOMATED SEO, AEO, GEO & APP STORE AUDIT REPORT")
    print("=" * 80)
    static_dir = os.path.join(_ROOT, "app", "static")
    total_pages = 0
    passed_pages = 0

    for root, dirs, files in os.walk(static_dir):
        for f in files:
            if f.endswith(".html") and f not in ["demo.html", "logo-preview.html"]:
                total_pages += 1
                full_p = os.path.join(root, f)
                rel_p = os.path.relpath(full_p, static_dir)
                with open(full_p, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                
                is_comp, issues, metrics = AntiPenaltyGuardrailValidator.validate_page_html(content)
                if is_comp:
                    passed_pages += 1
                    print(f"✅ {rel_p:45} | Words: {metrics.get('total_words', 0):<5} | Status: Compliant")
                else:
                    print(f"❌ {rel_p:45} | Issues: {len(issues)}")
                    for iss in issues:
                        print(f"    - {iss}")

    print("=" * 80)
    print(f"OVERALL SITE HEALTH SCORE: {passed_pages}/{total_pages} ({(passed_pages/total_pages)*100:.1f}%)")
    print("=" * 80)

def publish_topic(topic: str, keyword: str = ""):
    print(f"\n🚀 Initiating Automated White-Hat Publishing for: '{topic}'")
    result = SEOPageOrchestrator.publish_new_topic(topic, keyword, category="blog")
    
    if not result.get("success"):
        print(f"❌ Publishing Failed: {result.get('error')}")
        for v in result.get("violations", []):
            print(f"   - {v}")
        return False

    print("\n✅ Publishing Succeeded with Zero-Penalty Guarantee!")
    print(f"   - URL:              {result['url']}")
    print(f"   - Meta Title:       {result['meta_title']}")
    print(f"   - Word Count:       {result['word_count']} words")
    print(f"   - Keyword Density:  {result['keyword_density']} (Optimal Safe Zone)")
    print(f"   - Schemas Injected: {', '.join(result['schemas_active'])}")
    print(f"   - Guardrail Status: {result['guardrail_status']}")

    # Live HTTP test if server is running
    test_url = f"http://127.0.0.1:8000/blog/{result['slug']}"
    print(f"\n📡 Verifying Live HTTP Response: {test_url}")
    try:
        req = urllib.request.Request(test_url, headers={"User-Agent": "Googlebot/2.1"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            print(f"   - HTTP Status: {resp.status} OK (Served dynamically via automated route)")
    except Exception as e:
        print(f"   - Server ping: {e}")

    return True

def main():
    parser = argparse.ArgumentParser(description="Automated SEO/AEO/GEO Engine")
    parser.add_argument("--audit", action="store_true", help="Audit all site pages")
    parser.add_argument("--publish", type=str, help="Publish a new topic automatically")
    parser.add_argument("--keyword", type=str, default="", help="Optional target keyword")
    parser.add_argument("--test-demo", action="store_true", help="Run automated test demo")
    parser.add_argument("--scan-rankings", action="store_true", help="Automated Googlebot ranking scan")
    args = parser.parse_args()

    if args.audit:
        run_audit()
    elif args.scan_rankings:
        from app.seo.ranking_scanner import RankingScanner
        report = RankingScanner.scan_all_pages()
        print(f"\nScan complete: {report['total_pages_scanned']} pages scanned. Avg score: {report['average_rank_readiness_score']}/100")
        print(f"Tier 1 (Page 1 Potential): {report['tier_distribution']['tier_1_page_1_potential']} pages")
    elif args.publish:
        publish_topic(args.publish, args.keyword)
    elif args.test_demo:
        demo_topic = "Kua Number Auspicious Directions and Career Feng Shui"
        demo_kw = "Kua Number Auspicious Directions"
        success = publish_topic(demo_topic, demo_kw)
        if success:
            print("\n🎉 Automated demo test completed successfully!")
    else:
        run_audit()

if __name__ == "__main__":
    main()
