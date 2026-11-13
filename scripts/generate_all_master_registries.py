# -*- coding: utf-8 -*-
"""
GENERATE ALL MASTER REGISTRIES
Numeros Vision — Master Knowledge Engine
Populates:
1. app/data/birth_subdates_registry.json (Days 1 to 31 RAG-verified profiles)
2. data/knowledge_base/driver_conductor_81_rules.json (All 81 DC rules with positive/negative traits, star ratings, careers, warnings)
3. app/engine/driver_conductor_81_engine.py (O(1) fast deterministic lookup engine)
4. app/engine/five_elements_hygiene_engine.py (Panch Tattva bodyguards and hygiene remedies)
5. app/engine/number_characteristics_registry.py (incorporates the enriched sub-date registry)
"""

import json
import os
import sys

def get_subdates_data():
    return {
        1: {
            "day": 1, "root": 1, "code": "1(b)", "tier": "b",
            "strength_category": "B", "strength_title": "Category B — Normal Strength (Balanced Potency)",
            "strength_potency_score": 78,
            "planet": "Sun (Surya)", "is_karmic": False, "is_master": False,
            "archetype": "The Primal Originator & Sovereign Pioneer",
            "classical_symbol": "The Golden Monad / Solar Spark",
            "planetary_composition": "Pure Sun (Surya) Energy",
            "strength_value_breakdown": "Pure single-digit solar energy grants strong independence, executive willpower, and pioneering courage. Graded as Category B (Normal Strength) because single-digit 1 requires conscious cultivation of diplomatic partnership skills and team delegation to prevent autocratic isolation.",
            "core_personality": "Naturally self-directed, ambitious, and original. You despise being micromanaged and thrive when leading projects from inception. You project natural authority and expect excellence from peers.",
            "superpowers": ["Pioneering initiative", "Clear executive focus", "Unwavering self-trust", "Decisive crisis leadership", "Original conceptual vision"],
            "shadow_vulnerabilities": ["Impatience with slower minds", "Autocratic stubbornness", "Difficulty asking for assistance", "Ego sensitivity to perceived disrespect"],
            "career_and_wealth": "Supreme suitability for startup founders, corporate executive management, government administration, political strategy, and solo consulting.",
            "love_and_relationships": "Generous and protective partner, but requires an equal who respects personal autonomy and does not challenge basic independence.",
            "remedial_blueprint": {
                "practical_growth_action": "Practice active listening in meetings without interrupting; delegate at least one key daily task to build team trust.",
                "universal_secular_remedy": "Drink water from a pure copper bottle; start morning with 15 minutes of natural sunlight; Solfeggio 528 Hz for vitality.",
                "traditional_vedic_remedy": "Daily morning Surya Arghya (water offering with pinch of red kumkum/sandalwood in copper lota); Gayatri Mantra or Om Suryaya Namaha 108 times.",
                "auspicious_colors": ["Gold", "Amber", "Warm Yellow", "Saffron"],
                "auspicious_days": ["Sunday", "Monday"],
                "compatible_dates": [1, 10, 19, 28, 2, 3, 5, 9],
                "challenging_dates": [8, 17, 26, 4]
            },
            "report_narrative": "Born on the 1st, you carry the primal creative vibration of the Sun. Your life path is structured around self-reliance, original leadership, and visionary execution. While your executive willpower allows you to launch bold enterprises, your greatest evolution lies in turning solo brilliance into collaborative triumph.",
            "charm_ai_dialogue": "You are born on the 1st—pure solar power! You are a natural pioneer who thrives in autonomy. Your Category B strength gives you steady, focused drive. Remember: true kings don't command from isolation; they empower their circle. Balance your fiery ambition with patient delegation to see your vision soar."
        },
        10: {
            "day": 10, "root": 1, "code": "10(b)", "tier": "b",
            "strength_category": "B", "strength_title": "Category B — Normal Strength (Karmic 10 / Wheel of Fortune)",
            "strength_potency_score": 80,
            "planet": "Sun (Surya)", "is_karmic": True, "is_master": False,
            "archetype": "The Sovereign of the Wheel & Self-Made Architect",
            "classical_symbol": "The Wheel of Fortune (Cheiro Canon)",
            "planetary_composition": "Sun (1) + Cosmic Void (0) = Solar Infinity",
            "strength_value_breakdown": "The cipher (0) magnifies the Sun's ambition and introduces cyclical karmic turning points. Categorized as Category B (Normal Strength) because monumental rise and fall depend strictly on personal ethical choices and discipline.",
            "core_personality": "Possesses a charismatic, self-confident aura with a remarkable capacity to reinvent yourself after life disruptions. You believe deeply in your own destiny and reject defeat.",
            "superpowers": ["Rapid regenerative recovery", "Magnetic public confidence", "Systemic big-picture foresight", "Fearless commercial enterprise", "Natural executive gravity"],
            "shadow_vulnerabilities": ["Extreme all-or-nothing mindset", "Sudden detachment from routine commitments", "Over-confidence leading to financial overreach", "Resistance to emotional vulnerability"],
            "career_and_wealth": "Thrives in large enterprise management, venture building, investment banking, media production, and turn-around corporate stewardship.",
            "love_and_relationships": "Warm, generous, and dignified. Seeks a partner who celebrates accomplishments and provides a grounded, stable home base.",
            "remedial_blueprint": {
                "practical_growth_action": "Document long-term contingency plans rather than relying purely on momentum; celebrate milestones with heartfelt gratitude to your team.",
                "universal_secular_remedy": "Place a brass sun emblem or golden paperweight in the East sector of your workspace; hydrate regularly; practice evening reflection.",
                "traditional_vedic_remedy": "Aditya Hridaya Stotra on Sundays; donate golden wheat or jaggery (gur) to community kitchens; respect father figures.",
                "auspicious_colors": ["Golden Yellow", "Copper Orange", "Cream"],
                "auspicious_days": ["Sunday", "Tuesday"],
                "compatible_dates": [1, 10, 19, 28, 5, 23, 9],
                "challenging_dates": [8, 17, 26, 18]
            },
            "report_narrative": "Born on the 10th, you operate under the vibration of the Wheel of Fortune. The cosmic zero acts as an amplifier of your solar drive. You possess an innate ability to bounce back from any career setback stronger than before.",
            "charm_ai_dialogue": "Day 10 connects you to the Wheel of Fortune! With Category B strength, the zero behind your 1 amplifies your solar destiny. You are built to rise, rebuild, and conquer. Keep your ethical foundation rock-solid and every turn of the wheel will elevate your status."
        },
        19: {
            "day": 19, "root": 1, "code": "19(a)", "tier": "a",
            "strength_category": "A", "strength_title": "Category A — Good Strength (Karmic 19 / Prince of Heaven)",
            "strength_potency_score": 94,
            "planet": "Sun (Surya)", "is_karmic": True, "is_master": False,
            "archetype": "The Sovereign Conqueror & Radiant Champion",
            "classical_symbol": "The Prince of Heaven / The Radiant Sun (Cheiro Canon)",
            "planetary_composition": "Sun (1) + Mars (9) = 10 -> 1 (Fire + Fire Harmony)",
            "strength_value_breakdown": "Sun (Surya) and Mars (Mangal) are natural fire allies, creating unstoppable executive drive, supreme courage, and royal magnetism. Rated Category A (Good Strength / 94% Potency). Karmic 19 lesson: must overcome the shadow of carrying all burdens alone and asking no help.",
            "core_personality": "Radiant, high-octane, trendsetting, and fiercely ambitious. You carry royal pride and an instinct to protect others while pioneering new frontiers. Failure is never an option in your lexicon.",
            "superpowers": ["Unstoppable manifestation drive", "Heroic courage under pressure", "Trend-setting magnetic vision", "Rapid social and career ascendancy", "Protective leadership loyalty"],
            "shadow_vulnerabilities": ["Burdening yourself with everything alone", "Fierce temper when disrespect is perceived", "Resistance to admitting weakness", "Tendency to dominate peers"],
            "career_and_wealth": "Top-tier defense and security leadership, venture capitalism, high-stakes corporate law, disruptive tech founders, surgical specialties, and political office.",
            "love_and_relationships": "Passionate, protective, and generous. Demands absolute fidelity and deep mutual respect. Needs an emotionally secure partner who is not intimidated by high ambition.",
            "remedial_blueprint": {
                "practical_growth_action": "Practice asking for and receiving help with grace; share credit publicly with subordinates; cool your internal fire with mindful breathing.",
                "universal_secular_remedy": "Carry a red jasper or carnelian stone; use 432 Hz calming frequencies; keep a dedicated water carafe on your desk.",
                "traditional_vedic_remedy": "Recite Hanuman Chalisa daily; offer copper water arghya to early morning Sun; feed cows with soaked chana dal and jaggery on Tuesdays.",
                "auspicious_colors": ["Bright Gold", "Ruby Red", "Saffron", "Crimson"],
                "auspicious_days": ["Sunday", "Tuesday"],
                "compatible_dates": [1, 10, 19, 28, 9, 18, 27, 5, 14],
                "challenging_dates": [8, 17, 26, 2]
            },
            "report_narrative": "Born on the 19th, you hold the royal vibration known as the Prince of Heaven. With Category A strength and 94% intrinsic potency, the fusion of Sun and Mars grants you supreme executive charisma and pioneering authority. Transmuting the karmic test of isolation into collaborative strength unlocks effortless global influence.",
            "charm_ai_dialogue": "You are a Day 19 soul—the Prince of Heaven! This is Category A Good Strength at 94% potency. You blend the radiant vision of the Sun with the fearless courage of Mars. You're designed to set trends, lead from the front, and win. Just remember: true sovereigns don't fight alone—build your army, trust your allies, and your reign will be timeless."
        },
        28: {
            "day": 28, "root": 1, "code": "28(c)", "tier": "c",
            "strength_category": "C", "strength_title": "Category C — Lower Strength (Tested Strategist / High Friction)",
            "strength_potency_score": 64,
            "planet": "Sun (Surya)", "is_karmic": False, "is_master": False,
            "archetype": "The Tested Strategist & Legal Architect",
            "classical_symbol": "The Dual Trial / Overcoming Opposition (Chaldean Canon)",
            "planetary_composition": "Moon (2) + Saturn (8) = 10 -> 1 (Water vs Cold Earth Clash)",
            "strength_value_breakdown": "Moon (Chandra) and Saturn (Shani) are natural astrological adversaries. Combining sensitive emotion (2) with rigid karmic discipline (8) to yield Sun (1) causes internal emotional-material friction, delayed success, and legal/trust disputes. Graded Category C (64% Direct Ease) requiring conscious remedial architecture.",
            "core_personality": "Deeply analytical, cautious, and resilient. You experience intense early challenges that forge an ironclad strategic intellect. You have acute financial sense but tend to view the world with skepticism.",
            "superpowers": ["Unbreakable crisis resilience", "Exceptional risk and forensic financial analysis", "Shrewd corporate legal acumen", "Endurance through prolonged adversity", "Mastery of operational systems"],
            "shadow_vulnerabilities": ["Cynicism and trust issues", "Inner emotional anxiety under stress", "Vulnerability to partner deception or legal disputes", "Tendency to isolate emotionally"],
            "career_and_wealth": "Corporate litigation, restructuring finance, real estate development, supply chain logistics, institutional auditing, and forensic risk governance.",
            "love_and_relationships": "Guarded heart that opens slowly. Prone to feeling misunderstood or carrying unequal burdens in relationships. Fiercely devoted once trust is permanently proven.",
            "remedial_blueprint": {
                "practical_growth_action": "Never enter verbal business partnerships—mandate independent legal contracts for every financial agreement; cultivate emotional vulnerability with safe loved ones.",
                "universal_secular_remedy": "Wear a dual-tone silver and gold/brass metallic watch; practice earthing (barefoot grass walking) weekly; avoid all-black clothing in major negotiations.",
                "traditional_vedic_remedy": "Water a Peepal tree on Saturdays; donate mustard oil or black sesame to laborers; wear a silver ring on the little finger to calm lunar anxiety.",
                "auspicious_colors": ["Pearl White", "Muted Gold", "Steel Blue", "Cream"],
                "auspicious_days": ["Monday", "Sunday"],
                "compatible_dates": [1, 10, 12, 21, 5, 23],
                "challenging_dates": [8, 17, 26, 4, 13, 22]
            },
            "report_narrative": "Born on the 28th, you are a battle-tested master builder. While the compound of Moon and Saturn brings early struggle and trust lessons, it shapes you into an exceptional strategist. Your success matures steadily through patient discipline and meticulous legal-financial frameworks.",
            "charm_ai_dialogue": "Born on the 28th, you carry Category C tested strength. Moon (2) and Saturn (8) merge into Sun (1)—a path of deep grit and resilience. Early hurdles and trust tests are your training ground. When you formalize contracts, protect your emotional boundaries, and honor patience, your financial and executive structures become unshakeable."
        },
        2: {
            "day": 2, "root": 2, "code": "2(b)", "tier": "b",
            "strength_category": "B", "strength_title": "Category B — Normal Strength (Balanced Intuition)",
            "strength_potency_score": 75,
            "planet": "Moon (Chandra)", "is_karmic": False, "is_master": False,
            "archetype": "The Empathetic Diplomat & Intuitive Harmonizer",
            "classical_symbol": "The Silver Crescent / High Priestess Mirror",
            "planetary_composition": "Pure Moon (Chandra) Energy",
            "strength_value_breakdown": "Pure single-digit lunar energy brings high sensitivity, artistic imagination, and diplomatic empathy. Graded Category B (Normal Strength) because emotional equilibrium depends heavily on the surrounding environment and requires grounding against mood swings.",
            "core_personality": "Gentle, imaginative, peacemaking, and perceptive. You sense what others feel before they speak. You excel as a partner, mediator, and creative conduit.",
            "superpowers": ["Intuitive emotional reading", "Master dispute mediation", "Subtle artistic elegance", "Collaborative team cohesion", "Deep listening and empathy"],
            "shadow_vulnerabilities": ["Hypersensitivity to harsh words", "Indecisiveness and over-analyzing", "Moody withdrawal under pressure", "Tendency to play the martyr"],
            "career_and_wealth": "Diplomacy, psychology, human resources, interior aesthetics, nursing/healthcare, counseling, and culinary arts.",
            "love_and_relationships": "Deeply romantic, nurturing, and devoted. Thrives in an environment of gentle, steady emotional validation; wounded deeply by cold criticism.",
            "remedial_blueprint": {
                "practical_growth_action": "Set firm conversational boundaries; don't take on colleagues' emotional problems as your own; make decisions within 24 hours to cure hesitation.",
                "universal_secular_remedy": "Drink water from a silver cup; keep a clear quartz crystal on your nightstand; listen to 432 Hz frequency before sleep.",
                "traditional_vedic_remedy": "Chandra Beej Mantra (Om Som Somaya Namaha) on Mondays; donate white rice, milk, or sugar to mothers or poor women; respect your mother.",
                "auspicious_colors": ["Pearl White", "Silver", "Cream", "Sea Green"],
                "auspicious_days": ["Monday", "Sunday"],
                "compatible_dates": [2, 11, 20, 1, 10, 3, 5],
                "challenging_dates": [4, 8, 9, 29]
            },
            "report_narrative": "Born on the 2nd, your soul is governed by the gentle illumination of the Moon. You possess remarkable emotional intelligence and a natural gift for diplomacy. Your greatest success blossoms through creative partnerships and intuitive advisory roles.",
            "charm_ai_dialogue": "You are a Day 2 soul—ruled by the Moon! With Category B strength, your intuition and emotional intelligence are your greatest assets. You bring harmony and gentle brilliance everywhere you go. Protect your sensitive heart with firm boundaries and let your intuitive wisdom guide your decisions."
        },
        11: {
            "day": 11, "root": 2, "code": "11(a)", "tier": "a",
            "strength_category": "A", "strength_title": "Category A — Good Strength (Master Number 11 / The Illuminator)",
            "strength_potency_score": 92,
            "planet": "Moon (Chandra)", "is_karmic": False, "is_master": True,
            "archetype": "The Spiritual Illuminator & Visionary Conduit",
            "classical_symbol": "The Illuminator / The Double Pillar (11)",
            "planetary_composition": "Sun (1) + Sun (1) = Double Solar Intensity channeled through Lunar Intuition (2)",
            "strength_value_breakdown": "Two 1s generate double solar intensity funneling through the intuitive lunar receiver. Rated Category A (Good Strength / 92% Potency) due to visionary foresight and magnetic spiritual inspiration. Must ground nervous tension to prevent mental overload.",
            "core_personality": "A visionary conduit between the seen and unseen. You experience flashes of uncanny insight, prophetic dreams, and intense aesthetic sensitivity. You hold yourself to exacting ideals.",
            "superpowers": ["Visionary prophetic insight", "Charismatic spiritual leadership", "Original artistic inspiration", "Transformational healing presence", "High-frequency pattern recognition"],
            "shadow_vulnerabilities": ["Nervous anxiety and insomnia", "Acute self-doubt and imposter syndrome", "Extreme perfectionism", "Feeling misunderstood by mainstream society"],
            "career_and_wealth": "Spiritual teaching, advanced neuroscience, cutting-edge AI philosophy, architectural design, inspirational media, and high-level psychotherapy.",
            "love_and_relationships": "Seeks an authentic soul connection. Requires emotional depth and spiritual alignment; shallow interactions leave you exhausted.",
            "remedial_blueprint": {
                "practical_growth_action": "Ground high psychic energy through daily physical exercise; write down creative inspirations immediately; release perfectionism.",
                "universal_secular_remedy": "Daily barefoot walking on earth; wear natural rudraksha or white quartz crystal bracelet; practice 4-7-8 breathing.",
                "traditional_vedic_remedy": "Meditate on Lord Shiva or divine light; wear a genuine Pearl or Moonstone in silver on little finger on Monday evening; chant Om Namah Shivaya.",
                "auspicious_colors": ["Luminous White", "Silver", "Pale Yellow", "Lavender"],
                "auspicious_days": ["Monday", "Thursday"],
                "compatible_dates": [1, 2, 7, 11, 20, 25, 29],
                "challenging_dates": [4, 8, 9, 26]
            },
            "report_narrative": "Born on the 11th, you embody Master Number 11—The Illuminator. Your life operates at a higher spiritual voltage, blending double solar power with profound lunar intuition. When you ground your nervous energy into practical projects, your insights transform entire communities.",
            "charm_ai_dialogue": "Day 11 is Master Number 11—The Spiritual Illuminator! Holding Category A strength at 92% potency, you are wired for prophetic vision and deep insight. Ground your high-frequency energy with daily mindfulness and physical discipline. Your voice has the power to inspire millions."
        },
        20: {
            "day": 20, "root": 2, "code": "20(b)", "tier": "b",
            "strength_category": "B", "strength_title": "Category B — Normal Strength (The Awakening)",
            "strength_potency_score": 76,
            "planet": "Moon (Chandra)", "is_karmic": False, "is_master": False,
            "archetype": "The Contemplative Sage & Awakening Spirit",
            "classical_symbol": "The Awakening / The Judgment Call (Cheiro Canon)",
            "planetary_composition": "Moon (2) + Cosmic Void (0) = Deep Lunar Receptivity",
            "strength_value_breakdown": "The cipher (0) deepens lunar introspection and spiritual reflection. Graded Category B (Normal Strength) because material manifestation requires overcoming initial hesitation and emotional indecision.",
            "core_personality": "Quietly observant, deeply peaceful, family-oriented, and patient. You possess profound emotional depth and are naturally drawn to music, philosophy, and spiritual service.",
            "superpowers": ["Deep contemplative calm", "Nurturing maternal/protective wisdom", "Psychological discernment", "Harmonious domestic governance", "Patient long-term loyalty"],
            "shadow_vulnerabilities": ["Procrastination and passive waiting", "Nostalgic attachment to past memories", "Fear of confrontation", "Tendency to suppress personal ambition"],
            "career_and_wealth": "Childhood education, healthcare counseling, archive curation, documentary photography, non-profit community leadership, and mediation.",
            "love_and_relationships": "Deeply loving and devoted. Prioritizes family peace above all. Needs a partner who provides stability and encourages outward self-expression.",
            "remedial_blueprint": {
                "practical_growth_action": "Set firm deadlines for personal goals; speak up immediately when boundaries are crossed; engage in public expressive hobbies.",
                "universal_secular_remedy": "Keep a silver fountain or water feature in the North sector of home; listen to calming ambient nature sounds; wear silver accents.",
                "traditional_vedic_remedy": "Feed birds with water and grains daily; offer white flowers at temple or sacred space on Mondays; wear silver ornament touching chest.",
                "auspicious_colors": ["Milky White", "Soft Silver", "Light Gray", "Aqua"],
                "auspicious_days": ["Monday", "Friday"],
                "compatible_dates": [2, 11, 20, 1, 5, 23],
                "challenging_dates": [4, 8, 9, 29]
            },
            "report_narrative": "Born on the 20th, your consciousness is attuned to the Awakening. The zero alongside the Moon deepens your contemplative and healing capacities. Your path unfolds gracefully when you pair your gentle wisdom with proactive worldly action.",
            "charm_ai_dialogue": "Day 20 brings you the gift of the Awakening! With Category B strength, you carry a soothing, peaceful aura that heals those around you. Trust your inner voice and don't hesitate to take bold practical steps in the material world. Your quiet strength is your secret weapon."
        },
        29: {
            "day": 29, "root": 2, "code": "29(c)", "tier": "c",
            "strength_category": "C", "strength_title": "Category C — Lower Strength (Mystic Ocean / Intense Friction)",
            "strength_potency_score": 62,
            "planet": "Moon (Chandra)", "is_karmic": False, "is_master": False,
            "archetype": "The Mystic Warrior & Emotional Alchemist",
            "classical_symbol": "The Stormy Sea / Emotional Crucible",
            "planetary_composition": "Moon (2) + Mars (9) = 11 -> 2 (Water + Fire Contradiction)",
            "strength_value_breakdown": "Moon (softness, water) and Mars (fire, aggression) are mutually contradictory forces when unchanneled. Categorized as Category C (Lower Strength / 62% Direct Ease) due to intense relationship turbulence, sudden mood polarities, and vulnerability to deceit. Requires conscious emotional mastery.",
            "core_personality": "Intensely passionate, intuitive, and complex. You feel everything at maximum intensity. You alternate between deep empathetic tenderness and fierce, volcanic defensiveness.",
            "superpowers": ["Fierce defense of underdogs", "Unmatched emotional grit", "Hypnotic charismatic intensity", "Deep psychic insight", "Transformational emotional alchemy"],
            "shadow_vulnerabilities": ["Severe emotional mood swings", "Suspiciousness and jealousy", "Sudden explosive outbursts", "Vulnerability to betrayal in close partnerships"],
            "career_and_wealth": "Crisis psychology, investigative journalism, maritime leadership, trauma surgery, high-stakes arbitration, and martial arts therapy.",
            "love_and_relationships": "Deeply intense and demanding. Prone to stormy, all-consuming attachments. Must consciously choose calm, emotionally grounded partners.",
            "remedial_blueprint": {
                "practical_growth_action": "Channel emotional turbulence into vigorous daily physical workouts; practice cooling breathing exercises (Sheetali pranayama); count to 10 before reacting in arguments.",
                "universal_secular_remedy": "Drink water from a silver vessel; stay away from overly spicy foods at night; swim or spend time near flowing water.",
                "traditional_vedic_remedy": "Worship Lord Shiva with milk abhishek on Mondays; recite Hanuman Chalisa on Tuesdays; wear a silver kada (bangle) on right wrist.",
                "auspicious_colors": ["White", "Silver", "Ice Blue", "Soft Pink"],
                "auspicious_days": ["Monday", "Tuesday"],
                "compatible_dates": [2, 11, 20, 1, 7, 25],
                "challenging_dates": [4, 8, 9, 18, 27]
            },
            "report_narrative": "Born on the 29th, you carry the dynamic polarity of Moon and Mars reducing to Master 11 and root 2. This creates an emotional crucible that tests your resilience. Once you master the fire within your water, you become an unstoppable emotional healer and protector.",
            "charm_ai_dialogue": "You are a Day 29 soul—the Mystic Ocean! With Category C strength, Moon and Mars create high emotional waves. You feel deeply and fight fiercely for what you love. Channel your intense passion into physical discipline and creative mastery to turn every wave into personal triumph."
        },
        3: {
            "day": 3, "root": 3, "code": "3(c)", "tier": "c",
            "strength_category": "C", "strength_title": "Category C — Lower Strength (Scattered Creative Energy)",
            "strength_potency_score": 68,
            "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
            "archetype": "The Joyful Creative & Expressive Philosopher",
            "classical_symbol": "The Golden Triad / Creative Spark",
            "planetary_composition": "Pure Jupiter (Guru / Brihaspati) Energy",
            "strength_value_breakdown": "Single-digit 3 carries high wisdom, creative imagination, and social optimism. Dr. Misra's taxonomy classifies pure single 3 as Category C (Lower Strength / 68% Ease) because without rigorous grounding, its expansive energy easily scatters into superficial pursuits, unfinished projects, and over-generosity.",
            "core_personality": "Witty, creative, optimistic, and articulate. You light up rooms with humor and intellectual curiosity. You love freedom and resist rigid constraints.",
            "superpowers": ["Infectious optimism and humor", "Brilliant verbal storytelling", "Creative conceptual design", "Natural counseling warmth", "Philosophical expansiveness"],
            "shadow_vulnerabilities": ["Scattering energy across too many goals", "Procrastination on detailed follow-through", "Superficiality when bored", "Financial carelessness through excessive optimism"],
            "career_and_wealth": "Content creation, media journalism, advertising creative direction, public speaking, coaching, and stage arts.",
            "love_and_relationships": "Playful, affectionate, and charming. Needs intellectual banter and freedom; suffocates in jealous or overly routine partnerships.",
            "remedial_blueprint": {
                "practical_growth_action": "Enforce a strict 'rule of one'—finish one major project completely before starting another; establish an automated monthly investment plan.",
                "universal_secular_remedy": "Keep yellow flowers or a citrine crystal on your study desk; listen to uplifting classical harmonies; wear yellow or saffron accents.",
                "traditional_vedic_remedy": "Apply saffron or turmeric tilak on throat and forehead on Thursdays; offer chana dal and jaggery to a cow; Guru Mantra (Om Brihaspataye Namaha).",
                "auspicious_colors": ["Yellow", "Saffron", "Golden Amber", "Light Orange"],
                "auspicious_days": ["Thursday", "Tuesday"],
                "compatible_dates": [3, 12, 21, 30, 1, 5, 9],
                "challenging_dates": [6, 15, 24]
            },
            "report_narrative": "Born on the 3rd, you are blessed with Jupiterian creativity and communicative flair. Your radiant optimism attracts opportunities effortlessly. By anchoring your brilliant imagination into daily disciplined habits, your ideas translate into lasting commercial and intellectual wealth.",
            "charm_ai_dialogue": "You are a Day 3 soul—full of Jupiterian warmth! Graded Category C, your creative imagination is immense, but your secret to victory is focus. Don't scatter your gold into ten buckets; master one craft, finish what you begin, and your voice will inspire the world."
        },
        12: {
            "day": 12, "root": 3, "code": "12(a)", "tier": "a",
            "strength_category": "A", "strength_title": "Category A — Good Strength (Noble Counselor & Diplomat)",
            "strength_potency_score": 91,
            "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
            "archetype": "The Enlightened Mentor & Cosmic Diplomat",
            "classical_symbol": "The Golden Sceptre / Harmonious Council (12)",
            "planetary_composition": "Sun (1) + Moon (2) = 3 (Jupiter Wisdom)",
            "strength_value_breakdown": "Sun (sovereign executive will) and Moon (public grace and diplomacy) merge to manifest Jupiter (divine counsel). Graded Category A (Good Strength / 91% Potency) due to magnetic articulation, broad social respect, and respected mentorship.",
            "core_personality": "Wise, dignified, articulate, and deeply ethical. You possess a natural gift for uniting opposing parties and guiding others toward their highest potential.",
            "superpowers": ["Magnetic articulation and teaching", "Diplomatic consensus building", "High ethical integrity", "Inspiring mentorship authority", "Creative intellectual balance"],
            "shadow_vulnerabilities": ["Carrying other people's burdens excessively", "Vulnerability to guilt or sacrifice complex", "Difficulty declining requests for aid", "Over-intellectualizing emotional pain"],
            "career_and_wealth": "Higher education leadership, judicial law, publishing, ambassadorial diplomacy, philanthropic foundations, and strategic executive coaching.",
            "love_and_relationships": "Noble, loving, and deeply supportive. Creates a harmonious, cultured home. Needs a partner who respects their ethical standards.",
            "remedial_blueprint": {
                "practical_growth_action": "Set healthy boundaries on pro-bono advice; ensure financial agreements are documented; take dedicated time for personal rest.",
                "universal_secular_remedy": "Wear a natural wood or rudraksha bracelet to ground your aura; keep an amethyst cluster on your desk.",
                "traditional_vedic_remedy": "Feed cows with soaked chana dal and bananas on Thursdays; respect elders and teachers; chant Om Gurave Namaha.",
                "auspicious_colors": ["Golden Yellow", "Royal Blue", "Saffron", "Cream"],
                "auspicious_days": ["Thursday", "Sunday"],
                "compatible_dates": [1, 2, 3, 12, 21, 9, 27],
                "challenging_dates": [6, 15, 24]
            },
            "report_narrative": "Born on the 12th, you embody the union of Sun and Moon resolving into Jupiter's wisdom. With Category A strength and 91% potency, your natural diplomacy and mentoring presence command immense respect. You turn sacrifice into purposeful leadership.",
            "charm_ai_dialogue": "Day 12 is a mark of nobility! Rated Category A Good Strength at 91% potency, Sun (1) and Moon (2) come together to empower your Jupiterian wisdom (3). You are a natural teacher, counselor, and leader. Guide others boldly, but always remember to keep your own boundaries secure."
        },
        21: {
            "day": 21, "root": 3, "code": "21(b)", "tier": "b",
            "strength_category": "B", "strength_title": "Category B — Normal Strength (The Crown of the Magi)",
            "strength_potency_score": 82,
            "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
            "archetype": "The Victorious Cosmopolitan & Crowned Achiever",
            "classical_symbol": "The Crown of the Magi / The Universe (Cheiro Canon)",
            "planetary_composition": "Moon (2) + Sun (1) = 3 (Jupiterian Elevation)",
            "strength_value_breakdown": "Moon intuition leads Sun initiative into Jupiterian achievement. Graded Category B (Normal Strength) because monumental success compounds progressively after persistent effort; confers late-blooming honor and global connections.",
            "core_personality": "Cosmopolitan, socially graceful, magnetic, and worldly. You attract support from influential people and possess a knack for international or cross-cultural success.",
            "superpowers": ["Global perspective and networking", "Graceful public communication", "Progressive career elevation", "Charming diplomatic presence", "Artistic and commercial versatility"],
            "shadow_vulnerabilities": ["Complacency after early milestones", "Over-optimism in commercial deals", "Susceptibility to flattering acquaintances", "Restless desire for constant acclaim"],
            "career_and_wealth": "International trade, travel and hospitality, media broadcasting, corporate communications, luxury public relations, and diplomatic affairs.",
            "love_and_relationships": "Charming, social, and affectionate. Seeks a worldly, cultured partner who enjoys social gatherings and cultural exploration.",
            "remedial_blueprint": {
                "practical_growth_action": "Reinvest early financial windfalls into long-term compounding assets; avoid casual lending to social acquaintances.",
                "universal_secular_remedy": "Keep a world map or globe in the North-West zone of your study; wear a yellow sapphire or citrine pendant in silver/gold.",
                "traditional_vedic_remedy": "Donate books or educational supplies to needy students on Thursdays; Guru Puja; wear light yellow or cream attire.",
                "auspicious_colors": ["Golden Yellow", "Turquoise", "Cream", "Emerald"],
                "auspicious_days": ["Thursday", "Monday"],
                "compatible_dates": [3, 12, 21, 30, 1, 5, 7],
                "challenging_dates": [6, 15, 24]
            },
            "report_narrative": "Born on the 21st, you carry the vibration of the Crown of the Magi. With Category B strength, your life trajectory resembles a steady mountain ascent. Each hurdle overcome elevates your reputation, culminating in broad public honor and international success.",
            "charm_ai_dialogue": "You are a Day 21 soul—blessed with the Crown of the Magi! With Category B strength, your intuitive grace and worldly charm open doors across cultures. Keep climbing steadily, invest your gains wisely, and you will wear your crown of success with honor."
        },
        30: {
            "day": 30, "root": 3, "code": "30(c)", "tier": "c",
            "strength_category": "C", "strength_title": "Category C — Lower Strength (Abstract Theorist / Aloof Mind)",
            "strength_potency_score": 66,
            "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
            "archetype": "The Solitary Philosopher & Abstract Theorist",
            "classical_symbol": "The Luminous Sage / The Silent Academy",
            "planetary_composition": "Jupiter (3) + Cosmic Void (0) = Philosophical Detachment",
            "strength_value_breakdown": "The cipher (0) magnifies intellectual contemplation and philosophical detachment. Graded Category C (66% Direct Material Ease) because worldly execution and financial monetization can be neglected in favor of abstract contemplation.",
            "core_personality": "Deeply reflective, mentally superior, independent, and intellectually uncompromising. You value knowledge above shallow material competition.",
            "superpowers": ["High-altitude philosophical vision", "Pedagogical genius in complex subjects", "Unbiased analytical detachment", "Creative original theories", "Deep meditative concentration"],
            "shadow_vulnerabilities": ["Commercial indifference and under-monetization", "Intellectual arrogance or aloofness", "Social withdrawal into theory", "Procrastination on routine practical duties"],
            "career_and_wealth": "University professorship, pure mathematics, theology, rare archive preservation, intellectual property strategy, and specialized editorial writing.",
            "love_and_relationships": "Requires deep mental communion before emotional warmth can ignite. Can appear aloof or detached; needs a partner who appreciates intellectual solitude.",
            "remedial_blueprint": {
                "practical_growth_action": "Ground theories into commercial deliverables with strict monetization milestones; engage in team discussions weekly.",
                "universal_secular_remedy": "Place a brass owl or globe in your library/office; practice daily walking in bustling markets to stay grounded.",
                "traditional_vedic_remedy": "Donate yellow lentils (chana dal) and saffron sweets at an educational or religious center on Thursdays; chant Gayatri Mantra.",
                "auspicious_colors": ["Bright Yellow", "Saffron", "Cream", "Sky Blue"],
                "auspicious_days": ["Thursday", "Tuesday"],
                "compatible_dates": [3, 12, 21, 1, 9],
                "challenging_dates": [6, 15, 24]
            },
            "report_narrative": "Born on the 30th, you possess an intellectual altitude that few can match. The cosmic zero elevates your Jupiterian mind into deep philosophical insight. By marrying your visionary concepts to practical commercial frameworks, your brilliance earns lasting worldly prosperity.",
            "charm_ai_dialogue": "Day 30 gives you a profound, philosophical mind! Graded Category C, the zero behind your 3 elevates your intellect to the stars. Your mission is to bring those lofty ideas down to earth—commercialize your knowledge, set practical targets, and turn your wisdom into lasting wealth."
        },
        4: {
            "day": 4, "root": 4, "code": "4(c)", "tier": "c",
            "strength_category": "C", "strength_title": "Category C — Lower Strength (Sudden Disruptions / High Friction)",
            "strength_potency_score": 64,
            "planet": "Rahu (North Node)", "is_karmic": False, "is_master": False,
            "archetype": "The Unconventional Architect & Disruptor",
            "classical_symbol": "The Lightning Bolt / Square of Opposition",
            "planetary_composition": "Pure Rahu Energy",
            "strength_value_breakdown": "Single-digit 4 is governed by Rahu. Prone to sudden disruptions, unexpected career reversals, stubborn friction with conservative authorities, and feeling misunderstood. Categorized as Category C (64% Ease) because material stability requires conscious patience and non-rebellious systems.",
            "core_personality": "Logical, methodical, unconventional, rebellious, and fiercely disciplined. You see structural flaws that others miss and build robust frameworks to fix them.",
            "superpowers": ["Disruptive technological innovation", "Complex system architecture", "Forensic investigative rigor", "Iron endurance under pressure", "Unconventional out-of-the-box strategy"],
            "shadow_vulnerabilities": ["Rebellious stubbornness", "Sudden impulsive temper flares", "Difficulty trusting established authorities", "Feeling perpetually alienated or isolated"],
            "career_and_wealth": "Software engineering, cybersecurity architecture, structural engineering, forensic accounting, alternative tech, and regulatory compliance.",
            "love_and_relationships": "Deeply loyal and protective, but slow to trust. Often struggles to express soft emotions; shows love through practical duty and problem-solving.",
            "remedial_blueprint": {
                "practical_growth_action": "Avoid sudden argumentative confrontations with supervisors; cultivate diplomatic phrasing; maintain a predictable daily routine.",
                "universal_secular_remedy": "Wear a natural wood or rudraksha bracelet to balance your Wood element; avoid all forms of speculative gambling; keep your workspace uncluttered.",
                "traditional_vedic_remedy": "Feed black dogs or street animals; donate blue blankets or mustard oil on Saturdays; Rahu Mantra (Om Raam Rahave Namaha); wear gomed (hessonite) only under expert astrological supervision.",
                "auspicious_colors": ["Smoky Blue", "Steel Gray", "Khaki", "Forest Green"],
                "auspicious_days": ["Saturday", "Sunday"],
                "compatible_dates": [1, 5, 6, 7],
                "challenging_dates": [2, 4, 8, 9, 13, 22]
            },
            "report_narrative": "Born on the 4th, your life is governed by Rahu's unconventional, structural genius. You are an architect of future systems. While sudden disruptions test your patience, your steadfast discipline transforms chaos into ironclad enterprise.",
            "charm_ai_dialogue": "You are a Day 4 soul—ruled by Rahu! With Category C strength, life tests you with sudden shifts and unconventional paths. You have the mind of a master engineer. Channel your rebellious streak into building flawless systems and you will outlast every competitor."
        },
        13: {
            "day": 13, "root": 4, "code": "13(d)", "tier": "d",
            "strength_category": "D", "strength_title": "Category D — Karmic Debt Transformation (The Phoenix Builder)",
            "strength_potency_score": 58,
            "planet": "Rahu (North Node)", "is_karmic": True, "is_master": False,
            "archetype": "The Phoenix Builder & Alchemical Transformer",
            "classical_symbol": "The Skeleton Transmuted / Phoenix from the Ashes (13)",
            "planetary_composition": "Sun (1) + Jupiter (3) = 4 (Rahu Karmic Debt 13)",
            "strength_value_breakdown": "Karmic Debt Number 13 carries the soul lesson of discipline, accountability, and persistent labor without shortcuts. Categorized as Category D (58% Initial Ease leaping to 92% Post-Mastery). Tests the individual with heavy early obstacles; once meticulous craftsmanship is embraced, they become unbeatable empire builders.",
            "core_personality": "Intensely resilient, serious, disciplined, and transformative. You have lived through crucibles that would break ordinary people. You possess an iron will and zero tolerance for superficial excuses.",
            "superpowers": ["Monumental crisis perseverance", "Rebuilding empires from ruins", "Relentless work ethic post-awakening", "High structural and organizational mastery", "Unshakeable honesty under pressure"],
            "shadow_vulnerabilities": ["Chronic frustration with delayed rewards", "Temptation to take risky shortcuts when exhausted", "Severe burnout and physical fatigue", "Bitter resentment toward peers who advance effortlessly"],
            "career_and_wealth": "Heavy infrastructure, corporate turnaround restructuring, mining/metallurgy, forensic litigation, high-risk industrial safety, and deep research.",
            "love_and_relationships": "Demands absolute fidelity and dependability. Disdains superficial pretense. Values practical acts of service and enduring loyalty over flowery romance.",
            "remedial_blueprint": {
                "practical_growth_action": "Never take shortcuts in paperwork, taxes, or contracts; embrace daily structure; take mandatory rest days to prevent burnout.",
                "universal_secular_remedy": "Wear a 5-Mukhi Rudraksha bracelet on left wrist; listen to 528 Hz Solfeggio sound therapy; practice rigorous time-blocking.",
                "traditional_vedic_remedy": "Worship Lord Ganesha to remove obstacles (Sankat Nashan Stotra); feed street dogs daily; donate food to construction laborers on Saturdays.",
                "auspicious_colors": ["Earthy Brown", "Navy Blue", "Deep Green", "Gray"],
                "auspicious_days": ["Saturday", "Thursday"],
                "compatible_dates": [1, 5, 7, 10, 14, 23],
                "challenging_dates": [2, 4, 8, 9, 13, 18, 26]
            },
            "report_narrative": "Born on the 13th, you walk the sacred path of Karmic Debt 13—The Phoenix Builder. Your soul is assigned to transform heavy trials into unshakeable mastery. By rejecting shortcuts and committing to meticulous discipline, you rise from every trial to construct enduring legacies.",
            "charm_ai_dialogue": "You are a Day 13 soul—the Phoenix! Classified in Category D Karmic Debt, your journey is an intense crucible designed to forge an unbreakable leader. Every obstacle you face is burning away shortcuts. When you build with pure discipline, your success will stand for generations."
        },
        22: {
            "day": 22, "root": 4, "code": "22(a)", "tier": "a",
            "strength_category": "A", "strength_title": "Category A — Good Strength (Master Number 22 / Master Builder)",
            "strength_potency_score": 96,
            "planet": "Rahu (North Node)", "is_karmic": False, "is_master": True,
            "archetype": "The Sovereign Master Builder & Architect of Empires",
            "classical_symbol": "The Master Builder / The Golden Compass (22)",
            "planetary_composition": "Moon (2) + Moon (2) = 4 (Master Builder Vibration)",
            "strength_value_breakdown": "Master Number 22 fuses profound intuitive vision (double Moon) with practical physical manifestation (Rahu 4). Rated Category A (Good Strength / 96% Potency), representing supreme capacity to manifest monumental institutions, global systems, and legacy infrastructure.",
            "core_personality": "A visionary titan. You combine grand philosophical ideals with practical, common-sense execution. You think in decades and centuries, not weeks.",
            "superpowers": ["Monumental megaproject execution", "Intuitive systemic engineering", "Pragmatic visionary idealism", "Commanding leadership presence", "Lasting multi-generational legacy creation"],
            "shadow_vulnerabilities": ["Overwhelming anxiety from scale of ambitions", "Paralyzing fear of failure", "Severe workaholism neglecting personal health", "Authoritarian impatience with mundane human limitations"],
            "career_and_wealth": "Multinational conglomerate leadership, urban mega-infrastructure, international banking architecture, national policy frameworks, and transformative clean-tech.",
            "love_and_relationships": "Deeply loyal, steady, and protective. Seeks a visionary partner who offers an emotional sanctuary from massive professional burdens.",
            "remedial_blueprint": {
                "practical_growth_action": "Break gigantic vision into quarterly actionable milestones; take weekly nature retreats to discharge mental tension; celebrate small wins.",
                "universal_secular_remedy": "Wear a dual-tone metallic watch; place a solid brass pyramid in the South-East of your office; practice grounding meditation.",
                "traditional_vedic_remedy": "Worship Goddess Saraswati for balance of intellect; donate green vegetables or grains to charity; chant Rahu Stotra; wear sandalwood.",
                "auspicious_colors": ["Royal Navy Blue", "Emerald Green", "Earth Brown", "Gold"],
                "auspicious_days": ["Sunday", "Wednesday"],
                "compatible_dates": [1, 5, 6, 7, 10, 14, 23],
                "challenging_dates": [2, 4, 8, 9]
            },
            "report_narrative": "Born on the 22nd, you hold Master Number 22—The Master Builder. With Category A strength and 96% potency, you possess the rare ability to manifest grand visions into physical reality. Your destiny is to construct systems that serve humanity for generations.",
            "charm_ai_dialogue": "Day 22 is Master Number 22—The Master Builder! Holding Category A strength at 96% potency, you are equipped with the power to manifest monumental dreams. Don't let the scale of your vision overwhelm you. Build one brick at a time, and you will construct an empire."
        },
        31: {
            "day": 31, "root": 4, "code": "31(b)", "tier": "b",
            "strength_category": "B", "strength_title": "Category B — Normal Strength (The Focused Pioneer)",
            "strength_potency_score": 80,
            "planet": "Rahu (North Node)", "is_karmic": False, "is_master": False,
            "archetype": "The Meticulous Pioneer & Pragmatic Innovator",
            "classical_symbol": "The Focused Compass / Fortified Intellect",
            "planetary_composition": "Jupiter (3) + Sun (1) = 4 (Rahu)",
            "strength_value_breakdown": "Jupiter's wisdom (3) guides the Sun's executive will (1) into Rahu's structural focus (4). Graded Category B (Normal Strength) because success is achieved steadily through organized research, technical skill, and disciplined self-sufficiency.",
            "core_personality": "Methodical, determined, intellectually acute, and organized. You possess strong mental stamina and dislike relying on anyone else to complete your tasks.",
            "superpowers": ["Systematic project organization", "Independent intellectual stamina", "Deep analytical research", "Steadfast reliable execution", "Original technical problem-solving"],
            "shadow_vulnerabilities": ["Emotional reserve and aloofness", "Tendency toward isolation and stubbornness", "Difficulty expressing romantic affection", "Pessimism when plans deviate"],
            "career_and_wealth": "Scientific R&D, intellectual property law, financial auditing, system database administration, precision manufacturing, and corporate planning.",
            "love_and_relationships": "Slow to open up emotionally, but remarkably steadfast once committed. Needs a warm, communicative partner who understands their need for focus.",
            "remedial_blueprint": {
                "practical_growth_action": "Schedule deliberate social interaction weekly to counter isolation; express verbal appreciation to family and colleagues.",
                "universal_secular_remedy": "Keep a clear quartz or fluorite crystal on your desk; practice daily gratitude journaling; wear blue or green accents.",
                "traditional_vedic_remedy": "Donate yellow grains or bananas on Thursdays; recite Gayatri Mantra; feed birds daily in the morning.",
                "auspicious_colors": ["Electric Blue", "Golden Amber", "Olive Green", "Charcoal"],
                "auspicious_days": ["Thursday", "Sunday"],
                "compatible_dates": [1, 3, 5, 7, 10, 12, 23],
                "challenging_dates": [2, 4, 8, 9]
            },
            "report_narrative": "Born on the 31st, you combine the wisdom of Jupiter and the executive drive of the Sun into Rahu's structured discipline. With Category B strength, you advance steadily through methodical persistence and independent brilliance.",
            "charm_ai_dialogue": "You are a Day 31 soul—the Focused Pioneer! With Category B strength, you merge Jupiter's counsel and the Sun's fire into practical mastery. Your methodical persistence is your golden ticket. Stay connected with your circle, keep your heart open, and your efforts will bear massive fruit."
        },
        5: {
            "day": 5, "root": 5, "code": "5(c)", "tier": "c",
            "strength_category": "C", "strength_title": "Category C — Lower Strength (Restless Versatility / Dark Horse)",
            "strength_potency_score": 66,
            "planet": "Mercury (Budh)", "is_karmic": False, "is_master": False,
            "archetype": "The Free-Spirited Explorer & Restless Communicator",
            "classical_symbol": "The Winged Messenger / Quicksilver",
            "planetary_composition": "Pure Mercury (Budh) Energy",
            "strength_value_breakdown": "Single-digit 5 is adaptable, communicative, and versatile. In Dr. Misra's taxonomy, it is classified as Category C (Lower Strength / 66% Direct Ease) because unregulated versatility leads to laziness, procrastination, scattered ventures, and loss of momentum without a grounding anchor.",
            "core_personality": "Charming, adaptable, curious, entertaining, and fast-thinking. You crave adventure, commercial variety, and intellectual novelty.",
            "superpowers": ["Rapid commercial pattern recognition", "Effortless conversational charm", "Instant adaptability to change", "Speed of calculation and thought", "Versatile multi-tasking"],
            "shadow_vulnerabilities": ["Procrastination and sudden laziness", "Restless boredom with routine", "Inconsistent financial discipline", "Tendency to abandon projects midway"],
            "career_and_wealth": "Commercial brokerage, sales marketing, travel media, digital trading, public relations, event management, and networking.",
            "love_and_relationships": "Fun, witty, and engaging. Suffocates in clingy, predictable relationships; requires an intellectually exciting partner.",
            "remedial_blueprint": {
                "practical_growth_action": "Pick one core commercial pursuit and commit to it for 12 months minimum; maintain a daily financial ledger.",
                "universal_secular_remedy": "Wear a green aventurine or emerald pendant; keep a green indoor plant on your desk; practice mindful stillness for 10 minutes daily.",
                "traditional_vedic_remedy": "Budh Beej Mantra (Om Bum Budhaya Namaha) on Wednesdays; feed green fodder or spinach to cows; donate green moong dal.",
                "auspicious_colors": ["Emerald Green", "Mint", "Turquoise", "White"],
                "auspicious_days": ["Wednesday", "Friday"],
                "compatible_dates": [1, 2, 3, 5, 6, 14, 23],
                "challenging_dates": [None]  # Mercury has no direct natural enemies
            },
            "report_narrative": "Born on the 5th, your soul dances to the quicksilver rhythm of Mercury. Your adaptability and commercial wit are unmatched. By anchoring your restless energy to a singular goal, your versatile genius turns into massive worldly success.",
            "charm_ai_dialogue": "You are a Day 5 soul—the Winged Messenger! With Category C strength, you have brilliant wit and speed, but your challenge is restlessness. Anchor your curiosity to one major ambition, stay consistent through the quiet phases, and you will achieve remarkable commercial milestones."
        },
        14: {
            "day": 14, "root": 5, "code": "14(a)", "tier": "a",
            "strength_category": "A", "strength_title": "Category A — Good Strength (Karmic 14 / Commercial Alchemist)",
            "strength_potency_score": 92,
            "planet": "Mercury (Budh)", "is_karmic": True, "is_master": False,
            "archetype": "The Dynamic Dealmaker & Commercial Alchemist",
            "classical_symbol": "The Golden Caduceus / Market Master (14)",
            "planetary_composition": "Sun (1) + Rahu (4) = 5 (Mercury Commercial Mastery)",
            "strength_value_breakdown": "Sun (executive authority) and Rahu (unconventional ambition) combine to turbocharge Mercury (commerce). Rated Category A (Good Strength / 92% Potency) due to sharp business acumen and commercial magnetism. Karmic 14 lesson: must maintain moderation and avoid speculative gambling.",
            "core_personality": "Dynamic, commercial, magnetic, persuasive, and sharp. You spot market trends before anyone else and thrive in fast-paced dealmaking.",
            "superpowers": ["High-stakes commercial magnetism", "Flawless negotiation genius", "Rapid financial pattern recognition", "Charismatic public persuasion", "Intuitive speculative agility"],
            "shadow_vulnerabilities": ["Temptation toward speculative gambling", "Restlessness and sensory overindulgence", "Impatience with slow administrative processes", "Tendency to take reckless risks"],
            "career_and_wealth": "Fintech entrepreneurship, venture capital, high-volume import/export, mergers & acquisitions, media brokerage, and real estate dealmaking.",
            "love_and_relationships": "Exciting, magnetic, and generous. Needs a modern, confident partner who enjoys an active lifestyle.",
            "remedial_blueprint": {
                "practical_growth_action": "Never speculate with money you cannot afford to lose; cultivate emotional moderation; maintain a strict savings allocation.",
                "universal_secular_remedy": "Wear a green tourmaline or peridot ring in silver/gold; practice breath-hold meditation to steady nervous energy.",
                "traditional_vedic_remedy": "Feed green vegetables to cows on Wednesdays; worship Lord Vishnu with Vishnu Sahasranama; donate green cloth to students.",
                "auspicious_colors": ["Emerald Green", "Bright Gold", "Teal", "White"],
                "auspicious_days": ["Wednesday", "Sunday"],
                "compatible_dates": [1, 5, 14, 23, 6, 15, 24],
                "challenging_dates": [8, 17, 26]
            },
            "report_narrative": "Born on the 14th, you carry Karmic Debt 14—The Commercial Alchemist. With Category A strength and 92% potency, your business instincts are razor-sharp. Mastering personal moderation and ethical discipline elevates your wealth into an enduring empire.",
            "charm_ai_dialogue": "Day 14 is a powerhouse of commerce! Holding Category A strength at 92% potency, Sun (1) and Rahu (4) fuse into Mercury's gold (5). You have an uncanny instinct for wealth and dealmaking. Guard against reckless speculation, stay disciplined, and your financial growth will be meteoric."
        },
        23: {
            "day": 23, "root": 5, "code": "23(b)", "tier": "b",
            "strength_category": "B", "strength_title": "Category B — Normal Strength (Royal Star of the Lion)",
            "strength_potency_score": 86,
            "planet": "Mercury (Budh)", "is_karmic": False, "is_master": False,
            "archetype": "The Royal Star of the Lion & Favored Diplomat",
            "classical_symbol": "The Royal Star of the Lion (Cheiro Canon)",
            "planetary_composition": "Moon (2) + Jupiter (3) = 5 (Mercurial Diplomacy)",
            "strength_value_breakdown": "Moon intuition and Jupiter wisdom fuse into brilliant Mercurial charm. Graded Category B (Normal Strength / 86% Potency) because it enjoys consistent divine protection, royal favor from superiors, and steady social popularity across all undertakings.",
            "core_personality": "Charming, diplomatic, popular, articulate, and fortunate. You attract assistance from influential mentors effortlessly and resolve disputes with a smile.",
            "superpowers": ["Magnetic personal charm", "Favor and patronage from superiors", "Effortless verbal persuasion", "Gift for peace and mediation", "Natural good fortune in social connections"],
            "shadow_vulnerabilities": ["Complacency due to easy luck", "Avoiding tough confrontations", "Over-reliance on charisma over deep research", "Taking friends for granted"],
            "career_and_wealth": "Corporate diplomacy, brand ambassadorship, international banking, luxury marketing, executive talent acquisition, and public governance.",
            "love_and_relationships": "Harmonious, romantic, and socially admired. Builds a warm, welcoming home filled with laughter and mutual respect.",
            "remedial_blueprint": {
                "practical_growth_action": "Back your natural charisma with rigorous technical preparation; mentor someone less privileged to balance your fortune.",
                "universal_secular_remedy": "Wear a dual-tone watch or clear quartz crystal; keep a brass lion figurine in the North sector of your home.",
                "traditional_vedic_remedy": "Worship Lord Vishnu or Laxmi-Narayana; wear a green emerald on little finger; donate yellow fruits on Thursdays.",
                "auspicious_colors": ["Light Green", "Gold", "Cream", "Sky Blue"],
                "auspicious_days": ["Wednesday", "Thursday"],
                "compatible_dates": [1, 2, 3, 5, 6, 14, 23],
                "challenging_dates": [None]
            },
            "report_narrative": "Born on the 23rd, you are blessed by the Royal Star of the Lion. With Category B strength and 86% potency, your life carries a golden touch. Mentors and patrons naturally step forward to support your path, elevating you into honored leadership.",
            "charm_ai_dialogue": "You are a Day 23 soul—blessed by the Royal Star of the Lion! With Category B strength, you hold the charm of the Moon, the wisdom of Jupiter, and the wit of Mercury. Doors open for you where others find walls. Stay humble, prepare thoroughly, and enjoy your royal favor."
        },
        6: {
            "day": 6, "root": 6, "code": "6(b)", "tier": "b",
            "strength_category": "B", "strength_title": "Category B — Normal Strength (Venusian Harmony)",
            "strength_potency_score": 79,
            "planet": "Venus (Shukra)", "is_karmic": False, "is_master": False,
            "archetype": "The Harmonizer & Aesthetic Protector",
            "classical_symbol": "The Mirror of Venus / The Sacred Hearth",
            "planetary_composition": "Pure Venus (Shukra) Energy",
            "strength_value_breakdown": "Pure single-digit Venus brings love of family, elegance, luxury, and artistic beauty. Graded Category B (Normal Strength) because life progresses steadily, though emotional over-protectiveness and susceptibility to flattery require conscious management.",
            "core_personality": "Affectionate, artistic, family-devoted, responsible, and graceful. You seek peace, beautiful surroundings, and harmonious relationships.",
            "superpowers": ["Aesthetic harmony and interior grace", "Deep domestic loyalty and protection", "Empathetic community counseling", "Refined artistic taste", "Diplomatic charm"],
            "shadow_vulnerabilities": ["Over-protectiveness suffocating loved ones", "Susceptibility to sweet flattery", "Difficulty establishing boundaries", "Obstinate stubbornness when challenged"],
            "career_and_wealth": "Interior architecture, luxury hospitality, fashion aesthetics, family law, counseling, fine culinary arts, and high-end retail.",
            "love_and_relationships": "Deeply loving, romantic, and devoted. The family home is your sacred temple; thrives when love and appreciation are vocalized regularly.",
            "remedial_blueprint": {
                "practical_growth_action": "Allow loved ones the freedom to make their own mistakes; do not take on family conflicts as personal failures.",
                "universal_secular_remedy": "Wear a gold metallic watch or brass accessories; use natural rose or sandalwood fragrance daily; keep spaces elegant and clean.",
                "traditional_vedic_remedy": "Shukra Beej Mantra (Om Shum Shukraya Namaha) on Fridays; donate white sweets or curd to needy girls; wear white zircon or diamond.",
                "auspicious_colors": ["White", "Silver", "Pastel Pink", "Sky Blue"],
                "auspicious_days": ["Friday", "Tuesday"],
                "compatible_dates": [6, 15, 24, 5, 14, 23, 1],
                "challenging_dates": [3, 12, 21, 30]  # Venus vs Jupiter (opposing Gurus)
            },
            "report_narrative": "Born on the 6th, your soul reflects Venusian grace and magnetic harmony. You are the emotional anchor of your circle. When you balance your generous care with healthy personal boundaries, your life blossoms into material abundance and deep relational fulfillment.",
            "charm_ai_dialogue": "You are a Day 6 soul—ruled by Venus! With Category B strength, you bring beauty, love, and comfort wherever you go. Your home is your palace. Just remember to set gentle boundaries so you don't deplete your own reservoir of care. True luxury begins within."
        },
        15: {
            "day": 15, "root": 6, "code": "15(a)", "tier": "a",
            "strength_category": "A", "strength_title": "Category A — Good Strength (Magnetic Enchanter)",
            "strength_potency_score": 93,
            "planet": "Venus (Shukra)", "is_karmic": False, "is_master": False,
            "archetype": "The Magnetic Enchanter & High Charisma Icon",
            "classical_symbol": "The Star of Eloquence and Luxury (15)",
            "planetary_composition": "Sun (1) + Mercury (5) = 6 (Venusian Magnetic Glory)",
            "strength_value_breakdown": "Sun (radiance) and Mercury (wit) combine to energize Venus (luxury and beauty). Rated Category A (Good Strength / 93% Potency) due to hypnotic personal magnetism, artistic eloquence, commercial charm, and financial luxury attraction.",
            "core_personality": "Irresistibly magnetic, eloquent, glamorous, and persuasive. You have a natural gift for speech, media arts, and drawing wealth into your orbit.",
            "superpowers": ["Hypnotic interpersonal charisma", "Artistic eloquence and media presence", "Effortless luxury manifestation", "Commercial persuasiveness", "Diplomatic mastery"],
            "shadow_vulnerabilities": ["Temptation to use charm manipulatively", "Over-indulgence in sensory pleasures", "Vanity and ego attachments", "Impatience with unglamorous routine"],
            "career_and_wealth": "Entertainment industry, celebrity management, luxury brand marketing, cinematic arts, diplomatic ambassadorship, and high-end hospitality.",
            "love_and_relationships": "Passionate, romantic, and expressive. Attracts admirers effortlessly; needs a grounded, loyal partner who loves your authentic soul, not just your glamour.",
            "remedial_blueprint": {
                "practical_growth_action": "Use your persuasive gifts for selfless upliftment; maintain strict financial budgeting for luxury expenses; cultivate inner spiritual depth.",
                "universal_secular_remedy": "Wear a gold metallic watch; use natural non-alcoholic attar (rose/sandalwood); practice morning mirror affirmations.",
                "traditional_vedic_remedy": "Worship Goddess Lakshmi with Sri Suktam on Fridays; offer white flowers at temple; wear a diamond or high-grade white zircon in silver/platinum.",
                "auspicious_colors": ["Cream", "Diamond White", "Rose Gold", "Royal Blue"],
                "auspicious_days": ["Friday", "Sunday"],
                "compatible_dates": [1, 5, 6, 15, 24, 14, 23],
                "challenging_dates": [3, 12, 21, 8]
            },
            "report_narrative": "Born on the 15th, you carry the radiant vibration of the Magnetic Enchanter. With Category A strength and 93% potency, Sun and Mercury amplify your Venusian magnetism. You hold the rare gift of effortless persuasion and luxury manifestation.",
            "charm_ai_dialogue": "Day 15 is sheer magnetism! Holding Category A strength at 93% potency, the Sun's light (1) and Mercury's wit (5) merge into Venus's glory (6). You captivate rooms and attract abundance with ease. Ground your brilliance in integrity, and your influence will be legendary."
        },
        24: {
            "day": 24, "root": 6, "code": "24(c)", "tier": "c",
            "strength_category": "C", "strength_title": "Category C — Lower Strength (Sacrificial Guardian / Heavy Burdens)",
            "strength_potency_score": 67,
            "planet": "Venus (Shukra)", "is_karmic": False, "is_master": False,
            "archetype": "The Sacrificial Guardian & Sensitive Nurturer",
            "classical_symbol": "The Sheltered Haven / Heavy Emotional Hearth",
            "planetary_composition": "Moon (2) + Rahu (4) = 6 (Venusian Family Duty)",
            "strength_value_breakdown": "Moon (sensitivity) and Rahu (illusions, burdens) channel into Venus (family). Graded Category C (Lower Strength / 67% Ease) because natives frequently carry disproportionate family burdens, suffer emotional exploitation by relatives, and struggle with setting personal boundaries.",
            "core_personality": "Selfless, deeply nurturing, domestic, and dependable. You put everyone else's comfort before your own, often carrying family secrets or financial debts.",
            "superpowers": ["Unconditional caregiving and loyalty", "Culinary and hospitality mastery", "Domestic financial resilience", "Gentle empathetic counseling", "Unshakeable family devotion"],
            "shadow_vulnerabilities": ["Martyr complex and inability to say no", "Emotional exploitation by relatives", "Financial losses through blind trust in family", "Resentment from unreciprocated care"],
            "career_and_wealth": "Healthcare administration, culinary catering, residential real estate, child welfare, interior decoration, and social enterprise.",
            "love_and_relationships": "Deeply devoted, romantic, and faithful. Prone to over-giving; must select an appreciative partner who reciprocates affection equally.",
            "remedial_blueprint": {
                "practical_growth_action": "Practice saying 'no' to non-essential requests without guilt; establish independent personal savings; do not co-sign financial loans for relatives.",
                "universal_secular_remedy": "Drink water from a silver cup; wear a dual-tone metallic watch; place a small water fountain in the North-East zone of your living room.",
                "traditional_vedic_remedy": "Offer milk and white sweets to young girls on Fridays; chant Mahamrityunjaya Mantra for family protection; wear a pearl or opal in silver.",
                "auspicious_colors": ["Pastel Pink", "Pearl White", "Soft Peach", "Mint Green"],
                "auspicious_days": ["Friday", "Monday"],
                "compatible_dates": [6, 15, 24, 2, 5, 14],
                "challenging_dates": [3, 12, 21, 9]
            },
            "report_narrative": "Born on the 24th, you are a guardian of the heart. While Moon and Rahu channel deep emotional duties into your Venusian path, your capacity for care is immense. Learning to honor your own needs first allows your nurturing gifts to thrive without burnout.",
            "charm_ai_dialogue": "You are a Day 24 soul—the Sacrificial Guardian! With Category C strength, you pour your heart into caring for others. Your empathy is pure gold, but remember: you cannot pour from an empty cup. Guard your financial and emotional boundaries, and let others care for you too."
        },
        7: {
            "day": 7, "root": 7, "code": "7(c)", "tier": "c",
            "strength_category": "C", "strength_title": "Category C — Lower Strength (The Introspective Mystic)",
            "strength_potency_score": 65,
            "planet": "Ketu (South Node)", "is_karmic": False, "is_master": False,
            "archetype": "The Introspective Mystic & Solitary Researcher",
            "classical_symbol": "The Hidden Temple / Mystic Veil",
            "planetary_composition": "Pure Ketu Energy",
            "strength_value_breakdown": "Single-digit 7 is ruled by Ketu (body without head). Introspective, philosophical, occult-minded, and detached from materialistic games. Classified as Category C (65% Direct Ease) due to low confidence in aggressive commercial negotiations, introversion, and emotional isolation.",
            "core_personality": "Analytical, intuitive, philosophical, secretive, and truth-seeking. You see straight through deception and seek the deeper meaning behind existence.",
            "superpowers": ["Deep analytical research", "Psychic intuition and lie detection", "Esoteric and occult mastery", "Spiritual diagnosis and healing", "Forensic problem-solving"],
            "shadow_vulnerabilities": ["Social anxiety and aloofness", "Low confidence in aggressive business deals", "Cynical skepticism", "Emotional detachment hurting close relationships"],
            "career_and_wealth": "Scientific research, data analytics, astrology/occult consulting, cybersecurity forensics, spiritual philosophy, and clinical psychology.",
            "love_and_relationships": "Needs profound mental and spiritual communion. Superficial small talk repels you. Requires an understanding partner who honors your need for solitude.",
            "remedial_blueprint": {
                "practical_growth_action": "Avoid speculative partnerships or risky business investments; partner with grounded practical leaders for commercial execution.",
                "universal_secular_remedy": "Wear a silver metallic watch on your wrist; practice daily silence (Maun Vrat) for 30 minutes; keep a smoky quartz crystal on your desk.",
                "traditional_vedic_remedy": "Feed street dogs daily (especially black or multi-colored dogs); recite Ketu Beej Mantra (Om Kem Ketave Namaha); wear Cat's Eye (Lehsuniya) only under expert guidance.",
                "auspicious_colors": ["Silver", "Smoky Gray", "White", "Pale Yellow"],
                "auspicious_days": ["Thursday", "Tuesday"],
                "compatible_dates": [7, 16, 25, 1, 2, 4],
                "challenging_dates": [8, 9]
            },
            "report_narrative": "Born on the 7th, your soul belongs to Ketu's temple of wisdom. You are a truth-seeker and intuitive analyst. When you channel your deep intellect into specialized research or healing arts rather than speculative business, your authority becomes unmatched.",
            "charm_ai_dialogue": "You are a Day 7 soul—the Introspective Mystic! With Category C strength, Ketu grants you uncanny intuition and sharp investigative eyes. Avoid risky speculative business partnerships. Focus on research, consulting, or healing where your depth of insight makes you indispensable."
        },
        16: {
            "day": 16, "root": 7, "code": "16(a)", "tier": "a",
            "strength_category": "A", "strength_title": "Category A — Good Strength (Karmic 16 / Lightning Awakener)",
            "strength_potency_score": 91,
            "planet": "Ketu (South Node)", "is_karmic": True, "is_master": False,
            "archetype": "The Lightning Awakener & Healer of Truth",
            "classical_symbol": "The Shattered Citadel / Lightning Awakening (16)",
            "planetary_composition": "Sun (1) + Venus (6) = 7 (Ketu Spiritual Awakening)",
            "strength_value_breakdown": "Karmic Debt Number 16. The Sun (ego) and Venus (material attachment) are shattered by Ketu's lightning to forge the highest spiritual awakening and healing genius. Rated Category A (Good Strength / 91% Potency) because once false pride is dissolved, this native possesses immense occult healing and investigative powers.",
            "core_personality": "Profound, transformative, spiritually awakened, and resilient. You have experienced sudden awakenings that dismantled superficial illusions. You see into souls with uncanny clarity.",
            "superpowers": ["Transcendent spiritual awakening", "Occult healing and psychic diagnostic power", "Unmasking illusions and false pretenses", "Forensic scientific brilliance", "Emotional and spiritual rebirth"],
            "shadow_vulnerabilities": ["Sudden ego collapses and humbling experiences", "Cynicism toward material achievements", "Pride preceding sudden falls", "Fear of emotional intimacy"],
            "career_and_wealth": "Alternative medicine, trauma therapy, deep scientific innovation, spiritual authorship, forensic auditing, and crisis consulting.",
            "love_and_relationships": "Walks through intense karmic relationships that teach unconditional love and non-possessiveness. Deeply loyal once spiritual alignment is reached.",
            "remedial_blueprint": {
                "practical_growth_action": "Practice humility proactively; never boast about material wealth; study spiritual and philosophical classics daily.",
                "universal_secular_remedy": "Wear a natural silver chain watch; use 528 Hz sound therapy; keep an amethyst or selenite wand in your bedroom.",
                "traditional_vedic_remedy": "Worship Lord Shiva (Mahamrityunjaya Mantra); donate white blankets or food to hermits and monks; feed street dogs on Tuesdays.",
                "auspicious_colors": ["Silver Gray", "Electric White", "Purple", "Sky Blue"],
                "auspicious_days": ["Monday", "Thursday"],
                "compatible_dates": [1, 2, 7, 16, 25, 4],
                "challenging_dates": [8, 9, 18]
            },
            "report_narrative": "Born on the 16th, you walk the transformative path of Karmic Debt 16—The Lightning Awakener. With Category A strength and 91% potency, the dismantling of superficial ego clears the way for profound healing mastery. You become a beacon of truth for those in darkness.",
            "charm_ai_dialogue": "Day 16 is the Lightning Awakener! Classified Category A Good Strength at 91% potency, Sun (1) and Venus (6) yield Ketu's divine awakening (7). Life strips away pretenses so your true soul power can shine. You are a natural healer and researcher—trust your inner light."
        },
        25: {
            "day": 25, "root": 7, "code": "25(b)", "tier": "b",
            "strength_category": "B", "strength_title": "Category B — Normal Strength (The Sage Observer)",
            "strength_potency_score": 83,
            "planet": "Ketu (South Node)", "is_karmic": False, "is_master": False,
            "archetype": "The Sage Observer & Discernment Master",
            "classical_symbol": "The Keen Observer / The Alchemical Crucible (25)",
            "planetary_composition": "Moon (2) + Mercury (5) = 7 (Ketu Analytical Depth)",
            "strength_value_breakdown": "Moon (intuition) and Mercury (sharp commercial intellect) combine into Ketu (analytical depth). Graded Category B (Normal Strength / 83% Potency) because wisdom and wealth mature steadily through lived experience, keen observation, and foreign travels.",
            "core_personality": "Perceptive, shrewd, analytical, calm, and intellectually observant. You learn through quiet observation rather than trial-and-error.",
            "superpowers": ["Acute psychological observation", "Intellectual discernment and data analysis", "Success in foreign lands and cross-cultural trade", "Intuitive commercial foresight", "Calm composure under crisis"],
            "shadow_vulnerabilities": ["Over-analyzing simple feelings", "Cynical detachment and aloofness", "Secretiveness creating distance with partners", "Hesitation to take emotional leaps"],
            "career_and_wealth": "Foreign trade, market intelligence, quantitative analytics, investigative journalism, university research, and psychological profiling.",
            "love_and_relationships": "Thoughtful, observant, and dependable. Needs an emotionally secure, cultured partner who respects their quiet introspection.",
            "remedial_blueprint": {
                "practical_growth_action": "Share your observations openly with trusted colleagues; maintain an analytical journal; avoid bottling up feelings.",
                "universal_secular_remedy": "Wear a silver metallic watch; keep a green fluorite stone on your desk; spend time walking near natural lakes or rivers.",
                "traditional_vedic_remedy": "Feed fish with wheat flour balls on Wednesdays or Thursdays; chant Ketu Gayatri Mantra; wear pearl or cat's eye under guidance.",
                "auspicious_colors": ["Silver", "Sea Green", "Smoky White", "Light Blue"],
                "auspicious_days": ["Wednesday", "Monday"],
                "compatible_dates": [2, 5, 7, 16, 25, 1, 23],
                "challenging_dates": [8, 9]
            },
            "report_narrative": "Born on the 25th, you carry the acute discernment of the Sage Observer. With Category B strength, Moon and Mercury blend into Ketu's deep analytical vision. Success comes through foreign connections, data mastery, and patient observation.",
            "charm_ai_dialogue": "You are a Day 25 soul—the Sage Observer! With Category B strength, Moon (2) and Mercury (5) give you razor-sharp eyes and intuitive depth (7). You learn from everything you see. Trust your observations, explore foreign or specialized fields, and you will achieve profound success."
        },
        8: {
            "day": 8, "root": 8, "code": "8(a)", "tier": "a",
            "strength_category": "A", "strength_title": "Category A — Good Strength (Pure Saturnian Authority)",
            "strength_potency_score": 92,
            "planet": "Saturn (Shani)", "is_karmic": False, "is_master": False,
            "archetype": "The Karmic Sovereign & Master of Governance",
            "classical_symbol": "The Scales of Justice / The Infinite Loop (8)",
            "planetary_composition": "Pure Saturn (Shani) Energy",
            "strength_value_breakdown": "Pure Saturnian energy. Categorized as Category A (Good Strength / 92% Potency) because while early life demands laborious hard work and struggle, it confers unyielding stamina, mastery of law and finance, and massive institutional power in adulthood.",
            "core_personality": "Determined, stoic, disciplined, just, and unyielding. You understand karma, law, and compounding effort. You build structures meant to last decades.",
            "superpowers": ["Ironclad endurance and stamina", "Systemic financial and institutional governance", "Unshakeable commitment to justice", "Monumental compounding wealth building", "Steely composure in adversity"],
            "shadow_vulnerabilities": ["Stern, unapproachable demeanor", "Argumentative stubbornness", "Difficulty expressing emotional warmth", "Holding onto grievances and workaholism"],
            "career_and_wealth": "Judiciary and litigation, institutional investment banking, real estate governance, mining and heavy metallurgy, corporate regulatory compliance, and industrial manufacturing.",
            "love_and_relationships": "Deeply loyal, stable, and protective. Expresses love through enduring responsibility, practical security, and steadfast duty.",
            "remedial_blueprint": {
                "practical_growth_action": "Consciously smile and express warmth to family and subordinates; engage in regular physical stretching; don't let work consume your weekends.",
                "universal_secular_remedy": "Wear a white quartz crystal bracelet to cool internal heat; hydrate well; avoid pure black or harsh dark clothes in celebrations.",
                "traditional_vedic_remedy": "Light a mustard oil lamp under a Peepal tree on Saturday evenings; donate black umbrellas, footwear, or food to physical laborers; Shani Chalisa.",
                "auspicious_colors": ["Navy Blue", "Charcoal Gray", "Steel Blue", "Dark Olive"],
                "auspicious_days": ["Saturday", "Wednesday"],
                "compatible_dates": [3, 5, 6, 8, 17, 26, 14, 23],
                "challenging_dates": [1, 2, 4, 9, 10, 19, 28]  # Saturn vs Sun/Moon/Mars
            },
            "report_narrative": "Born on the 8th, you are governed by the sovereign justice of Saturn. With Category A strength and 92% potency, your life is an epic of endurance and mastery. Early laborious trials forge you into an institutional pillar, achieving massive compounding authority in maturity.",
            "charm_ai_dialogue": "You are a Day 8 soul—ruled by Saturn! Graded Category A Good Strength at 92% potency, your life is built on iron discipline. Early struggles are simply Saturn's boot camp. Stay righteous, keep compounding, and you will rise to commanding wealth and authority."
        },
        17: {
            "day": 17, "root": 8, "code": "17(b)", "tier": "b",
            "strength_category": "B", "strength_title": "Category B — Normal Strength (The Star of the Magi)",
            "strength_potency_score": 85,
            "planet": "Saturn (Shani)", "is_karmic": False, "is_master": False,
            "archetype": "The Star of the Magi & Immortal Strategist",
            "classical_symbol": "The Star of the Magi / Star of Venus (Cheiro Canon)",
            "planetary_composition": "Sun (1) + Ketu (7) = 8 (Saturnian Victory)",
            "strength_value_breakdown": "Sun (radiant will) and Ketu (spiritual detachment) resolve into Saturn (karmic victory). Graded Category B (Normal Strength / 85% Potency) because it promises lasting peace, financial authority, and enduring reputation after overcoming early trials.",
            "core_personality": "Resilient, strategic, spiritual, intellectually formidable, and ambitious. You combine high executive drive with philosophical detachment.",
            "superpowers": ["Visionary long-range strategy", "Immortal public reputation", "Shrewd macro-financial acumen", "Spiritual resilience over obstacles", "Victorious perseverance through trials"],
            "shadow_vulnerabilities": ["Feeling burdened by a solitary destiny", "Slow to open up emotionally", "Perfectionism creating high stress", "Tendency to isolate when challenged"],
            "career_and_wealth": "Macro-economics, judicial consulting, literary authorship, scientific research institutions, legacy wealth management, and strategic policy leadership.",
            "love_and_relationships": "Dignified, protective, and deeply dependable. Seeks a mature, intelligent partner who shares their life mission.",
            "remedial_blueprint": {
                "practical_growth_action": "Share your strategic vision with a trusted inner circle; allow yourself time for leisure and creative hobbies.",
                "universal_secular_remedy": "Wear a dual-tone metallic watch; carry an amethyst stone; practice evening contemplation.",
                "traditional_vedic_remedy": "Donate food and warm clothing to the elderly or disabled; chant Hanuman Chalisa or Shani Mantra; wear amethyst or blue sapphire under advice.",
                "auspicious_colors": ["Royal Navy", "Silver", "Charcoal", "Deep Indigo"],
                "auspicious_days": ["Saturday", "Sunday"],
                "compatible_dates": [1, 5, 6, 7, 17, 23, 25],
                "challenging_dates": [2, 4, 8, 9]
            },
            "report_narrative": "Born on the 17th, you walk under the blessing of the Star of the Magi. With Category B strength, Sun and Ketu elevate Saturn into enduring victory. After navigating early karmic tests, your name and achievements earn lasting renown.",
            "charm_ai_dialogue": "Day 17 is the Star of the Magi! With Category B strength, the Sun's light (1) and Ketu's depth (7) elevate Saturn (8) into victorious mastery. Early trials were simply paving your road to glory. Stay disciplined, and your legacy will shine brightly."
        },
        26: {
            "day": 26, "root": 8, "code": "26(c)", "tier": "c",
            "strength_category": "C", "strength_title": "Category C — Lower Strength (Partnership Crucible / Financial Friction)",
            "strength_potency_score": 63,
            "planet": "Saturn (Shani)", "is_karmic": False, "is_master": False,
            "archetype": "The Tested Steward & Partnership Crucible",
            "classical_symbol": "The Heavy Crucible of Love & Finance (26)",
            "planetary_composition": "Moon (2) + Venus (6) = 8 (Saturnian Duty)",
            "strength_value_breakdown": "Moon (emotions) and Venus (desire, love) collide with Saturn's strict karmic balance. Graded Category C (Lower Strength / 63% Ease) because natives face severe trials in business partnerships, financial contracts, and marital disputes, requiring strict caution.",
            "core_personality": "Warm, artistic, hardworking, family-devoted, and serious. You care deeply about financial security and family duty, but often feel taken for granted.",
            "superpowers": ["Heavy asset stewardship", "Artistic and material patience", "Managing complex family or estate finances", "Endurance through partnership trials", "Deep loyalty to duty"],
            "shadow_vulnerabilities": ["Financial losses through blind trust in partners", "Emotional exploitation by loved ones", "Vulnerability to contractual disputes", "Pessimism under prolonged stress"],
            "career_and_wealth": "Real estate asset management, luxury estate governance, family enterprise stewardship, commercial contract law, banking oversight, and hospitality.",
            "love_and_relationships": "Deeply romantic yet prone to disillusionment. Must strictly separate emotional love from financial and legal business partnerships.",
            "remedial_blueprint": {
                "practical_growth_action": "Never co-mingle personal relationships with joint business contracts without strict independent legal review; establish personal financial autonomy.",
                "universal_secular_remedy": "Drink water from a silver cup; wear a white quartz crystal bracelet; avoid all-black attire in social gatherings.",
                "traditional_vedic_remedy": "Donate black sesame seeds and milk to temple on Saturdays; feed cows with green grass on Fridays; chant Om Namah Shivaya.",
                "auspicious_colors": ["Silver Gray", "Cream", "Steel Blue", "Pastel Violet"],
                "auspicious_days": ["Friday", "Saturday"],
                "compatible_dates": [3, 5, 6, 14, 23, 24],
                "challenging_dates": [1, 4, 8, 9, 18, 28]
            },
            "report_narrative": "Born on the 26th, your soul navigates the partnership crucible. Moon and Venus pour emotional and material devotion into Saturn's strict ledger. Success flourishes when you enforce firm legal and personal boundaries.",
            "charm_ai_dialogue": "You are a Day 26 soul—the Tested Steward! With Category C strength, Moon (2) and Venus (6) channel into Saturn (8). You have immense love and financial capability, but beware of blind trust in business partners. Protect your contracts, guard your boundaries, and your estate will thrive."
        },
        9: {
            "day": 9, "root": 9, "code": "9(a)", "tier": "a",
            "strength_category": "A", "strength_title": "Category A — Good Strength (Pure Martian Champion)",
            "strength_potency_score": 93,
            "planet": "Mars (Mangal)", "is_karmic": False, "is_master": False,
            "archetype": "The Fearless Warrior & Humanitarian Champion",
            "classical_symbol": "The Blazing Sword / Sovereign Shield (9)",
            "planetary_composition": "Pure Mars (Mangal) Energy",
            "strength_value_breakdown": "Pure Mars energy. Categorized as Category A (Good Strength / 93% Potency) due to fearless courage, rough-and-tough resilience, decisive executive action, and passionate defense of humanity.",
            "core_personality": "Courageous, rough-and-tough, energetic, hot-tempered, and deeply humanitarian. You fight fearlessly for the oppressed and lead from the front lines.",
            "superpowers": ["Decisive, fearless courage", "Heroic humanitarian advocacy", "Immense physical and mental stamina", "Crisis intervention leadership", "Unshakeable protective loyalty"],
            "shadow_vulnerabilities": ["Explosive temper and impatience", "Impulsive aggression when crossed", "Difficulty with gentle diplomacy", "Vulnerability to accidental physical injuries"],
            "career_and_wealth": "Defense and armed forces, emergency surgery, sports management, civil rights advocacy, heavy machinery engineering, and crisis leadership.",
            "love_and_relationships": "Passionate, protective, and ardent. Demands absolute loyalty; tempers fiery outbursts with genuine, warm devotion.",
            "remedial_blueprint": {
                "practical_growth_action": "Channel fiery physical energy into regular intense athletic workouts; practice taking three deep breaths before responding in anger.",
                "universal_secular_remedy": "Tie a red thread (mauli) on right wrist; apply red tilak (ashtagandha); do morning sun salutations; hydrate regularly.",
                "traditional_vedic_remedy": "Recite Hanuman Chalisa daily; offer red flowers or vermilion (sindoor) to Lord Hanuman on Tuesdays; wear red coral in copper only after consultation.",
                "auspicious_colors": ["Crimson Red", "Maroon", "Gold", "Warm Saffron"],
                "auspicious_days": ["Tuesday", "Sunday"],
                "compatible_dates": [1, 9, 10, 19, 27, 3, 5],
                "challenging_dates": [2, 4, 8, 18, 26]
            },
            "report_narrative": "Born on the 9th, you are crowned with the fearless flame of Mars. With Category A strength and 93% potency, you are a natural warrior and humanitarian protector. Directing your fiery energy toward noble causes elevates you into a legendary champion.",
            "charm_ai_dialogue": "You are a Day 9 soul—the Fearless Warrior! Holding Category A strength at 93% potency, you possess raw courage, fierce loyalty, and a champion's heart. Channel your fire into discipline and sports, protect the underdogs, and your leadership will be unstoppable."
        },
        18: {
            "day": 18, "root": 9, "code": "18(c)", "tier": "c",
            "strength_category": "C", "strength_title": "Category C — Lower Strength (Conflict of Light & Shadow)",
            "strength_potency_score": 61,
            "planet": "Mars (Mangal)", "is_karmic": False, "is_master": False,
            "archetype": "The Tested Commander & Karmic Warrior",
            "classical_symbol": "The Rayed Moon / Conflict of Light and Shadow (Cheiro Canon)",
            "planetary_composition": "Sun (1) + Saturn (8) = 9 (Mars Battle)",
            "strength_value_breakdown": "Sun (light, ego, father) and Saturn (shadow, restriction, karma) are arch-enemies, resolving into Mars (war). Categorized as Category C (61% Ease) due to bitter family/business feuds, deception from close associates, and intense internal friction.",
            "core_personality": "Battle-hardened, strategic, skeptical, resilient, and formidable. You have navigated fierce rivalries and understand the harsh realities of power.",
            "superpowers": ["Titanic crisis resilience", "Battle-hardened strategic acumen", "Mastery of hostile environments", "Fierce humanitarian loyalty", "Unyielding defense in conflict"],
            "shadow_vulnerabilities": ["Bitter quarrels and family feuds", "Deception by trusted associates", "Explosive defensive temper", "Deep-seated skepticism and cynicism"],
            "career_and_wealth": "Criminal litigation, corporate crisis management, defense strategy, industrial turnarounds, and high-conflict arbitration.",
            "love_and_relationships": "Complex and guarded. Needs an emotionally mature partner who offers peace and avoids engaging in petty power struggles.",
            "remedial_blueprint": {
                "practical_growth_action": "Avoid petty disputes and inheritance battles; practice forgiveness daily; surround yourself with calm, transparent advisors.",
                "universal_secular_remedy": "Drink water from a copper bottle; wear a white quartz crystal bracelet to cool internal heat; practice evening meditation.",
                "traditional_vedic_remedy": "Feed stray dogs on Tuesdays and Saturdays; worship Lord Hanuman and Lord Shiva; avoid wearing pure black and bright red together.",
                "auspicious_colors": ["Maroon", "Steel Gray", "Gold", "Navy Blue"],
                "auspicious_days": ["Tuesday", "Saturday"],
                "compatible_dates": [1, 3, 5, 9, 27],
                "challenging_dates": [2, 4, 8, 18, 28]
            },
            "report_narrative": "Born on the 18th, you navigate the sacred battle between Sun and Saturn resolving into Mars. With Category C strength, life tests your resilience through intense trials of strength. By choosing peace over pointless conflict, you become an unconquerable protector.",
            "charm_ai_dialogue": "Day 18 brings you the mantle of the Karmic Warrior. Graded Category C, Sun (1) and Saturn (8) clash into Mars (9), creating intense tests of strength. Rise above petty feuds, choose your battles with wisdom, and your battle-tested leadership will triumph."
        },
        27: {
            "day": 27, "root": 9, "code": "27(b)", "tier": "b",
            "strength_category": "B", "strength_title": "Category B — Normal Strength (The Sceptre of Command)",
            "strength_potency_score": 86,
            "planet": "Mars (Mangal)", "is_karmic": False, "is_master": False,
            "archetype": "The Sceptre of Command & Intuitive General",
            "classical_symbol": "The Sceptre of Command (Cheiro Canon)",
            "planetary_composition": "Moon (2) + Ketu (7) = 9 (Mars Wisdom & Command)",
            "strength_value_breakdown": "Moon (mind) and Ketu (spiritual insight) unite into Mars (command). Graded Category B (Normal Strength / 86% Potency) because it confers an intellectual sceptre of authority, brilliant strategic vision, and respected leadership that advances steadily through wisdom.",
            "core_personality": "Commanding, intuitive, noble, disciplined, and humanitarian. You blend warrior courage with spiritual insight, leading with quiet authority.",
            "superpowers": ["Executive command and authority", "Intuitive strategic foresight", "High mental clarity under pressure", "Protective humanitarian advocacy", "Dignified moral composure"],
            "shadow_vulnerabilities": ["Aloofness and emotional detachment", "Stubborn defense of opinions", "Sensitivity hidden behind a tough exterior", "Impatience with dishonesty"],
            "career_and_wealth": "High-level corporate strategy, defense intelligence, investigative surgery, international governance, publishing, and public policy.",
            "love_and_relationships": "Noble, protective, and deeply intuitive. Detects unspoken feelings instantly; requires an honest, dignified partner.",
            "remedial_blueprint": {
                "practical_growth_action": "Listen patiently to contrary perspectives; temper your command with gentle empathy; engage in charitable service.",
                "universal_secular_remedy": "Wear a silver metallic watch; keep a red jasper stone on your desk; practice swimming or water meditation.",
                "traditional_vedic_remedy": "Support charitable hospitals or animal shelters on Tuesdays; chant Hanuman Chalisa; wear a pearl and coral combination only under guidance.",
                "auspicious_colors": ["Crimson", "Silver", "Gold", "Royal Red"],
                "auspicious_days": ["Tuesday", "Monday"],
                "compatible_dates": [1, 2, 7, 9, 18, 27, 3, 5],
                "challenging_dates": [4, 8, 26]
            },
            "report_narrative": "Born on the 27th, you hold the Sceptre of Command. With Category B strength and 86% potency, Moon and Ketu endow Mars with visionary wisdom. You are an intuitive general whose authority stems from moral clarity and disciplined strategy.",
            "charm_ai_dialogue": "You are a Day 27 soul—holding the Sceptre of Command! With Category B strength, Moon (2) and Ketu (7) give Mars (9) visionary insight. You lead with dignity, courage, and intuition. Lead with compassion, and your authority will command universal respect."
        }
    }

