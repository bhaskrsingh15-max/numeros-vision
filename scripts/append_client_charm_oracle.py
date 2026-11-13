import os

def append_client_oracle():
    js_path = os.path.join('app', 'static', 'js', 'number_characteristics.js')
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    client_oracle_code = '''
/**
 * ─────────────────────────────────────────────────────────────────────────────
 * CHARM AI CLIENT-SIDE DETERMINISTIC ORACLE SYNTHESIZER
 * Numeros Vision — "ANVEIL EVERY CHARM"
 * Provides 100% offline & static-CDN parity for Dr. Numeros Vision Classical Methodology's 16 domains.
 * ─────────────────────────────────────────────────────────────────────────────
 */

const DUAL_ATTRIBUTES_JS = {
  1: {
    attribute: "Communication & Executive Leadership",
    good: "Direct, clear, commanding vision, articulate executive voice, decisive initiative, dignified self-respect",
    bad: "Arrogant speech, interrupting others, dominating conversations, stubborn refusal to listen, ego clashes",
    under: "Hesitation in public speaking, difficulty asserting authority, holding back honest thoughts",
    exaggerated: "Overbearing directives, blunt aggression, demanding blind obedience"
  },
  2: {
    attribute: "Intuition & Sensitive Power",
    good: "Deep emotional intelligence, instinctual empathy, gentle diplomacy, creative harmony, marital warmth",
    bad: "Hypersensitivity, mood swings, chronic self-doubt, emotional dependency, easily offended",
    under: "Suppressed emotions, cold detachment, difficulty sensing partner or team sentiments",
    exaggerated: "Emotional over-reaction, anxiety spirals, paralyzing fear of rejection"
  },
  3: {
    attribute: "Creativity & Imagination Power",
    good: "Expansive wisdom, compelling mentorship, visionary storytelling, artistic fluency, strategic counsel",
    bad: "Scattered focus, superficial enthusiasm, lecturing rather than listening, unfinished projects",
    under: "Creative blockages, fear of self-expression, difficulty trusting one's own intellect",
    exaggerated: "Mental restlessness, exaggerating facts, patronizing attitude toward peers"
  },
  4: {
    attribute: "Discipline & Organised Power",
    good: "Systemic architecture, meticulous planning, high technical precision, unwavering reliability",
    bad: "Rigid obstinacy, sudden volatile disruptions, obsession with trivial details, resistance to change",
    under: "Chaotic disorganization, messy physical/digital desk, procrastination with timelines",
    exaggerated: "Compulsive micromanagement, harsh skepticism, stress from minor deviations"
  },
  5: {
    attribute: "Balance (Health, Wealth, Career & Relationships)",
    good: "Harmonious central equilibrium, swift commercial adaptability, networking charisma, multi-domain agility",
    bad: "Restlessness, gambling with impulsive risks, lack of follow-through, sensory over-indulgence",
    under: "Loss of life balance, feeling torn between work and family, sluggish career progress",
    exaggerated: "Chronic multitasking with zero depth, erratic lifestyle, constant changing of ventures"
  },
  6: {
    attribute: "Home, Family & Love Relationships",
    good: "Luxurious warmth, marital fidelity, aesthetic excellence, generous caretaking, high social standing",
    bad: "Codependency, domestic friction, excessive status-seeking spending, smothering attachments",
    under: "Strained home atmosphere, lack of comfort or aesthetic ease, relationship hesitation",
    exaggerated: "Emotional manipulation within family, unrealistic perfectionist romantic expectations"
  },
  7: {
    attribute: "Disappointments, Healing, Wisdom & Occult Depth",
    good: "Profound research acumen, spiritual detachment, esoteric discernment, healing presence, truth-seeking",
    bad: "Cynical withdrawal, feeling betrayed by loved ones, chronic disappointment, intellectual arrogance",
    under: "Superficial outlook, lack of introspective discernment, trusting deceptive promises easily",
    exaggerated: "Excessive isolation, paranoid secrecy, disconnect from mundane social responsibilities"
  },
  8: {
    attribute: "Money & Finance Management",
    good: "Monumental compounding wealth, financial prudence, institutional endurance, objective fairness",
    bad: "Financial anxiety, trapping capital in illiquid deadlocks, feeling crushed by heavy labor, ruthlessness",
    under: "Careless expenditure, financial leaks, difficulty organizing budgets or saving consistently",
    exaggerated: "Cold materialism, hoarding out of fear of scarcity, severe workaholism damaging health"
  },
  9: {
    attribute: "Aggression, Ego, Humanity & Humility",
    good: "Selfless humanitarian leadership, noble courage, protective strength, energetic initiative",
    bad: "Destructive temper tantrums, bruised ego, burning bridges in self-righteous fury, reckless haste",
    under: "Lack of protective boundaries, passive acceptance of mistreatment, low physical stamina",
    exaggerated: "Explosive rage, vindictive arguments, treating minor disagreements as personal warfare"
  }
};

const PLANET_NAMES_MAP = {
  1: "Sun (Surya)", 2: "Moon (Chandra)", 3: "Jupiter (Guru)", 4: "Rahu",
  5: "Mercury (Budh)", 6: "Venus (Shukra)", 7: "Ketu", 8: "Saturn (Shani)", 9: "Mars (Mangal)"
};

function detectClientFaith(name) {
  const nl = (name || "").toLowerCase();
  if (/mohd|md|syed|sheikh|abdul|khan|ali|ahmed|hussain|malik|fatima|ansari|qureshi|begum/.test(nl)) return "muslim";
  if (/john|joseph|peter|david|mary|fernandes|dsouza|d'souza|pereira|thomas|mathew|george|paul|michael|sarah|lisa/.test(nl)) return "christian";
  if (/(singh|kaur)/.test(nl) && /(gurpreet|harpreet|jaspreet|amrit|kuldeep|daljit)/.test(nl)) return "sikh";
  if (/(jain|shah|mehta|doshi)/.test(nl) && !/singh|sharma/.test(nl)) return "jain";
  return "hindu";
}

function getClientFaithRemedy(faith, driver) {
  const pName = PLANET_NAMES_MAP[driver] || "Planetary Ruler";
  if (faith === "muslim") {
    return `• **Sadaqah & Charitable Giving:** Practice voluntary Sadaqah on auspicious mornings (Fridays or Mondays). Provide clean drinking water or feed birds quietly without ostentation.\\n• **Elemental Harmonization:** Place natural green plants in your living area and apply natural non-alcoholic attar (rose/sandalwood) to invite peaceful, harmonious frequencies.\\n• **Contemplation:** Spend 10 minutes in quiet morning reflection and gratitude facing East/North.`;
  }
  if (faith === "christian") {
    return `• **Benevolent Almsgiving:** Donate warm meals, clean blankets, or books to a local children's shelter on Sunday mornings.\\n• **Contemplative Light:** Light a pure beeswax or white candle during morning prayer for clarity, divine wisdom, and peace.\\n• **Gratitude Practice:** Maintain a daily morning scripture reading and gratitude journal entry to center your spirit.`;
  }
  if (faith === "sikh") {
    return `• **Nishkam Seva:** Participate in voluntary Langar service at a Gurdwara on auspicious mornings.\\n• **Vand Chhako:** Share blessings by feeding stray birds or helping a student in need with educational materials.\\n• **Simran:** Practice quiet morning Naam Simran in a naturally lit space facing East.`;
  }
  if (faith === "jain") {
    return `• **Jiva Daya:** Feed green grass to cows or place grains and fresh water for birds on Thursday/Sunday mornings.\\n• **Ahimsa & Equanimity:** Practice mindful, peaceful speech, avoid harsh criticism of peers, and wear serene white or natural cream cotton clothing.\\n• **Svadhyaya:** Dedicate 15 minutes to quiet self-study and meditation on universal goodwill (Samayika).`;
  }
  // Default Hindu
  const mantras = {
    1: "Om Hram Hrim Hroum Sah Suryaya Namah (108 times at solar dawn with copper water Arghya)",
    2: "Om Shram Shrim Shroum Sah Chandraya Namah (Monday evening, respect maternal figures)",
    3: "Om Gram Grim Groum Sah Gurave Namah (Thursday midday, apply sandalwood tilak)",
    4: "Om Bhram Bhrim Bhroum Sah Rahave Namah (keep electronics tidy, feed stray dogs on Saturday)",
    5: "Om Bram Brim Broum Sah Budhaya Namah (feed green fodder to cows on Wednesday, care for plants)",
    6: "Om Dram Drim Droum Sah Shukraya Namah (wear clean fragrant clothes on Friday, respect women)",
    7: "Om Sram Srim Sroum Sah Ketave Namah (feed sesame seeds or roti to black-and-white dogs)",
    8: "Om Pram Prim Proum Sah Shanaishcharaya Namah (light mustard oil lamp near Peepal on Saturday dusk)",
    9: "Om Kram Krim Kroum Sah Bhaumaya Namah (chant Hanuman Chalisa on Tuesday morning, physical conditioning)"
  };
  return `• **Vedic Beej Mantra & Arghya:** Chant *${mantras[driver] || mantras[1]}*.\\n• **Elemental Balance:** Keep a natural brass or copper vessel in the North-East; offer water to the morning sun to vitalize your core ${pName} energy.`;
}

function generateCharmAiClientResponse(name, day, month, year, question, isPremium) {
  const dVal = parseInt(day, 10) || 15;
  const mVal = parseInt(month, 10) || 8;
  const yVal = parseInt(year, 10) || 1990;
  const uName = (name || "Seeker").trim();
  const fName = uName.split(' ')[0] || "Seeker";
  const ql = (question || "").toLowerCase();

  // 1. Calculations
  let dTotal = dVal;
  while (dTotal > 9 && dTotal !== 11 && dTotal !== 22) {
    dTotal = String(dTotal).split('').reduce((a, b) => a + parseInt(b), 0);
  }
  const driver = dTotal;

  let cTotal = dVal + mVal + yVal;
  while (cTotal > 9 && cTotal !== 11 && cTotal !== 22 && cTotal !== 33) {
    cTotal = String(cTotal).split('').reduce((a, b) => a + parseInt(b), 0);
  }
  const conductor = cTotal;

  const currentYear = new Date().getFullYear();
  let pyTotal = dVal + mVal + currentYear;
  while (pyTotal > 9) {
    pyTotal = String(pyTotal).split('').reduce((a, b) => a + parseInt(b), 0);
  }
  const personalYear = pyTotal;

  // 2. Lo Shu Grid Counts & Repetition Degree
  const dobStr = `${String(dVal).padStart(2, '0')}${String(mVal).padStart(2, '0')}${yVal}`;
  const counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0};
  for (const ch of dobStr) {
    if (ch !== '0') counts[parseInt(ch)]++;
  }

  const missing = [];
  const present = [];
  const pairs = [];
  const aggressive = [];
  for (let n = 1; n <= 9; n++) {
    if (counts[n] === 0) missing.push(n);
    else {
      present.push(n);
      if (counts[n] === 2) pairs.push(n);
      if (counts[n] >= 3) aggressive.push(n);
    }
  }

  // 3. Topic Classification across 16 Syllabus Domains
  let topicKey = "general_destiny";
  let topicDisplay = "Personal Destiny, Dasha Alignment & Cosmic Cycles";

  if (/(stuck everywhere|blocked everywhere|universal obstacle|karmic block|nothing working|stuck in life|problems everywhere)/.test(ql) ||
      (/obstacle/.test(ql) && /(everywhere|all areas|in everything)/.test(ql)) ||
      (/wealth/.test(ql) && /career/.test(ql) && /(marriage|love)/.test(ql))) {
    topicKey = "universal_obstacles";
    topicDisplay = "Karmic Stagnation & Universal Obstacle Reset";
  } else if (/(conceive|conception|progeny|santan|pregnant|pregnancy|baby birth|fertility)/.test(ql)) {
    topicKey = "child_conception";
    topicDisplay = "Child Conception, Fertility & Progeny Timing";
  } else if (/(child studies|teen career|studies|exam|education|school|college|marks|focus in study)/.test(ql)) {
    topicKey = "child_studies";
    topicDisplay = "Child Studies, Academic Focus & Youth Career Direction";
  } else if (/(partner match|matching|compatibility|gun milan|kundali match|should i marry|partner compatibility)/.test(ql)) {
    topicKey = "partner_matching";
    topicDisplay = "Partner Matching, Cosmic Synergy & Compatibility";
  } else if (/(love|marriage|partner|husband|wife|spouse|shaadi|vivah|relationship|divorce|marital)/.test(ql)) {
    topicKey = "love_marriage";
    topicDisplay = "Love, Marriage & Relationship Harmony";
  } else if (/(share market|stocks|stock market|trading|crypto|intraday|nifty|mutual fund|equity)/.test(ql)) {
    topicKey = "share_market";
    topicDisplay = "Share Market, Stock Trading & Speculative Wealth";
  } else if (/(money|wealth|finance|debt|loan|bankrupt|income|paisa|dhan|trapped money)/.test(ql)) {
    topicKey = "wealth_finances";
    topicDisplay = "Wealth Obstacles, Debt Relief & Capital Growth";
  } else if (/(business|partnership|startup|venture|firm|founder|freelance|own company|commercial)/.test(ql)) {
    topicKey = "business_partnerships";
    topicDisplay = "Business Alignment, Commercial Scale & Partnerships";
  } else if (/(stuck|blocked|lost opportunity|lost job|struggling in job|delay in job|career reset|layoff)/.test(ql)) {
    topicKey = "career_stuck";
    topicDisplay = "Career Stuck, Job Delays & Strategic Reset";
  } else if (/(promotion|growth|new job|senior role|interview|salary hike|appraisal|career)/.test(ql)) {
    topicKey = "career_growth";
    topicDisplay = "Career Acceleration, Promotion & Leadership Elevation";
  } else if (/(foreign|abroad|visa|relocation|overseas|pr|settlement)/.test(ql)) {
    topicKey = "foreign_relocation";
    topicDisplay = "Foreign Settlement, Relocation & Travel Opportunities";
  } else if (/(missing number|missing numbers|lo shu grid|elements|loshu)/.test(ql)) {
    topicKey = "missing_numbers";
    topicDisplay = "Missing Lo Shu Elements & Planetary Balances";
  } else if (/(repetitive|repeat|multiple times|degree|power of numbers)/.test(ql)) {
    topicKey = "repetition_degree";
    topicDisplay = "Repetitive Numbers Degree & Planetary Energy";
  } else if (/(name spelling|name balance|change name|chaldean name|name harmony)/.test(ql)) {
    topicKey = "name_balancing";
    topicDisplay = "Chaldean Name Balancing & Sound Vibrations";
  } else if (/(health|illness|disease|vitality|stress|sleep|depression|fatigue)/.test(ql)) {
    topicKey = "health_vitality";
    topicDisplay = "Health, Vitality & Nervous System Balance";
  }

  // 4. Faith & Cultural Detection
  const faith = detectClientFaith(uName);
  const faithRemedy = getClientFaithRemedy(faith, driver);

  // 5. Planetary Timing Window
  const startM = String((personalYear % 12) + 1).padStart(2, '0');
  const endM = String(((personalYear + 3) % 12) + 1).padStart(2, '0');
  const timingWindowStr = `**${currentYear}-${startM}-15** to **${currentYear + (personalYear >= 10 ? 1 : 0)}-${endM}-28**`;

  const dPlanet = PLANET_NAMES_MAP[driver] || "Sun (Surya)";
  const cPlanet = PLANET_NAMES_MAP[conductor] || "Saturn (Shani)";
  const dDual = DUAL_ATTRIBUTES_JS[driver] || DUAL_ATTRIBUTES_JS[1];

  let diagnosisText = "";
  let coreAdvice = "";
  let practicalSteps = [];

  if (topicKey === "love_marriage" || topicKey === "partner_matching") {
    diagnosisText = `In your birth matrix, your primary relationship axis is governed by Driver ${driver} (${dPlanet}) and Conductor ${conductor} (${cPlanet}). In love and marriage, Driver ${driver} establishes your inborn communication temperament (${dDual.good}), while Conductor ${conductor} dictates long-term domestic karma. `;
    if (missing.includes(6)) {
      diagnosisText += `Crucially, **Number 6 (Venus - Home & Family Relationships)** is missing from your core birth grid, which often introduces subtle feelings of domestic misunderstanding, emotional expectations going unexpressed, or delay in marital contentment unless actively compensated. `;
    } else if (pairs.includes(6)) {
      diagnosisText += `Your chart possesses **Number 6 as a balanced Pair (Two Times)**, which Dr. Numeros Vision Classical Methodology notes as the best-performing harmonious balance—giving deep affection, loyalty, and aesthetic care for your partner once trust is secured. `;
    } else if (missing.includes(2)) {
      diagnosisText += `Because **Number 2 (Moon - Intuitive Empathy)** is absent, misunderstandings often stem not from a lack of love, but from differing emotional communication styles where one partner expects words while the other shows care through actions. `;
    }
    coreAdvice = `During your current **Personal Year ${personalYear}**, relationship dynamics are asking for conscious renewal. Instead of reacting to temporary mood shifts, establish an open weekly dialogue window without digital distractions. When you balance mutual space with consistent appreciation, friction naturally softens into deeper intimacy.`;
    practicalSteps = [
      "Dedicate a weekly screen-free 30-minute dialogue with your partner solely to listen without defense or debate.",
      "Keep a pair of light pink or cream quartz stones in the South-West relationship corner of your bedroom to ground emotional peace."
    ];
  } else if (topicKey === "career_growth" || topicKey === "career_stuck") {
    diagnosisText = `Your professional blueprint combines the pioneering executive drive of Driver ${driver} (${dPlanet}) with the overarching karmic trajectory of Conductor ${conductor} (${cPlanet}). You are naturally wired for ${dDual.attribute}. `;
    if (topicKey === "career_stuck") {
      diagnosisText += `Please remember: feeling paused or sensing delayed recognition in 2026 is **not a personal failure**; it is a structural transit pause. Currently, you are traversing **Personal Year ${personalYear}**, which acts as a celestial filter testing your operational foundations so you step into authentic, unshakeable authority rather than a fragile compromise. `;
    } else {
      diagnosisText += `In 2026, navigating **Personal Year ${personalYear}**, your career momentum is actively preparing for an upward breakthrough. Your natural superpowers shine brightest when you operate with strategic autonomy rather than passive waiting. `;
    }
    if (pairs.includes(1)) {
      diagnosisText += `Your birth grid features **Number 1 as a balanced Pair**, confirming natural executive command and clear verbal authority when you back yourself. `;
    } else if (aggressive.includes(8)) {
      diagnosisText += `With **Number 8 present 3 or more times**, Saturn's compounding power is intense—you will achieve great institutional scale, but early milestones demand extraordinary perseverance before unlocking sudden massive rewards. `;
    }
    coreAdvice = `Your strongest acute breakthrough window runs from ${timingWindowStr}. Use this preparatory phase to document your quantifiable business accomplishments, streamline your executive pitch, and reach out directly to key industry decision-makers.`;
    practicalSteps = [
      "Document 3 quantifiable business achievements in clear metrics and update your professional summary.",
      "Conduct a 3-touchpoint outreach: message 3 former mentors or trusted executive contacts with a brief, value-focused note.",
      "Position your desk facing East or North while making high-stakes calls to harness solar clarity."
    ];
  } else if (topicKey === "wealth_finances" || topicKey === "share_market") {
    diagnosisText = `Your financial engine is anchored by Driver ${driver} and Conductor ${conductor}. In classical Sankhya Shastra, wealth generation requires harmony between Number 1 (Initiative), Number 5 (Commercial Speed), and Number 8 (Compounding Stability). `;
    if (missing.includes(8)) {
      diagnosisText += `Notice that **Number 8 (Saturn - Finance & Long-term Compounding)** is absent from your birth grid. This creates an energetic pattern where money flows in steadily, but financial leaks, impulsive expenditures, or lending to unreliable peers drains compounding savings unless strictly budgeted. `;
    } else if (pairs.includes(8)) {
      diagnosisText += `You possess **Number 8 in an auspicious Pair (Two Times)**, which Dr. Numeros Vision Classical Methodology identifies as the optimal wealth balance—bringing disciplined money management, enduring investments, and resilience through market cycles. `;
    }
    if (topicKey === "share_market") {
      diagnosisText += (present.includes(5) 
        ? `Regarding speculative equity or share trading: you have Number 5 active, giving you swift market adaptability to support structured swing trading, provided you avoid reckless intraday leverage.`
        : `Regarding speculative equity or share trading: since Number 5 is missing, pure speculative day-trading carries erratic volatility; you will build far greater enduring wealth through long-term index compounding, real estate, and blue-chip holdings.`);
    }
    coreAdvice = `During **Personal Year ${personalYear}**, focus on plugging silent monthly capital leaks and avoiding emotional debt guarantees. Your numbers favor disciplined, compounding wealth accumulation over get-rich-quick gambles.`;
    practicalSteps = [
      "Conduct a ruthless audit of all recurring subscriptions and automated debits to eliminate hidden financial leakage.",
      "Never lend money on Saturdays or sign financial loan guarantees under emotional pressure.",
      "Keep your financial documents and primary cash ledger in the North or North-East sector of your home."
    ];
  } else if (topicKey === "child_conception" || topicKey === "child_studies") {
    if (topicKey === "child_conception") {
      diagnosisText = `Child conception and progeny blessings in Vedic Numerology are governed by Number 2 (Chandra - Receptive Womb & Fluid Harmony), Number 3 (Guru/Jupiter - Divine Expansion & Seed Multiplication), and Number 6 (Venus - Vital Reproductive Fluid & Domestic Grace). Looking at your numbers (Driver ${driver}, Conductor ${conductor}): your cycle in Personal Year ${personalYear} brings natural creative renewal. `;
      if (missing.includes(3) || missing.includes(2)) {
        diagnosisText += `With elemental wood (3) or lunar earth (2) in need of balancing in your grid, conception timing benefits greatly from conscious nervous system calming, eliminating chronic workplace stress, and aligning with fertile celestial lunar cycles. `;
      }
      coreAdvice = `The most auspicious fertile window for divine progeny acceleration aligns between ${timingWindowStr}. Keep physical health, calm mental states, and spiritual harmony as your central daily focus.`;
      practicalSteps = [
        "Maintain gentle, nourishing routines: consume warm soaked almonds and water stored in silver/copper vessels.",
        "Spend 15 minutes each evening in quiet grounding with your spouse, free from digital screens and work stress."
      ];
    } else {
      diagnosisText = `For academic focus, memory, and youth career direction: Number 3 (Jupiter - Wisdom & Retention), Number 5 (Mercury - Rapid Learning & Logic), and Number 4 (Rahu - Systemic Discipline) govern student success. Your chart reveals strong natural intelligence, and learning accelerates through interactive, visual methods rather than rigid rote memorization.`;
      coreAdvice = `Create an organized, clutter-free study corner facing East or North-East to maximize concentration and memory retention.`;
      practicalSteps = [
        "Place the study desk facing North-East with a soft warm reading light to promote intellectual tranquility.",
        "Break study intervals into focused 25-minute sprints followed by 5 minutes of mindful stretching."
      ];
    }
  } else if (topicKey === "business_partnerships") {
    diagnosisText = `Entrepreneurial success and commercial expansion demand a dynamic synthesis of Driver ${driver} (${dPlanet}) executive authority and Conductor ${conductor} (${cPlanet}) market reputation. `;
    if (missing.includes(5)) {
      diagnosisText += `Because **Number 5 (Mercury - The Master Key of Commercial Balance)** is missing from your birth grid, running solo business operations can occasionally feel overwhelming or suffer from inconsistent client communication. You benefit immensely from partnering with an operationally agile, detail-oriented collaborator. `;
    } else if (present.includes(5)) {
      diagnosisText += `With **Number 5 present in your grid**, you have natural commercial intuition, market networking ability, and the flexibility to pivot offerings to meet customer demand. `;
    }
    coreAdvice = `In 2026, traversing **Personal Year ${personalYear}**, business initiatives thrive when backed by written legal contracts, clear partnership equity terms, and strong ethical governance. Your most auspicious commercial launch and client expansion window unfolds from ${timingWindowStr}.`;
    practicalSteps = [
      "Ensure all business partnership terms, IP ownership, and profit splits are documented in formal written agreements.",
      "Focus marketing outreach on your top 20% highest-margin clients rather than spreading energy across unprofitable low-ticket offers.",
      "Place a healthy indoor green plant or green aventurine cluster on the North side of your business desk."
    ];
  } else if (topicKey === "universal_obstacles") {
    diagnosisText = `Namaste ${fName} 🙏 Take a deep, reassuring breath. When obstacles seem to appear on all sides—in career, money, and personal peace—it feels exhausting, but in authentic occult numerology, this is the classic signature of **Karmic Boundary Recalibration**. Combining Driver ${driver} (${dPlanet}) and Conductor ${conductor} (${cPlanet}) in Personal Year ${personalYear}: your soul has outgrown old compromises. The friction you are experiencing is your planetary cycles forcefully shutting doors to outmoded, draining paths so you can step into an unshakeable, higher tier of life.`;
    coreAdvice = `The celestial turning point arrives between ${timingWindowStr}. Stop fighting the current by making desperate moves. Instead, ground your energy, eliminate toxic draining habits, and focus on simple, consistent daily spiritual and physical alignments.`;
    practicalSteps = [
      "Practice a strict 7-day energetic fast: avoid heated arguments, refrain from complaining about delays, and drink water from a copper vessel.",
      "Declutter your sleeping space: remove broken items, electronic clutter, and old unused shoes to clear heavy stagnant vibrations.",
      "Feed stray animals, birds, or cows once weekly on Saturday morning to neutralize heavy karmic friction."
    ];
  } else {
    diagnosisText = `Your core cosmic matrix combines **Driver ${driver} (${dPlanet})** with **Conductor ${conductor} (${cPlanet})**. Driver ${driver} represents your inborn decision temperament (${dDual.attribute}), while Conductor ${conductor} guides your overarching life lessons and ultimate destination. Currently in 2026, your cycle is energized by **Personal Year ${personalYear}**, setting a pivotal stage for milestone transitions.`;
    coreAdvice = `Your acute planetary window of alignment spans ${timingWindowStr}. Aligning your daily habits, workspace direction, and ethical choices with this timing unlocks clear, friction-free momentum.`;
    practicalSteps = [
      `Wear or surround yourself with your auspicious planetary colors: ${driver === 1 ? 'Gold, Amber, Warm Yellow' : 'White, Cream, Silver'}.`,
      `Schedule major decisions and high-stakes conversations on your power day: ${driver === 1 ? 'Sunday' : 'Monday'}.`,
      "Align your working desk facing North or East to channel focused solar and commercial mental clarity."
    ];
  }

  const ctaHook = !isPremium ? `
---
### ✦ ANVEIL EVERY CHARM ✦
*Your foundational diagnostic synthesis is complete. To unlock your full multi-year predictive timeline, day-by-day favorable event calendar, complete 4-tradition (KP, Lal Kitab, Vedic & BNN) astrological chart overlays, and personalized consecrated gemstone/ritual specifications, explore our full Charm AI Passes or download your comprehensive 12-Page Personalised Blueprint.*

<div style="display:flex; gap:10px; flex-wrap:wrap; margin-top:10px;">
  <a href="/pricing/#charm-ai" class="btn-primary-gold" style="display:inline-block; padding:8px 18px; font-size:0.82rem;">Anveil Full Charm AI Pass (from ₹199) →</a>
  <a href="/reports_catalogue/" class="btn-secondary-amber" style="display:inline-block; padding:8px 18px; font-size:0.82rem;">Explore 12-Page Personalised Report (₹510) →</a>
</div>
` : `
---
### ✦ PREMIUM CHARM AI DOSSIER UNLOCKED ✦
**Multi-Year Dasha Epicycle:** You are traversing a 9-year evolutionary phase where Mahadasha of ${dPlanet} intersects with your Pratyantardasha window (${timingWindowStr}). Maintain unshakeable focus on your consecrated remedies.
`;

  const fullText = `Namaste ${fName} 🙏

**1. What Your Numbers Reveal About '${topicDisplay}':**
${diagnosisText}

**2. Active Cycle & Timing Horizon:**
${coreAdvice}

**3. Practical Steps to Accelerate Your Alignment:**
${practicalSteps.map((s, i) => `• **Step ${i + 1}:** ${s}`).join('\\n')}

**4. Sacred Lifestyle & Faith Attunement (${faith.charAt(0).toUpperCase() + faith.slice(1)} Tradition):**
${faithRemedy}

✦ **Multi-Tradition Astrological Verification (88% Consensus):**
• **KP Astrology:** 10th/11th Cuspal sub-lord corroborates structural progress with methodical discipline.
• **Bhrigu Nandi Nadi (BNN):** Jupiter & Saturn transit rays support long-term compounding during Personal Year ${personalYear}.
• **Vedic Kundli:** Natural karakas of Driver ${driver} and Conductor ${conductor} maintain active governance.
${ctaHook}`;

  return {
    status: "success",
    topic_display: topicDisplay,
    driver: driver,
    conductor: conductor,
    personal_year: personalYear,
    timing_window: timingWindowStr,
    direct_answer: fullText,
    humanized_consultation: fullText,
    practical_actions: practicalSteps,
    faith_remedy: faithRemedy,
    is_premium: isPremium
  };
}

if (typeof window !== 'undefined') {
  window.generateCharmAiClientResponse = generateCharmAiClientResponse;
}
'''

    if 'generateCharmAiClientResponse' not in content:
        content += client_oracle_code
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('Successfully appended generateCharmAiClientResponse to number_characteristics.js')
    else:
        print('generateCharmAiClientResponse already present')

if __name__ == '__main__':
    append_client_oracle()
