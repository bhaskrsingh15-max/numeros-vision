import os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

replacements = [
    # Explicit phrases first
    ('Kundali Milan', 'Compatibility Synastry'),
    ('kundali-milan', 'compatibility-calculator'),
    ('Astrological Evidence', 'Planetary Resonance Evidence'),
    ('astrological evidence', 'planetary resonance evidence'),
    ('Vedic, Astrological & Practical', 'Vedic Gharelu, Elemental & Practical'),
    ('Vedic, Astrological &amp; Practical', 'Vedic Gharelu, Elemental &amp; Practical'),
    ('astrological or occult', 'numerological or vibrational'),
    ('astrology or occult', 'numerology or analytical systems'),
    ('Astrology & Occult', 'Numerology & Analytical Systems'),
    ('Astrology &amp; Occult', 'Numerology &amp; Analytical Systems'),
    ('Astrology, and Gemology', 'Numerology, and Planetary Vibrations'),
    ('Astrology, and', 'Numerology, and'),
    ('Astrology,', 'Numerology,'),
    ('astrology,', 'numerology,'),
    ('"Astrology"', '"Numerology"'),
    ('"Astrologer"', '"Numerology Consultant"'),
    ('"Astrologer / Numerologist / Tarot Reader"', '"Master Numerologist & Systems Consultant"'),
    ('Astrologer / Numerologist / Tarot Reader', 'Master Numerologist & Systems Consultant'),
    ('Astrologer', 'Numerology Consultant'),
    ('astrologer', 'numerology consultant'),
    ('astrological', 'numerological'),
    ('Astrological', 'Numerological'),
    ('astrology', 'numerology'),
    ('Astrology', 'Numerology'),
    ('kundali', 'natal numerology chart'),
    ('Kundali', 'Natal Numerology Chart'),
    ('kundli', 'natal numerology chart'),
    ('Kundli', 'Natal Numerology Chart'),
    ('zodiac', 'planetary archetype'),
    ('Zodiac', 'Planetary Archetype'),
    ('horoscope', 'destiny forecast'),
    ('Horoscope', 'Destiny Forecast'),
]

count = 0
for root, dirs, files in os.walk('app/static'):
    for f in files:
        if f.endswith('.html'):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                modified = False
                for target, repl in replacements:
                    if target in content:
                        content = content.replace(target, repl)
                        modified = True
                if modified:
                    with open(p, 'w', encoding='utf-8') as fp:
                        fp.write(content)
                    count += 1
            except Exception as e:
                print(f"Error on {p}: {e}")

print(f"Total HTML files scrubbed of astrology words: {count}")