print("Subdates dictionary compiled.")


def get_driver_conductor_81_data():
    """
    Authoritative 81 Driver-Conductor rules as taught by Dr. Numeros Vision Classical Methodology.
    Includes exact star rating (out of 5 stars or ? Warning), relationship type,
    positive traits, negative traits, career alignments, and warnings.
    """
    raw_specs = {
        # ?? DRIVER 1 (SUN / KING) ?????????????????????????????????????????????
        (1, 1): {
            "driver": 1, "conductor": 1, "driver_planet": "Sun (Surya)", "conductor_planet": "Sun (Surya)",
            "planet_combination": "Sun-Sun (King + King)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Strong Synergy)",
            "synergy_title": "1-1: Two Kings in Conjunction",
            "positive_traits": ["High executive power", "Natural commanding leadership", "Independent initiative", "Unshakable self-confidence"],
            "negative_traits": ["Ego clashes with peers", "Resistance to compromise", "Stubbornness", "Difficulty accepting second position"],
            "recommended_careers": ["Government Administration", "Public Policy", "Executive Directorship", "Political Leadership", "Entrepreneurship"],
            "warnings_and_cautions": "Dual king energy causes ego friction; one star is dropped due to mutual pride. Must cultivate active listening.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Two Kings: immense executive power and independent authority, but requires conscious humility to avoid ego deadlock."
        },
        (1, 2): {
            "driver": 1, "conductor": 2, "driver_planet": "Sun (Surya)", "conductor_planet": "Moon (Chandra)",
            "planet_combination": "Sun-Moon (King + Queen)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Royal Harmony)",
            "synergy_title": "1-2: King and Queen Harmonic Alliance",
            "positive_traits": ["Balanced authority and empathy", "Diplomatic charm", "High administrative intelligence", "Public popularity"],
            "negative_traits": ["Mood swings under stress", "Occasional emotional hesitation", "Over-concern with public perception"],
            "recommended_careers": ["Naval Defense & Maritime Leadership", "Armed Forces (Colonel/Captain)", "Water & Beverage Industries", "Public Diplomacy", "Civil Services"],
            "warnings_and_cautions": "Water and Fire balance naturally. Because 2 is water-linked, top positions in Navy, maritime, or water resources bring stellar success.",
            "harmonizing_poorak_number": 9,
            "fast_summary": "King and Queen: authority tempered by emotional intelligence; supreme aptitude for Navy, defense, and high public administration."
        },
        (1, 3): {
            "driver": 1, "conductor": 3, "driver_planet": "Sun (Surya)", "conductor_planet": "Jupiter (Guru)",
            "planet_combination": "Sun-Jupiter (King + Dev Guru)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Royal Wisdom)",
            "synergy_title": "1-3: King Guided by the Divine Counselor",
            "positive_traits": ["Moral authority", "Visionary wisdom", "High administrative ethics", "Natural counseling ability", "Respected leadership"],
            "negative_traits": ["Self-righteous dogmatism", "Impatience with corruption", "Tendency to preach without listening"],
            "recommended_careers": ["Judiciary & Corporate Law", "Higher Education Leadership", "Institutional Governance", "Spiritual Counseling", "Publishing"],
            "warnings_and_cautions": "A highly fortunate intellectual and ethical pairing. Avoid dogmatic intellectual arrogance.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "King and Dev Guru: wisdom meets command; exceptional for judiciary, higher education, and institutional directorship."
        },
        (1, 4): {
            "driver": 1, "conductor": 4, "driver_planet": "Sun (Surya)", "conductor_planet": "Rahu (North Node)",
            "planet_combination": "Sun-Rahu (King + Unconventional Architect)", "relationship_type": "Neutral",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Neutral Technical Synergy)",
            "synergy_title": "1-4: Sovereign Disruptor & Political Strategist",
            "positive_traits": ["Strategic political acumen", "Out-of-the-box system vision", "High technological focus", "Disruptive innovation"],
            "negative_traits": ["Sudden career ups and downs", "Friction with conservative authorities", "Secretiveness", "Impulsive decisions"],
            "recommended_careers": ["Politics & Government Liaison", "Cybersecurity Strategy", "IT Enterprise Leadership", "Structural Engineering", "Public Affairs"],
            "warnings_and_cautions": "Rahu creates sudden shifts; maintain strict adherence to legal and financial compliance to prevent sudden setbacks.",
            "harmonizing_poorak_number": 6,
            "fast_summary": "King and Rahu: bold political and technical strategist; excellent for government liaison, IT systems, and innovative enterprise."
        },
        (1, 5): {
            "driver": 1, "conductor": 5, "driver_planet": "Sun (Surya)", "conductor_planet": "Mercury (Budh)",
            "planet_combination": "Sun-Mercury (King + Prince / Budhaditya Yoga)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Commercial Sovereign)",
            "synergy_title": "1-5: The Budhaditya Sovereign & Commercial Master",
            "positive_traits": ["Supreme business acumen", "Rapid calculation and dealmaking", "Articulate executive communication", "Natural financial magnetism"],
            "negative_traits": ["Restless desire for constant expansion", "Impatience with routine operational details", "Over-committing"],
            "recommended_careers": ["Investment Banking", "Venture Capital", "Commercial Trading", "Fintech Enterprise", "Corporate Brokerage"],
            "warnings_and_cautions": "Forms a classical Budhaditya resonance. Thrives in business, banking, and commerce; keep routine operations grounded.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "King and Prince: supreme commercial instinct and negotiation power; highly favored for banking, trading, and massive business growth."
        },
        (1, 6): {
            "driver": 1, "conductor": 6, "driver_planet": "Sun (Surya)", "conductor_planet": "Venus (Shukra)",
            "planet_combination": "Sun-Venus (King + Daitya Guru / Luxury)", "relationship_type": "Neutral",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Diplomatic Luxury)",
            "synergy_title": "1-6: Sovereign of Luxury & Diplomatic Arts",
            "positive_traits": ["Refined public charisma", "High aesthetic taste", "Luxury lifestyle attraction", "Media and public presence"],
            "negative_traits": ["Extravagance in spending", "Ego clashes in romance", "Sensory distractions from core mission"],
            "recommended_careers": ["Luxury Brand Leadership", "Cinematic Arts & Entertainment", "Diplomatic Ambassadorship", "High-End Hospitality", "Cosmetic Real Estate"],
            "warnings_and_cautions": "Sun and Venus require balance between executive duty and luxury desires. Guard against lifestyle inflation.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "King and Daitya Guru: charismatic, luxurious, and media-savvy; excels in high-end brand leadership, cinema, and luxury enterprise."
        },
        (1, 7): {
            "driver": 1, "conductor": 7, "driver_planet": "Sun (Surya)", "conductor_planet": "Ketu (South Node)",
            "planet_combination": "Sun-Ketu (King + Mystic Researcher)", "relationship_type": "Neutral",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Mystic Advisory)",
            "synergy_title": "1-7: The Sovereign Researcher & Occult Master",
            "positive_traits": ["Deep research intelligence", "Occult and philosophical depth", "Intuitive truth-seeking", "Independent authority"],
            "negative_traits": ["Spiritual aloofness", "Lack of interest in mundane corporate games", "Feeling misunderstood", "Secretive nature"],
            "recommended_careers": ["Higher Academic Research", "Occult & Astrology Consultation", "Alternative Healing", "Deep Data Intelligence", "Spiritual Authorship"],
            "warnings_and_cautions": "Ketu is a body without a head, reducing raw material aggression. If native enters research, occult, or healing, results multiply exponentially.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "King and Ketu: profound researcher and occult healer; excels in higher education, esoteric consultation, and scientific analytics."
        },
        (1, 8): {
            "driver": 1, "conductor": 8, "driver_planet": "Sun (Surya)", "conductor_planet": "Saturn (Shani)",
            "planet_combination": "Sun-Saturn (Father + Estranged Son / Mutual Enemies)", "relationship_type": "Enemy",
            "star_rating": 0.5, "star_display": "? WARNING (Karmic Enemy / High Struggle)",
            "synergy_title": "1-8: The Sun-Saturn Karmic Crucible",
            "positive_traits": ["Titanic crisis stamina post-mastery", "Ironclad legal and administrative discipline", "Ability to rebuild after devastation"],
            "negative_traits": ["Severe career and financial struggle", "Sudden massive rise followed by abrupt losses", "Deep marriage discord or late marriage", "Father-son or authority conflicts"],
            "recommended_careers": ["Corporate Restructuring Law", "Labor Governance", "Mining & Metallurgy", "Forensic Auditing", "Heavy Construction"],
            "warnings_and_cautions": "CRITICAL LIFETIME WARNING: Sun and Saturn are astrological arch-enemies. Takes native high then drops abruptly. High struggle in marriage and partnerships. Mandatory remedies required.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Permanent Warning: Father and Son clash; intense career and marriage hurdles; requires continuous Panch Tattva hygiene and legal vigilance."
        },
        (1, 9): {
            "driver": 1, "conductor": 9, "driver_planet": "Sun (Surya)", "conductor_planet": "Mars (Mangal)",
            "planet_combination": "Sun-Mars (King + Senapati / Commander-in-Chief)", "relationship_type": "Friendly",
            "star_rating": 5.0, "star_display": "?????? (5/5 Stars ? Super Success / Crown Alliance)",
            "synergy_title": "1-9: Sovereign & Supreme Commander (Super Success)",
            "positive_traits": ["Unstoppable manifestation power", "Heroic courage", "Supreme administrative status", "Fearless execution", "Radiant public authority"],
            "negative_traits": ["Hot temper when provoked", "Impatient with slow pace", "High personal expectations causing stress"],
            "recommended_careers": ["Defense & Military Command", "Civil Police & IPS", "Top-Tier Administration (IAS)", "Surgical Medicine", "Disruptive Industrial Enterprise"],
            "warnings_and_cautions": "BEST COMBINATION IN NUMEROLOGY. Mars melts its ego before the King, delivering full 5-star super success across all endeavors.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Super Success: King and Commander-in-Chief; five out of five stars; supreme authority, courage, and unstoppable administrative victory."
        },

        # ?? DRIVER 2 (MOON / QUEEN) ???????????????????????????????????????????
        (2, 1): {
            "driver": 2, "conductor": 1, "driver_planet": "Moon (Chandra)", "conductor_planet": "Sun (Surya)",
            "planet_combination": "Moon-Sun (Queen Backed by King)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Harmonic Alignment)",
            "synergy_title": "2-1: The Intuitive Sovereign",
            "positive_traits": ["Diplomatic grace backed by power", "High public empathy", "Creative vision", "Support from influential patrons"],
            "negative_traits": ["Occasional hesitation before asserting command", "Mood shifts under heavy executive pressure"],
            "recommended_careers": ["Public Administration", "Arts & Cultural Diplomacy", "Hospitality Management", "Counseling Psychology", "Public Relations"],
            "warnings_and_cautions": "Queen holds steering but is backed by King's power; delivers steady success when native trusts their inner intuition.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Queen backed by King: intuitive grace supported by executive power; excellent for cultural diplomacy, public service, and counseling."
        },
        (2, 2): {
            "driver": 2, "conductor": 2, "driver_planet": "Moon (Chandra)", "conductor_planet": "Moon (Chandra)",
            "planet_combination": "Moon-Moon (Dual Queen)", "relationship_type": "Neutral",
            "star_rating": 2.5, "star_display": "?????? (2.5/5 Stars ? Dual Sensitivity)",
            "synergy_title": "2-2: Deep Sensitivity & Emotional Mirror",
            "positive_traits": ["Profound empathy", "High artistic intuition", "Gentle healing nature", "Caring domestic presence"],
            "negative_traits": ["Chronic indecision", "Hypersensitivity to criticism", "Vulnerability to emotional depression", "Fear of confrontation"],
            "recommended_careers": ["Creative Arts & Poetry", "Nursing & Pediatric Care", "Culinary Arts", "Interior Decorating", "Child Psychology"],
            "warnings_and_cautions": "Two Queens struggle to make hard decisions; requires a grounded partner and daily emotional grounding exercises.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Dual Moon: profound artistic empathy, but prone to chronic indecision and mood swings; needs structured daily anchors."
        },
        (2, 3): {
            "driver": 2, "conductor": 3, "driver_planet": "Moon (Chandra)", "conductor_planet": "Jupiter (Guru)",
            "planet_combination": "Moon-Jupiter (Queen + Dev Guru)", "relationship_type": "Friendly",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Wise Counselor)",
            "synergy_title": "2-3: Intuitive Wisdom & Graceful Guidance",
            "positive_traits": ["Warm teaching presence", "High moral empathy", "Creative imagination", "Philosophical optimism"],
            "negative_traits": ["Over-promising assistance", "Emotional exhaustion from helping others", "Difficulty charging fair commercial fees"],
            "recommended_careers": ["School & University Counseling", "Creative Writing & Literature", "Social Welfare Leadership", "Holistic Wellness", "Community Arts"],
            "warnings_and_cautions": "A gentle, nurturing vibration. Guard against financial exploitation by overly relying on trust.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Queen and Dev Guru: warm counseling and creative wisdom; highly suitable for education, counseling, and spiritual literature."
        },
        (2, 4): {
            "driver": 2, "conductor": 4, "driver_planet": "Moon (Chandra)", "conductor_planet": "Rahu (North Node)",
            "planet_combination": "Moon-Rahu (Eclipse Energy / Grahan Yoga)", "relationship_type": "Enemy",
            "star_rating": 1.5, "star_display": "? WARNING (Grahan Friction / Depression Risk)",
            "synergy_title": "2-4: The Eclipse Struggle & Emotional Crucible",
            "positive_traits": ["Unconventional artistic insight", "Deep interest in psychology", "Ability to perceive hidden realities"],
            "negative_traits": ["Vulnerability to severe depression and anxiety", "Chronic mental stress", "Over-thinking and restlessness", "Sudden emotional breakdowns"],
            "recommended_careers": ["Psychological Research", "Subconscious Behavioral Studies", "Alternative Arts", "Forensic Photography"],
            "warnings_and_cautions": "Forms classical Grahan (Eclipse) energy. Prone to anxiety and emotional depression. Regular meditation and silver water remedies mandatory.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Warning: Moon-Rahu eclipse friction; prone to depression, over-thinking, and mental stress; requires strict emotional grounding."
        },
        (2, 5): {
            "driver": 2, "conductor": 5, "driver_planet": "Moon (Chandra)", "conductor_planet": "Mercury (Budh)",
            "planet_combination": "Moon-Mercury (Queen + Prince)", "relationship_type": "Friendly",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Commercial Wit)",
            "synergy_title": "2-5: Intuitive Commerce & Public Communication",
            "positive_traits": ["Articulate persuasive speech", "Sharp commercial intuition", "Fast adaptability", "Sociable and engaging"],
            "negative_traits": ["Fickle decision-making", "Restlessness", "Difficulty focusing on long-term routine projects"],
            "recommended_careers": ["Commercial Banking", "Public Relations", "Media Reporting", "Dairy & Food Trading", "Event Management"],
            "warnings_and_cautions": "Queen and Prince form a friendly alliance. Good for commercial trading and communication when focus is sustained.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Queen and Prince: sharp communication and commercial instinct; excels in PR, media trading, and financial banking."
        },
        (2, 6): {
            "driver": 2, "conductor": 6, "driver_planet": "Moon (Chandra)", "conductor_planet": "Venus (Shukra)",
            "planet_combination": "Moon-Venus (Queen + Venus / Luxury Arts)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Luxurious Harmony)",
            "synergy_title": "2-6: The Sovereign of Beauty, Water & Luxury",
            "positive_traits": ["Exceptional aesthetic and culinary taste", "Natural luxury attraction", "Deep romantic warmth", "Hospitality genius"],
            "negative_traits": ["Over-indulgence in comfort", "Susceptibility to emotional heartbreak", "Financial over-spending on luxury"],
            "recommended_careers": ["Dairy, Water & Beverage Trade", "Luxury Hospitality & Resorts", "Cosmetics & Fine Perfumes", "Fashion Design", "Interior Decor"],
            "warnings_and_cautions": "Water (2) and Luxury (6) unite. Any profession linked to water, dairy, beverages, cosmetics, or luxury hospitality yields top success.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Queen and Venus: supreme artistic elegance; excels in water-linked businesses, dairy, cosmetics, hospitality, and luxury fashion."
        },
        (2, 7): {
            "driver": 2, "conductor": 7, "driver_planet": "Moon (Chandra)", "conductor_planet": "Ketu (South Node)",
            "planet_combination": "Moon-Ketu (Intuitive Water & Detachment)", "relationship_type": "Neutral",
            "star_rating": 2.5, "star_display": "?????? (2.5/5 Stars ? Mystic Intuition)",
            "synergy_title": "2-7: The Mystic Intuitive & Solitary Healer",
            "positive_traits": ["Uncanny psychic intuition", "Deep healing touch", "Philosophical contemplation", "Truth-seeking intellect"],
            "negative_traits": ["Emotional moodiness and withdrawal", "Low confidence in material transactions", "Feeling misunderstood"],
            "recommended_careers": ["Astrology & Tarot Consultation", "Spiritual Healing & Reiki", "Psychological Research", "Water Conservation", "Esoteric Writing"],
            "warnings_and_cautions": "Gentle, non-materialistic pairing. Avoid speculative business; focus on consultative, healing, and research roles.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Queen and Ketu: intense psychic intuition and healing talent; best suited for occult consultation, research, and holistic therapy."
        },
        (2, 8): {
            "driver": 2, "conductor": 8, "driver_planet": "Moon (Chandra)", "conductor_planet": "Saturn (Shani)",
            "planet_combination": "Moon-Saturn (Vish Yoga / Extreme Struggle)", "relationship_type": "Enemy",
            "star_rating": 1.0, "star_display": "? WARNING (Vish Yoga / Health & Delay)",
            "synergy_title": "2-8: The Vish Yoga Crucible",
            "positive_traits": ["Endurance through deep suffering", "Patience with elderly or chronically ill", "Realistic grounding post-mastery"],
            "negative_traits": ["Severe chronic delays and depression", "Health vulnerabilities (bones, joints, fluids)", "Prolonged struggle in career", "Cold relationship dynamics"],
            "recommended_careers": ["Geriatric Healthcare", "Palliative Care", "Historical Research", "Mining Safety", "Waste Water Management"],
            "warnings_and_cautions": "Forms classical Vish Yoga. Heavy struggle and health challenges. Never ignore mental health or joint issues; regular remedies essential.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Warning: Vish Yoga friction; brings health and emotional delays; requires persistent patience, white crystal remedies, and service to elders."
        },
        (2, 9): {
            "driver": 2, "conductor": 9, "driver_planet": "Moon (Chandra)", "conductor_planet": "Mars (Mangal)",
            "planet_combination": "Moon-Mars (Water vs Fire Clash)", "relationship_type": "Enemy",
            "star_rating": 1.5, "star_display": "? WARNING (Fire-Water Clash / Marital Friction)",
            "synergy_title": "2-9: The Stormy Passion & Marital Crucible",
            "positive_traits": ["Raw emotional drive", "Fierce protection of family", "High creative passion", "Resilience in adversity"],
            "negative_traits": ["Relationship and marital conflict", "Late marriage or emotional friction", "Impulsive temper conflicting with sensitivity"],
            "recommended_careers": ["Trauma Medicine & Nursing", "Crisis Response", "Culinary Arts with Fire/Baking", "Maritime Engineering"],
            "warnings_and_cautions": "Moon (water) and Mars (fire) clash emotionally. Causes marital friction and relationship volatility. Cultivate calm communication.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Warning: Water and Fire contradiction; causes late marriage or relationship friction; requires cooling mindfulness and emotional balance."
        },

        # ?? DRIVER 3 (JUPITER / DEV GURU) ?????????????????????????????????????
        (3, 1): {
            "driver": 3, "conductor": 1, "driver_planet": "Jupiter (Guru)", "conductor_planet": "Sun (Surya)",
            "planet_combination": "Jupiter-Sun (Dev Guru + King)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Sovereign Wisdom)",
            "synergy_title": "3-1: The Sovereign Sage & Supreme Mentor",
            "positive_traits": ["Commanding wisdom", "High administrative ethics", "Visionary mentorship", "Executive respect across institutions"],
            "negative_traits": ["Intellectual self-righteousness", "Impatience with corruption", "High expectations of peers"],
            "recommended_careers": ["Judiciary & Supreme Court Law", "University Chancellorship", "National Policy Making", "Religious Leadership", "Executive Advisory"],
            "warnings_and_cautions": "A noble, victorious combination. Especially powerful after age 40 when Jupiterian wisdom fully aligns with solar command.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Dev Guru backed by King: supreme intellectual authority and administrative respect; thrives in law, higher education, and policy leadership."
        },
        (3, 2): {
            "driver": 3, "conductor": 2, "driver_planet": "Jupiter (Guru)", "conductor_planet": "Moon (Chandra)",
            "planet_combination": "Jupiter-Moon (Dev Guru + Queen / Gajakesari Energy)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Gentle Sage)",
            "synergy_title": "3-2: The Gajakesari Harmonics & Peaceful Mentor",
            "positive_traits": ["Profound emotional wisdom", "Gentle counseling presence", "Creative literary genius", "Public respect and warmth"],
            "negative_traits": ["Over-generosity leading to personal depletion", "Hesitation in aggressive commercial battles"],
            "recommended_careers": ["Psychotherapy & Counseling", "Higher Educational Administration", "Literary Publishing", "Holistic Wellness", "Philanthropic Foundations"],
            "warnings_and_cautions": "Forms classical Gajakesari resonance. Excellent for peace, respect, and counseling; maintain commercial firmness.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Dev Guru and Queen: Gajakesari resonance; brings broad public affection, teaching grace, and deep psychological counseling wisdom."
        },
        (3, 3): {
            "driver": 3, "conductor": 3, "driver_planet": "Jupiter (Guru)", "conductor_planet": "Jupiter (Guru)",
            "planet_combination": "Jupiter-Jupiter (Dual Guru)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Pure Wisdom)",
            "synergy_title": "3-3: The Double Temple of Wisdom",
            "positive_traits": ["Immense philosophical knowledge", "Natural teaching authority", "High ethical stature", "Creative conceptual power"],
            "negative_traits": ["Dogmatism and intellectual stubbornness", "Preaching rather than acting", "Under-monetization of practical skills"],
            "recommended_careers": ["Academic Professorship", "Spiritual Authorship", "Theology & Philosophy", "Higher Judiciary", "Master Educational Coaching"],
            "warnings_and_cautions": "Deeply spiritual and intellectual. Ensure that lofty philosophical ideals are translated into grounded revenue streams.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Dual Jupiter: monumental knowledge and teaching authority; outstanding for professorship, spirituality, and legal jurisprudence."
        },
        (3, 4): {
            "driver": 3, "conductor": 4, "driver_planet": "Jupiter (Guru)", "conductor_planet": "Rahu (North Node)",
            "planet_combination": "Jupiter-Rahu (Guru-Chandal Tension / Innovative Knowledge)", "relationship_type": "Neutral",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Unconventional Knowledge)",
            "synergy_title": "3-4: The Unconventional Philosopher & Tech Theorist",
            "positive_traits": ["Disruptive intellectual models", "Ability to merge ancient wisdom with modern tech", "Sharp strategic analysis"],
            "negative_traits": ["Intellectual skepticism", "Sudden conflicts with conservative traditions", "Restlessness with routine academia"],
            "recommended_careers": ["AI Philosophy & Ethics", "Cybersecurity Strategy", "Intellectual Property Law", "Alternative Educational Tech", "Forensic Data Research"],
            "warnings_and_cautions": "Forms Guru-Chandal undertones. Channel into modern tech ethics or advanced research to avoid ideological conflicts.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Dev Guru and Rahu: bridges ancient wisdom with cutting-edge technology; excels in AI ethics, tech law, and innovative research."
        },
        (3, 5): {
            "driver": 3, "conductor": 5, "driver_planet": "Jupiter (Guru)", "conductor_planet": "Mercury (Budh)",
            "planet_combination": "Jupiter-Mercury (Dev Guru + Prince)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Commercial Wisdom)",
            "synergy_title": "3-5: The Strategic Economist & Corporate Advisor",
            "positive_traits": ["Brilliant commercial logic", "Strategic communication", "Fast deal structuring", "High financial intelligence"],
            "negative_traits": ["Restlessness to expand too fast", "Over-intellectualizing simple operational issues"],
            "recommended_careers": ["Corporate Financial Advisory", "Commercial Arbitration", "Wealth Management", "Economic Journalism", "Executive Consulting"],
            "warnings_and_cautions": "Blends wisdom with commercial speed. Highly successful in business, wealth management, and corporate strategy.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Dev Guru and Prince: wisdom meets mercantile speed; top-tier alignment for wealth management, corporate advisory, and economics."
        },
        (3, 6): {
            "driver": 3, "conductor": 6, "driver_planet": "Jupiter (Guru)", "conductor_planet": "Venus (Shukra)",
            "planet_combination": "Jupiter-Venus (Dev Guru vs Daitya Guru / 36 ka Aankda)", "relationship_type": "Enemy",
            "star_rating": 1.5, "star_display": "? WARNING (Opposing Gurus / Health & Marital Caution)",
            "synergy_title": "3-6: The Opposing Gurus Crucible (36 ka Aankda)",
            "positive_traits": ["High creative and aesthetic talent", "Sophisticated philosophical taste", "Charismatic speaking"],
            "negative_traits": ["Relationship and marital conflict", "Ego clashes in partnerships", "Health vulnerabilities (hormonal/digestive)", "Hypocrisy in personal versus public ethics"],
            "recommended_careers": ["Art History & Curatorial Research", "Creative Media Ethics", "Luxury Philosophy", "Fashion Journalism"],
            "warnings_and_cautions": "CRITICAL OPPOSING GURUS WARNING: Jupiter and Venus represent conflicting ideological masters (spiritual vs luxury). High risk of marital and health issues. Need careful Lo Shu balancing.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Warning: Opposing Gurus conflict; high potential for marital ego clashes and health vulnerabilities; requires mutual patience and Lo Shu remedies."
        },
        (3, 7): {
            "driver": 3, "conductor": 7, "driver_planet": "Jupiter (Guru)", "conductor_planet": "Ketu (South Node)",
            "planet_combination": "Jupiter-Ketu (Divine Spiritual Conjunction)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Spiritual Master)",
            "synergy_title": "3-7: The Divine Connection & Occult Healer",
            "positive_traits": ["Profound spiritual intuition", "Occult and esoteric mastery", "Natural teaching and coaching authority", "High research genius", "Divine inner connection"],
            "negative_traits": ["Detachment from mundane material wealth", "Impatience with superficial commercial games"],
            "recommended_careers": ["Occult & Vedic Astrology", "Spiritual Coaching & Teaching", "Higher Research & Philosophy", "Alternative Medicine & Healing", "Theological Authorship"],
            "warnings_and_cautions": "One of the most powerful spiritual pairings. Dr. Misra highlights 3-7 for education, occult, healing, research, and divine connection.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Dev Guru and Ketu: four out of five stars; supreme alignment for occult wisdom, spiritual coaching, healing, and higher research."
        },
        (3, 8): {
            "driver": 3, "conductor": 8, "driver_planet": "Jupiter (Guru)", "conductor_planet": "Saturn (Shani)",
            "planet_combination": "Jupiter-Saturn (Wisdom + Karmic Law)", "relationship_type": "Neutral",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Institutional Law)",
            "synergy_title": "3-8: The Judicial Pillar & Institutional Arbiter",
            "positive_traits": ["Steadfast legal discipline", "Long-term institutional governance", "High ethical stamina", "Compounding financial intellect"],
            "negative_traits": ["Overly serious or stern demeanor", "Slow initial career momentum", "Rigid adherence to doctrine"],
            "recommended_careers": ["Judiciary & Constitutional Law", "Institutional Regulatory Compliance", "Corporate Governance", "Estate Management", "Historical Academia"],
            "warnings_and_cautions": "Steady and disciplined. Progress is slow initially but leads to commanding judicial or institutional respect.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Dev Guru and Saturn: ethical wisdom meets karmic discipline; highly suited for judiciary, corporate governance, and institutional law."
        },
        (3, 9): {
            "driver": 3, "conductor": 9, "driver_planet": "Jupiter (Guru)", "conductor_planet": "Mars (Mangal)",
            "planet_combination": "Jupiter-Mars (Dev Guru + Senapati)", "relationship_type": "Friendly",
            "star_rating": 4.5, "star_display": "?????? (4.5/5 Stars ? Righteous Champion)",
            "synergy_title": "3-9: The Righteous Warrior & Medical Leader",
            "positive_traits": ["Commanding executive energy", "Fearless defense of truth", "High academic and physical discipline", "Inspiring administrative presence"],
            "negative_traits": ["Fierce indignation against injustice", "Impatience with administrative bureaucracy", "Hot temper when crossed"],
            "recommended_careers": ["Medical & Surgical Leadership", "Armed Forces Administration (Defense/IPS)", "University Directorship", "Civil Services", "Athletic Directorship"],
            "warnings_and_cautions": "Combines Jupiterian wisdom with Martian courage. Highly favored for top doctors, surgeons, army officers, and civil administrators.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Dev Guru and Mars: four and a half stars; righteous champion; supreme aptitude for top surgeons, military command, and civil administration."
        },

        # ?? DRIVER 4 (RAHU / UNCONVENTIONAL ARCHITECT) ????????????????????????
        (4, 1): {
            "driver": 4, "conductor": 1, "driver_planet": "Rahu (North Node)", "conductor_planet": "Sun (Surya)",
            "planet_combination": "Rahu-Sun (Disruptor Backed by Sovereign)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Political Power)",
            "synergy_title": "4-1: The Political Strategist & System Architect",
            "positive_traits": ["Acute political and tactical intellect", "Ability to forge government connections", "Unconventional system leadership", "Disruptive ambition"],
            "negative_traits": ["Sudden friction with superiors", "Tendency to push ethical boundaries", "Secretive power plays"],
            "recommended_careers": ["Political Strategy & Governance", "Government Liaison & Regulatory Affairs", "Cybersecurity Command", "Disruptive Tech Founder", "Infrastructure Logistics"],
            "warnings_and_cautions": "Dr. Misra highlights 4-1 for politicians, government officers, or leaders closely connected with political power.",
            "harmonizing_poorak_number": 6,
            "fast_summary": "Rahu backed by Sun: sharp political strategist; excels in government liaison, disruptive tech leadership, and infrastructure."
        },
        (4, 2): {
            "driver": 4, "conductor": 2, "driver_planet": "Rahu (North Node)", "conductor_planet": "Moon (Chandra)",
            "planet_combination": "Rahu-Moon (Eclipse Tension / Depression Risk)", "relationship_type": "Enemy",
            "star_rating": 1.5, "star_display": "? WARNING (Mental Stress / Depression Risk)",
            "synergy_title": "4-2: The Restless Mind & Eclipse Friction",
            "positive_traits": ["Psychological perceptiveness", "Unconventional creative concepts", "Deep emotional complexity"],
            "negative_traits": ["Vulnerability to depression and anxiety", "Sudden mental panic", "Suspicion and trust issues", "Erratic moods"],
            "recommended_careers": ["Subconscious Psychology", "Surrealist Arts", "Forensic Mental Health", "Night Operations Logistics"],
            "warnings_and_cautions": "Rahu eclipses the Moon. Causes depression, emotional anxiety, and erratic sleep. Silver water and grounding essential.",
            "harmonizing_poorak_number": 6,
            "fast_summary": "Warning: Rahu-Moon eclipse friction; prone to depression and mental anxiety; requires regular emotional grounding and silver water remedies."
        },
        (4, 3): {
            "driver": 4, "conductor": 3, "driver_planet": "Rahu (North Node)", "conductor_planet": "Jupiter (Guru)",
            "planet_combination": "Rahu-Jupiter (Unconventional Intellect)", "relationship_type": "Neutral",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Innovative Wisdom)",
            "synergy_title": "4-3: The Radical Theorist & Systems Philosopher",
            "positive_traits": ["Unorthodox problem-solving", "Technological foresight", "Ability to challenge outdated dogmas", "Broad systemic vision"],
            "negative_traits": ["Rebellious cynicism toward tradition", "Impatience with routine academic pace", "Intellectual restlessness"],
            "recommended_careers": ["AI Architecture", "Data Science & Quantum Computing", "Patent Law", "Alternative Energy Research", "Systems Engineering"],
            "warnings_and_cautions": "Channel rebellious intellect into cutting-edge technology or patent law rather than ideological debates.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Rahu and Dev Guru: radical intellect; excels in artificial intelligence, patent law, quantum systems, and alternative tech."
        },
        (4, 4): {
            "driver": 4, "conductor": 4, "driver_planet": "Rahu (North Node)", "conductor_planet": "Rahu (North Node)",
            "planet_combination": "Rahu-Rahu (Permanent Dual Rahu / High Friction)", "relationship_type": "Enemy",
            "star_rating": 1.0, "star_display": "? WARNING (Extreme Struggle / Accident Risk)",
            "synergy_title": "4-4: The Permanent Rahu Struggle & High Volatility",
            "positive_traits": ["Unprecedented technical disruptions", "Genius level out-of-box invention", "Iron resilience under pressure"],
            "negative_traits": ["Severe career and life instability", "High risk of accidents, surgeries, or sudden reversals", "Extreme rebellious stubbornness", "Chronic misunderstandings"],
            "recommended_careers": ["Advanced Cybersecurity Forensics", "Extreme Tech R&D", "Demolition & Structural Recovery", "High-Risk Systems Engineering"],
            "warnings_and_cautions": "LIFETIME STRUGGLE WARNING: Two Rahus create permanent friction. High risk of surgeries, sudden accidents, and disruptions. Daily Wood element hygiene non-negotiable.",
            "harmonizing_poorak_number": 6,
            "fast_summary": "Critical Warning: Dual Rahu; high risk of surgeries, sudden disruptions, and severe career struggle; requires continuous Panch Tattva shielding."
        },
        (4, 5): {
            "driver": 4, "conductor": 5, "driver_planet": "Rahu (North Node)", "conductor_planet": "Mercury (Budh)",
            "planet_combination": "Rahu-Mercury (Sharp Commercial Wit)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Digital Dealmaker)",
            "synergy_title": "4-5: The Digital Dealmaker & Systems Marketer",
            "positive_traits": ["Exceptional digital marketing instinct", "Fast algorithmic thinking", "Lucrative commercial networking", "High adaptability"],
            "negative_traits": ["Temptation to take speculative shortcuts", "Restless financial focus", "Impatience with slow compliance"],
            "recommended_careers": ["Digital Growth Marketing", "IT Brokerage & SaaS", "E-commerce Logistics", "Data Analytics Trading", "Commercial Tech"],
            "warnings_and_cautions": "Rahu and Mercury create sharp commercial minds. Ideal for digital marketing, software, and tech trade.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Rahu and Prince: dynamic tech dealmaker; highly successful in digital marketing, e-commerce, SaaS, and algorithmic commerce."
        },
        (4, 6): {
            "driver": 4, "conductor": 6, "driver_planet": "Rahu (North Node)", "conductor_planet": "Venus (Shukra)",
            "planet_combination": "Rahu-Venus (Glamour & Media Tech)", "relationship_type": "Friendly",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Glamour Tech)",
            "synergy_title": "4-6: The Media Visionary & Modern Aesthetician",
            "positive_traits": ["Futuristic aesthetic design", "Glamour and cinematic magnetism", "Luxurious technological vision", "Creative branding"],
            "negative_traits": ["Extravagant financial spending", "Romantic illusions and complicated attachments", "Hedonistic temptations"],
            "recommended_careers": ["Cinematography & CGI VFX", "Modern Interior Architecture", "Fashion Tech", "Celebrity Digital Media", "Luxury Gaming"],
            "warnings_and_cautions": "Rahu expands Venusian desire. Excellent for cinema, animation, and fashion; maintain strict personal financial boundaries.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Rahu and Venus: modern glamour and digital media; excels in cinema, visual effects, luxury gaming, and futuristic design."
        },
        (4, 7): {
            "driver": 4, "conductor": 7, "driver_planet": "Rahu (North Node)", "conductor_planet": "Ketu (South Node)",
            "planet_combination": "Rahu-Ketu (Head Meets Body / Complete Entity)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Body Completed / High Success)",
            "synergy_title": "4-7: The Body Completed & Unconventional Master",
            "positive_traits": ["Complete cosmic entity (Head + Body)", "Phenomenal sales and marketing power", "Deep occult and investigative brilliance", "Global success"],
            "negative_traits": ["Unconventional lifestyle baffling traditional peers", "Periods of deep withdrawal following public triumphs"],
            "recommended_careers": ["High-Ticket Marketing & Sales", "International Trade", "Occult & Esoteric Consultation", "Forensic Data Intelligence", "Foreign Relations"],
            "warnings_and_cautions": "Dr. Misra highlights 4-7: Rahu (head) leading Ketu (body) completes the individual, creating immense success in sales, marketing, and occult.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Four stars: Head meets Body; complete entity; immense breakthrough success in sales, marketing, foreign business, and occult sciences."
        },
        (4, 8): {
            "driver": 4, "conductor": 8, "driver_planet": "Rahu (North Node)", "conductor_planet": "Saturn (Shani)",
            "planet_combination": "Rahu-Saturn (Double Dark Karmic Friction)", "relationship_type": "Enemy",
            "star_rating": 1.0, "star_display": "? WARNING (Extreme Karmic Struggle & Delays)",
            "synergy_title": "4-8: The Dark Karmic Crucible & Structural Battle",
            "positive_traits": ["Ironclad endurance through severe adversity", "Mastery of harsh industrial environments", "Unyielding persistence"],
            "negative_traits": ["Heavy chronic delays and obstacles", "Litigation and contractual disputes", "Physical bone/joint or systemic strain", "Severe career frustration"],
            "recommended_careers": ["Heavy Metallurgy & Mining", "Industrial Demolition", "Environmental Hazard Recovery", "Litigation Law"],
            "warnings_and_cautions": "CRITICAL PERMANENT WARNING: Rahu and Saturn together create extreme karmic delay and structural friction. Regular Saturn/Rahu remedies mandatory.",
            "harmonizing_poorak_number": 6,
            "fast_summary": "Permanent Warning: Rahu and Saturn create intense delays and legal/structural struggle; demands continuous patience and ethical rigor."
        },
        (4, 9): {
            "driver": 4, "conductor": 9, "driver_planet": "Rahu (North Node)", "conductor_planet": "Mars (Mangal)",
            "planet_combination": "Rahu-Mars (Angarak / Surgical-Combat Friction)", "relationship_type": "Enemy",
            "star_rating": 1.5, "star_display": "? WARNING (Angarak Tension / Surgical Power)",
            "synergy_title": "4-9: The Angarak Crucible & Master Surgeon",
            "positive_traits": ["Fearless crisis intervention", "Natural affinity for surgical instruments and blood medicine", "Engineering brilliance under extreme pressure"],
            "negative_traits": ["High risk of physical accidents and surgeries", "Volcanic rage when provoked", "Fierce disputes with competitors"],
            "recommended_careers": ["General & Trauma Surgery", "Emergency Medicine", "Military Weapons Engineering", "Forensic Investigation", "Heavy Industrial Mechanics"],
            "warnings_and_cautions": "Dr. Misra highlights 4-9: Mars and Rahu connection governs blood, surgery, and combat. Risk of accidents or surgery, but makes brilliant surgeons/doctors.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Warning / Dual Destiny: Mars-Rahu Angarak tension; brings accident and surgery risks, but creates world-class trauma surgeons and defense engineers."
        },

        # ?? DRIVER 5 (MERCURY / PRINCE - FUTURE KING) ?????????????????????????
        # Five has NO enemies! All pairings are 3.5 to 5.0 stars!
        (5, 1): {
            "driver": 5, "conductor": 1, "driver_planet": "Mercury (Budh)", "conductor_planet": "Sun (Surya)",
            "planet_combination": "Mercury-Sun (Prince Backed by King)", "relationship_type": "Friendly",
            "star_rating": 4.5, "star_display": "?????? (4.5/5 Stars ? Commercial Sovereign)",
            "synergy_title": "5-1: The Crowned Commercial Leader",
            "positive_traits": ["Brilliant business strategy", "Commanding persuasive articulation", "Executive dealmaking", "Rapid market dominance"],
            "negative_traits": ["Impatience with slow partners", "Tendency to demand immediate commercial results"],
            "recommended_careers": ["Commercial Enterprise Leadership", "Banking & Finance Directorship", "Corporate Strategy", "High-Tech Trade", "Government Commerce"],
            "warnings_and_cautions": "God-gifted commercial talent. Mercury leads and the Sun provides sovereign authority; high success across all business lines.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Four and a half stars: Prince backed by King; supreme commercial leadership, banking authority, and rapid enterprise expansion."
        },
        (5, 2): {
            "driver": 5, "conductor": 2, "driver_planet": "Mercury (Budh)", "conductor_planet": "Moon (Chandra)",
            "planet_combination": "Mercury-Moon (Prince + Queen)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Creative Commerce)",
            "synergy_title": "5-2: Intuitive Commerce & Public Communications",
            "positive_traits": ["Empathetic salesmanship", "Articulate communication", "Public charm", "Versatile commercial adaptability"],
            "negative_traits": ["Mood swings affecting financial focus", "Restless pivoting before project completion"],
            "recommended_careers": ["Public Relations & Media", "Dairy & Food Industry Trade", "Advertising Copywriting", "Travel Hospitality", "Import/Export"],
            "warnings_and_cautions": "Combines emotional appeal with sharp wit. Highly successful in PR, creative media, and hospitality trading.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Prince and Queen: intuitive communication and public charm; excels in media, PR, dairy trading, and creative advertising."
        },
        (5, 3): {
            "driver": 5, "conductor": 3, "driver_planet": "Mercury (Budh)", "conductor_planet": "Jupiter (Guru)",
            "planet_combination": "Mercury-Jupiter (Prince + Dev Guru)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Financial Counselor)",
            "synergy_title": "5-3: The Strategic Economist & Wealth Counselor",
            "positive_traits": ["Deep economic intelligence", "High financial advisory ethics", "Clear analytical teaching", "Lucrative commercial publishing"],
            "negative_traits": ["Over-intellectualizing market trends", "Hesitation to take aggressive speculative risks"],
            "recommended_careers": ["Wealth Management", "Corporate Law & Compliance", "Economic Journalism", "Higher Commercial Education", "Financial Planning"],
            "warnings_and_cautions": "A highly respected intellectual-commercial combination. Success in financial consulting, corporate law, and wealth management.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Four stars: Prince and Dev Guru; blends commercial agility with deep ethical counsel; top-tier for wealth management and corporate law."
        },
        (5, 4): {
            "driver": 5, "conductor": 4, "driver_planet": "Mercury (Budh)", "conductor_planet": "Rahu (North Node)",
            "planet_combination": "Mercury-Rahu (Digital Wit & Systems Commerce)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Digital Disruptor)",
            "synergy_title": "5-4: The Algorithmic Trader & Tech Marketer",
            "positive_traits": ["Sharp digital marketing instincts", "Fast algorithmic pattern recognition", "Lucrative e-commerce strategy", "High adaptability"],
            "negative_traits": ["Temptation toward speculative day-trading", "Impatience with slow compliance protocols"],
            "recommended_careers": ["Algorithmic Trading & Fintech", "Digital Performance Marketing", "E-Commerce Enterprise", "IT Systems Logistics", "Software Sales"],
            "warnings_and_cautions": "Sharp technical-commercial acumen. Avoid speculative gambling; channel into scalable digital marketing and SaaS.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Prince and Rahu: sharp digital strategist; highly successful in fintech, algorithmic marketing, e-commerce, and software trade."
        },
        (5, 5): {
            "driver": 5, "conductor": 5, "driver_planet": "Mercury (Budh)", "conductor_planet": "Mercury (Budh)",
            "planet_combination": "Mercury-Mercury (Double Prince / Pure Quicksilver)", "relationship_type": "Friendly",
            "star_rating": 4.5, "star_display": "?????? (4.5/5 Stars ? Pure Mercantile Genius)",
            "synergy_title": "5-5: The Master Trader & Quicksilver Genius",
            "positive_traits": ["Supreme versatility and speed of thought", "Unmatched commercial negotiation", "Natural business magnetism", "Rapid international trade"],
            "negative_traits": ["Extreme restlessness", "Procrastination when routine sets in", "Difficulty with long stillness"],
            "recommended_careers": ["International Commodity Brokerage", "High-Volume Trade", "Media Network Ownership", "Venture Building", "Commercial Brokerage"],
            "warnings_and_cautions": "Dr. Misra highlights 5: God-gifted natural talent for business. With double 5, commercial success is virtually guaranteed if focused.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Four and a half stars: Double Mercury; natural mercantile genius; excels in large-scale trade, brokerage, and rapid commercial expansion."
        },
        (5, 6): {
            "driver": 5, "conductor": 6, "driver_planet": "Mercury (Budh)", "conductor_planet": "Venus (Shukra)",
            "planet_combination": "Mercury-Venus (Prince + Daitya Guru / Luxury Commerce)", "relationship_type": "Friendly",
            "star_rating": 4.5, "star_display": "?????? (4.5/5 Stars ? Luxury Commercial Star)",
            "synergy_title": "5-6: The Luxury Merchant & Media Magnate",
            "positive_traits": ["Effortless luxury brand attraction", "High glamour and persuasive charm", "Lucrative entertainment networking", "Aesthetic commercial taste"],
            "negative_traits": ["Extravagance in lifestyle spending", "Distraction by luxury indulgences"],
            "recommended_careers": ["Luxury Brand Ownership", "Cinematic Media Production", "High-End Fashion & Jewelry Trade", "Boutique Hospitality", "Cosmetic Real Estate"],
            "warnings_and_cautions": "Mercury and Venus form a golden commercial-luxury pairing. Brings immense wealth through fashion, luxury retail, and media arts.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Four and a half stars: Prince and Venus; golden luxury alignment; supreme aptitude for high-end fashion, luxury hospitality, and media magnate roles."
        },
        (5, 7): {
            "driver": 5, "conductor": 7, "driver_planet": "Mercury (Budh)", "conductor_planet": "Ketu (South Node)",
            "planet_combination": "Mercury-Ketu (Analytical Intellect & Occult Trade)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Esoteric Analytics)",
            "synergy_title": "5-7: The Data Strategist & Occult Commercialist",
            "positive_traits": ["Deep analytical acumen", "Occult commercialization", "Keen investigative intelligence", "Truth-seeking discernment"],
            "negative_traits": ["Skeptical hesitation", "Over-analyzing simple financial opportunities"],
            "recommended_careers": ["Data Science & Analytics", "Occult & Astrology Publishing", "Market Research Intelligence", "Forensic Auditing", "Specialized Consulting"],
            "warnings_and_cautions": "Combines commercial wit with Ketu's depth. Highly suitable for data analytics, market research, and specialized consultancy.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Prince and Ketu: analytical depth meets commercial wit; excels in market research intelligence, data science, and esoteric consulting."
        },
        (5, 8): {
            "driver": 5, "conductor": 8, "driver_planet": "Mercury (Budh)", "conductor_planet": "Saturn (Shani)",
            "planet_combination": "Mercury-Saturn (Commercial Prudence & Land)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Grounded Commerce)",
            "synergy_title": "5-8: The Property Mogul & Pragmatic Trader",
            "positive_traits": ["Grounded real estate acumen", "Meticulous contractual negotiation", "Long-term wealth compounding", "Agricultural and land intelligence"],
            "negative_traits": ["Slow commercial turnaround initially", "Over-cautious hesitation during market rallies"],
            "recommended_careers": ["Real Estate Development & Brokerage", "Agricultural Commerce", "Contractual Trade & Logistics", "Property Valuation", "Asset Management"],
            "warnings_and_cautions": "Dr. Misra highlights 5-8 for property, land, real estate, and agriculture. Patience yields solid compounding wealth.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Prince and Saturn: grounded commerce and land wealth; highly favored for real estate development, property brokerage, and agriculture."
        },
        (5, 9): {
            "driver": 5, "conductor": 9, "driver_planet": "Mercury (Budh)", "conductor_planet": "Mars (Mangal)",
            "planet_combination": "Mercury-Mars (Prince + Senapati / Dynamic Commerce)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Dynamic Enterprise)",
            "synergy_title": "5-9: The High-Speed Industrialist & Sports Marketer",
            "positive_traits": ["Decisive commercial action", "High energetic drive", "Sports and industrial trade acumen", "Fearless market initiative"],
            "negative_traits": ["Impulsive business decisions", "Occasional temper flares with partners"],
            "recommended_careers": ["Manufacturing & Heavy Equipment Trade", "Sports Equipment & Apparel Commerce", "Automotive Brokerage", "Emergency Supply Logistics"],
            "warnings_and_cautions": "Blends commercial speed with Martian fire. High success in manufacturing, athletic trade, and rapid enterprise scaling.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Four stars: Prince and Mars; high-speed dynamic enterprise; excels in manufacturing, athletic commerce, and industrial trade."
        },

        # ?? DRIVER 6 (VENUS / DAITYA GURU - MATERIAL KING) ????????????????????
        (6, 1): {
            "driver": 6, "conductor": 1, "driver_planet": "Venus (Shukra)", "conductor_planet": "Sun (Surya)",
            "planet_combination": "Venus-Sun (Luxury Backed by Sovereign)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Public Luxury)",
            "synergy_title": "6-1: The Sovereign of Aesthetics & Public Arts",
            "positive_traits": ["Dignified public charm", "High executive taste", "Magnetic leadership in creative fields", "Generous philanthropy"],
            "negative_traits": ["Ego battles in personal romance", "Extravagant expenditures to maintain status"],
            "recommended_careers": ["Cultural & Heritage Administration", "Luxury Real Estate", "Public Diplomacy", "High-End Media Production", "Fashion Directorship"],
            "warnings_and_cautions": "Luxury and Authority align. Great for public leadership in aesthetic, cultural, or luxury sectors.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Venus backed by Sun: dignified aesthetic authority; excels in luxury real estate, fashion directorship, and cultural diplomacy."
        },
        (6, 2): {
            "driver": 6, "conductor": 2, "driver_planet": "Venus (Shukra)", "conductor_planet": "Moon (Chandra)",
            "planet_combination": "Venus-Moon (Double Artistic Grace)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Artistic Harmony)",
            "synergy_title": "6-2: The Aesthetic Nurturer & Water-Luxury Master",
            "positive_traits": ["Exquisite aesthetic sensitivity", "Warm domestic hospitality", "Culinary and interior elegance", "Refined artistic gifts"],
            "negative_traits": ["Emotional vulnerability in love", "Susceptibility to flattering admirers", "Difficulty enforcing tough commercial terms"],
            "recommended_careers": ["Fine Dining & Culinary Hospitality", "Dairy & Water-Based Luxury Products", "Cosmetic Design", "Interior Architecture", "Fine Arts"],
            "warnings_and_cautions": "Dr. Misra highlights 6-2 for water-related, dairy, cosmetics, and fine arts. Brings abundant creative wealth.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Venus and Moon: artistic elegance and domestic warmth; top success in fine dining, cosmetic luxury, dairy, and interior architecture."
        },
        (6, 3): {
            "driver": 6, "conductor": 3, "driver_planet": "Venus (Shukra)", "conductor_planet": "Jupiter (Guru)",
            "planet_combination": "Venus-Jupiter (Daitya Guru vs Dev Guru / 36 ka Aankda)", "relationship_type": "Enemy",
            "star_rating": 1.5, "star_display": "? WARNING (Opposing Gurus / Health & Marital Caution)",
            "synergy_title": "6-3: The Dual Mentors Conflict (36 ka Aankda)",
            "positive_traits": ["High creative and philosophical talent", "Deep appreciation of cultural classics", "Charismatic speaking"],
            "negative_traits": ["Marital and partnership friction", "Health vulnerabilities (hormonal, liver, digestive)", "Ego clashes between spiritual and material values"],
            "recommended_careers": ["Cultural Heritage Preservation", "Art History Professorship", "Fashion Ethics Advisory", "Literary Review"],
            "warnings_and_cautions": "CRITICAL OPPOSING GURUS WARNING: Venus leading Jupiter triggers 36 ka aankda. High friction in marriage and health. Regular Lo Shu remedies required.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Warning: Opposing Gurus conflict; triggers marital discord and health vulnerabilities; requires conscious emotional balance and Lo Shu remedies."
        },
        (6, 4): {
            "driver": 6, "conductor": 4, "driver_planet": "Venus (Shukra)", "conductor_planet": "Rahu (North Node)",
            "planet_combination": "Venus-Rahu (Amplified Glamour & Media)", "relationship_type": "Friendly",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Glamour Media)",
            "synergy_title": "6-4: The Cinematic Producer & Modern Stylist",
            "positive_traits": ["Disruptive modern aesthetic", "Glamour and cinematic media instinct", "Magnetic public presence", "High commercial ambition"],
            "negative_traits": ["Hedonistic lifestyle temptations", "Complicated romantic relationships", "Financial over-expansion"],
            "recommended_careers": ["Cinema & Video Production", "VFX & Digital Media Animation", "Modern Fashion & Modeling", "Nightclub & Event Hospitality"],
            "warnings_and_cautions": "Rahu amplifies Venusian desires. Brilliant for entertainment, cinema, and fashion; guard against complicated relational entanglements.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Venus and Rahu: amplified glamour and cinematic production; excels in cinema, modern fashion, visual arts, and event entertainment."
        },
        (6, 5): {
            "driver": 6, "conductor": 5, "driver_planet": "Venus (Shukra)", "conductor_planet": "Mercury (Budh)",
            "planet_combination": "Venus-Mercury (Daitya Guru + Prince)", "relationship_type": "Friendly",
            "star_rating": 4.5, "star_display": "?????? (4.5/5 Stars ? Luxury Commerce Super Star)",
            "synergy_title": "6-5: The Sovereign Luxury Merchant",
            "positive_traits": ["Unrivaled commercial charm", "Effortless luxury salesmanship", "Lucrative international networking", "Refined business elegance"],
            "negative_traits": ["Lavish lifestyle expenses", "Impatience with dry administrative tasks"],
            "recommended_careers": ["Luxury Brand Directorship", "Fine Jewelry & Gemstone Commerce", "High-End Real Estate", "Boutique Hospitality", "Celebrity Management"],
            "warnings_and_cautions": "Dr. Misra highlights 6-5: Very rare to find an unsuccessful 6-5 individual. Sky is the limit in luxury commerce and hospitality.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Four and a half stars: Daitya Guru and Prince; golden commercial luxury pairing; exceptional for luxury retail, jewelry, and fine hospitality."
        },
        (6, 6): {
            "driver": 6, "conductor": 6, "driver_planet": "Venus (Shukra)", "conductor_planet": "Venus (Shukra)",
            "planet_combination": "Venus-Venus (Double Shukra / Pure Luxury)", "relationship_type": "Friendly",
            "star_rating": 5.0, "star_display": "?????? (5/5 Stars ? Super Success / Pure Venusian Glory)",
            "synergy_title": "6-6: The Emperor of Luxury & Artistic Glory",
            "positive_traits": ["Supreme aesthetic and artistic genius", "Effortless attraction of luxury and comfort", "Magnetic romantic charisma", "Lavish domestic abundance"],
            "negative_traits": ["Extreme love of comfort and luxury", "Resistance to austerity or hardship", "Vulnerability to romantic flattery"],
            "recommended_careers": ["High-End Entertainment & Cinema", "Luxury Fashion Conglomerates", "Super-Luxury Hospitality & Resorts", "Fine Jewelry", "Aesthetic Medicine"],
            "warnings_and_cautions": "SUPER SUCCESS COMBINATION: Dr. Misra explicitly states: '6-6 is extremely rare to find unsuccessful. Sky is the limit!' Unprecedented wealth in luxury arts.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Super Success: Double Venus; five out of five stars; sky is the limit in entertainment, luxury hospitality, fashion, and lavish material wealth."
        },
        (6, 7): {
            "driver": 6, "conductor": 7, "driver_planet": "Venus (Shukra)", "conductor_planet": "Ketu (South Node)",
            "planet_combination": "Venus-Ketu (Artistic Detachment & Spiritual Grace)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Mystic Aesthetics)",
            "synergy_title": "6-7: The Sacred Artist & Esoteric Healer",
            "positive_traits": ["Deep spiritual beauty", "Occult and aesthetic healing", "Refined artistic contemplation", "Gentle empathetic counseling"],
            "negative_traits": ["Emotional detachment in close romance", "Periods of dissatisfaction with material pleasures"],
            "recommended_careers": ["Sacred Arts & Temple Architecture", "Holistic Spa & Healing Resorts", "Jewelry & Crystal Consultation", "Art Therapy", "Herbal Wellness"],
            "warnings_and_cautions": "Combines Venusian beauty with Ketu's spiritual detachment. Highly suited for sacred arts, holistic wellness, and healing.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Venus and Ketu: sacred art and esoteric healing; excels in wellness resorts, crystal design, art therapy, and holistic aesthetics."
        },
        (6, 8): {
            "driver": 6, "conductor": 8, "driver_planet": "Venus (Shukra)", "conductor_planet": "Saturn (Shani)",
            "planet_combination": "Venus-Saturn (Luxury + Karmic Discipline)", "relationship_type": "Neutral",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Enduring Luxury)",
            "synergy_title": "6-8: The Luxury Real Estate Developer & Estate Master",
            "positive_traits": ["Long-term asset creation", "Patience with high-end architectural builds", "Solid commercial endurance", "Prudent financial management"],
            "negative_traits": ["Delayed material payoffs initially", "Stern emotional boundaries in romance", "Heavy workload burden"],
            "recommended_careers": ["Luxury Real Estate & Architecture", "Leather Goods & Textile Manufacturing", "Heavy Asset Management", "Contractual Design Governance"],
            "warnings_and_cautions": "Brings delayed but solid luxury wealth through real estate, architecture, and leather/textile manufacturing.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Venus and Saturn: enduring luxury through hard work; highly favored for luxury real estate, architecture, and leather/textile enterprises."
        },
        (6, 9): {
            "driver": 6, "conductor": 9, "driver_planet": "Venus (Shukra)", "conductor_planet": "Mars (Mangal)",
            "planet_combination": "Venus-Mars (Passion vs Fire / Scandal Risk)", "relationship_type": "Enemy",
            "star_rating": 2.0, "star_display": "? WARNING (Scandal Risk / Passion Friction)",
            "synergy_title": "6-9: The Passionate Volatility & Scandal Crucible",
            "positive_traits": ["Charismatic romantic passion", "Artistic vitality and stage energy", "Generous humanitarian giving"],
            "negative_traits": ["High risk of romantic scandals or controversy", "Marital disputes and volatile temper", "Impulsive expenditures on passion projects"],
            "recommended_careers": ["Stage & Performing Arts", "Athletic Fashion & Sports Media", "Celebrity Public Relations", "Cosmetic Surgery Support"],
            "warnings_and_cautions": "Dr. Misra highlights 6-9: Must be extremely careful regarding scandals, controversies, and marriage disputes. Maintain strict ethical clarity.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Warning: Venus-Mars passion clash; high risk of romantic scandals and marital controversy; requires moral vigilance and emotional restraint."
        },

        # ?? DRIVER 7 (KETU / INTROSPECTIVE MYSTIC) ????????????????????????????
        (7, 1): {
            "driver": 7, "conductor": 1, "driver_planet": "Ketu (South Node)", "conductor_planet": "Sun (Surya)",
            "planet_combination": "Ketu-Sun (Mystic Supported by King)", "relationship_type": "Neutral",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Institutional Research)",
            "synergy_title": "7-1: The Sovereign Research Advisor",
            "positive_traits": ["Deep research intelligence", "High administrative counsel", "Objective analytical truth-seeking", "Independent authority"],
            "negative_traits": ["Social isolation", "Reluctance to engage in public politicking", "Intellectual stubbornness"],
            "recommended_careers": ["Government Research Institutes", "Higher Scientific Academia", "Occult & Strategic Consulting", "Policy Intelligence"],
            "warnings_and_cautions": "Ketu lacks a head; Sun provides sovereign direction. Avoid speculative business; focus on consultative and research governance.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Ketu supported by Sun: sovereign research advisor; excels in government research institutes, strategic policy, and occult consultation."
        },
        (7, 2): {
            "driver": 7, "conductor": 2, "driver_planet": "Ketu (South Node)", "conductor_planet": "Moon (Chandra)",
            "planet_combination": "Ketu-Moon (Mystic Supported by Queen)", "relationship_type": "Neutral",
            "star_rating": 2.5, "star_display": "?????? (2.5/5 Stars ? Intuitive Healer)",
            "synergy_title": "7-2: The Intuitive Healer & Subconscious Guide",
            "positive_traits": ["Deep psychic empathy", "Gentle holistic healing", "Subconscious truth perception", "Spiritual counseling"],
            "negative_traits": ["Vulnerability to mood swings and melancholy", "Indecisiveness in commercial decisions", "Extreme introversion"],
            "recommended_careers": ["Spiritual & Energy Healing", "Tarot & Intuitive Reading", "Subconscious Psychology", "Water Therapy", "Poetic Literature"],
            "warnings_and_cautions": "Highly sensitive and psychic. Requires grounded emotional anchors; avoid commercial businesses with high financial risk.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Ketu and Moon: intense psychic empathy and healing grace; best suited for holistic healing, counseling, and subconscious psychology."
        },
        (7, 3): {
            "driver": 7, "conductor": 3, "driver_planet": "Ketu (South Node)", "conductor_planet": "Jupiter (Guru)",
            "planet_combination": "Ketu-Jupiter (Mystic Supported by Dev Guru)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Divine Guru)",
            "synergy_title": "7-3: The Divine Scholar & Master Occultist",
            "positive_traits": ["Profound spiritual mastery", "Higher academic research brilliance", "Teaching and coaching genius", "Divine intuitive connection"],
            "negative_traits": ["Detachment from worldly competition", "Impatience with materialistic greed"],
            "recommended_careers": ["Vedic & Occult Astrology", "Higher University Teaching", "Spiritual Authorship", "Alternative Medicine & Naturopathy", "Theological Research"],
            "warnings_and_cautions": "Dr. Misra highlights 7-3: Four stars for education, occult, healing, research, and divine connection. Super successful in knowledge fields.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Four stars: Ketu and Dev Guru; divine intellectual alignment; supreme aptitude for occult sciences, higher research, teaching, and spiritual authorship."
        },
        (7, 4): {
            "driver": 7, "conductor": 4, "driver_planet": "Ketu (South Node)", "conductor_planet": "Rahu (North Node)",
            "planet_combination": "Ketu-Rahu (Body Backed by Head)", "relationship_type": "Neutral",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Tactical Research)",
            "synergy_title": "7-4: The Technical Forensics & Cyber Intelligence",
            "positive_traits": ["Acute investigative forensics", "Cybersecurity and intelligence acumen", "Deep technical research", "Unconventional problem-solving"],
            "negative_traits": ["Feeling alienated or misunderstood", "Sudden detachment from professional networks", "Unorthodox lifestyle friction"],
            "recommended_careers": ["Cybersecurity Forensics", "Data Intelligence & Surveillance", "Alternative Science R&D", "Forensic Accounting", "Foreign Affairs Analysis"],
            "warnings_and_cautions": "Ketu (body) leading Rahu (head) has one star less than 4-7 because driver lacks the head. Excellent for technical forensics.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Ketu and Rahu: tactical forensics and cyber intelligence; thrives in technical investigation, cybersecurity, and foreign intelligence."
        },
        (7, 5): {
            "driver": 7, "conductor": 5, "driver_planet": "Ketu (South Node)", "conductor_planet": "Mercury (Budh)",
            "planet_combination": "Ketu-Mercury (Mystic Backed by Prince)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Commercial Data)",
            "synergy_title": "7-5: The Data Strategist & Consultative Analyst",
            "positive_traits": ["Sharp analytical intelligence", "Ability to monetize specialized research", "Prudent commercial advice", "Truth-seeking communication"],
            "negative_traits": ["Skeptical hesitation before launching deals", "Tendency to isolate when overwhelmed"],
            "recommended_careers": ["Quantitative Market Research", "Data Strategy & Analytics", "Specialized Consulting", "Esoteric Publishing", "Technical Writing"],
            "warnings_and_cautions": "Mercury provides the commercial head that Ketu lacks. Excellent for monetizing research, data strategy, and consulting.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Ketu backed by Prince: monetizes analytical research; highly successful in data science, quantitative market research, and consulting."
        },
        (7, 6): {
            "driver": 7, "conductor": 6, "driver_planet": "Ketu (South Node)", "conductor_planet": "Venus (Shukra)",
            "planet_combination": "Ketu-Venus (Mystic Backed by Luxury)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Luxury Research)",
            "synergy_title": "7-6: The Luxury Researcher & Aesthetic Healer",
            "positive_traits": ["Sophisticated aesthetic research", "Occult luxury and jewelry intelligence", "Refined holistic healing", "Subtle artistic elegance"],
            "negative_traits": ["Romantic detachment", "Perfectionist dissatisfaction with superficial luxury"],
            "recommended_careers": ["Gemstone & Mineralogy Consultation", "Luxury Spa & Healing Center Directorship", "Fine Antique Appraisal", "Sacred Architecture", "Art Curating"],
            "warnings_and_cautions": "Venus provides resource power to Ketu. High success in luxury research, gemstone consulting, antique curation, and wellness resorts.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Four stars: Ketu backed by Venus; luxury research and aesthetic healing; excels in antique curation, gemstone consulting, and luxury wellness."
        },
        (7, 7): {
            "driver": 7, "conductor": 7, "driver_planet": "Ketu (South Node)", "conductor_planet": "Ketu (South Node)",
            "planet_combination": "Ketu-Ketu (Dual Ketu / Extreme Detachment)", "relationship_type": "Neutral",
            "star_rating": 1.0, "star_display": "? WARNING (Zero Speculative Business / Partnership Risk)",
            "synergy_title": "7-7: The Pure Ascetic & Solitary Researcher",
            "positive_traits": ["Monumental psychic and occult depth", "Total immunity to superficial illusions", "Profound meditative genius", "Pure research dedication"],
            "negative_traits": ["Complete lack of commercial aggression", "Extreme financial vulnerability in partnerships (99-100% loss risk)", "Social isolation"],
            "recommended_careers": ["Solitary Academic Research", "Occult & Esoteric Healing", "Astrology & Palmistry Mastery", "Deep Science & Philosophy", "Monastic or Spiritual Life"],
            "warnings_and_cautions": "CRITICAL BUSINESS WARNING: Dr. Misra explicitly states: 'Never do business in partnership—loss is 100% guaranteed. Never do risky business.' Must choose research, occult, or healing.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Critical Warning: Dual Ketu; strictly avoid speculative business and partnerships (100% loss risk); supreme mastery in research, occult, and healing."
        },
        (7, 8): {
            "driver": 7, "conductor": 8, "driver_planet": "Ketu (South Node)", "conductor_planet": "Saturn (Shani)",
            "planet_combination": "Ketu-Saturn (Ascetic Detachment + Karma)", "relationship_type": "Enemy",
            "star_rating": 1.5, "star_display": "? WARNING (Isolation & Karmic Burden)",
            "synergy_title": "7-8: The Solitary Hermit & Karmic Burden",
            "positive_traits": ["Iron endurance in solitude", "Deep historical and archaeological insight", "Complete lack of fear of hardship"],
            "negative_traits": ["Severe career delays and feelings of loneliness", "Pessimism and emotional detachment", "Heavy karmic burdens"],
            "recommended_careers": ["Archaeological Research", "Mining Geology", "Historical Preservation", "Ascetic Philosophy", "Deep Earth Sciences"],
            "warnings_and_cautions": "Brings heavy isolation and karmic delay. Do not isolate yourself; maintain steady daily connections and practical service.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Warning: Ketu-Saturn karmic isolation; brings delays and solitary burdens; requires conscious social connection and white crystal remedies."
        },
        (7, 9): {
            "driver": 7, "conductor": 9, "driver_planet": "Ketu (South Node)", "conductor_planet": "Mars (Mangal)",
            "planet_combination": "Ketu-Mars (Mystic + Warrior / Impulsive Fire)", "relationship_type": "Enemy",
            "star_rating": 1.5, "star_display": "? WARNING (Impulsive Temper & Accident Risk)",
            "synergy_title": "7-9: The Mystic Combatant & Impulsive Flame",
            "positive_traits": ["Fearless occult defense", "High martial arts stamina", "Passionate defense of righteousness", "Surgical precision"],
            "negative_traits": ["Impulsive temper without strategic direction", "Accident vulnerabilities", "Sudden aggressive outbursts followed by regret"],
            "recommended_careers": ["Martial Arts Mastery", "Alternative Surgical Therapy", "Occult Defense & Security", "Forestry Protection", "Emergency Rescue"],
            "warnings_and_cautions": "Ketu has no head; Mars provides fiery force. Can lead to headless aggressive actions or accidents. Ground with physical discipline.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Warning: Ketu-Mars headless aggression; risk of impulsive temper and accidents; channel into disciplined martial arts or emergency rescue."
        },

        # ?? DRIVER 8 (SATURN / SHANI - JUDGE OF KARMA) ????????????????????????
        (8, 1): {
            "driver": 8, "conductor": 1, "driver_planet": "Saturn (Shani)", "conductor_planet": "Sun (Surya)",
            "planet_combination": "Saturn-Sun (Son vs Father / Bitter Enemies)", "relationship_type": "Enemy",
            "star_rating": 0.5, "star_display": "? CRITICAL WARNING (Karmic Enemy / Rise & Fall Risk)",
            "synergy_title": "8-1: The Saturn-Sun Sovereign Clash",
            "positive_traits": ["Titanic crisis stamina", "Mastery of harsh legal and corporate governance", "Iron endurance in adversity"],
            "negative_traits": ["Severe lifetime career struggle", "High rise followed by catastrophic drop", "Severe marital conflict and divorce risk", "Father-son or legal litigation"],
            "recommended_careers": ["Corporate Litigation Law", "Labor Dispute Governance", "Heavy Metallurgy & Mining", "Turnaround Restructuring"],
            "warnings_and_cautions": "CRITICAL LIFETIME WARNING: Saturn and Sun are bitter arch-enemies. Takes native high then drops abruptly. High marriage and partnership friction. Mandatory daily remedies.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Critical Warning: Bitter arch-enemies; brings massive rise and sudden fall; extreme marital friction; mandatory legal and planetary remedies."
        },
        (8, 2): {
            "driver": 8, "conductor": 2, "driver_planet": "Saturn (Shani)", "conductor_planet": "Moon (Chandra)",
            "planet_combination": "Saturn-Moon (Vish Yoga / Heavy Melancholy)", "relationship_type": "Enemy",
            "star_rating": 1.0, "star_display": "? WARNING (Vish Yoga / Health & Delay)",
            "synergy_title": "8-2: The Saturnian Vish Yoga & Emotional Crucible",
            "positive_traits": ["Endurance through profound hardship", "Patience with chronically distressed people", "Realistic grounding"],
            "negative_traits": ["Chronic health challenges (joints, fluids, depression)", "Sudden financial setbacks", "Cold emotional atmosphere", "Severe delays in business"],
            "recommended_careers": ["Geriatric Care Administration", "Waste Water Management", "Historical Archive Governance", "Palliative Healthcare"],
            "warnings_and_cautions": "Forms Vish Yoga. Dr. Misra warns: Business may go well initially then suddenly health or mental issues disrupt progress. White quartz essential.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Warning: Vish Yoga; causes chronic health and emotional delays; business momentum disrupted by sudden setbacks; requires white crystal hygiene."
        },
        (8, 3): {
            "driver": 8, "conductor": 3, "driver_planet": "Saturn (Shani)", "conductor_planet": "Jupiter (Guru)",
            "planet_combination": "Saturn-Jupiter (Karmic Judge Guided by Wisdom)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Judicial Wisdom)",
            "synergy_title": "8-3: The Constitutional Arbiter & Corporate Judge",
            "positive_traits": ["Monumental legal acumen", "High judicial ethics", "Prudent institutional management", "Compounding wealth intelligence"],
            "negative_traits": ["Stern demeanor", "Slow early career momentum", "Difficulty expressing informal warmth"],
            "recommended_careers": ["Judiciary & Supreme Court Law", "Corporate Regulatory Governance", "Institutional Banking Oversight", "Estate Trusts Administration"],
            "warnings_and_cautions": "Saturn and Jupiter align on justice and law. Slow initial progress matures into supreme judicial or institutional authority.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Saturn and Dev Guru: judicial wisdom meets karmic justice; highly respected in corporate law, judiciary, and institutional compliance."
        },
        (8, 4): {
            "driver": 8, "conductor": 4, "driver_planet": "Saturn (Shani)", "conductor_planet": "Rahu (North Node)",
            "planet_combination": "Saturn-Rahu (Permanent Dark Karma / Structural Friction)", "relationship_type": "Enemy",
            "star_rating": 1.0, "star_display": "? WARNING (Heavy Karmic Delays & Litigation)",
            "synergy_title": "8-4: The Permanent Dark Crucible & Legal Obstacles",
            "positive_traits": ["Ironclad physical and mental endurance", "Mastery of extreme industrial systems", "Unshakeable persistence under adversity"],
            "negative_traits": ["Severe career delays and chronic struggle", "Litigation and contractual disputes", "Health strains", "Pessimism and isolation"],
            "recommended_careers": ["Heavy Infrastructure & Mining", "Industrial Demolition", "Environmental Remediation", "Criminal Law"],
            "warnings_and_cautions": "CRITICAL PERMANENT WARNING: Saturn and Rahu together create heavy karmic delays and legal hurdles. Daily Panch Tattva hygiene essential.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Permanent Warning: Saturn-Rahu creates chronic delays and legal/structural struggle; requires strict ethical compliance and continuous remedies."
        },
        (8, 5): {
            "driver": 8, "conductor": 5, "driver_planet": "Saturn (Shani)", "conductor_planet": "Mercury (Budh)",
            "planet_combination": "Saturn-Mercury (Karmic Judge + Prince)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Real Estate & Trade)",
            "synergy_title": "8-5: The Real Estate Mogul & Pragmatic Financier",
            "positive_traits": ["Phenomenal property and land acumen", "Meticulous contractual dealmaking", "Steady compounding wealth", "Solid commercial endurance"],
            "negative_traits": ["Over-calculating risk", "Slow initial execution while verifying details"],
            "recommended_careers": ["Real Estate Development & Brokerage", "Heavy Industrial Trading", "Agricultural Commerce", "Contractual Logistics", "Asset Management"],
            "warnings_and_cautions": "Dr. Misra highlights 8-5: Outstanding for property, land, real estate, and finance. Mercury's speed balances Saturn's prudence.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Four stars: Saturn and Prince; phenomenal real estate and land wealth; highly favored for property development, commerce, and finance."
        },
        (8, 6): {
            "driver": 8, "conductor": 6, "driver_planet": "Saturn (Shani)", "conductor_planet": "Venus (Shukra)",
            "planet_combination": "Saturn-Venus (Karmic Discipline + Luxury)", "relationship_type": "Friendly",
            "star_rating": 3.5, "star_display": "?????? (3.5/5 Stars ? Enduring Luxury)",
            "synergy_title": "8-6: The Architect of Luxury Estates & Fine Leather",
            "positive_traits": ["Exceptional architectural and design stamina", "Luxury asset stewardship", "Solid financial patience", "Aesthetic material quality"],
            "negative_traits": ["Delayed gratification in romance", "Stern domestic rules", "Heavy workload burden"],
            "recommended_careers": ["Luxury Real Estate & Interior Architecture", "High-End Leather & Metallurgy Goods", "Commercial Asset Management", "Textile Manufacturing"],
            "warnings_and_cautions": "Saturn and Venus are friendly. Delivers massive compounding wealth through luxury real estate, architecture, and fine manufacturing.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Saturn and Venus: enduring luxury through patience; excels in luxury real estate, architecture, fine leather goods, and manufacturing."
        },
        (8, 7): {
            "driver": 8, "conductor": 7, "driver_planet": "Saturn (Shani)", "conductor_planet": "Ketu (South Node)",
            "planet_combination": "Saturn-Ketu (Karmic Judge + Mystic Detachment)", "relationship_type": "Neutral",
            "star_rating": 2.5, "star_display": "?????? (2.5/5 Stars ? Solitary Ascetic)",
            "synergy_title": "8-7: The Ascetic Researcher & Historical Geologist",
            "positive_traits": ["Profound research stamina", "Deep detachment from shallow trends", "Historical and geological intelligence", "Philosophical endurance"],
            "negative_traits": ["Solitary isolation and gloominess", "Slow material compounding", "Emotional coldness toward peers"],
            "recommended_careers": ["Mining & Geological Survey", "Historical Archaeology", "Deep Philosophy & Theology", "Forensic Data Preservation"],
            "warnings_and_cautions": "Brings heavy isolation if disconnected from society. Maintain active social ties and avoid melancholy.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Saturn and Ketu: ascetic researcher and deep earth scientist; excels in geological survey, archaeology, and historical research."
        },
        (8, 8): {
            "driver": 8, "conductor": 8, "driver_planet": "Saturn (Shani)", "conductor_planet": "Saturn (Shani)",
            "planet_combination": "Saturn-Saturn (Double Saturn / Supreme Laborious Karma)", "relationship_type": "Enemy",
            "star_rating": 1.5, "star_display": "? WARNING (Double Saturn Struggle / Heavy Duty)",
            "synergy_title": "8-8: The Iron Sovereign of Hard Labor & Justice",
            "positive_traits": ["Titanic endurance that outlasts all peers", "Unbending devotion to justice and law", "Ability to manage colossal physical systems", "Compounding master"],
            "negative_traits": ["Prolonged severe struggle and delayed payoffs", "Stern, unapproachable presence", "Workaholism destroying personal health", "Heavy karmic tests"],
            "recommended_careers": ["High Judiciary & Constitutional Law", "Heavy Metallurgy & Steel Manufacturing", "National Infrastructure & Mining", "Labor Union Governance"],
            "warnings_and_cautions": "LIFETIME STRUGGLE WARNING: Double Saturn creates monumental labor and delayed success. Victory comes through sheer righteousness and unbending discipline.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Warning: Double Saturn; monumental labor, struggle, and delayed payoffs; master of justice, law, metallurgy, and heavy enterprise."
        },
        (8, 9): {
            "driver": 8, "conductor": 9, "driver_planet": "Saturn (Shani)", "conductor_planet": "Mars (Mangal)",
            "planet_combination": "Saturn-Mars (Cold Earth vs Fiery Iron / Struggle Tension)", "relationship_type": "Neutral",
            "star_rating": 2.5, "star_display": "?????? (2.5/5 Stars ? Heavy Engineering / Defense)",
            "synergy_title": "8-9: The Battle-Hardened Engineer & Armed Protector",
            "positive_traits": ["Immense physical and structural stamina", "Fearless crisis management in industrial zones", "Command over heavy engineering and defense"],
            "negative_traits": ["Internal friction between patience and impulsive action", "Stubbornness", "Risk of physical strain or injuries"],
            "recommended_careers": ["Heavy Machinery & Automotive Engineering", "Armed Forces Logistics", "Orthopedic & Trauma Surgery", "Metallurgy & Defense Production"],
            "warnings_and_cautions": "Dr. Misra highlights 8-9: Saturn and Mars require proper career alignment (heavy engineering, defense, surgery) to convert struggle into immense strength.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Saturn and Mars: battle-hardened industrial power; supreme aptitude for heavy machinery, defense production, trauma surgery, and metallurgy."
        },

        # ?? DRIVER 9 (MARS / MANGAL - COMMANDER-IN-CHIEF) ?????????????????????
        (9, 1): {
            "driver": 9, "conductor": 1, "driver_planet": "Mars (Mangal)", "conductor_planet": "Sun (Surya)",
            "planet_combination": "Mars-Sun (Senapati Leading King)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Commanding Leadership)",
            "synergy_title": "9-1: The Commander-in-Chief & Valiant Sovereign",
            "positive_traits": ["Fierce executive drive", "Decisive courage", "Natural administrative authority", "Heroic protection of subordinates"],
            "negative_traits": ["Fiery temper when questioned", "Impatience with slow diplomatic protocols"],
            "recommended_careers": ["Armed Forces Directorship", "IPS & Civil Police Command", "Trauma & Surgical Directorship", "Top Industrial Executive", "Sports Governance"],
            "warnings_and_cautions": "Dr. Misra notes: 1-9 is 5 stars (King leading Senapati), while 9-1 is 4 stars because the King prefers being in front. Still a supreme executive combination.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Four stars: Commander leading with King's authority; supreme courage, decisive executive leadership, and administrative triumph."
        },
        (9, 2): {
            "driver": 9, "conductor": 2, "driver_planet": "Mars (Mangal)", "conductor_planet": "Moon (Chandra)",
            "planet_combination": "Mars-Moon (Fiery Commander + Gentle Queen)", "relationship_type": "Enemy",
            "star_rating": 2.0, "star_display": "? WARNING (Fire-Water Conflict / Marital Friction)",
            "synergy_title": "9-2: The Fiery Heart & Emotional Clash",
            "positive_traits": ["Passionate defense of loved ones", "High athletic stamina", "Raw creative energy"],
            "negative_traits": ["Severe relationship and marital friction", "Volcanic anger clashing with sensitivity", "Impulsive decisions followed by regret"],
            "recommended_careers": ["Emergency Response & Paramedic Leadership", "Culinary Fire Arts", "Maritime Engineering", "Sports Coaching"],
            "warnings_and_cautions": "Mars (fire) and Moon (water) clash emotionally. Causes marital friction and relationship volatility. Cultivate calm communication.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Warning: Fire and Water conflict; causes emotional volatility and marital friction; requires cooling mindfulness and gentle communication."
        },
        (9, 3): {
            "driver": 9, "conductor": 3, "driver_planet": "Mars (Mangal)", "conductor_planet": "Jupiter (Guru)",
            "planet_combination": "Mars-Jupiter (Senapati + Dev Guru)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Righteous Commander)",
            "synergy_title": "9-3: The Righteous Warrior & Medical Leader",
            "positive_traits": ["High administrative and moral courage", "Inspirational leadership", "Discipline in higher knowledge and physical arts", "Noble humanitarian defense"],
            "negative_traits": ["Moral indignation leading to fiery confrontations", "Impatience with bureaucratic corruption"],
            "recommended_careers": ["Surgical Medicine", "Armed Forces Administration", "University Directorship", "Civil Services", "Athletic Directorship"],
            "warnings_and_cautions": "Combines Martian courage with Jupiterian wisdom. Highly favored for top doctors, surgeons, army officers, and civil administrators.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Four stars: Commander guided by Dev Guru; righteous courage; supreme aptitude for top surgeons, military command, and civil administration."
        },
        (9, 4): {
            "driver": 9, "conductor": 4, "driver_planet": "Mars (Mangal)", "conductor_planet": "Rahu (North Node)",
            "planet_combination": "Mars-Rahu (Angarak Tension / Surgical Power)", "relationship_type": "Enemy",
            "star_rating": 1.5, "star_display": "? WARNING (Angarak Tension / Surgical Power)",
            "synergy_title": "9-4: The Angarak Crucible & Master Surgeon",
            "positive_traits": ["Fearless crisis intervention", "Natural affinity for surgical instruments and blood medicine", "Engineering brilliance under extreme pressure"],
            "negative_traits": ["High risk of physical accidents and surgeries", "Volcanic rage when provoked", "Fierce disputes with competitors"],
            "recommended_careers": ["General & Trauma Surgery", "Emergency Medicine", "Military Weapons Engineering", "Forensic Investigation", "Heavy Industrial Mechanics"],
            "warnings_and_cautions": "Dr. Misra highlights 9-4: Mars and Rahu connection governs blood, surgery, and combat. Risk of accidents or surgery, but makes brilliant surgeons/doctors.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Warning / Dual Destiny: Mars-Rahu Angarak tension; brings accident and surgery risks, but creates world-class trauma surgeons and defense engineers."
        },
        (9, 5): {
            "driver": 9, "conductor": 5, "driver_planet": "Mars (Mangal)", "conductor_planet": "Mercury (Budh)",
            "planet_combination": "Mars-Mercury (Senapati + Prince / Dynamic Trade)", "relationship_type": "Friendly",
            "star_rating": 4.0, "star_display": "?????? (4/5 Stars ? Dynamic Business)",
            "synergy_title": "9-5: The High-Speed Industrialist & Sports Marketer",
            "positive_traits": ["Decisive commercial action", "High energetic drive", "Sports and industrial trade acumen", "Fearless market initiative"],
            "negative_traits": ["Impulsive business decisions", "Occasional temper flares with partners"],
            "recommended_careers": ["Manufacturing & Heavy Equipment Trade", "Sports Equipment & Apparel Commerce", "Automotive Brokerage", "Emergency Supply Logistics"],
            "warnings_and_cautions": "Blends commercial speed with Martian fire. High success in manufacturing, athletic trade, and rapid enterprise scaling.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Four stars: Commander and Prince; high-speed dynamic enterprise; excels in manufacturing, athletic commerce, and industrial trade."
        },
        (9, 6): {
            "driver": 9, "conductor": 6, "driver_planet": "Mars (Mangal)", "conductor_planet": "Venus (Shukra)",
            "planet_combination": "Mars-Venus (Passion vs Luxury / Scandal Risk)", "relationship_type": "Enemy",
            "star_rating": 2.0, "star_display": "? WARNING (Passion Clash / Scandal Risk)",
            "synergy_title": "9-6: The Passionate Volatility & Scandal Crucible",
            "positive_traits": ["Charismatic romantic passion", "Artistic vitality and stage energy", "Generous humanitarian giving"],
            "negative_traits": ["High risk of romantic scandals or controversy", "Marital disputes and volatile temper", "Impulsive expenditures on passion projects"],
            "recommended_careers": ["Stage & Performing Arts", "Athletic Fashion & Sports Media", "Celebrity Public Relations", "Cosmetic Surgery Support"],
            "warnings_and_cautions": "Dr. Misra highlights 9-6: Must be extremely careful regarding scandals, controversies, and marriage disputes. Maintain strict ethical clarity.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Warning: Mars-Venus passion clash; high risk of romantic scandals and marital controversy; requires moral vigilance and emotional restraint."
        },
        (9, 7): {
            "driver": 9, "conductor": 7, "driver_planet": "Mars (Mangal)", "conductor_planet": "Ketu (South Node)",
            "planet_combination": "Mars-Ketu (Warrior + Mystic / Righteous Force)", "relationship_type": "Friendly",
            "star_rating": 3.0, "star_display": "?????? (3/5 Stars ? Occult Warrior)",
            "synergy_title": "9-7: The Righteous Protector & Occult Warrior",
            "positive_traits": ["Fearless defense of justice", "Spiritual and occult discipline", "High physical and martial stamina", "Intuitive protective reflexes"],
            "negative_traits": ["Sudden explosive outbursts", "Impatience with deceit", "Tendency to isolate after battles"],
            "recommended_careers": ["Martial Arts Instruction", "Defense Intelligence", "Occult & Tantric Protection", "Emergency Rescue Leadership", "Surgical Technology"],
            "warnings_and_cautions": "Dr. Misra highlights 9-7 for occult, teaching, armed forces, and protective leadership. Channel into disciplined martial arts or surgery.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Three stars: Mars and Ketu; occult warrior; excels in martial arts, defense intelligence, emergency rescue, and surgical technology."
        },
        (9, 8): {
            "driver": 9, "conductor": 8, "driver_planet": "Mars (Mangal)", "conductor_planet": "Saturn (Shani)",
            "planet_combination": "Mars-Saturn (Fiery Iron vs Cold Earth / Heavy Industry)", "relationship_type": "Neutral",
            "star_rating": 2.5, "star_display": "?????? (2.5/5 Stars ? Heavy Engineering / Struggle)",
            "synergy_title": "9-8: The Industrial Commander & Structural Builder",
            "positive_traits": ["Immense physical and mechanical stamina", "Fearless leadership in heavy industrial zones", "Command over metallurgy and defense"],
            "negative_traits": ["Internal tension between hasty action and slow delay", "Stubbornness", "Risk of physical injury in heavy environments"],
            "recommended_careers": ["Heavy Metallurgy & Foundry", "Automotive & Heavy Equipment", "Civil Infrastructure Construction", "Military Logistics"],
            "warnings_and_cautions": "Mars and Saturn require proper career alignment (heavy engineering, metallurgy, infrastructure) to convert friction into monumental achievement.",
            "harmonizing_poorak_number": 5,
            "fast_summary": "Mars and Saturn: heavy industrial stamina; excels in automotive engineering, heavy metallurgy, civil infrastructure, and military logistics."
        },
        (9, 9): {
            "driver": 9, "conductor": 9, "driver_planet": "Mars (Mangal)", "conductor_planet": "Mars (Mangal)",
            "planet_combination": "Mars-Mars (Permanent Double Mars / Volcanic Anger)", "relationship_type": "Enemy",
            "star_rating": 1.5, "star_display": "? WARNING (Volcanic Temper / Marital Strife)",
            "synergy_title": "9-9: The Permanent Double Mars & Volcanic Fire",
            "positive_traits": ["Titanic physical courage and stamina", "Heroic humanitarian protection", "Fearless front-line leadership", "Decisive crisis action"],
            "negative_traits": ["Volcanic explosive temper", "Severe marital and relationship discord", "Impulsive aggression risking physical injuries", "Intolerance of dissent"],
            "recommended_careers": ["Special Armed Forces / Commando", "Emergency Trauma Surgery", "High-Risk Fire & Rescue", "Competitive Professional Sports", "Heavy Machinery"],
            "warnings_and_cautions": "CRITICAL TEMPER & MARITAL WARNING: Dr. Misra highlights 9-9: Permanent relation of double Mars creates extreme temper, anger, fighting, and marital strife. Mandatory cooling exercises and red thread remedies.",
            "harmonizing_poorak_number": 1,
            "fast_summary": "Critical Warning: Permanent double Mars; volcanic temper, anger, and marital discord; must channel fire into rigorous sports and emergency surgery."
        }
    }

    # Format into canonical dictionary indexed by f"{driver}_{conductor}"
    formatted = {}
    for (d, c), data in raw_specs.items():
        key = f"{d}_{c}"
        formatted[key] = {
            "driver": d,
            "conductor": c,
            "key": key,
            "driver_planet": data["driver_planet"],
            "conductor_planet": data["conductor_planet"],
            "planet_combination": data["planet_combination"],
            "relationship_type": data["relationship_type"],
            "star_rating": data["star_rating"],
            "star_display": data["star_display"],
            "synergy_title": data["synergy_title"],
            "positive_traits": data["positive_traits"],
            "negative_traits": data["negative_traits"],
            "recommended_careers": data["recommended_careers"],
            "warnings_and_cautions": data["warnings_and_cautions"],
            "harmonizing_poorak_number": data["harmonizing_poorak_number"],
            "fast_summary": data["fast_summary"],
            "source": "SRC-DR-CHAITANYAA-MISRA-DAY6-DAY7-LECTURE",
            "rule_status": "APPROVED"
        }
    return formatted


