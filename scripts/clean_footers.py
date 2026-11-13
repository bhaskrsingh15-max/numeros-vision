import glob
import re
import os

files = [
    'app/static/blog/gemstone-remedies.html',
    'app/static/blog/life-path-numbers-explained.html',
    'app/static/blog/vedic-gemstone-remedies.html',
    'app/static/blog/what-is-numerology.html',
    'app/static/tools/life-path-calculator.html',
    'app/static/tools/lo-shu-grid.html',
    'app/static/tools/lucky-number.html',
    'app/static/tools/name-balancing.html',
    'app/static/tools/name-numerology.html',
    'app/static/tools/profession-calculator.html',
    'app/static/blog/kua-number-auspicious-directions-and-career-feng-shui.html'
]

for fpath in files:
    if not os.path.exists(fpath):
        print(f"Skipping missing {fpath}")
        continue
    with open(fpath, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    # 1. Remove Enterprise Shielded from footer-copy or footer-bar
    c = c.replace(' Enterprise Shielded &amp; 256-Bit Encrypted.', '')
    c = c.replace(' Enterprise Shielded & 256-Bit Encrypted.', '')
    c = c.replace('Enterprise Shielded &amp; 256-Bit Encrypted.', '')
    c = c.replace('Enterprise Shielded & 256-Bit Encrypted.', '')
    
    # 2. Remove footer-disclaimer div (multiline)
    c = re.sub(r'\s*<div class="footer-disclaimer">[\s\S]*?</div>', '', c)
    
    # 3. Add /disclaimer to footer-links if not present
    if '/disclaimer' not in c:
        if '<a href="/blog/what-is-numerology">Wisdom Blog</a>' in c:
            c = c.replace('<a href="/blog/what-is-numerology">Wisdom Blog</a>', '<a href="/disclaimer">Disclaimer</a>\n    <a href="/blog/what-is-numerology">Wisdom Blog</a>')
        elif '<a href="/contact"' in c:
            c = c.replace('<a href="/contact"', '<a href="/disclaimer" style="color:#7A654D; text-decoration:none;">Disclaimer</a> · \n        <a href="/contact"')
        elif '<a href="/#consultation">Book Consultation</a>' in c:
            c = c.replace('<a href="/#consultation">Book Consultation</a>', '<a href="/disclaimer">Disclaimer</a>\n      <a href="/#consultation">Book Consultation</a>')
        elif '<a href="/tools/mobile-numerology">Mobile Numerology</a>' in c:
            c = c.replace('<a href="/tools/mobile-numerology">Mobile Numerology</a>', '<a href="/tools/mobile-numerology">Mobile Numerology</a>\n      <a href="/disclaimer">Disclaimer</a>')

    with open(fpath, 'w', encoding='utf-8') as fp:
        fp.write(c)

print('Updated 11 files successfully.')
