# NUMEROS VISION — CHARM AI MASTER BRAND LOGO SPECIFICATION
**Version:** 1.0.0  
**Effective Date:** 2026-10-29  
**Status:** Canonical & Mandatory Across All Platforms  
**Scope:** Desktop, Mobile, Tablet, PWA, Chat Interface, Marketing Materials, and Future Updates.

---

## 1. Executive Summary

To maintain elite brand distinction and visual recognition across all platforms, **Charm AI** utilizes a single, unified canonical emblem:
**The Circular Jupiter Gold Talisman Medallion with the Celestial 4-Pointed Star (`✦`)**.

Under Master Rules, no operating system emojis (such as `✨`), square squircles, ivory backgrounds, or alternative star geometries may ever be substituted for the official Charm AI emblem.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       CANONICAL CHARM AI BRAND EMBLEM                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                                 ╭───────╮                                   │
│                               ╭╯   ✦   ╰╮                                  │
│                              │  (WHITE)  │   ◄── 4-Point Celestial Star    │
│                              │  CELESTIAL│       in Pure #FFFFFF           │
│                               ╰╮  STAR ╭╯                                  │
│                                 ╰───────╯                                   │
│                                     ▲                                       │
│                                     │                                       │
│          Circular Jupiter Gold Talisman Medallion:                          │
│          Linear Gradient (#E2B84B → #C9A227 → #8B6914)                      │
│          Venus Pearl Outer Border: #FFFDF7                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Mathematical SVG Specification

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="100%" height="100%" fill="none" shape-rendering="geometricPrecision">
  <defs>
    <!-- Master Jupiter Gold Gradient -->
    <linearGradient id="charmGoldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#E2B84B"/>
      <stop offset="45%" stop-color="#C9A227"/>
      <stop offset="100%" stop-color="#8B6914"/>
    </linearGradient>
  </defs>

  <!-- Canonical Circular Gold Medallion -->
  <circle cx="12" cy="12" r="11" fill="url(#charmGoldGrad)" stroke="#FFFDF7" stroke-width="0.75"/>

  <!-- Canonical White 4-Pointed Celestial Star -->
  <path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z" 
        fill="none" stroke="#FFFFFF" stroke-width="1.25"/>
</svg>
```

---

## 3. Surface Application Matrix

| Surface Location | Component Class / Tag | Dimensions | Border | Background Gradient | Star Fill / Stroke |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Mobile Bottom Navigation** | `.nv-bottom-center-btn` | $46 \times 46\text{px}$ | $2.5\text{px}$ `#FFFDF7` | `#E2B84B` $\to$ `#C9A227` $\to$ `#8B6914` | Stroke `#FFFFFF` ($2.2\text{px}$) |
| **Scroll Floating Launcher** | `.nv-charm-bot-avatar-btn` | $58 \times 58\text{px}$ | $2.5\text{px}$ `#FFFDF7` | `#E2B84B` $\to$ `#C9A227` $\to$ `#8B6914` | Stroke `#FFFFFF` ($2.2\text{px}$) |
| **Desktop Navigation Header** | `.nv-charm-medallion-icon` | $24 \times 24\text{px}$ | $1.8\text{px}$ `#FFFDF7` | `#E2B84B` $\to$ `#C9A227` $\to$ `#8B6914` | Stroke `#FFFFFF` ($2.4\text{px}$) |
| **Chat Window Message Avatar**| `.ai-avatar-wrap` | $44 \times 44\text{px}$ | $2.0\text{px}$ `#FFFDF7` | `#E2B84B` $\to$ `#C9A227` $\to$ `#8B6914` | Stroke `#FFFFFF` ($2.2\text{px}$) |
| **Mobile Drawer Menu** | `.nv-charm-medallion-icon` | $24 \times 24\text{px}$ | $1.8\text{px}$ `#FFFDF7` | `#E2B84B` $\to$ `#C9A227` $\to$ `#8B6914` | Stroke `#FFFFFF` ($2.4\text{px}$) |

---

## 4. Master Assets Registry

1. **`app/static/logos/charm-bot-avatar.svg`**: Canonical 24x24 scalable vector asset.
2. **`app/static/logos/charm-ai-logo.svg`**: Identical canonical emblem.
3. **`app/static/logos/charm-sketch-thumbnail.svg`**: Synchronized fallback asset.

---

## 5. Non-Negotiable Directives for Future Updates

1. **Never Revert to Emojis:** The character `✨` must never be used in navigation bars, headers, or buttons as the logo of Charm AI.
2. **Never Use Square/Squircle Containers:** Charm AI's emblem is strictly a circle (`border-radius: 50% !important`).
3. **Preserve Vector SVG:** Prefer vector SVG implementations directly in CSS/HTML components to eliminate asset loading latency and avoid stale client caching.