def get_five_elements_hygiene_data():
    """
    Panch Tattva Basic Hygiene & Bodyguards as taught by Dr. Numeros Vision Classical Methodology.
    Non-negotiable foundational shielding required before any gemstone or complex ritual.
    """
    return {
        "WOOD": {
            "element": "Wood",
            "tattva_hindi": "वृहस्पत / अन्तरिक्ष / वायु (Wood / Growth)",
            "associated_numbers": [3, 4],
            "governing_planets": ["Jupiter (Guru / Dev Guru)", "Rahu (North Node / Shadow Architect)"],
            "governing_cardinal_directions": ["East (Jupiter)", "South-East (Rahu)"],
            "vital_organs_and_aura": "Heart equilibrium, vital aura shielding, spiritual expansion, personal growth",
            "hygiene_prescription": {
                "core_rule": "Must touch physical skin continuously (necklace, bracelet, or bangle).",
                "item_options": [
                    "Natural 5-Mukhi Rudraksha bracelet or mala (Universal, highly recommended)",
                    "Tulsi mala or bracelet (FOR STRICT VEGETARIANS ONLY; do NOT wear if consuming non-vegetarian food)",
                    "Natural sandalwood (Chandan) beads or wooden bangle"
                ],
                "dietary_diet_caveat": "Non-vegetarians must strictly avoid Tulsi beads and use natural Rudraksha or Sandalwood instead.",
                "why_it_protects": "Acts as your primary vibrational bodyguard for aura expansion and heart protection."
            }
        },
        "EARTH": {
            "element": "Earth",
            "tattva_hindi": "पृथ्वी (Earth / Stability)",
            "associated_numbers": [2, 5, 8],
            "governing_planets": ["Moon (Chandra)", "Mercury (Budh)", "Saturn (Shani)"],
            "governing_cardinal_directions": ["South-West (Moon)", "Center / Brahma Sthana (Mercury)", "North-East (Saturn)"],
            "vital_organs_and_aura": "Blood pressure regulation, anger cooling, mental stability, decisive grounding, electromagnetic balance",
            "hygiene_prescription": {
                "core_rule": "Wear a natural Clear White Quartz (Sphatik / White Quartz) bracelet or mala (10mm to 12mm beads).",
                "properties": "Sphatik remains naturally icy-cold even under direct scorching sunlight, drawing electromagnetic heat out of the body.",
                "item_options": [
                    "White Quartz (Sphatik) 10mm-12mm bead bracelet on left or right wrist",
                    "Sphatik mala worn around the neck touching throat/chest chakra"
                ],
                "why_it_protects": "Soothes blood pressure, arrests volcanic aggression, grounds erratic overthinking, and restores earth stability."
            }
        },
        "FIRE": {
            "element": "Fire",
            "tattva_hindi": "अग्नि (Fire / Vitality)",
            "associated_numbers": [9],
            "governing_planets": ["Mars (Mangal / Senapati)"],
            "governing_cardinal_directions": ["South (Mars)"],
            "vital_organs_and_aura": "Cellular vitality, digestive fire (Agni), courage, proactive initiative, immune resistance, Vitamin D synthesis",
            "hygiene_prescription": {
                "core_rule": "Tie a sacred red thread (Mauli / Kalawa) on right wrist; apply red tilak (Ashtagandha / Roli); receive morning sunlight.",
                "item_options": [
                    "Sacred red cotton thread (Mauli / Kalawa) tied on wrist",
                    "Red Ashtagandha / Roli tilak on forehead or throat chakra daily",
                    "15 minutes of early morning natural sunlight exposure (Surya Arghya)"
                ],
                "color_caveat": "Even if red is technically not a personal lucky number color, the red thread on wrist is an ELEMENTAL balancer, not a planet garment, so it causes ZERO harm.",
                "why_it_protects": "Ignites vital stamina, balances inner digestive fire, and wards off lethargy and chronic procrastination."
            }
        },
        "WATER": {
            "element": "Water",
            "tattva_hindi": "जल (Water / Flow)",
            "associated_numbers": [1],
            "governing_planets": ["Sun (Surya - Life Giver)"],
            "governing_cardinal_directions": ["North (Water / Career)"],
            "vital_organs_and_aura": "76% of physical body constitution, cellular hydration, lymphatic purification, kidney vitality, career momentum",
            "hygiene_prescription": {
                "core_rule": "Carry a pure Copper bottle or sipper (Tambe ka bartan) and drink water in small mindful sips throughout the day.",
                "item_options": [
                    "Pure Copper water bottle / small sipper (250ml - 500ml) carried in daily bag",
                    "Jal Arghya (offering water in copper lota to morning sun with a pinch of red kumkum)",
                    "Two daily bathing rituals for aura cleansing"
                ],
                "hydration_protocol": "Sipping copper-infused water in controlled small amounts revitalizes cellular energy and strengthens the North-career axis.",
                "why_it_protects": "Prevents dehydration, flushes cellular toxins, and ensures unobstructed flow in career and life direction."
            }
        },
        "METAL_AIR": {
            "element": "Metal / Air",
            "tattva_hindi": "धातु / वायु (Metal / Prana / Cosmic Harmony)",
            "associated_numbers": [6, 7],
            "governing_planets": ["Venus (Gold Metal / Shukra)", "Ketu (Silver Metal / Ketu)"],
            "governing_cardinal_directions": ["North-West (Venus)", "West (Ketu)"],
            "vital_organs_and_aura": "Nervous transmission, prana breathing, aesthetic grace, strategic detachment, cosmic electromagnetic conductivity",
            "hygiene_prescription": {
                "core_rule": "Wear a high-quality metallic chain watch on the wrist (Silver for 7, Gold/Brass for 6, or Dual-Tone for both).",
                "metal_breakdown": {
                    "number_7_ketu": "Silver metallic chain watch (Silver represents Ketu and lunar-mental clarity).",
                    "number_6_venus": "Gold or brass metallic chain watch (Gold represents Venusian luxury, abundance, and grace).",
                    "dual_balancing": "Dual-Tone (Silver + Gold) metallic watch is universally optimal if seeking balance of both aesthetics and research."
                },
                "why_it_protects": "Acts as an electromagnetic antenna, harmonizing subtle air and metal prana throughout the body's nervous meridian system."
            }
        }
    }


