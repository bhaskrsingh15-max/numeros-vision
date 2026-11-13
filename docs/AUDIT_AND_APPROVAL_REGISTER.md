# NUMEROS VISION — AUDIT & APPROVAL REGISTER
**Document Status**: PENDING USER APPROVAL  
**Generated Date**: 2026-11-10  
**Scope**: Site audit, internal terminology, claims moderation, duplicate content, URL slugs, and local landing pages.

---

## 1. Internal Labels To Remove / Replace
The following internal project codenames and engineering terms leaked into public user interfaces and should be updated to professional customer-facing terminology:

| Location | Current Internal Label | Proposed Customer-Facing Replacement | Reason |
| :--- | :--- | :--- | :--- |
| `app/static/calculator_hub.html` (Card 10) | "Logo Intelligence & Google Nano Banana Design Studio" | "Logo Intelligence & Brand Harmonization Studio" | "Google Nano Banana" is an internal developer pipeline code name. |
| `app/static/calculator_hub.html` (Card 10 body) | "...generate harmonized vector brand marks via Google Nano Banana image models." | "...generate harmonized vector brand marks via certified AI generative design models." | Protects internal architecture and maintains brand elevation. |
| `app/static/index.html` (Tool 8 Badge) | `<span class="calc-tool-badge">Nano Banana Studio</span>` | `<span class="calc-tool-badge">Brand Vector Studio</span>` | Removes internal codename from public homepage grid. |
| `app/static/index.html` (Tool 8 Title & Body) | "Logo Intelligence Studio ... via Google Nano Banana" | "Logo Intelligence Studio ... via generative vector models" | Eliminates internal system references. |
| `app/static/tools/lo-shu-grid.html` (Subheading) | "Bottom Permutation & Combination Conversion Matrix" | "Plane & Elemental Planetary Combinations" | "Conversion Matrix" is conversion-rate-optimization jargon unsuitable for customers. |
| `app/static/tools/lo-shu-grid.html` (Preview Label) | "Quick Pitch Previews:" | "Explore Key Harmonic Yogas:" | "Quick Pitch" is sales jargon; "Harmonic Yogas" aligns with the authentic numerology context. |

---

## 2. Terminology: "Lucky Number" Naming Standardization
The term "lucky number" conflicts with statutory guidelines (Drugs and Magic Remedies Act 1954) and the scientific/deterministic positioning of Numeros Vision ("Zero superstition, 100% deterministic mathematics").

| Item | Current Term | Recommended Replacement | Alternate Option |
| :--- | :--- | :--- | :--- |
| Route URL | `/tools/lucky-number/` | `/tools/harmonic-numbers/` (with 301 from old) | `/tools/auspicious-numbers/` |
| Calculator Title | "Lucky Numbers & Attunements" | "Harmonic Numbers & Planetary Resonance" | "Auspicious Alignment Calculator" |
| Report Section | "Your Lucky Numbers" | "Your Harmonic Resonance Numbers" | "Aligned Numbers & Favorable Days" |

---

## 3. Duplicate Blog Articles: Gemstones & Crystal Remedies
Two nearly identical blog posts currently exist in the repository:
1. `app/static/blog/gemstone-remedies.html` (43,363 bytes)
2. `app/static/blog/vedic-gemstone-remedies.html` (43,405 bytes)

**Observation**: Both share identical H1 (`Gemstone & Crystal Remedies by Numerology Number`), identical body sections, and identical table layouts. Having both indexed splits page authority and risks search engine duplicate content penalties.
**Recommendation**:
- Consolidate onto canonical `/blog/vedic-gemstone-remedies/`.
- Issue a 301 Permanent Redirect in `_worker.js` from `/blog/gemstone-remedies/` (and `.html`) to `/blog/vedic-gemstone-remedies/`.
- Update all internal anchor links across the site to link directly to `/blog/vedic-gemstone-remedies/`.

---

## 4. Local City Landing Pages (`/local/*`)
The repository contains 5 localized landing pages:
- `/local/` (`local_hub.html`)
- `/local/delhi/` (`local_delhi.html`)
- `/local/mumbai/` (`local_mumbai.html`)
- `/local/bangalore/` (`local_bangalore.html`)
- `/local/dubai/` (`local_dubai.html`)

**Status**:
- These pages currently render localized consultation value propositions for Delhi NCR, Mumbai, Bengaluru, and Dubai.
- All 5 routes are mapped in `ROUTING_MAP`, build cleanly into `dist_cloudflare_pages/local/*/index.html`, and are listed in `sitemap.xml` with real Git timestamps.
- **Decision Required**: Confirm whether to keep these 5 pages active for local SEO or merge/archive them.

---

## 5. Marketing Claims Moderation & Statutory Alignment
Under Section 1 (Directive 4) and Section 19 of `AGENTS.md`:
- Never present traditional interpretations as scientifically proven causal claims or promise commercial/financial success.
- Ensure all pages explicitly frame guidance around self-reflection, personal awareness, and lifestyle habits.
- Words such as "Guaranteed windfall", "Surefire wealth", or "Change your destiny overnight" must strictly remain barred across all copy.
