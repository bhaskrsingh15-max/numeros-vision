"""
Canonical builder for Numeros Vision Mulank Pilot Cards (Mulank 1 to 9).
Delegates to scripts/revise_mulank_pilot_cards.py.
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.revise_mulank_pilot_cards import write_files

if __name__ == '__main__':
    write_files()
