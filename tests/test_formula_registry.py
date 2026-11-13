import os
import sys
import json
import unittest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

class TestFormulaRegistry(unittest.TestCase):
    """
    Golden unit test suite for the Master Canonical Formula Registry.
    Tests every formula schema, boundary conditions, edge cases, letter mappings,
    and reduction policies without external network or LLM dependencies.
    """

    @classmethod
    def setUpClass(cls):
        registry_path = os.path.join(_ROOT, "data", "knowledge_base", "formula_registry.json")
        cls.assertTrue(cls, os.path.exists(registry_path), f"Missing {registry_path}")
        with open(registry_path, "r", encoding="utf-8") as f:
            cls.registry = json.load(f)
        cls.formulas_by_id = {f["formula_id"]: f for f in cls.registry["formulas"]}

    def test_registry_metadata_and_integrity(self):
        """Verify registry has valid top-level schema and at least 8 approved formulas."""
        self.assertIn("version", self.registry)
        self.assertIn("formulas", self.registry)
        self.assertGreaterEqual(len(self.registry["formulas"]), 8)
        for formula in self.registry["formulas"]:
            for required_field in ["formula_id", "tradition", "topic", "inputs", "steps", "reduction_policy", "status"]:
                self.assertIn(required_field, formula, f"Formula {formula.get('formula_id')} missing {required_field}")
            self.assertIn(formula["status"], ["approved", "needs_review", "draft"])

    def test_chaldean_name_calculation_edge_cases(self):
        """Test Chaldean name calculations: uppercase, lowercase, whitespace, hyphens, compound numbers."""
        formula = self.formulas_by_id["chaldean.name.compound_and_root.v1"]
        mapping = formula["mapping"]

        def calc_chaldean(name: str):
            clean = "".join(c.upper() for c in name if c.isalpha())
            compound = sum(mapping.get(c, 0) for c in clean)
            root = compound
            while root > 9:
                root = sum(int(d) for d in str(root))
            return compound, root

        # Standard case: "Bhaskr" (15) + "Singh" (17) = 32 -> 5
        comp, root = calc_chaldean("Bhaskr Singh")
        self.assertEqual(comp, 32)
        self.assertEqual(root, 5)

        # Mixed-case, whitespace, and hyphens
        comp2, root2 = calc_chaldean("  bHaSkR - sInGh  ")
        self.assertEqual(comp2, 32)
        self.assertEqual(root2, 5)

        # Elon Musk: E(5)+L(3)+O(7)+N(5)=20, M(4)+U(6)+S(3)+K(2)=15. Total = 35 -> 8
        comp3, root3 = calc_chaldean("Elon Musk")
        self.assertEqual(comp3, 35)
        self.assertEqual(root3, 8)

        # Cheiro: C(2)+H(5)+E(5)+I(1)+R(2)+O(7) = 22 -> 4
        comp4, root4 = calc_chaldean("Cheiro")
        self.assertEqual(comp4, 22)
        self.assertEqual(root4, 4)

        # Verify Digit 9 is excluded from Chaldean alphabet values
        self.assertNotIn("9", [str(v) for v in mapping.values()])

    def test_pythagorean_expression_and_master_numbers(self):
        """Test Pythagorean expression calculation and preservation of Master Numbers 11, 22, 33."""
        formula = self.formulas_by_id["pythagorean.expression.v1"]
        mapping = formula["mapping"]

        def calc_pythagorean(name: str):
            clean = "".join(c.upper() for c in name if c.isalpha())
            raw_sum = sum(mapping.get(c, 0) for c in clean)
            val = raw_sum
            while val > 9 and val not in (11, 22, 33):
                val = sum(int(d) for d in str(val))
            return raw_sum, val, (val in (11, 22, 33))

        # "John Doe": J(1)+O(6)+H(8)+N(5) + D(4)+O(6)+E(5) = 20 + 15 = 35 -> 8
        raw, expr, is_master = calc_pythagorean("John Doe")
        self.assertEqual(expr, 8)
        self.assertFalse(is_master)

        # All letters A-Z mapped sequentially 1-9
        for i, char in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            expected_val = (i % 9) + 1
            self.assertEqual(mapping[char], expected_val, f"Mismatch for {char}")

    def test_vedic_mulank_calculation(self):
        """Test Mulank (Driver Number) calculation for days 1 to 31."""
        def calc_mulank(day: int):
            while day > 9:
                day = sum(int(d) for d in str(day))
            return day

        self.assertEqual(calc_mulank(1), 1)
        self.assertEqual(calc_mulank(9), 9)
        self.assertEqual(calc_mulank(10), 1)
        self.assertEqual(calc_mulank(15), 6)
        self.assertEqual(calc_mulank(28), 1)
        self.assertEqual(calc_mulank(29), 2)
        self.assertEqual(calc_mulank(31), 4)

    def test_vedic_bhagyank_calculation(self):
        """Test Bhagyank (Conductor / Destiny Number) calculation from full date."""
        def calc_bhagyank(day: int, month: int, year: int):
            digits = [int(d) for d in f"{day:02d}{month:02d}{year:04d}"]
            total = sum(digits)
            while total > 9:
                total = sum(int(d) for d in str(total))
            return total

        # 28-11-1981: 2+8+1+1+1+9+8+1 = 31 -> 3+1 = 4
        self.assertEqual(calc_bhagyank(28, 11, 1981), 4)
        # 15-08-1947: 1+5+0+8+1+9+4+7 = 35 -> 3+5 = 8
        self.assertEqual(calc_bhagyank(15, 8, 1947), 8)

    def test_loshu_grid_and_planes(self):
        """Test Lo Shu 3x3 Magic Square digit coordinates and plane detection."""
        formula = self.formulas_by_id["loshu.grid_and_planes.v1"]
        coord_map = formula["mapping"]

        # 3x3 Grid values: 4-9-2 (Row 0), 3-5-7 (Row 1), 8-1-6 (Row 2)
        expected_coords = {
            "4": (0, 0), "9": (0, 1), "2": (0, 2),
            "3": (1, 0), "5": (1, 1), "7": (1, 2),
            "8": (2, 0), "1": (2, 1), "6": (2, 2)
        }
        for digit_str, (row, col) in expected_coords.items():
            self.assertEqual(coord_map[digit_str]["row"], row)
            self.assertEqual(coord_map[digit_str]["col"], col)

        # Plane definitions
        planes = {
            "Mental": [4, 9, 2],
            "Emotional": [3, 5, 7],
            "Practical": [8, 1, 6],
            "Thought": [4, 3, 8],
            "Will": [9, 5, 1],
            "Action": [2, 7, 6],
            "Golden": [4, 5, 6],
            "Silver": [2, 5, 8]
        }

        # Date 28-11-1981 with Mulank 1, Bhagyank 4: digits = [2,8,1,1,1,9,8,1, 1, 4]
        digits = [2, 8, 1, 1, 1, 9, 8, 1, 1, 4]
        present_digits = set(digits)
        missing_digits = [d for d in range(1, 10) if d not in present_digits]
        self.assertEqual(missing_digits, [3, 5, 6, 7])

        # Check planes present:
        # Mental (4,9,2): 4 present, 9 present, 2 present -> FULL MENTAL PLANE PRESENT!
        self.assertTrue(all(d in present_digits for d in [4, 9, 2]))
        # Emotional (3,5,7): 3,5,7 missing -> Emotional plane completely absent
        self.assertFalse(any(d in present_digits for d in [3, 5, 7]))

    def test_personal_year_calculation(self):
        """Test Personal Year cycle calculation."""
        def calc_personal_year(birth_day: int, birth_month: int, target_year: int):
            digits = [int(d) for d in f"{birth_day:02d}{birth_month:02d}{target_year:04d}"]
            total = sum(digits)
            while total > 9:
                total = sum(int(d) for d in str(total))
            return total

        # Birthday Nov 28 (28-11), Year 2026: 2+8 + 1+1 + 2+0+2+6 = 10 + 2 + 10 = 22 -> 4
        self.assertEqual(calc_personal_year(28, 11, 2026), 4)
        # Birthday Aug 15 (15-08), Year 2026: 1+5 + 0+8 + 2+0+2+6 = 6 + 8 + 10 = 24 -> 6
        self.assertEqual(calc_personal_year(15, 8, 2026), 6)

if __name__ == "__main__":
    unittest.main()
