"""
Generates canonical packs.json and packs.ts directly from pricing_config.py.
Enforces:
- Standalone reports active
- Charm AI packs active
- 3 Bundles defined as report vouchers but marked status: 'inactive'
- Strike-through prices eliminated
- Monetary amounts in integer paise
"""

import json
import os
import sys

sys.path.insert(0, os.path.abspath("."))
from app.config.pricing_config import REPORT_TIERS, BUNDLES, CHARM_AI_PACKS

packs = {
    "version": "2.1.0",
    "currency": "INR",
    "updated_at": "2026-11-06T17:30:00Z",
    "core_reports": {},
    "bundles": {},
    "charm_ai": {}
}

# 1. Standalone Reports
for tier_id, data in REPORT_TIERS.items():
    pack_key = f"report_{tier_id}"
    packs["core_reports"][pack_key] = {
        "pack_id": pack_key,
        "tier_id": tier_id,
        "name": data["name"],
        "display_name": data["display_name"],
        "pages": data["pages"],
        "price_inr": data["price_inr"],
        "amount_paise": data["price_inr"] * 100,
        "digital_root": data["digital_root"],
        "status": "active",
        "deliverables": data["deliverables"],
        "progressive_unlock": "includes_basic" if tier_id in ["advanced", "premium"] else "entry"
    }

# 2. Multi-Report Bundles (Defined with vouchers, marked INACTIVE pending confirmation)
for bundle_id, data in BUNDLES.items():
    packs["bundles"][bundle_id] = {
        "pack_id": bundle_id,
        "name": data["name"],
        "display_name": data["display_name"],
        "price_inr": data["bundle_price_inr"],
        "amount_paise": data["bundle_price_inr"] * 100,
        "digital_root": data["digital_root"],
        "status": "inactive",  # Pending user price confirmation
        "voucher_allocation": {
            "basic_vouchers": data.get("basic_report_count", 0),
            "advanced_vouchers": data.get("advanced_report_count", 0),
            "premium_vouchers": data.get("premium_report_count", 0)
        },
        "deliverables": data["deliverables"]
    }

# 3. Charm AI Packs
for pack_id, data in CHARM_AI_PACKS.items():
    # Only charm_free and charm_single are active; multi and extended held inactive pending question count confirmation
    is_active = pack_id in ["charm_free", "charm_single"]
    packs["charm_ai"][pack_id] = {
        "pack_id": pack_id,
        "name": data["name"],
        "display_name": data["display_name"],
        "price_inr": data["price_inr"],
        "amount_paise": data["amount_paise"],
        "questions_count": data["questions_count"],
        "digital_root": data.get("digital_root", 0),
        "status": "active" if is_active else "inactive",
        "deliverables": data["deliverables"]
    }

# Save JSON
json_path = os.path.join("app", "config", "packs.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(packs, f, indent=2)

# Save TypeScript definition
ts_path = os.path.join("app", "config", "packs.ts")
ts_content = f"""/**
 * NUMEROS VISION — CANONICAL PACK CATALOG (TypeScript)
 * Auto-generated from app/config/pricing_config.py
 * Enforces server-side authority, integer paise, and voucher architectures.
 */

export interface PackDefinition {{
  pack_id: string;
  name: string;
  display_name: string;
  price_inr: number;
  amount_paise: number;
  digital_root?: number;
  status: 'active' | 'inactive';
  pages?: number;
  deliverables: string[];
  voucher_allocation?: {{
    basic_vouchers: number;
    advanced_vouchers: number;
    premium_vouchers: number;
  }};
  questions_count?: number;
  progressive_unlock?: string;
}}

export const PACK_CATALOG: {{
  version: string;
  currency: string;
  core_reports: Record<string, PackDefinition>;
  bundles: Record<string, PackDefinition>;
  charm_ai: Record<string, PackDefinition>;
}} = {json.dumps(packs, indent=2)};

export default PACK_CATALOG;
"""
with open(ts_path, "w", encoding="utf-8") as f:
    f.write(ts_content)

print("Successfully generated app/config/packs.json and app/config/packs.ts")