def get_complementary_poorak_data():
    """
    Master Complementary (Poorak / पूरक) Numbers Knowledge Base.
    Acts as the cosmic peacemaker and grid-completion harmonizer.
    """
    return {
        "master_poorak_map": {
            1: {"complementary": [9], "planet": "Mars (Mangal)", "role": "Provides executive courage, physical vitality, and fearless action to Sun's leadership."},
            2: {"complementary": [5, 7], "planet": "Mercury & Ketu", "role": "Mercury (5) provides rational communication and commercial stability to Moon's sensitivity; Ketu (7) provides intuitive spiritual alignment."},
            3: {"complementary": [5, 7], "planet": "Mercury & Ketu", "role": "Mercury (5) monetizes and commercially structures Jupiter's wisdom; Ketu (7) deepens divine esoteric research."},
            4: {"complementary": [8], "planet": "Saturn (Shani)", "role": "Provides grounded physical discipline, legal compliance, and structural stamina to Rahu's unconventional systems."},
            5: {"complementary": [1, 6], "planet": "Universal Master Key", "role": "Number 5 is the Universal Balancer (Mercury); neutral and friendly to all. Supported by Sun (1) for authority and Venus (6) for luxury."},
            6: {"complementary": [5], "planet": "Mercury (Budh)", "role": "Provides witty commercial networking and agile dealmaking to Venusian luxury and domestic aesthetics."},
            7: {"complementary": [3], "planet": "Jupiter (Guru)", "role": "Provides structured philosophical teaching, public mentorship, and ethical direction to Ketu's solitary insights."},
            8: {"complementary": [4, 5], "planet": "Rahu & Mercury", "role": "Rahu (4) provides unconventional system engineering; Mercury (5) provides commercial flexibility and diplomatic speed to Saturnian rigidity."},
            9: {"complementary": [1], "planet": "Sun (Surya)", "role": "Provides sovereign executive command, public status, and noble direction to Martian physical force and raw energy."}
        },
        "friction_pair_peacemakers": {
            "1_8": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 dissolves Sun-Saturn father-son friction with commerce, diplomacy, and neutral mental agility."},
            "8_1": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 dissolves Saturn-Sun authority deadlock through contractual flexibility and commercial compromise."},
            "2_4": {"poorak": 6, "peacemaker_planet": "Venus (Shukra)", "rationale": "Number 6 soothes Moon-Rahu eclipse anxiety through aesthetic beauty, domestic harmony, and gentle luxury."},
            "4_2": {"poorak": 6, "peacemaker_planet": "Venus (Shukra)", "rationale": "Number 6 softens Rahu-Moon mental turbulence with artistic grace and emotional reassurance."},
            "2_8": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 stabilizes Moon-Saturn Vish Yoga depression through active logical communication and commercial focus."},
            "8_2": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 overcomes Saturn-Moon chronic delays with energetic adaptability and social networking."},
            "2_9": {"poorak": 1, "peacemaker_planet": "Sun (Surya)", "rationale": "Number 1 brings noble sovereign harmony to Moon-Mars fire-water volatility, commanding mutual respect."},
            "9_2": {"poorak": 1, "peacemaker_planet": "Sun (Surya)", "rationale": "Number 1 grounds Mars-Moon emotional clashes through dignified executive purpose."},
            "3_6": {"poorak": 7, "peacemaker_planet": "Ketu (South Node)", "rationale": "Number 7 reconciles Dev Guru (3) and Daitya Guru (6) by transmuting luxury into sacred philanthropy and high healing insight."},
            "6_3": {"poorak": 7, "peacemaker_planet": "Ketu (South Node)", "rationale": "Number 7 harmonizes Venus-Jupiter 36 ka aankda through spiritual detachment and deep holistic research."},
            "4_4": {"poorak": 6, "peacemaker_planet": "Venus (Shukra)", "rationale": "Number 6 cools dual Rahu erratic disruptions with domestic peace, artistic elegance, and luxury comfort."},
            "4_8": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 breaks Rahu-Saturn dark karmic stagnation through light commercial movement and flexible trading."},
            "8_4": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 introduces agile communication to Saturn-Rahu heavy delays, unlocking contractual progress."},
            "4_9": {"poorak": 6, "peacemaker_planet": "Venus (Shukra)", "rationale": "Number 6 cools Rahu-Mars Angarak combative tension with diplomatic charm and aesthetic pacing."},
            "9_4": {"poorak": 6, "peacemaker_planet": "Venus (Shukra)", "rationale": "Number 6 tempers Mars-Rahu surgical aggression with peaceful luxury and balanced restraint."},
            "6_9": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 grounds Venus-Mars passion scandal risk through sharp intellect, witty communication, and objective logic."},
            "9_6": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 channels Mars-Venus volatile emotional friction into active commercial marketing and creative trade."},
            "7_7": {"poorak": 1, "peacemaker_planet": "Sun (Surya)", "rationale": "Number 1 gives a sovereign executive head and clear goal direction to dual headless Ketus."},
            "8_8": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 relieves double Saturn heavy labor with commercial ease, trade agility, and intellectual joy."},
            "9_9": {"poorak": 1, "peacemaker_planet": "Sun (Surya)", "rationale": "Number 1 channels double Mars volcanic anger into righteous sovereign leadership and noble public service."}
        }
    }


