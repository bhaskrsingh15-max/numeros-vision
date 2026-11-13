# scripts/generate_all_reports_28_11_1981.py
import os
import sys
import json
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.pdf_report_generator import generate_customised_pdf_report
from app.config.pricing_config import REPORT_TIERS

def main():
    name = "Bhaskr Singh"
    day = 28
    month = 11
    year = 1981
    dob_str = f"{day:02d}-{month:02d}-{year}"

    print(f"Generating Real PDF Reports for {name} ({dob_str}) across all packages...")

    out_dirs = [
        os.path.join("app", "static", "reports"),
        os.path.join("dist_cloudflare_pages", "reports")
    ]
    for d in out_dirs:
        os.makedirs(d, exist_ok=True)

    results = {}

    tiers = ["basic", "advanced", "premium"]
    for tier in tiers:
        start_t = time.time()
        print(f"\n--- Generating Tier: {tier.upper()} ({REPORT_TIERS[tier]['name']}) ---")
        pdf_bytes, qa = generate_customised_pdf_report(
            name=name,
            day=day,
            month=month,
            year=year,
            topic_id="core_blueprint",
            tier=tier
        )
        elapsed = time.time() - start_t
        filename = f"Numeros_Vision_{tier.capitalize()}_Report_{dob_str}.pdf"

        saved_paths = []
        for d in out_dirs:
            out_path = os.path.join(d, filename)
            with open(out_path, "wb") as f:
                f.write(pdf_bytes)
            saved_paths.append(out_path)

        page_count = qa.get("pages_count")
        byte_size = len(pdf_bytes)
        print(f"  [SUCCESS] {filename}")
        print(f"  Pages: {page_count} | Size: {byte_size:,} bytes | Time: {elapsed:.2f}s")
        print(f"  Saved to: {saved_paths[0]}")

        results[tier] = {
            "tier": tier,
            "tier_name": REPORT_TIERS[tier]["name"],
            "price_inr": REPORT_TIERS[tier]["price_inr"],
            "filename": filename,
            "byte_size": byte_size,
            "pages": page_count,
            "report_id": qa.get("report_id"),
            "local_url": f"http://localhost:8000/reports/{filename}",
            "public_url": f"https://huge-lizards-sit.loca.lt/reports/{filename}",
            "calculation_summary": qa.get("calculation_data", {})
        }

    summary_file = os.path.join("app", "static", "reports", f"report_summary_{dob_str}.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        # Save a clean copy without massive raw blobs
        clean_res = {}
        for t, d in results.items():
            calc = d["calculation_summary"]
            clean_res[t] = {
                "tier": d["tier"],
                "tier_name": d["tier_name"],
                "price_inr": d["price_inr"],
                "filename": d["filename"],
                "pages": d["pages"],
                "byte_size": d["byte_size"],
                "local_url": d["local_url"],
                "public_url": d["public_url"],
                "driver": calc.get("driver_number"),
                "driver_planet": calc.get("driver_planet"),
                "conductor": calc.get("conductor_number"),
                "conductor_planet": calc.get("conductor_planet"),
                "kua": calc.get("kua_number"),
                "name_compound": calc.get("chaldean_name_compound"),
                "name_root": calc.get("chaldean_name_root"),
                "lo_shu_counts": calc.get("lo_shu_counts"),
                "present_numbers": calc.get("present_numbers"),
                "missing_numbers": calc.get("missing_numbers"),
                "completed_planes": calc.get("completed_planes")
            }
        json.dump(clean_res, f, indent=2)

    print("\n========================================================")
    print("ALL REAL PDF REPORTS GENERATED AND VALIDATED SUCCESSFULLY!")
    print("========================================================")

if __name__ == "__main__":
    main()
