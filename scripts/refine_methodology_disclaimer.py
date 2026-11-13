import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

path_meth = os.path.join(BASE_DIR, "app", "static", "methodology.html")
with open(path_meth, "r", encoding="utf-8") as f:
    meth = f.read()

meth = meth.replace(
    "Charm AI draws upon a sanitized corpus of 10,826 validated occult literature passages, including classical texts by Cheiro, Classical Vedic Tradition, and traditional Vedic authorities.",
    "Numeros Vision draws upon authoritative classical literature and time-honored traditions, including verified works by Cheiro and foundational Vedic authorities."
)

with open(path_meth, "w", encoding="utf-8") as f:
    f.write(meth)

path_disc = os.path.join(BASE_DIR, "app", "static", "disclaimer.html")
with open(path_disc, "r", encoding="utf-8") as f:
    disc = f.read()

disc = disc.replace(
    "While our model has been evaluated for consistency",
    "While our readings are structured for consistency"
)

with open(path_disc, "w", encoding="utf-8") as f:
    f.write(disc)

print("✓ methodology.html and disclaimer.html refined.")
