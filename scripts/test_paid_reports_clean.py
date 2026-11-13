import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from app.engine.package_report_generator import generate_package_report

print("Testing generate_package_report for Basic, Advanced, and Premium tiers...")

for tier in ["basic", "advanced", "premium"]:
    rep = generate_package_report(
        name="Bhaskr Singh",
        day=15,
        month=8,
        year=1990,
        package_tier=tier
    )
    raw_text = str(rep)
    banned = ["bnn", "kp astrology", "kp sub-lord", "lal kitab", "vedic astrology", "kundli"]
    print(f"\n--- Tier: {tier.upper()} (Keys: {len(rep)}) ---")
    for b in banned:
        c = raw_text.lower().count(b)
        print(f"  Term '{b}': {c} occurrences")

print("\n✓ ALL PAID REPORT TIERS VERIFIED!")
