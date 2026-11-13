import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

print(f"Removing technical jargon & mechanism disclosures across frontend: {BASE_DIR}")

# 1. charm_ai.html: Remove the entire Guardrails & Transparency box and its CSS
path_cai = os.path.join(BASE_DIR, "app", "static", "charm_ai.html")
with open(path_cai, "r", encoding="utf-8") as f:
    cai = f.read()

# Remove HTML guardrails box
cai = re.sub(
    r'\s*<div class="guardrails-box">.*?</div>\s*',
    '\n',
    cai,
    flags=re.DOTALL
)

# Remove CSS for guardrails-box
cai = re.sub(
    r'\.guardrails-box\s*\{[^}]*\}\s*\.guardrails-box\s+h3\s*\{[^}]*\}\s*\.guardrails-box\s+ul\s*\{[^}]*\}',
    '',
    cai
)

with open(path_cai, "w", encoding="utf-8") as f:
    f.write(cai)
print("✓ app/static/charm_ai.html: Removed Guardrails & Transparency box completely.")

# 2. faq.html
path_faq = os.path.join(BASE_DIR, "app", "static", "faq.html")
with open(path_faq, "r", encoding="utf-8") as f:
    faq = f.read()

faq = faq.replace(
    '<div class="faq-question">How does Charm AI prevent hallucinations? <span>✦</span></div>',
    '<div class="faq-question">How does Charm AI ensure consultation accuracy? <span>✦</span></div>'
)
faq = faq.replace(
    'Charm AI operates under strict classical wisdom protocols. It references a verified corpus of 10,826 classical scriptural passages from classical numerology and ephemeris tables. It is prohibited from generating unsupported claims, predicting exact health diagnoses, or fabricating planetary associations.',
    'Charm AI operates under authentic classical wisdom principles. Every consultation is grounded in authentic numerological traditions, verified calculations, and ethical guidance standards, ensuring reliable, thoughtful, and deeply personalized reflections.'
)

with open(path_faq, "w", encoding="utf-8") as f:
    f.write(faq)
print("✓ app/static/faq.html: Cleaned hallucination/corpus technical claims.")

# 3. index.html
path_idx = os.path.join(BASE_DIR, "app", "static", "index.html")
with open(path_idx, "r", encoding="utf-8") as f:
    idx = f.read()

idx = idx.replace(
    "<p><strong>3. Transparent Guarantee:</strong> Hard-coded mathematical calculations are strictly separated from AI generated reflections.</p>",
    "<p><strong>3. Authentic Tradition:</strong> Every reading is grounded in verified classical numerology principles and personalized reflections.</p>"
)

with open(path_idx, "w", encoding="utf-8") as f:
    f.write(idx)
print("✓ app/static/index.html: Cleaned hard-coded / AI separation disclosure.")

# 4. reports_catalogue.html
path_rc = os.path.join(BASE_DIR, "app", "static", "reports_catalogue.html")
with open(path_rc, "r", encoding="utf-8") as f:
    rc = f.read()

rc = rc.replace(
    '<div class="trust-chip"><span class="star">✦</span> 100% Deterministic Engine</div>',
    '<div class="trust-chip"><span class="star">✦</span> 100% Classical Precision</div>'
)
rc = rc.replace(
    '100% deterministic arithmetic. No generative AI arithmetic hallucinations. DPDP 2023 compliant.',
    '100% mathematical precision. Authentic classical numerology. DPDP 2023 compliant.'
)

with open(path_rc, "w", encoding="utf-8") as f:
    f.write(rc)
print("✓ app/static/reports_catalogue.html: Cleaned deterministic engine & hallucination chips.")

# 5. disclaimer.html
path_disc = os.path.join(BASE_DIR, "app", "static", "disclaimer.html")
with open(path_disc, "r", encoding="utf-8") as f:
    disc = f.read()

disc = re.sub(
    r'The Charm AI system uses advanced generative neural networks grounded in Classical Calculation Precisionematical calcula[^\.]*\.',
    'The Charm AI system provides personalized reflections grounded in classical mathematical calculations.',
    disc
)

with open(path_disc, "w", encoding="utf-8") as f:
    f.write(disc)
print("✓ app/static/disclaimer.html: Cleaned neural network & technical calculation claims.")

# 6. methodology.html
path_meth = os.path.join(BASE_DIR, "app", "static", "methodology.html")
with open(path_meth, "r", encoding="utf-8") as f:
    meth = f.read()

