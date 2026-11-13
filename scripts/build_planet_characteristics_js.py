import os
import sys
import json

sys.path.insert(0, os.path.abspath('.'))
from app.engine.number_characteristics_registry import NUMBER_REGISTRY
from app.engine.core_matrix_engine import PLANETARY_MATRIX

def build_js_bundle():
    data = {}
    for num, entry in NUMBER_REGISTRY.items():
        pm = PLANETARY_MATRIX.get(num, {})
        data[num] = {
            "number": entry.get("number"),
            "planet": entry.get("planet"),
            "alternative_planet": entry.get("alternative_planet", ""),
            "element": entry.get("element", ""),
            "direction": pm.get("direction", "Universal"),
            "core_characteristics": entry.get("core_characteristics", ""),
            "strengths": entry.get("strengths", []),
            "challenges": entry.get("challenges", []),
            "behavioural_tendencies": entry.get("behavioural_tendencies", ""),
            "communication_tendencies": entry.get("communication_tendencies", ""),
            "leadership_tendencies": entry.get("leadership_tendencies", ""),
            "career_associations": entry.get("career_associations", []),
            "favourable_colours": entry.get("favourable_colours", []),
            "colours_to_avoid": entry.get("colours_to_avoid", []),
            "favourable_days": entry.get("favourable_days", []),
            "friendly_numbers": entry.get("friendly_numbers", []),
            "neutral_numbers": entry.get("neutral_numbers", []),
            "enemy_numbers": entry.get("enemy_numbers", []),
            "remedy_references": entry.get("remedy_references", []),
            "yantra_references": entry.get("yantra_references", [])
        }

    js_code = f"""/**
 * NUMEROS VISION — NUMBER & PLANET CHARACTERISTICS REGISTRY (CLIENT BUNDLE)
 * Generated from app/engine/number_characteristics_registry.py & core_matrix_engine.py
 * Version 1.1.0 · Single source of truth for planetary traits, elements, strengths, and remedies.
 */

const NUMBER_CHARACTERISTICS_REGISTRY = {json.dumps(data, indent=2)};

/**
 * Evaluates the planetary relationship between Driver (Mulank) and Conductor (Bhagyank).
 */
function getPlanetarySynergy(driver, conductor) {{
  const dNum = parseInt(driver, 10) || 1;
  const cNum = parseInt(conductor, 10) || 1;

  const dProfile = NUMBER_CHARACTERISTICS_REGISTRY[dNum] || NUMBER_CHARACTERISTICS_REGISTRY[String(dNum)] || {{}};
  const cProfile = NUMBER_CHARACTERISTICS_REGISTRY[cNum] || NUMBER_CHARACTERISTICS_REGISTRY[String(cNum)] || {{}};

  const dPlanet = dProfile.planet || 'Ruler ' + dNum;
  const cPlanet = cProfile.planet || 'Ruler ' + cNum;

  if (dNum === cNum) {{
    return {{
      type: 'Harmonious Dual Resonance',
      badgeClass: 'synergy-resonance',
      status: 'Intensified Harmonic Momentum',
      score: '96%',
      summary: `Both your inborn decision instinct (Driver ${{dNum}}) and your overarching destiny path (Conductor ${{cNum}}) are governed by ${{dPlanet}}. This creates remarkable focus, consistency of purpose, and an undiluted expression of your core planetary archetype.`
    }};
  }}

  const isFriendly = (cProfile.friendly_numbers || []).includes(dNum) || (dProfile.friendly_numbers || []).includes(cNum);
  const isEnemy = (cProfile.enemy_numbers || []).includes(dNum) || (dProfile.enemy_numbers || []).includes(cNum);

  if (isEnemy) {{
    let customNote = '';
    if ((dNum === 1 && cNum === 8) || (dNum === 8 && cNum === 1)) {{
      customNote = 'Sun represents immediate executive initiative, visibility, and sovereign willpower, while Saturn governs compounding patience, structural discipline, and karmic resilience. This creates creative growth tension: early challenges demand maturity, leading to formidable, enduring mastery.';
    }} else if ((dNum === 3 && cNum === 6) || (dNum === 6 && cNum === 3)) {{
      customNote = 'Jupiter represents expansive philosophical mentorship and wisdom, while Venus governs luxury, aesthetic magnetism, and material celebration. Harmonizing both requires balancing spiritual discipline with worldly elegance.';
    }} else {{
      customNote = `${{dPlanet}} drives your instinctive choices, while ${{cPlanet}} shapes your long-term karmic lessons. This dynamic tension sharpens your discernment, turning friction into resilience through conscious self-awareness.`;
    }}

    return {{
      type: 'Creative Growth Tension',
      badgeClass: 'synergy-tension',
      status: 'Karmic Catalyst & Discipline',
      score: '78%',
      summary: customNote
    }};
  }}

  if (isFriendly) {{
    return {{
      type: 'Harmonious Mutual Catalyst',
      badgeClass: 'synergy-friendly',
      status: 'Fluid Natural Alignment',
      score: '92%',
      summary: `${{dPlanet}} and ${{cPlanet}} operate in natural synergy. Your instinctive decision temperament naturally supports and accelerates your outer life path lessons, allowing fluid adaptability across personal and professional pursuits.`
    }};
  }}

  return {{
    type: 'Complementary Pragmatic Alliance',
    badgeClass: 'synergy-neutral',
    status: 'Balanced Versatility',
    score: '84%',
    summary: `${{dPlanet}} and ${{cPlanet}} form a neutral, pragmatic partnership. Your instinctive persona and outer destiny provide complementary perspectives, giving you the versatility to navigate diverse crossroads without rigid bias.`
  }};
}}

/**
 * Builds the comprehensive HTML breakdown for the Planetary Characteristics Dossier.
 */
function renderPlanetaryCharacteristicsHtml(driver, conductor) {{
  const dNum = parseInt(driver, 10) || 1;
  const cNum = parseInt(conductor, 10) || 8;
  const d = NUMBER_CHARACTERISTICS_REGISTRY[dNum] || NUMBER_CHARACTERISTICS_REGISTRY[String(dNum)] || NUMBER_CHARACTERISTICS_REGISTRY[1];
  const c = NUMBER_CHARACTERISTICS_REGISTRY[cNum] || NUMBER_CHARACTERISTICS_REGISTRY[String(cNum)] || NUMBER_CHARACTERISTICS_REGISTRY[8];
  const syn = getPlanetarySynergy(dNum, cNum);

  return `
    <div class="planet-chars-card">
      <div class="planet-chars-header">
        <span class="planet-chars-eyebrow">✦ DETERMINISTIC CANONICAL REGISTRY ✦</span>
        <h3 class="planet-chars-title">Planetary Characteristics &amp; Archetype Synthesis</h3>
        <p class="planet-chars-sub">
          Detailed behavioral characteristics, strengths, challenges, and harmonization remedies governed by your primary planetary rulers.
        </p>
      </div>

      <!-- Dual Profile Grid -->
      <div class="planet-chars-grid">
        <!-- Driver Card -->
        <div class="planet-archetype-box">
          <div class="archetype-badge driver-badge">DRIVER · MULANK ${{driver}}</div>
          <h4 class="archetype-name">${{d.planet}}</h4>
          <div class="archetype-meta">
            <span><strong>Element:</strong> ${{d.element}}</span>
            <span>·</span>
            <span><strong>Direction:</strong> ${{d.direction}}</span>
          </div>
          
          <div class="archetype-section">
            <span class="archetype-sec-label">Core Persona &amp; Instinct</span>
            <p class="archetype-text">${{d.core_characteristics}}</p>
          </div>

          <div class="archetype-section">
            <span class="archetype-sec-label">Primary Superpower Strengths</span>
            <div class="archetype-chips">
              ${{d.strengths.slice(0, 4).map(s => `<span class="chip chip-strength">✓ ${{s}}</span>`).join('')}}
            </div>
          </div>

          <div class="archetype-section">
            <span class="archetype-sec-label">Growth Blindspots &amp; Challenges</span>
            <div class="archetype-chips">
              ${{d.challenges.slice(0, 3).map(ch => `<span class="chip chip-challenge">⚠ ${{ch}}</span>`).join('')}}
            </div>
          </div>

          <div class="archetype-footer-meta">
            <div><strong>Auspicious Colours:</strong> ${{d.favourable_colours.slice(0, 4).join(', ')}}</div>
            <div><strong>Auspicious Days:</strong> ${{d.favourable_days.join(', ')}}</div>
            <div><strong>Career Affinities:</strong> ${{d.career_associations.slice(0, 3).join(', ')}}</div>
          </div>
        </div>

        <!-- Conductor Card -->
        <div class="planet-archetype-box">
          <div class="archetype-badge conductor-badge">CONDUCTOR · BHAGYANK ${{conductor}}</div>
          <h4 class="archetype-name">${{c.planet}}</h4>
          <div class="archetype-meta">
            <span><strong>Element:</strong> ${{c.element}}</span>
            <span>·</span>
            <span><strong>Direction:</strong> ${{c.direction}}</span>
          </div>

          <div class="archetype-section">
            <span class="archetype-sec-label">Destiny Path &amp; Life Purpose</span>
            <p class="archetype-text">${{c.core_characteristics}}</p>
          </div>

          <div class="archetype-section">
            <span class="archetype-sec-label">Karmic Strengths</span>
            <div class="archetype-chips">
              ${{c.strengths.slice(0, 4).map(s => `<span class="chip chip-strength">✓ ${{s}}</span>`).join('')}}
            </div>
          </div>

          <div class="archetype-section">
            <span class="archetype-sec-label">Karmic Lessons &amp; Blindspots</span>
            <div class="archetype-chips">
              ${{c.challenges.slice(0, 3).map(ch => `<span class="chip chip-challenge">⚠ ${{ch}}</span>`).join('')}}
            </div>
          </div>

          <div class="archetype-footer-meta">
            <div><strong>Auspicious Colours:</strong> ${{c.favourable_colours.slice(0, 4).join(', ')}}</div>
            <div><strong>Auspicious Days:</strong> ${{c.favourable_days.join(', ')}}</div>
            <div><strong>Career Affinities:</strong> ${{c.career_associations.slice(0, 3).join(', ')}}</div>
          </div>
        </div>
      </div>

      <!-- Synergy Strip -->
      <div class="planet-synergy-strip">
        <div class="synergy-header">
          <span class="synergy-tag ${{syn.badgeClass}}">${{syn.type}} (${{syn.score}} Harmony)</span>
          <h4 class="synergy-title">Driver ${{driver}} (${{d.planet.split(' ')[0]}}) × Conductor ${{conductor}} (${{c.planet.split(' ')[0]}}) Synthesis</h4>
        </div>
        <p class="synergy-text">${{syn.summary}}</p>
      </div>

      <!-- Harmonization Remedies Box -->
      <div class="planet-remedies-box">
        <div class="remedies-title">✦ Traditional Planetary Harmonization &amp; Lifestyle Attunement ✦</div>
        <div class="remedies-grid">
          <div class="remedy-col">
            <strong>${{d.planet.split(' ')[0]}} Attunement (Driver ${{driver}}):</strong>
            <ul>
              ${{d.remedy_references.slice(0, 2).map(r => `<li>${{r}}</li>`).join('')}}
            </ul>
          </div>
          <div class="remedy-col">
            <strong>${{c.planet.split(' ')[0]}} Attunement (Conductor ${{conductor}}):</strong>
            <ul>
              ${{c.remedy_references.slice(0, 2).map(r => `<li>${{r}}</li>`).join('')}}
            </ul>
          </div>
        </div>
        <div class="remedies-note">
          Numeros Vision follows safe, non-fear lifestyle remedies. Consecrated gemstone and acoustic name balancing recommendations are calibrated strictly to your birth epoch without fear-based predictions.
        </div>
      </div>
    </div>
  `;
}}

if (typeof window !== 'undefined') {{
  window.NUMBER_CHARACTERISTICS_REGISTRY = NUMBER_CHARACTERISTICS_REGISTRY;
  window.getPlanetarySynergy = getPlanetarySynergy;
  window.renderPlanetaryCharacteristicsHtml = renderPlanetaryCharacteristicsHtml;
}}
"""

    out_path = 'app/static/js/number_characteristics.js'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(js_code)
    print(f'Successfully generated {out_path} ({len(js_code)} bytes)')

if __name__ == '__main__':
    build_js_bundle()
