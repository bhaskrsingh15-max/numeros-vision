"""
Golden 10-Date Calculation Test (Single-Digit 1..9 Contract)
============================================================
Verifies that core_matrix_engine.py and pdf_report_generator.py
produce identical single-digit Driver (Mulank 1..9), Conductor (Bhagyank 1..9,
with master numbers 11/22/33 retained only as intermediate reduction path notes),
and Planet from the reduced digit across all 10 golden dates.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.engine.core_matrix_engine import (
    calculate_driver,
    calculate_conductor,
    calculate_conductor_details,
)
from app.services.pdf_report_generator import run_deterministic_calculation

GOLDEN_10_DATES = [
    # (dob_str, day, month, year, expected_driver, expected_conductor_raw, expected_conductor_root, expected_conductor_display, expected_planet_short)
    ("28-11-1981", 28, 11, 1981, 1, 4, 4, "4", "Rahu"),
    ("15-07-1990", 15, 7, 1990, 6, 5, 5, "5", "Mercury"),
    ("10-08-1990", 10, 8, 1990, 1, 1, 1, "1", "Sun"),
    ("12-03-1982", 12, 3, 1982, 3, 8, 8, "8", "Saturn"),
    ("01-01-2007", 1, 1, 2007, 1, 2, 2, "2", "Moon"),
    ("14-06-1980", 14, 6, 1980, 5, 2, 2, "2", "Moon"),
    ("02-09-2009", 2, 9, 2009, 2, 4, 4, "4", "Rahu"),
    ("29-11-1999", 29, 11, 1999, 2, 5, 5, "5", "Mercury"),
    ("15-08-1990", 15, 8, 1990, 6, 6, 6, "6", "Venus"),
    ("24-09-1999", 24, 9, 1999, 6, 7, 7, "7", "Ketu"),
]


def test_golden_10_dates_python():
    for (
        dob_str,
        d,
        m,
        y,
        exp_drv,
        exp_raw,
        exp_root,
        exp_disp,
        exp_planet,
    ) in GOLDEN_10_DATES:
        # 1. Core Matrix Engine
        drv = calculate_driver(d)
        raw = calculate_conductor(d, m, y)
        details = calculate_conductor_details(d, m, y)
        assert drv == exp_drv, f"{dob_str}: driver {drv} != {exp_drv}"
        assert raw == exp_raw, f"{dob_str}: conductor_raw {raw} != {exp_raw}"
        assert details["conductor_root"] == exp_root, (
            f"{dob_str}: conductor_root {details['conductor_root']} != {exp_root}"
        )
        assert details["conductor_display"] == exp_disp, (
            f"{dob_str}: conductor_display {details['conductor_display']} != {exp_disp}"
        )
        assert details["conductor_planet"] == exp_planet, (
            f"{dob_str}: conductor_planet {details['conductor_planet']} != {exp_planet}"
        )

        # 2. PDF Report Generator
        pdf_calc = run_deterministic_calculation("Golden Seeker", d, m, y)
        assert pdf_calc["driver_number"] == exp_drv, (
            f"{dob_str} PDF: driver {pdf_calc['driver_number']} != {exp_drv}"
        )
        assert pdf_calc["conductor_number"] == exp_raw, (
            f"{dob_str} PDF: conductor_number {pdf_calc['conductor_number']} != {exp_raw}"
        )
        assert pdf_calc["conductor_root"] == exp_root, (
            f"{dob_str} PDF: conductor_root {pdf_calc['conductor_root']} != {exp_root}"
        )
        assert pdf_calc["conductor_display"] == exp_disp, (
            f"{dob_str} PDF: conductor_display {pdf_calc['conductor_display']} != {exp_disp}"
        )
        assert pdf_calc["conductor_planet"].startswith(exp_planet), (
            f"{dob_str} PDF: conductor_planet {pdf_calc['conductor_planet']} does not start with {exp_planet}"
        )

    print("PASS: All 10 golden dates verified across core_matrix_engine.py and pdf_report_generator.py.")


if __name__ == "__main__":
    test_golden_10_dates_python()
