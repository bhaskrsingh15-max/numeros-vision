import os
import sys
import json

sys.path.insert(0, os.path.abspath('.'))

from app.engine.number_characteristics_registry import NUMBER_REGISTRY, BIRTH_DAY_SUBDATE_REGISTRY
from app.engine.core_matrix_engine import PLANETARY_MATRIX
from app.engine.complementary_poorak_engine import POORAK_DATA
from app.engine.five_elements_hygiene_engine import FIVE_ELEMENTS_HYGIENE

# Load 81 DC rules
with open('data/knowledge_base/driver_conductor_81_rules.json', 'r', encoding='utf-8') as f:
    dc_81_data = json.load(f)

# Format NUMBER_CHARACTERISTICS_REGISTRY
number_chars = {}
for num, entry in NUMBER_REGISTRY.items():
    pm = PLANETARY_MATRIX.get(num, {})
    number_chars[num] = {
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

subdates_json = json.dumps(BIRTH_DAY_SUBDATE_REGISTRY, indent=2, ensure_ascii=False)
dc_81_json = json.dumps(dc_81_data, indent=2, ensure_ascii=False)
number_chars_json = json.dumps(number_chars, indent=2, ensure_ascii=False)
poorak_data_json = json.dumps(POORAK_DATA, indent=2, ensure_ascii=False)
hygiene_rules_json = json.dumps(FIVE_ELEMENTS_HYGIENE, indent=2, ensure_ascii=False)

js_content = f"""/**
 * NUMEROS VISION — MASTER NUMBER & PLANETARY CHARACTERISTICS CLIENT BUNDLE
 * Version 2.0.0 · Unified Single Source of Truth
 * Includes:
 * 1. Root Number Characteristics (1-9)
 * 2. Birth Sub-Dates (1-31) Strength Categories (A, B, C, D) & Potency Scores
 * 3. Driver-Conductor 81 Combinations Registry (Star Ratings, Synergies, Warnings)
 * 4. Complementary (Poorak / पूरक) Harmonizer Engine
 * 5. Panch Tattva (Five Elements) Bodyguard Hygiene Engine
 * 6. Lo Shu Degree of Repetition & Dual Attribute Matrix
 */

const NUMBER_CHARACTERISTICS_REGISTRY = {number_chars_json};
const BIRTH_DAY_SUBDATE_REGISTRY = {subdates_json};
const DRIVER_CONDUCTOR_81_REGISTRY = {dc_81_json};
const POORAK_DATA = {poorak_data_json};
const FIVE_ELEMENTS_HYGIENE = {hygiene_rules_json};

/**
 * Calculates Complementary (Poorak) Number in client JS
 */
function calculateClientPoorak(driver, conductor, missingNums) {{
  const d = parseInt(driver, 10) || 1;
  const c = parseInt(conductor, 10) || 1;
  const pairKey = d + "_" + c;
  
  const frictionMap = POORAK_DATA.friction_pair_peacemakers || {{}};
  if (frictionMap[pairKey]) {{
    const info = frictionMap[pairKey];
    return {{
      poorak_number: info.peacemaker_number,
      poorak_planet: info.peacemaker_planet,
      is_friction_resolution: true,
      synergy_type: "Friction Peacemaker Bridge",
      rationale: info.rationale,
      harmonizing_ritual: info.harmonizing_ritual
    }};
  }}
  
  const masterMap = POORAK_DATA.master_poorak_map || {{}};
  const dStr = String(d);
  if (masterMap[dStr]) {{
    const item = masterMap[dStr];
    const pNum = item.complementary[0];
    return {{
      poorak_number: pNum,
      poorak_planet: item.planet,
      is_friction_resolution: false,
      synergy_type: "Natural Harmonic Completer",
      rationale: item.role,
      harmonizing_ritual: `Incorporate Number ${{pNum}} into daily planning, workspace accents, and cardinal alignments.`
    }};
  }}
  
  return {{
    poorak_number: 5,
    poorak_planet: "Mercury (Budh)",
    is_friction_resolution: false,
    synergy_type: "Central Grounding Stabilizer",
    rationale: "Number 5 provides universal commercial adaptability and central elemental balance.",
    harmonizing_ritual: "Place a healthy green plant in the North/Center of your home or workspace."
  }};
}}

/**
 * Evaluates the planetary relationship between Driver (Mulank) and Conductor (Bhagyank).
 */
function getPlanetarySynergy(driver, conductor) {{
  const dNum = parseInt(driver, 10) || 1;
  const cNum = parseInt(conductor, 10) || 1;
  const pairKey = dNum + "_" + cNum;
  
  if (DRIVER_CONDUCTOR_81_REGISTRY[pairKey]) {{
    const rule = DRIVER_CONDUCTOR_81_REGISTRY[pairKey];
    const isEnemy = rule.relationship_type === 'Enemy' || rule.relationship_type === 'Warning';
    const isFriendly = rule.relationship_type === 'Friendly';
    
    return {{
      type: rule.relationship_type + ' Synergy',
      badgeClass: isEnemy ? 'synergy-tension' : (isFriendly ? 'synergy-friendly' : 'synergy-neutral'),
      status: rule.star_rating + ' / 5.0 Stars',
      score: Math.round(rule.star_rating * 20) + '%',
      star_rating: rule.star_rating,
      positive_traits: rule.positive_traits || [],
      negative_traits: rule.negative_traits || [],
      recommended_careers: rule.recommended_careers || [],
      high_risk_warning: rule.high_risk_warning || '',
      summary: rule.high_risk_warning ? rule.high_risk_warning : (rule.positive_traits || []).slice(0, 3).join(', ')
    }};
  }}

  const dProfile = NUMBER_CHARACTERISTICS_REGISTRY[dNum] || NUMBER_CHARACTERISTICS_REGISTRY[1];
  const cProfile = NUMBER_CHARACTERISTICS_REGISTRY[cNum] || NUMBER_CHARACTERISTICS_REGISTRY[1];
  return {{
    type: 'Harmonious Mutual Catalyst',
    badgeClass: 'synergy-friendly',
    status: '4.0 / 5.0 Stars',
    score: '80%',
    star_rating: 4.0,
    positive_traits: ['Natural leadership', 'Executive focus'],
    negative_traits: ['Occasional rigidity'],
    recommended_careers: ['Administration', 'Strategic Planning'],
    high_risk_warning: '',
    summary: `${{dProfile.planet}} and ${{cProfile.planet}} operate in steady alignment.`
  }};
}}

/**
 * Builds the comprehensive HTML breakdown for the Planetary Characteristics Dossier.
 */
function renderPlanetaryCharacteristicsHtml(driver, conductor, day, missingNumbers, gridCounts) {{
  const dNum = parseInt(driver, 10) || 1;
  const cNum = parseInt(conductor, 10) || 8;
  const birthDay = parseInt(day, 10) || dNum;
  const missing = missingNumbers || [];
  const counts = gridCounts || {{}};

  const d = NUMBER_CHARACTERISTICS_REGISTRY[dNum] || NUMBER_CHARACTERISTICS_REGISTRY[1];
  const c = NUMBER_CHARACTERISTICS_REGISTRY[cNum] || NUMBER_CHARACTERISTICS_REGISTRY[8];
  const syn = getPlanetarySynergy(dNum, cNum);
  const subdate = BIRTH_DAY_SUBDATE_REGISTRY[birthDay] || BIRTH_DAY_SUBDATE_REGISTRY[String(birthDay)] || {{}};
  const poorak = calculateClientPoorak(dNum, cNum, missing);

  // Category Color Class
  const cat = subdate.strength_category || 'B';
  let catBadgeStyle = 'background:rgba(201,162,39,0.15); color:#8B6914; border:1px solid #C9A227;';
  if (cat === 'A') catBadgeStyle = 'background:rgba(22,131,91,0.15); color:#16835B; border:1px solid #16835B;';
  else if (cat === 'C') catBadgeStyle = 'background:rgba(180,155,110,0.2); color:#7A654D; border:1px solid #8B6914;';
  else if (cat === 'D') catBadgeStyle = 'background:rgba(102,51,153,0.15); color:#663399; border:1px solid #663399;';

  const starsCount = syn.star_rating || 4.0;
  const starsDisplay = '★'.repeat(Math.floor(starsCount)) + (starsCount % 1 >= 0.5 ? '½' : '');

  // Subdate Card HTML
  let subdateHtml = '';
  if (subdate && subdate.day) {{
    subdateHtml = `
      <div style="background:linear-gradient(135deg, rgba(255,253,247,0.98) 0%, rgba(247,243,234,0.95) 100%); border:1.5px solid rgba(201,162,39,0.35); border-radius:14px; padding:18px 22px; margin-bottom:20px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:12px;">
          <div>
            <span style="display:inline-block; font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; padding:4px 12px; border-radius:20px; ${{catBadgeStyle}}">
              Sub-Date ${{subdate.code}} · Category ${{cat}} (${{subdate.strength_title}})
            </span>
            <h4 style="font-family:'Cormorant Garamond', Georgia, serif; font-size:1.45rem; color:#8B6914; margin:6px 0 2px 0; font-weight:700;">
              Day ${{birthDay}}: ${{subdate.archetype}}
            </h4>
            <div style="font-size:0.8rem; color:#7A654D;">Planetary Energy: <strong>${{subdate.planetary_composition}}</strong> · Classical Symbol: <em>${{subdate.classical_symbol}}</em></div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:1.6rem; font-weight:700; color:#8B6914; line-height:1;">${{subdate.strength_potency_score}}%</div>
            <div style="font-size:0.7rem; color:#7A654D; text-transform:uppercase; letter-spacing:0.08em; font-weight:600;">Intrinsic Potency</div>
          </div>
        </div>
        <p style="font-size:0.86rem; color:#523E28; line-height:1.55; margin:0 0 12px 0;">${{subdate.core_personality}}</p>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; font-size:0.82rem;">
          <div>
            <strong style="color:#16835B; display:block; margin-bottom:4px;">✦ Inborn Superpowers:</strong>
            <ul style="margin:0; padding-left:18px; color:#523E28; line-height:1.45;">
              ${{(subdate.superpowers || []).slice(0, 3).map(sp => `<li>${{sp}}</li>`).join('')}}
            </ul>
          </div>
          <div>
            <strong style="color:#8B6914; display:block; margin-bottom:4px;">⚠️ Shadow Vulnerabilities:</strong>
            <ul style="margin:0; padding-left:18px; color:#523E28; line-height:1.45;">
              ${{(subdate.shadow_vulnerabilities || []).slice(0, 3).map(sv => `<li>${{sv}}</li>`).join('')}}
            </ul>
          </div>
        </div>
      </div>
    `;
  }}

  // Driver-Conductor 81 Synergy HTML
  const dc81Html = `
    <div style="background:#FFFDF7; border:1.5px solid rgba(201,162,39,0.35); border-radius:14px; padding:18px 22px; margin-bottom:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:10px;">
        <div>
          <span class="synergy-tag ${{syn.badgeClass}}">${{syn.type}}</span>
          <h4 style="font-family:'Cormorant Garamond', Georgia, serif; font-size:1.35rem; color:#523E28; margin:4px 0 0 0; font-weight:700;">
            Driver ${{dNum}} (${{d.planet.split(' ')[0]}}) × Conductor ${{cNum}} (${{c.planet.split(' ')[0]}})
          </h4>
        </div>
        <div style="text-align:right;">
          <div style="font-size:1.35rem; font-weight:700; color:#8B6914;">${{starsDisplay}} (${{starsCount}}/5)</div>
          <div style="font-size:0.72rem; color:#7A654D; text-transform:uppercase;">Synergy Score: ${{syn.score}}</div>
        </div>
      </div>
      ${{syn.high_risk_warning ? `
        <div style="background:rgba(201,162,39,0.12); border-left:3px solid #8B6914; padding:8px 12px; border-radius:4px; font-size:0.83rem; color:#523E28; margin-bottom:10px;">
          <strong>⚠️ Vital Alignment Alert:</strong> ${{syn.high_risk_warning}}
        </div>
      ` : ''}}
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; font-size:0.82rem; margin-top:8px;">
        <div>
          <strong style="color:#16835B;">✓ Signature Strengths:</strong>
          <div style="color:#523E28; margin-top:3px;">${{(syn.positive_traits || []).slice(0, 3).join(', ') || 'Natural executive momentum'}}</div>
        </div>
        <div>
          <strong style="color:#8B6914;">💼 Prime Career Trajectories:</strong>
          <div style="color:#523E28; margin-top:3px;">${{(syn.recommended_careers || []).slice(0, 3).join(', ') || 'Leadership & Administration'}}</div>
        </div>
      </div>
    </div>
  `;

  // Complementary (Poorak) Card HTML
  const poorakHtml = `
    <div style="background:linear-gradient(135deg, rgba(22,131,91,0.06) 0%, rgba(255,253,247,0.98) 100%); border:1.5px solid rgba(22,131,91,0.32); border-radius:14px; padding:18px 22px; margin-bottom:20px;">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:8px;">
        <div>
          <span style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; padding:3px 10px; border-radius:20px; background:rgba(22,131,91,0.15); color:#16835B; border:1px solid rgba(22,131,91,0.3);">
            ✦ ${{poorak.synergy_type}} ✦
          </span>
          <h4 style="font-family:'Cormorant Garamond', Georgia, serif; font-size:1.35rem; color:#16835B; margin:4px 0 0 0; font-weight:700;">
            Harmonizing Poorak Number ${{poorak.poorak_number}} (${{poorak.poorak_planet}})
          </h4>
        </div>
        <div style="background:#FFFFFF; border:1.5px solid #16835B; border-radius:50%; width:44px; height:44px; display:flex; align-items:center; justify-content:center; font-size:1.4rem; font-weight:700; color:#16835B;">
          ${{poorak.poorak_number}}
        </div>
      </div>
      <p style="font-size:0.86rem; color:#523E28; line-height:1.55; margin:0 0 8px 0;">${{poorak.rationale}}</p>
      <div style="font-size:0.82rem; color:#16835B; background:rgba(22,131,91,0.08); padding:8px 12px; border-radius:8px;">
        <strong>Recommended Harmonization Ritual:</strong> ${{poorak.harmonizing_ritual}}
      </div>
    </div>
  `;

  // Panch Tattva Bodyguard Hygiene HTML
  const hygieneHtml = `
    <div style="background:#FFFDF7; border:1.5px solid rgba(201,162,39,0.35); border-radius:14px; padding:18px 22px; margin-bottom:20px;">
      <div style="font-size:0.74rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:#8B6914; margin-bottom:4px;">
        ✦ STEP 0 NON-NEGOTIABLE FOUNDATION ✦
      </div>
      <h4 style="font-family:'Cormorant Garamond', Georgia, serif; font-size:1.3rem; color:#523E28; margin:0 0 6px 0; font-weight:700;">
        Panch Tattva (Five Elements) Bodyguard Hygiene
      </h4>
      <p style="font-size:0.84rem; color:#7A654D; margin:0 0 12px 0;">
        Must touch physical skin continuously before performing any expensive gemstone or ritual practices:
      </p>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:10px; font-size:0.81rem;">
        <div style="background:#FFFFFF; border:1px solid rgba(201,162,39,0.25); border-radius:8px; padding:8px 12px;">
          <strong style="color:#16835B;">🌳 Wood Element (3, 4):</strong>
          <div style="color:#523E28;">Wear Rudraksha or Tulsi mala/bracelet touching neck or wrist.</div>
        </div>
        <div style="background:#FFFFFF; border:1px solid rgba(201,162,39,0.25); border-radius:8px; padding:8px 12px;">
          <strong style="color:#8B6914;">🌍 Earth Element (2, 5, 8):</strong>
          <div style="color:#523E28;">Wear White Quartz (Sphatik) bracelet (10-12mm) to cool body heat.</div>
        </div>
        <div style="background:#FFFFFF; border:1px solid rgba(201,162,39,0.25); border-radius:8px; padding:8px 12px;">
          <strong style="color:#C9A227;">🔥 Fire Element (9):</strong>
          <div style="color:#523E28;">Tie red cotton Mauli/Kalawa on wrist + 15 min morning sunlight.</div>
        </div>
        <div style="background:#FFFFFF; border:1px solid rgba(201,162,39,0.25); border-radius:8px; padding:8px 12px;">
          <strong style="color:#523E28;">💧 Water Element (1):</strong>
          <div style="color:#523E28;">Drink water stored in a pure Copper Bottle in mindful sips.</div>
        </div>
        <div style="background:#FFFFFF; border:1px solid rgba(201,162,39,0.25); border-radius:8px; padding:8px 12px;">
          <strong style="color:#7A654D;">⚔️ Metal / Air Element (6, 7):</strong>
          <div style="color:#523E28;">Wear a metallic chain watch (Silver for 7, Gold/Brass for 6).</div>
        </div>
      </div>
    </div>
  `;

  return `
    <div class="planet-chars-card">
      <div class="planet-chars-header">
        <span class="planet-chars-eyebrow">✦ DETERMINISTIC CANONICAL REGISTRY ✦</span>
        <h3 class="planet-chars-title">Planetary Characteristics &amp; Archetype Synthesis</h3>
        <p class="planet-chars-sub">
          Detailed behavioral characteristics, strengths, challenges, and harmonization remedies governed by Dr. Numeros Vision Classical Methodology's master numerology framework.
        </p>
      </div>

      ${{subdateHtml}}
      ${{dc81Html}}
      ${{poorakHtml}}
      ${{hygieneHtml}}

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

      <!-- Traditional Harmonization Remedies Box -->
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
        <div class="remedies-note" style="margin-top:10px; font-size:0.75rem; color:#7A654D; text-align:center;">
          Numeros Vision follows safe, non-fear lifestyle remedies. Consecrated gemstone and acoustic name balancing require personalized audit.
        </div>
      </div>
    </div>
  `;
}}

if (typeof window !== 'undefined') {{
  window.NUMBER_CHARACTERISTICS_REGISTRY = NUMBER_CHARACTERISTICS_REGISTRY;
  window.BIRTH_DAY_SUBDATE_REGISTRY = BIRTH_DAY_SUBDATE_REGISTRY;
  window.DRIVER_CONDUCTOR_81_REGISTRY = DRIVER_CONDUCTOR_81_REGISTRY;
  window.POORAK_DATA = POORAK_DATA;
  window.FIVE_ELEMENTS_HYGIENE = FIVE_ELEMENTS_HYGIENE;
  window.getPlanetarySynergy = getPlanetarySynergy;
  window.calculateClientPoorak = calculateClientPoorak;
  window.renderPlanetaryCharacteristicsHtml = renderPlanetaryCharacteristicsHtml;
}}
"""

out_path = 'app/static/js/number_characteristics.js'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"SUCCESS: Exported full master client bundle to {out_path} ({len(js_content)} bytes)")
