import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

matrix = {
    "version": "1.0.0",
    "framework": "NV THINK™ Logic-to-Psychology Intelligence Framework",
    "governance": "Hypotheses and behavioral expressions, not fixed labels. Context and validation mandatory.",
    "numbers": {
        "1": {
            "planet": "Sun",
            "element": "Fire / Water (Lo Shu North)",
            "traditional_logic": "Origination, supreme autonomy, executive impulse, sovereign individuality.",
            "dimensions": {
                "identity": "Perceives self as an initiator, pioneer, or anchor responsible for forging a distinctive path.",
                "motivation": "Driven by personal autonomy, original creation, and the psychological freedom to act without external permission.",
                "ambition": "Desires sovereign self-mastery and visible recognition for unique contributions or enterprise ownership.",
                "confidence": "Grounded when leading direct action; may experience hidden vulnerability or self-doubt when forced into passive subordinate roles.",
                "communication": "Direct, purposeful, and concise. Prefers setting agendas; may display impatience with circular or redundant conversation.",
                "emotional_responses": "Responds to prolonged pressure by tightening personal control or withdrawing into intense independent effort.",
                "decision_making": "Decisive and action-first; prone to testing hypotheses through execution rather than waiting for exhaustive external consensus.",
                "relationships": "Values respect and mutual autonomy; struggles when a partner or associate attempts to restrict independence or micromanage.",
                "conflict": "Addresses disagreement directly; prefers rapid clarity or clean disengagement over prolonged passive tension.",
                "money": "Views financial capital as a tool for personal autonomy and strategic freedom rather than mere passive security.",
                "career": "Thrives in autonomous executive leadership, solo entrepreneurship, directorship, or cutting-edge architectural initiatives.",
                "leadership": "Commands by personal example and clear vision; needs to consciously practice supportive delegation to prevent burnout.",
                "adaptability": "Rapidly adapts when leading change; can show friction when forced to conform to slow, rigid bureaucratic shifts.",
                "challenges": "Tendency toward isolation, over-functioning, difficulty asking for support, and vulnerability to physical exhaustion.",
                "growth": "Developing strategic delegation, active listening, emotional receptivity, and cultivating collaborative peer partnerships."
            },
            "duality_patterns": [
                {
                    "title": "Sovereign Initiative vs. Isolation Fear",
                    "dynamic": "High outward autonomy coexisting with an internal burden of feeling solely responsible for survival and success."
                },
                {
                    "title": "Decisive Command vs. Delegation Reluctance",
                    "dynamic": "Desire for large-scale enterprise expansion while secretly believing 'if I don't do it myself, it won't be done right'."
                }
            ]
        },
        "2": {
            "planet": "Moon",
            "element": "Water / Earth (Lo Shu SW)",
            "traditional_logic": "Receptivity, partnership, intuitive perception, diplomatic synthesis, emotional resonance.",
            "dimensions": {
                "identity": "Perceives self as an empathetic mediator, intuitive supporter, and harmonious harmonizer of environments.",
                "motivation": "Driven by relational security, genuine emotional connection, and cooperative collaboration.",
                "ambition": "Seeks peaceful influence, trusted partnership, artistic expression, and supportive community impact.",
                "confidence": "Flourishes in supportive, respectful atmospheres; can waver in aggressive, confrontational, or cold corporate settings.",
                "communication": "Gentle, considerate, and diplomatic. Listens deeply; often perceives unspoken nuances and emotional subtexts.",
                "emotional_responses": "Absorbs surrounding atmospheres; under severe pressure may internalize stress, resulting in mood fluctuations or withdrawal.",
                "decision_making": "Intuitive and relational; evaluates how choices will emotionally and practically affect others before finalizing.",
                "relationships": "Loyal, deeply devoted, and sensitive; highly attuned to subtle shifts in affection, tone, or partner consistency.",
                "conflict": "Naturally seeks mediation and consensus; may avoid direct confrontation at the cost of personal needs.",
                "money": "Approaches finances prudently, prioritizing household security, stability, and family protection.",
                "career": "Excels in counseling, psychology, diplomacy, partnership mediation, healthcare, HR, and creative design.",
                "leadership": "Leads through empathy, quiet consensus, moral support, and team cohesion rather than authoritarian command.",
                "adaptability": "Emotionally responsive to change; navigates transitions best when given relational support and clear reassurance.",
                "challenges": "Tendency to over-accommodate, hypersensitivity to criticism, hesitation in claiming credit, and emotional boundary blurring.",
                "growth": "Building robust personal boundaries, asserting independent needs, and honoring emotional intuition without absorbing external panic."
            },
            "duality_patterns": [
                {
                    "title": "Deep Empathy vs. Self-Erasure",
                    "dynamic": "Acute awareness of others' emotional states resulting in neglecting one's own core needs."
                },
                {
                    "title": "Diplomatic Harmony vs. Suppressed Resentment",
                    "dynamic": "Maintaining outward peace while quietly harboring unspoken disappointment."
                }
            ]
        },
        "3": {
            "planet": "Jupiter",
            "element": "Wood (Lo Shu East)",
            "traditional_logic": "Expansion, wisdom, creative expression, optimism, conceptual synthesis, mentoring.",
            "dimensions": {
                "identity": "Perceives self as an educator, creative communicator, joyful explorer, and visionary guide.",
                "motivation": "Driven by knowledge acquisition, joyful self-expression, teaching, and conceptual expansion.",
                "ambition": "Desires intellectual authority, creative legacy, respected advisorship, and widespread inspirational reach.",
                "confidence": "High when sharing ideas, advising, or inspiring; can feel stifled in narrow, repetitive, or joyless administrative roles.",
                "communication": "Expressive, articulate, warm, and engaging. Naturally uses metaphors, humor, and enthusiastic storytelling.",
                "emotional_responses": "Tends to reframe setbacks through positive meaning; under extreme pressure may scatter energy across multiple interests.",
                "decision_making": "Optimistic and conceptually expansive; connects disparate ideas rapidly; benefits from grounded operational checks.",
                "relationships": "Enthusiastic, generous, and stimulating; thrives with partners who appreciate intellectual conversation and emotional warmth.",
                "conflict": "Uses verbal reasoning and philosophical framing to resolve tension; may struggle with cold emotional detachment.",
                "money": "Generous and abundant mindset; tends to invest in education, experiences, and lifestyle; needs structured saving automation.",
                "career": "Ideal for mentorship, public speaking, publishing, legal advisory, creative direction, academia, and executive coaching.",
                "leadership": "Inspires and uplifts through visionary optimism; empowers subordinates through knowledge and enthusiastic encouragement.",
                "adaptability": "Highly adaptable to new intellectual ideas and creative trends; needs discipline to complete multi-year operational cycles.",
                "challenges": "Diffused focus, over-promising, difficulty handling mundane detail, and avoidance of deeper melancholy.",
                "growth": "Developing laser prioritization, finishing commenced projects, and anchoring big philosophies into daily habits."
            },
            "duality_patterns": [
                {
                    "title": "Expansive Vision vs. Scattered Execution",
                    "dynamic": "Conceiving brilliant large-scale frameworks while struggling to sustain the repetitive mundane routines to build them."
                },
                {
                    "title": "Public Optimism vs. Private Restlessness",
                    "dynamic": "Uplifting and advising everyone around them while quietly wrestling with personal focus and direction."
                }
            ]
        },
        "4": {
            "planet": "Rahu",
            "element": "Wood / Earth (Lo Shu SE)",
            "traditional_logic": "Structure, unconventional strategy, methodical resilience, system architecture, ground reality.",
            "dimensions": {
                "identity": "Perceives self as a builder, rigorous realist, strategic problem solver, and defender of functional order.",
                "motivation": "Driven by tangible security, systemic predictability, mastery of complex technical frameworks, and enduring foundations.",
                "ambition": "Seeks unbreakable financial stability, deep domain mastery, operational efficiency, and institutional resilience.",
                "confidence": "Rock-solid when blueprints, data, and processes are verified; can feel uneasy in ambiguous, ungrounded environments.",
                "communication": "Measured, candid, structured, and factual. Focuses on pragmatic implementation rather than airy promises.",
                "emotional_responses": "Contains emotions under pressure; processes difficulties through intensified labor and systematic troubleshooting.",
                "decision_making": "Methodical, deliberate, and risk-calculated; tests structural integrity before committing resources.",
                "relationships": "Dependable, deeply loyal, and protective; shows love through practical acts, reliable presence, and financial safety.",
                "conflict": "Stands firm on verified facts; can become unyielding if challenged without logical evidence or practical alternatives.",
                "money": "Prudent, systematic, and capital-protective; builds wealth through tangible assets, steady compounding, and reserve buffers.",
                "career": "Thrives in system architecture, engineering, finance, legal contracts, real estate, operations, and logistics.",
                "leadership": "Manages through clear standards, accountability, and dependable infrastructure; leads by reliable execution.",
                "adaptability": "Prefers planned, incremental evolution; resists sudden, chaotic shifts that lack logical justification.",
                "challenges": "Rigidity, stubbornness, skepticism, fear of sudden instability, and tendency toward workaholic tendencies.",
                "growth": "Cultivating emotional flexibility, embracing spontaneous moments, and recognizing when 'good enough' is better than perfection."
            },
            "duality_patterns": [
                {
                    "title": "Unconventional Innovation vs. Rigid Need for Control",
                    "dynamic": "Attraction to disruptive unconventional strategies paired with an intense need for strict internal predictability."
                },
                {
                    "title": "Practical Reliability vs. Hidden Burnout",
                    "dynamic": "Being the dependable rock for an entire organization while silently carrying physical and mental strain."
                }
            ]
        },
        "5": {
            "planet": "Mercury",
            "element": "Earth (Lo Shu Center)",
            "traditional_logic": "Adaptability, commerce, rapid communication, intellectual agility, networking, equilibrium.",
            "dimensions": {
                "identity": "Perceives self as an agile communicator, versatile connector, curious explorer, and market-savvy strategist.",
                "motivation": "Driven by dynamic variety, intellectual freedom, commercial velocity, and discovering new horizons.",
                "ambition": "Seeks versatile success, rapid transaction cycles, widespread influence, and freedom from routine monotony.",
                "confidence": "High when navigating fast-changing environments and social networks; drops when confined to rigid repetitive tasks.",
                "communication": "Quick-witted, persuasive, versatile, and highly engaging. Masters multiple communication channels effortlessly.",
                "emotional_responses": "Externalizes stress through rapid activity, multi-tasking, or verbal processing; may exhibit restless nervous energy.",
                "decision_making": "Fast, opportunistic, and calculated; spots market trends quickly; needs discipline to avoid premature pivot fatigue.",
                "relationships": "Engaging, stimulating, and charming; requires intellectual rapport and personal breathing room in intimate bonds.",
                "conflict": "Prefers negotiating and reframing terms; disengages or changes topics if arguments become heavily emotional or bogged down.",
                "money": "Fluid approach to money; skilled in cashflow arbitrage and dynamic commerce; benefits from automated vaulting.",
                "career": "Flourishes in sales, adtech, marketing, trading, international commerce, media, journalism, and dynamic tech startups.",
                "leadership": "Leads through agility, rapid problem-solving, and cross-functional communication; inspires through adaptability.",
                "adaptability": "Supreme adaptability; shifts gears effortlessly and pivots rapidly in volatile circumstances.",
                "challenges": "Restlessness, inconsistency, impatience with long gestation periods, and difficulty sustaining single-point focus.",
                "growth": "Mastering the power of depth over breadth, establishing grounding routines, and committing to long-term compounding."
            },
            "duality_patterns": [
                {
                    "title": "Commercial Agility vs. Restless Dispersion",
                    "dynamic": "High ability to spark profitable opportunities coupled with difficulty staying long enough to harvest full rewards."
                },
                {
                    "title": "Social Connectedness vs. Emotional Detachment",
                    "dynamic": "Knowing hundreds of valuable contacts while feeling deeply understood by only a very select few."
                }
            ]
        },
        "6": {
            "planet": "Venus",
            "element": "Metal (Lo Shu NW)",
            "traditional_logic": "Harmony, aesthetics, domestic responsibility, nurturing, ethical refinement, luxury.",
            "dimensions": {
                "identity": "Perceives self as a guardian of harmony, aesthetic curator, devoted family protector, and provider of comfort.",
                "motivation": "Driven by peaceful domestic stability, beauty, reciprocal affection, and upholding family/community well-being.",
                "ambition": "Desires gracious living, artistic elegance, respected community standing, and a thriving, secure family haven.",
                "confidence": "Radiant when environments are harmonious and loved ones are secure; deeply distressed by domestic discord or ugliness.",
                "communication": "Warm, encouraging, courteous, and diplomatic. Speaks with grace; emphasizes comfort, care, and moral values.",
                "emotional_responses": "Takes personal responsibility for others' happiness; under extreme stress may become overly worried or martyrdom-prone.",
                "decision_making": "Values-aligned and family-conscious; balances aesthetic appeal, ethical integrity, and domestic welfare.",
                "relationships": "Deeply devoted, affectionate, and romantic; expects emotional reciprocity, mutual respect, and shared domestic values.",
                "conflict": "Strives to restore harmony and mutual understanding; can become stubbornly passive-aggressive if deeply hurt or taken for granted.",
                "money": "Appreciates quality, luxury, and comfort; invests in home, hospitality, art, and loved ones; needs to protect emergency savings.",
                "career": "Excels in luxury branding, design, hospitality, healthcare, HR, marriage/family advisory, arts, and relationship consulting.",
                "leadership": "Nurturing, supportive, and values-driven; creates warm, highly loyal team cultures where people feel appreciated.",
                "adaptability": "Adapts smoothly if changes benefit family or group harmony; resists changes that threaten home or relational stability.",
                "challenges": "Over-possessiveness, interfering out of 'love', difficulty saying no, and carrying burdens that belong to others.",
                "growth": "Allowing loved ones to face their own lessons, releasing the need to control domestic outcomes, and self-care prioritization."
            },
            "duality_patterns": [
                {
                    "title": "Selfless Caregiving vs. Quiet Resentment",
                    "dynamic": "Giving lavishly to partners, children, or teams while secretly yearning for equal unprompted care in return."
                },
                {
                    "title": "Aesthetic Perfection vs. Messy Reality",
                    "dynamic": "Craving idealized domestic and professional harmony while struggling to accept inevitable human flaws."
                }
            ]
        },
        "7": {
            "planet": "Ketu",
            "element": "Metal (Lo Shu West)",
            "traditional_logic": "Introspection, analytical depth, spiritual seeking, non-conformity, research, truth.",
            "dimensions": {
                "identity": "Perceives self as an independent thinker, truth seeker, analytical observer, and guardian of profound depth.",
                "motivation": "Driven by understanding the underlying truth, spiritual insight, intellectual mastery, and quiet mental autonomy.",
                "ambition": "Seeks technical or spiritual mastery, profound philosophical realization, respected expertise, and inner peace.",
                "confidence": "Grounded in private research, solitude, and verified knowledge; uncomfortable with superficial social banter.",
                "communication": "Measured, quiet, insightful, and penetrating. Speaks only when having something substantive to contribute.",
                "emotional_responses": "Withdraws into solitude to process stress; may appear detached or aloof while internal mental processing is intense.",
                "decision_making": "Deeply analytical, investigative, and intuitive; questions surface appearances and searches for root causes.",
                "relationships": "Selectivity in intimacy; requires shared intellectual/spiritual depth and respect for solitude; highly guarded at first.",
                "conflict": "Analyzes the philosophical root of conflict; detaches emotionally from screaming matches; may exit without prolonged drama.",
                "money": "Detached yet observant; values financial sufficiency for independence rather than conspicuous vanity; can alternate between saving and apathy.",
                "career": "Ideal for data science, investigative research, philosophy, psychology, esoteric studies, spiritual coaching, and technical audit.",
                "leadership": "Leads through specialist expertise, calm objective analysis, and ethical integrity; not a loud cheerleader.",
                "adaptability": "Internally flexible due to spiritual detachment; can feel disoriented in noisy, chaotic, high-density environments.",
                "challenges": "Excessive skepticism, emotional isolation, social aloofness, over-intellectualization, and cynicism.",
                "growth": "Sharing wisdom openly, staying grounded in physical reality, and allowing warmth into close relationships."
            },
            "duality_patterns": [
                {
                    "title": "Desire for Deep Connection vs. Fear of Intimacy Intrusion",
                    "dynamic": "Craving profound soul-level companionship while fiercely defending personal solitude and privacy."
                },
                {
                    "title": "Acute Intuitive Insight vs. Paralyzing Skepticism",
                    "dynamic": "Sensing truths instantly but over-analyzing them with clinical doubt until the moment to act passes."
                }
            ]
        },
        "8": {
            "planet": "Saturn",
            "element": "Earth (Lo Shu NE)",
            "traditional_logic": "Endurance, karma, institutional authority, material mastery, systematic discipline, justice.",
            "dimensions": {
                "identity": "Perceives self as a serious builder, steward of large resources, enduring survivor, and guardian of accountability.",
                "motivation": "Driven by long-term financial security, tangible mastery, institutional respect, and building lasting legacies.",
                "ambition": "Seeks commanding industry authority, substantial asset wealth, organizational governance, and self-sufficient independence.",
                "confidence": "Built through surviving tough trials and proven execution; dislikes unearned praise or superficial flattery.",
                "communication": "Direct, economical, serious, and authoritative. Focuses on outcomes, metrics, timelines, and commitments.",
                "emotional_responses": "Contains vulnerability stoically; takes on heavy responsibilities during crises; rarely displays public weakness.",
                "decision_making": "Strategic, cautious, and long-term oriented; weighs risk-reward meticulously; plans for worst-case contingencies.",
                "relationships": "Deeply loyal, steadfast, and protective; takes time to trust; expresses devotion through dependable financial and life security.",
                "conflict": "Unflinching in confrontation; relies on contractual clarity, evidence, and patience to outlast opponents.",
                "money": "Meticulous money manager; understands compounding, asset accumulation, and cost discipline; guards against financial vulnerability.",
                "career": "Dominates in enterprise scaling, heavy industry, real estate, legal governance, banking, corporate restructuring, and judiciary.",
                "leadership": "Authoritative, demanding, fair, and disciplined; holds high standards for self and team; rewards genuine loyalty and grit.",
                "adaptability": "Methodical transition planner; shifts strategy when structural data dictates, but refuses to be stampeded into panic.",
                "challenges": "Pessimism, difficulty relaxing, holding grudges, feeling victimized by heavy responsibility, and emotional aloofness.",
                "growth": "Practicing forgiveness, celebrating small wins, delegating tasks without suspicion, and allowing lighthearted joy into life."
            },
            "duality_patterns": [
                {
                    "title": "Immense Inner Power vs. Lingering Inadequacy Fear",
                    "dynamic": "Projecting unshakeable executive authority while secretly fearing that one slip-up will collapse the entire edifice."
                },
                {
                    "title": "Steadfast Loyalty vs. Unforgiving Resentment",
                    "dynamic": "Giving years of unwavering commitment to a cause or person, but cutting them off completely if betrayed."
                }
            ]
        },
        "9": {
            "planet": "Mars",
            "element": "Fire (Lo Shu South)",
            "traditional_logic": "Courage, universal humanitarianism, passionate vitality, completion, protective defense.",
            "dimensions": {
                "identity": "Perceives self as a passionate crusader, protector of the vulnerable, warrior for justice, and charismatic catalyst.",
                "motivation": "Driven by righteous causes, transformative impact, defending principles, and bringing full cycles to completion.",
                "ambition": "Seeks significant global or social influence, heroic accomplishments, public distinction, and moral leadership.",
                "confidence": "High-octane and fearless when fighting for a cause or facing direct challenges; can feel frustrated when idle.",
                "communication": "Passionate, commanding, energetic, and candid. Speaks with emotional resonance and inspirational fire.",
                "emotional_responses": "High emotional intensity; may react with sudden fiery indignation when observing injustice or disloyalty, followed by quick recovery.",
                "decision_making": "Courageous, values-first, and instinctual; willing to take bold risks for significant outcomes.",
                "relationships": "Generous, protective, and ardent; demands honesty and shared passion; deeply hurt by petty deception.",
                "conflict": "Confronts injustice head-on with courage; fights for principles; needs to avoid escalating minor frictions into major battles.",
                "money": "Generous with wealth; uses money to fund ventures and support others; needs structured savings to avoid impulsive depletion.",
                "career": "Excels in entrepreneurship, sports/fitness, defense, civil advocacy, public relations, politics, surgery, and emergency response.",
                "leadership": "Charismatic, courageous, and inspiring; leads from the front lines; rallies teams to overcome impossible odds.",
                "adaptability": "Resilient in crisis situations; handles sudden disruptions with warrior courage; finds slow bureaucracy irritating.",
                "challenges": "Hot temper, impatience with incompetence, burnout from taking on too many battles, and difficulty letting go of the past.",
                "growth": "Channeling passion into cool strategic execution, practicing patience with slower peers, and mastering emotional restraint."
            },
            "duality_patterns": [
                {
                    "title": "Universal Compassion vs. Fiery Aggression",
                    "dynamic": "Deep love for humanity paired with sudden explosive anger when dealing with petty individual selfishness."
                },
                {
                    "title": "Heroic Armor vs. Vulnerable Need for Appreciation",
                    "dynamic": "Fighting battles for everyone else while privately feeling lonely and unappreciated for the sacrifices made."
                }
            ]
        }
    }
}

output_path = os.path.join('data', 'knowledge_base', 'nv_psychology_matrix.json')
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(matrix, f, indent=2, ensure_ascii=False)

print(f"Generated complete NV THINK™ Psychological & Behavioral Knowledge Matrix: {output_path}")
print(f"Numbers documented: {list(matrix['numbers'].keys())}")
print(f"Dimensions per number: 15 core dimensions + duality patterns")