meth = meth.replace(
    'In many conventional "AI astrology" tools, Large Language Models are asked to compute birth numbers and planetary positions directly. This invariably causes mathematical hallucinations, incorrect reductions, and invented astrological dates.',
    'In conventional automated tools, software frequently approximates calculations or produces inconsistent results.'
)
meth = meth.replace(
    'At Numeros Vision, **AI never computes math**. Our architecture enforces a hard architectural boundary:',
    'At Numeros Vision, every calculation follows authentic mathematical precision rooted in classical tradition:'
)
meth = meth.replace(
    'Seeker Chart Data ➔ Classical Calculation Engine ➔ Scriptural Wisdom Corpus ➔ Charm AI Synthesis',
    'Seeker Profile Data ➔ Classical Calculation Formulas ➔ Traditional Wisdom Heritage ➔ Personalized Reflections'
)
meth = meth.replace(
    'Charm AI draws upon a sanitized corpus of 10,826 validated occult literature passages, including classical texts by Cheiro, Classical Vedic Tradition, and traditional Vedic authorities.',
    'Numeros Vision draws upon authoritative classical literature and time-honored traditions, including verified works by Cheiro and foundational Vedic authorities.'
)

with open(path_meth, "w", encoding="utf-8") as f:
    f.write(meth)
print("✓ app/static/methodology.html: Cleaned LLM, architectural boundary & corpus disclosures.")

# 7. tools/life-path-calculator.html & tools/lo-shu-grid.html
path_lpc = os.path.join(BASE_DIR, "app", "static", "tools", "life-path-calculator.html")
with open(path_lpc, "r", encoding="utf-8") as f:
    lpc = f.read()

lpc = lpc.replace(
    "Instant PDF Delivery &bull; Deterministic Engine Precision &bull; Confidential &amp; Secure",
    "Instant PDF Delivery &bull; Classical Numerology Precision &bull; Confidential &amp; Secure"
)
with open(path_lpc, "w", encoding="utf-8") as f:
    f.write(lpc)
print("✓ app/static/tools/life-path-calculator.html: Cleaned trust banner.")

path_lsg = os.path.join(BASE_DIR, "app", "static", "tools", "lo-shu-grid.html")
with open(path_lsg, "r", encoding="utf-8") as f:
    lsg = f.read()

lsg = lsg.replace(
    "// Add natal DOB digits (Standard Deterministic Engine)",
    "// Add natal DOB digits (Standard Calculation)"
)
with open(path_lsg, "w", encoding="utf-8") as f:
    f.write(lsg)
print("✓ app/static/tools/lo-shu-grid.html: Cleaned JS comments.")

# 8. Blogs & AMP Blogs
blog_files = [
    "app/static/blog/what-is-numerology.html",
    "app/static/amp/blog/what-is-numerology.html",
    "app/static/blog/chaldean-numerology.html",
    "app/static/amp/blog/chaldean-numerology.html",
    "app/static/amp/index.html"
]

for bf in blog_files:
    full_p = os.path.join(BASE_DIR, bf)
    if os.path.exists(full_p):
        with open(full_p, "r", encoding="utf-8") as f:
            bt = f.read()
        
        bt = bt.replace(
            "Calculations run on a deterministic Python engine rather than generative language models. We do not make predictive guarantees, promise zero",
            "All calculations follow authentic mathematical principles rooted in classical numerological tradition. We do not make predictive guarantees, promise zero"
        )
        bt = bt.replace(
            "Classical Calculation Precisionematical algorithms",
            "classical mathematical formulas"
        )
        bt = bt.replace(
            "zero-hallucination",
            "authentic"
        )
        bt = bt.replace(
            "zero-hallucinating",
            "authentic"
        )
        
        with open(full_p, "w", encoding="utf-8") as f:
            f.write(bt)
        print(f"✓ {bf}: Cleaned technical mechanism claims.")

# 9. js/funnel_journey.js
path_fj = os.path.join(BASE_DIR, "app", "static", "js", "funnel_journey.js")
with open(path_fj, "r", encoding="utf-8") as f:
    fj = f.read()

fj = fj.replace(
    "Charm AI answers with zero-hallucination classical numerology and astrology synthesis. Explore 15 detaile",
    "Charm AI answers with authentic classical numerology synthesis. Explore 15 detailed"
)
fj = fj.replace(
    "'Zero hallucination guarantee bound to classical texts'",
    "'Authentic mathematical precision bound to classical traditions'"
)
with open(path_fj, "w", encoding="utf-8") as f:
    f.write(fj)
print("✓ app/static/js/funnel_journey.js: Cleaned zero-hallucination mentions.")

# 10. demo.html
path_demo = os.path.join(BASE_DIR, "app", "static", "demo.html")
with open(path_demo, "r", encoding="utf-8") as f:
    dt = f.read()

dt = dt.replace("Trade Secret Shield", "Confidential Privacy Shield")
dt = dt.replace("Enterprise Shielded Firewall, proprietary trade secret keyword shield", "Enterprise Shielded Security, privacy protection")
with open(path_demo, "w", encoding="utf-8") as f:
    f.write(dt)
print("✓ app/static/demo.html: Cleaned trade secret disclosures.")

print("\nAll frontend technical jargon & mechanism exposures successfully cleared!")
