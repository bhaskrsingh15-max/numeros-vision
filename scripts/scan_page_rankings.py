"""
scripts/scan_page_rankings.py
Automated Search Engine Ranking & Competitiveness Scanner CLI.

Emulates Googlebot, crawls all 30 pages, evaluates SERP ranking readiness,
identifies Page 1 potential, and outputs an actionable audit matrix.

Usage:
  python scripts/scan_page_rankings.py
  python scripts/scan_page_rankings.py --target "http://127.0.0.1:8000"
"""

import sys
import io
import os
import argparse

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.seo.ranking_scanner import RankingScanner

def main():
    parser = argparse.ArgumentParser(description="Automated Search Engine Ranking Scanner")
    parser.add_argument("--target", type=str, default="http://127.0.0.1:8000", help="Base URL to scan")
    args = parser.parse_args()

    print("=" * 85)
    print("NUMEROS VISION — AUTOMATED SEARCH ENGINE RANKING SCANNER")
    print(f"Crawler Emulation: Googlebot/2.1 (Smartphone / Desktop)")
    print(f"Target Host:       {args.target}")
    print("=" * 85)

    report = RankingScanner.scan_all_pages(args.target)

    print(f"\n📊 SCAN COMPLETE — {report['total_pages_scanned']} Pages Evaluated")
    print(f"⭐ Average Rank-Readiness Score: {report['average_rank_readiness_score']} / 100")
    print(f"🏆 Tier 1 (Page 1 Potential):     {report['tier_distribution']['tier_1_page_1_potential']} pages")
    print(f"🥈 Tier 2 (Top 10-20 Contenders): {report['tier_distribution']['tier_2_top_20_contenders']} pages")
    print(f"🔧 Tier 3 (Needs Tuning):         {report['tier_distribution']['tier_3_needs_tuning']} pages")

    print("\n" + "-" * 85)
    print(f"{'PATH':<40} | {'SCORE':<6} | {'TIER':<24} | {'LATENCY'}")
    print("-" * 85)

    for p in report["pages"]:
        path = p.get("path", "")
        score = p.get("rank_readiness_score", 0)
        tier = p.get("predicted_serp_tier", "Unknown").split(":")[0]
        ttfb = f"{p.get('ttfb_ms', 0)} ms"
        print(f"{path:<40} | {score:<6} | {tier:<24} | {ttfb}")

    print("-" * 85)
    print(f"💾 Full Ranking Audit Report persisted to: {report['saved_to']}")
    print("=" * 85)

if __name__ == "__main__":
    main()
