"""
NUMEROS VISION — NUMEROLOGICAL DIGIT SUM TEST FOR ALL PRICES & MRPS
Validates that every displayed price, launch offer MRP, Charm AI pack,
bundle/upgrade price, and geo-pricing amount reduces to 1, 3, 5, or 6 (Sun, Jupiter, Mercury, Venus).
"""

import unittest
import json
import os
import re

ALLOWED_DIGIT_ROOTS = {1, 3, 5, 6}

def reduce_to_root(num_or_str) -> int:
    # Extract all digits
    digits = [int(c) for c in str(num_or_str) if c.isdigit()]
    if not digits:
        raise ValueError(f"No digits found in {num_or_str}")
    total = sum(digits)
    while total > 9:
        total = sum(int(c) for c in str(total))
    return total

class TestPriceDigitSums(unittest.TestCase):

    def test_packs_json_core_reports(self):
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        packs_file = os.path.join(root_dir, 'app', 'config', 'packs.json')
        with open(packs_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for pack_id, pack in data.get('core_reports', {}).items():
            price = pack.get('price_inr')
            mrp = pack.get('mrp_inr')
            if price:
                r_price = reduce_to_root(price)
                self.assertIn(r_price, ALLOWED_DIGIT_ROOTS,
                              f"Pack {pack_id} price {price} reduces to {r_price}, expected one of {ALLOWED_DIGIT_ROOTS}")
            if mrp:
                r_mrp = reduce_to_root(mrp)
                self.assertIn(r_mrp, ALLOWED_DIGIT_ROOTS,
                              f"Pack {pack_id} MRP {mrp} reduces to {r_mrp}, expected one of {ALLOWED_DIGIT_ROOTS}")

    def test_planner_pricing(self):
        offer_price = 1499
        mrp = 1999
        r_offer = reduce_to_root(offer_price)
        r_mrp = reduce_to_root(mrp)
        self.assertIn(r_offer, ALLOWED_DIGIT_ROOTS, f"Planner offer {offer_price} root {r_offer} invalid")
        self.assertIn(r_mrp, ALLOWED_DIGIT_ROOTS, f"Planner MRP {mrp} root {r_mrp} invalid")

    def test_charm_ai_packs(self):
        charm_packs = [
            ("5 questions", 199),
            ("12 questions", 399),
            ("25 questions", 699)
        ]
        for name, price in charm_packs:
            r = reduce_to_root(price)
            self.assertIn(r, ALLOWED_DIGIT_ROOTS, f"Charm AI pack '{name}' price {price} root {r} invalid")

    def test_bundle_and_upgrades(self):
        items = [
            ("Bundle (Premium + Planner)", 1949),
            ("Upgrade Basic -> Advanced", 289),
            ("Upgrade Advanced -> Premium", 561),
            ("Upgrade Basic -> Premium", 851)
        ]
        for name, price in items:
            r = reduce_to_root(price)
            self.assertIn(r, ALLOWED_DIGIT_ROOTS, f"Item '{name}' price {price} root {r} invalid")

    def test_geo_pricing_us_usd(self):
        us_prices = [
            ("Basic Offer", "5.99"), ("Basic MRP", "8.49"),
            ("Advanced Offer", "12.99"), ("Advanced MRP", "18.95"),
            ("Premium Offer", "24.99"), ("Premium MRP", "35.49"),
            ("Planner Offer", "28.99"), ("Planner MRP", "37.99")
        ]
        for label, val in us_prices:
            r = reduce_to_root(val)
            self.assertIn(r, ALLOWED_DIGIT_ROOTS, f"US '{label}' ${val} digit sum root {r} invalid")

    def test_geo_pricing_europe_eur(self):
        eur_prices = [
            ("Basic Offer", "5.99"), ("Basic MRP", "8.49"),
            ("Advanced Offer", "14.99"), ("Advanced MRP", "21.99"),
            ("Premium Offer", "28.99"), ("Premium MRP", "41.99"),
            ("Planner Offer", "32.99"), ("Planner MRP", "43.95")
        ]
        for label, val in eur_prices:
            r = reduce_to_root(val)
            self.assertIn(r, ALLOWED_DIGIT_ROOTS, f"Europe '{label}' €{val} digit sum root {r} invalid")

    def test_geo_pricing_middle_east_aed(self):
        aed_prices = [
            ("Basic Offer", "21.99"), ("Basic MRP", "30.99"),
            ("Advanced Offer", "46.99"), ("Advanced MRP", "66.99"),
            ("Premium Offer", "91.99"), ("Premium MRP", "131.99"),
            ("Planner Offer", "105.99"), ("Planner MRP", "140.99")
        ]
        for label, val in aed_prices:
            r = reduce_to_root(val)
            self.assertIn(r, ALLOWED_DIGIT_ROOTS, f"Middle East '{label}' AED {val} digit sum root {r} invalid")

if __name__ == '__main__':
    unittest.main()
