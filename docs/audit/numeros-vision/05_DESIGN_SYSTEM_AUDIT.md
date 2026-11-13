# Numeros Vision — Design System & Frontend Architecture Audit
**Phase 1: Read-Only Audit & Baseline Gap Analysis**  
**Execution Timestamp:** 2026-10-16  

---

## 1. Design Tokens Inventory (`app/static/css/theme.css`)

```css
:root {
  /* Surfaces & Backgrounds */
  --bg: #FFFDF7;           /* Venus Pearl primary canvas */
  --bg-mid: #F7F3EA;       /* Warm secondary canvas */
  --bg-card: #FFFFFF;      /* Clean card surface */
  
  /* Planetary Brand Accents */
  --gold: #C9A227;         /* Jupiter Gold (Core Brand Accent) */
  --gold-light: #E2B84B;   /* Radiant Gold Highlight */
  --gold-dark: #8B6914;    /* Deep Antiqued Gold (Headings) */
  --accent-emerald: #16835B; /* Mercury Jade (CTAs, Conversion Buttons) */
  
  /* Borders & Dividers */
  --border: rgba(180, 155, 110, 0.22);
  --border-gold: rgba(201, 162, 39, 0.38);
  
  /* Typography Colors (Zero Pure Black) */
  --text-primary: #523E28; /* Warm Deep Jupiter Bronze (Body Text) */
  --text-muted: #7A654D;   /* Medium Bronze (Subtitles, Meta) */
  --text-faint: #A89880;   /* Light Warm Taupe (Captions, Tags) */
  
  /* Layout Geometry */
  --radius: 14px;
  --radius-lg: 24px;
}
```

---

## 2. Typography Scale Evaluation

| Semantic Level | Font Family | Size Rule | Weight | Line Height |
|---|---|---|---|---|
| **$H_1$ Hero** | `Cormorant Garamond`, Georgia, serif | `clamp(2rem, 6vw, 4.2rem)` | 600 / 700 | 1.15 |
| **$H_2$ Section** | `Cormorant Garamond`, Georgia, serif | `clamp(1.65rem, 4.5vw, 2.8rem)` | 600 | 1.20 |
| **$H_3$ Subsection** | `Cormorant Garamond`, Georgia, serif | `clamp(1.25rem, 3.5vw, 1.8rem)` | 500 / 600 | 1.25 |
| **$H_4$ Card Header** | `Cormorant Garamond`, Georgia, serif | `clamp(1.05rem, 2.5vw, 1.4rem)` | 600 | 1.30 |
| **Body Primary** | `Inter`, -apple-system, sans-serif | `1.0rem (16px)` | 400 | 1.60 |
| **Body Small / Captions** | `Inter`, sans-serif | `0.85rem – 0.92rem` | 400 | 1.50 |
| **Pills & Badges** | `Cinzel` / `Inter` | `0.75rem – 0.82rem` | 600 / 700 | 1.00 |

---

## 3. Component Architecture & Reusability

1. **Buttons (`.silo-btn`, `.btn-primary`, `.cta-gold`)**:
   - Primary: Mercury Jade (`#16835B`) with hover state `#2AAE7A` and white text.
   - Secondary: Gold outline (`border: 1.5px solid var(--gold)`) with gold text and subtle hover fill.
   - Consistent padding, border-radius (`8px` to `12px`), and transition timings (`0.2s ease`).
2. **Cards (`.calculator-card`, `.takeaways-box`, `.snippet-box`)**:
   - Border radius: `14px` standard, `24px` for hero containers.
   - Elevated drop shadow: `0 4px 16px rgba(0,0,0,0.04)` to `0 8px 24px rgba(22, 131, 91, 0.08)`.
3. **Responsive Breakpoints**:
   - Mobile: `< 600px` (single column layout, stacked inputs).
   - Tablet: `600px – 1024px` (2-column grids, collapsed sidebar navigation).
   - Desktop: `> 1024px` (multi-column matrix tables, 960px–1200px max page container).

---

## 4. Key Design System Findings
- **Strengths**: Highly unified visual language. Pristine aesthetic alignment with the Vedic/Western classical theme. Zero discordant neon or generic SaaS blue colors.
- **Improvement Target**: Standardize token usage across all 24 blog pages so all inline styles (`style="color: #523E28;"`) reference CSS custom properties (`color: var(--text-primary);`) exclusively.
