import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Clean sample2.html
path_s2 = os.path.join(BASE_DIR, "app", "static", "sample2.html")
if os.path.exists(path_s2):
    with open(path_s2, "r", encoding="utf-8") as f:
        s2 = f.read()

    s2 = s2.replace("Vedic astrology, read to the degree", "Vedic Numerology, calculated to the root")
    s2 = s2.replace("Remedies &amp; Lal Kitab", "Remedies &amp; Elemental Balancing")
    s2 = s2.replace("Advanced · KP", "Advanced · Timing Dasha")
    s2 = s2.replace("Cuspal sub-lords (KP)", "Dasha Epicycles &amp; Timing")
    s2 = s2.replace("KP cuspal sub-lord timing: when an event manifests, to the antardasha.", "Temporal Dasha timing: when an event manifests, to the Pratyantardasha window.")
    s2 = s2.replace("Vedic astrology and numerology engine", "Planetary and Chaldean numerology engine")
    s2 = s2.replace("Free Kundli, compatibility, transit predictions", "Free Lo Shu, compatibility, cycle predictions")

    with open(path_s2, "w", encoding="utf-8") as f:
        f.write(s2)
    print("✓ app/static/sample2.html scrubbed successfully.")

# Clean demo.html
path_demo = os.path.join(BASE_DIR, "app", "static", "demo.html")
if os.path.exists(path_demo):
    with open(path_demo, "r", encoding="utf-8") as f:
        demo = f.read()

    demo = demo.replace("Lal Kitab", "Vedic Numerology")
    with open(path_demo, "w", encoding="utf-8") as f:
        f.write(demo)
    print("✓ app/static/demo.html scrubbed successfully.")
