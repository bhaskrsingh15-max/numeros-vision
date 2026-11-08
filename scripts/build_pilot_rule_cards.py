import json
import os

PILOT_RULE_CARDS = {
    "metadata": {
        "title": "NV THINK™ Pilot Rule Cards (Mulank 1 to 9)",
        "version": "1.0.0",
        "governing_rules": "AGENTS.md Section 6 & .agents/rules/nv_think_framework.md",
        "validation_status": "untested",
        "prediction_eligibility": "blocked",
        "reviewed_sources": [
            "Aleka Ghose: Chaldean Numerology Study Notes (EEKAPARNIKA, pp. 12-25, 37-57)",
            "Cooper: Chaldean Numerology Name Analysis (Chaldean Planetary Matrices)",
            "Richard Webster: Chinese Numerology - The Universal Guide to the Magic Square (1998, Lo Shu Planes)",
            "Richard Craze: Practical Numerology (1998, Core Archetypes 1-9)"
        ]
    },
    "cards": {
        "1": {
            "mulank": 1,
            "title": "Mulank 1 — The Sovereign Initiator",
            "logic": {
                "cosmological_principle": "The Monad; the primal point from which all mathematical progression originates.",
                "tradition_attribution": "Chaldean: Sun (Surya). Lo Shu: North coordinate, Water element (Life Path & Vocational Journey). Pythagorean: The point, masculine active principle.",
                "provenance": "Aleka Ghose pp. 13-14; Webster pp. 28-31; Craze pp. 18-19; Cooper matrix."
            },
            "observation": {
                "natal_criteria": "Born on the 1st, 10th, 19th, or 28th of any calendar month.",
                "chart_manifestation": "Single 1 in Lo Shu denotes standard communicative autonomy; repeated 1s (11, 111, 1111) indicate intensifying internal focus on self-directed execution.",
                "compound_sub_variants": {
                    "1": "Pure unitary impulse; uncompromising self-reliance.",
                    "10": "The Wheel of Fortune; completion of past cycle and sovereign fresh origination.",
                    "19": "The Prince of Heaven; high vitality with profound karmic tests of ego balance.",
                    "28": "The Trusting Lamb; executive ambition navigating relational negotiations and partnership dependencies."
                }
            },
            "behaviour": {
                "summary": "Tends to initiate projects independently and prefers setting direction rather than following pre-established consensus. When facing ambiguous tasks, typically creates their own working framework. In collaborative settings, prefers direct, concise communication and takes ownership of critical outcomes, occasionally showing impatience when team pacing lags behind their conceptual roadmap.",
                "workplace_patterns": "Naturally gravitates toward individual contributor leadership, founder roles, or autonomous departmental ownership.",
                "delegation_habits": "Tends to retain architectural control; delegates operational steps while monitoring execution closely.",
                "source_citations": "Aleka Ghose pp. 13-14 (leadership, creation impulse, high ambition); Cooper matrix (sovereign executive drive); Webster pp. 28-31 (vibrational career independence); Craze pp. 18-19 (independent initiative)."
            },
            "psychology": {
                "summary": "Core emotional security is anchored in autonomy and self-determination. The underlying cognitive driver is a need to author one's own trajectory without needing external validation or permission. Under chronic stress, tends to withdraw into solitary problem-solving rather than asking for assistance, as asking for help can internally register as an admission of personal inadequacy or loss of sovereignty.",
                "core_need": "Autonomy and self-directed agency.",
                "vulnerability_trigger": "Being placed in micromanaged or highly constrained administrative environments with zero decision-making authority.",
                "stress_response": "Unilateral decision-making, emotional armor, and accelerated independent exertion.",
                "source_citations": "Aleka Ghose p. 14 (critical self-expectation, intolerance of subordination); Craze p. 19 (fear of dependency); Webster p. 29 (inner drive for individual recognition)."
            },
            "interpretation": {
                "contextual_expression": "In supportive environments with high trust, manifests as an inspiring, generous pioneer who shoulders responsibility effortlessly. In toxic or oppressive environments, can present as aloof, rigid, or defensive, protecting internal autonomy through sharp boundaries.",
                "duality": "Outward executive certainty coexisting with a quiet internal loneliness rooted in the belief that one must always carry the burden alone."
            },
            "conflicts_and_discrepancies": {
                "discrepancies_recorded": [
                    "Elemental Discrepancy: Chaldean / Vedic traditions attribute Fire and the Sun to Number 1, whereas Lo Shu (Webster) assigns Number 1 to the North Water element governing career flow. These are kept distinct: Chaldean explains the fiery initiative, while Lo Shu explains career fluidity.",
                    "Compound 28 Tension: While Craze groups all 1s under pure leadership, Chaldean sources (Ghose p. 37, Cooper) emphasize that 28 brings heavy relational friction (2+8=10=1) where personal drive conflicts with partnership obligations."
                ],
                "resolution": "Zero averaging. The Chaldean planetary ruler (Sun) and Lo Shu elemental vector (Water) operate in parallel as separate diagnostic layers."
            },
            "validation": {
                "status": "untested",
                "notes": "Hypothesis catalogued from reviewed literature. Requires correlation against verified case cohort."
            },
            "prediction": {
                "status": "blocked",
                "notes": "Deterministic predictions based on Mulank 1 are prohibited under NV THINK™ governance."
            }
        },
        "2": {
            "mulank": 2,
            "title": "Mulank 2 — The Diplomatic Harmonizer",
            "logic": {
                "cosmological_principle": "The Dyad; the reflective polarity, reception, duality, and relational balance.",
                "tradition_attribution": "Chaldean: Moon (Chandra). Lo Shu: South-West coordinate, Earth element (Relationships & Domestic Alliances). Pythagorean: Line, feminine receptive principle.",
                "provenance": "Aleka Ghose pp. 14-15; Webster pp. 32-35; Craze pp. 20-21; Cooper matrix."
            },
            "observation": {
                "natal_criteria": "Born on the 2nd, 11th, 20th, or 29th of any calendar month.",
                "chart_manifestation": "Single 2 in Lo Shu indicates intuitive relational awareness; multiple 2s (22, 222) suggest heightened sensitivity to interpersonal atmosphere.",
                "compound_sub_variants": {
                    "2": "Gentle reflective partnership; natural peacemaking.",
                    "11": "Master Number / Lion Muzzled; intense visionary inspiration paired with internal emotional vulnerability.",
                    "20": "The Awakening / Judgement; deep reflective incubation and calling toward collective service.",
                    "29": "The Grace Under Pressure; heavy relational trials testing personal discernment and emotional boundaries."
                }
            },
            "behaviour": {
                "summary": "Tends to approach challenges through mediation, negotiation, and building consensus among stakeholders. Observes subtle group dynamics and tone of voice before offering opinions. Avoids abrupt confrontation, often preferring indirect or quiet diplomacy to resolve friction. In task execution, works well in collaborative tandems and supportive co-pilot roles.",
                "workplace_patterns": "Thrives in diplomatic roles, counseling, mediation, executive partnership, and cross-functional coordination.",
                "delegation_habits": "Shares responsibility comfortably; values reciprocal trust and open feedback over command-and-control oversight.",
                "source_citations": "Aleka Ghose pp. 14-15 (gentle calm nature, emotional attunement, partnership focus); Cooper matrix (diplomatic sensitivity); Webster pp. 32-35 (relational Earth grounding); Craze pp. 20-21 (peacemaking instinct)."
            },
            "psychology": {
                "summary": "Core emotional stability is tethered to relational harmony and psychological safety. Deeply attuned to environmental mood, often absorbing ambient tension without conscious intent. When conflict erupts, the initial instinct is to de-escalate or accommodate, occasionally at the expense of asserting personal boundaries, because discord can feel like an existential threat to stability.",
                "core_need": "Harmonious connection, emotional validation, and peaceful equilibrium.",
                "vulnerability_trigger": "Aggressive, high-conflict environments with overt hostility or dismissive communication.",
                "stress_response": "Passive withdrawal, internal rumination, emotional hesitation, or over-accommodation.",
                "source_citations": "Aleka Ghose p. 15 (cold calm Moon, high emotional receptivity); Craze p. 21 (fear of discord and rejection); Webster p. 33 (desire for relational security)."
            },
            "interpretation": {
                "contextual_expression": "In respectful, emotionally mature environments, acts as an indispensable cultural anchor and strategic diplomat. In chaotic or hostile environments, may become indecisive, overly defensive, or anxious.",
                "duality": "Exceptional empathic insight into others coexisting with difficulty clarifying and communicating one's own immediate needs."
            },
            "conflicts_and_discrepancies": {
                "discrepancies_recorded": [
                    "Master Number Reduction: Western traditions (Craze) preserve 11 as a pure Master Number without single-digit reduction. Chaldean / Vedic systems (Ghose, Cooper) reduce 11 to root 2 for planetary rulership (Moon) while evaluating 11 as a potent compound indicator.",
                    "Elemental Discrepancy: Chaldean links 2 to Water (Moon), whereas Lo Shu places 2 in South-West Earth. Reconciled: Water represents emotional fluidity; Earth represents relational stability."
                ],
                "resolution": "Both compound status (11) and root planet (2/Moon) are stored. Zero blending of reduction methods."
            },
            "validation": {
                "status": "untested",
                "notes": "Hypothesis catalogued from reviewed literature. Requires correlation against verified case cohort."
            },
            "prediction": {
                "status": "blocked",
                "notes": "Deterministic predictions based on Mulank 2 are prohibited under NV THINK™ governance."
            }
        },
        "3": {
            "mulank": 3,
            "title": "Mulank 3 — The Expressive Strategist",
            "logic": {
                "cosmological_principle": "The Triad; synthesis of duality, creative expansion, conceptual expression, and wisdom.",
                "tradition_attribution": "Chaldean: Jupiter (Guru / Brihaspati). Lo Shu: East coordinate, Wood element (Family, Ancestral Heritage & Mental Growth). Pythagorean: The triangle, first complete geometric plane.",
                "provenance": "Aleka Ghose pp. 16-17; Webster pp. 36-39; Craze pp. 22-23; Cooper matrix."
            },
            "observation": {
                "natal_criteria": "Born on the 3rd, 12th, 21st, or 30th of any calendar month.",
                "chart_manifestation": "Single 3 in Lo Shu marks natural conceptual fluency and teaching instinct; multiple 3s (33, 333) indicate intense communicative output with potential scattering.",
                "compound_sub_variants": {
                    "3": "Pure expressive and philosophical optimism; direct advisory impulse.",
                    "12": "The Sacrifice / Reversal; high intellectual creativity tested through overcoming misunderstandings.",
                    "21": "The Crown of the Magi; successful synthesis of artistic insight and long-term public accomplishment.",
                    "30": "The Luminous Mind; profound intellectual and spiritual contemplation, capable of high detachment."
                }
            },
            "behaviour": {
                "summary": "Communicates ideas with enthusiasm, articulate structure, and educational intent. Readily synthesizes complex theoretical concepts into understandable principles. In group settings, often assumes the role of advisor, mentor, or creative catalyst. Paces work in energetic bursts driven by intellectual fascination, occasionally struggling with repetitive operational routine.",
                "workplace_patterns": "Excels in education, advisory consulting, marketing architecture, legal scholarship, publishing, and creative leadership.",
                "delegation_habits": "Prefers communicating the grand vision and theoretical outline, leaving tactical mechanics to operational specialists.",
                "source_citations": "Aleka Ghose pp. 16-17 (Jupiter Guru, knowledge stewardship, optimism, creative speech); Cooper matrix (intellectual pride and executive articulation); Webster pp. 36-39 (Wood growth and conceptual clarity); Craze pp. 22-23 (creative communication)."
            },
            "psychology": {
                "summary": "Core cognitive satisfaction derives from intellectual contribution, teaching, and conceptual freedom. Fears mental confinement, intellectual dismissal, or being trapped in dogmatic routines. When bored or unsupported, can experience restlessness, spreading attention across multiple half-finished ventures rather than consolidating a single path.",
                "core_need": "Self-expression, intellectual recognition, and freedom of conceptual expansion.",
                "vulnerability_trigger": "Having ideas silenced, dismissed as trivial, or forced into rigid rote memorization.",
                "stress_response": "Intellectual rationalization, excessive speech, sarcasm, or scattered focus across too many interests.",
                "source_citations": "Aleka Ghose p. 16 (expansive nature, pride in knowledge); Craze p. 23 (fear of monotony and self-doubt masked by optimism); Webster p. 37 (expressive energy needing grounding)."
            },
            "interpretation": {
                "contextual_expression": "In stimulated, open environments, shines as a visionary thought leader and inspiring mentor. Under restrictive bureaucracy, may become cynical, pedantic, or distracted.",
                "duality": "Public optimism and inspiring articulation coexisting with private periods of intellectual exhaustion and self-critical doubt."
            },
            "conflicts_and_discrepancies": {
                "discrepancies_recorded": [
                    "Discipline vs. Free Expression: Classical Chaldean (Ghose p. 16, Cooper) views Jupiter 3 as an authoritative, disciplined advisor demanding respect. In contrast, modern Western numerology (Craze p. 22) often frames 3 primarily as an easy-going social entertainer or artist.",
                    "Master Number 33: Western tradition reserves 33 as the Master Teacher. Chaldean reduces 33 to 6 (Venus) while evaluating 33's specific karmic burden of self-sacrifice."
                ],
                "resolution": "Both traditions recorded side-by-side. Jupiterian mentorship is prioritized for professional analysis; artistic expression is noted for creative pursuits."
            },
            "validation": {
                "status": "untested",
                "notes": "Hypothesis catalogued from reviewed literature. Requires correlation against verified case cohort."
            },
            "prediction": {
                "status": "blocked",
                "notes": "Deterministic predictions based on Mulank 3 are prohibited under NV THINK™ governance."
            }
        },
        "4": {
            "mulank": 4,
            "title": "Mulank 4 — The Methodical Architect",
            "logic": {
                "cosmological_principle": "The Tetrad; physical foundation, cubic stability, structural order, and boundary enforcement.",
                "tradition_attribution": "Chaldean: Uranus / Rahu (North Node). Lo Shu: South-East coordinate, Wood element (Wealth, Practical Organization & Order). Pythagorean: The square, terrestrial stability.",
                "provenance": "Aleka Ghose pp. 17-18; Webster pp. 40-43; Craze pp. 24-25; Cooper matrix."
            },
            "observation": {
                "natal_criteria": "Born on the 4th, 13th, 22nd, or 31st of any calendar month.",
                "chart_manifestation": "Single 4 in Lo Shu indicates methodical attention to detail and practical realism; multiple 4s (44, 444) suggest profound tenacity with potential risk of excessive rigidity.",
                "compound_sub_variants": {
                    "4": "Structural builder; unyielding loyalty to orderly process.",
                    "13": "The Karmic Upheaval / Transformation; intense breaking of old conventions to build lasting structures.",
                    "22": "Master Builder; translating ambitious humanitarian vision into physical, institutional reality.",
                    "31": "The Methodical Thinker; intellectual precision grounded in practical, cautious execution."
                }
            },
            "behaviour": {
                "summary": "Tends to break down complex goals into systematic, repeatable procedures. Demonstrates exceptional patience for detailed documentation, technical quality, and risk management. Questions unproven shortcuts and sudden shifts in protocol until empirical evidence is presented. In relationships, values reliability, punctual commitments, and demonstrated consistency over charismatic promises.",
                "workplace_patterns": "Excels in systems architecture, engineering, risk management, financial accounting, logistics, and legal compliance.",
                "delegation_habits": "Delegates with explicit criteria and milestones; expects rigorous adherence to agreed-upon procedures.",
                "source_citations": "Aleka Ghose pp. 17-18 (discipline, order, service, hard angles of the number 4); Cooper matrix (unconventional resilience and structural loyalty); Webster pp. 40-43 (practical order and financial accumulation); Craze pp. 24-25 (methodical craftsmanship)."
            },
            "psychology": {
                "summary": "Core emotional calm depends on order, predictability, and reliable boundaries. Chaos, broken agreements, or ambiguous guidelines trigger deep psychological discomfort. To manage uncertainty, constructs detailed plans and contingencies. When pushed to pivot rapidly without rationale, can manifest defensive resistance or stubborn entrenchment as a protective reflex.",
                "core_need": "Structural predictability, stability, and tangible security.",
                "vulnerability_trigger": "Sudden uncoordinated disruption of workflows, broken contracts, or being forced into reckless speculation.",
                "stress_response": "Rigidity, micro-management of minutiae, stubborn silence, or skepticism toward all new ideas.",
                "source_citations": "Aleka Ghose p. 18 (limitation, service, enduring discipline); Craze p. 25 (fear of instability and chaos); Webster p. 41 (pragmatism grounded in caution)."
            },
            "interpretation": {
                "contextual_expression": "In well-structured environments, serves as the unshakeable bedrock that ensures operational viability. Under arbitrary or erratic leadership, can become perceived as obstinate, overly cautious, or unyielding.",
                "duality": "Extraordinary capacity to construct enduring security for others coexisting with an internal fear that the ground beneath one's own feet is fragile."
            },
            "conflicts_and_discrepancies": {
                "discrepancies_recorded": [
                    "Planetary Rulership: Chaldean systems (Cheiro, Ghose p. 17, Cooper) assign Number 4 to Uranus (or Rahu in Vedic astrology), emphasizing sudden unconventional breakthroughs and unconventional perspectives. Modern Western numerology (Craze) emphasizes purely Saturnine/Earthly convention and traditional routine.",
                    "Elemental Discrepancy: Western treats 4 as physical Earth. Lo Shu (Webster) assigns 4 to South-East Wood (wealth accumulation and methodical progress)."
                ],
                "resolution": "Recorded without synthesis: Rahu/Uranus explains the unconventional problem-solving mind; the cubic 4 geometry explains the methodical execution."
            },
            "validation": {
                "status": "untested",
                "notes": "Hypothesis catalogued from reviewed literature. Requires correlation against verified case cohort."
            },
            "prediction": {
                "status": "blocked",
                "notes": "Deterministic predictions based on Mulank 4 are prohibited under NV THINK™ governance."
            }
        },
        "5": {
            "mulank": 5,
            "title": "Mulank 5 — The Adaptable Catalyst",
            "logic": {
                "cosmological_principle": "The Pentad; the central pivot, quintessence, sensory exploration, and dynamic versatility.",
                "tradition_attribution": "Chaldean: Mercury (Budh). Lo Shu: Center coordinate, Earth element (Core Balance, Central Nexus). Pythagorean: The pentagram, human versatility.",
                "provenance": "Aleka Ghose pp. 18-19; Webster pp. 44-47; Craze pp. 26-27; Cooper matrix."
            },
            "observation": {
                "natal_criteria": "Born on the 5th, 14th, or 23rd of any calendar month.",
                "chart_manifestation": "Single 5 in Lo Shu represents core stability and emotional adaptability; multiple 5s (55, 555) indicate rapid sensory processing and high volatility in daily routines.",
                "compound_sub_variants": {
                    "5": "Pure mercurial fluidity; natural trade and networking acuity.",
                    "14": "The Movement / Magnetic Catalyst; dynamic enterprise tested through maintaining focus amidst constant temptation.",
                    "23": "The Royal Star of the Lion; high commercial success and persuasive social charm supported by superiors."
                }
            },
            "behaviour": {
                "summary": "Adapts rapidly to shifting environments, novel information, and diverse cultural contexts. Connects disparate ideas and people with ease. Communicates with persuasive agility, often utilizing humor, storytelling, and quick wit. Paces daily life dynamically, seeking varied projects and resisting prolonged confinement in repetitive desk routines.",
                "workplace_patterns": "Thrives in international business, public relations, investigative media, technology innovation, sales strategy, and travel.",
                "delegation_habits": "Delegates quickly to maintain personal velocity; focuses on new frontiers while leaving operational maintenance to others.",
                "source_citations": "Aleka Ghose pp. 18-19 (Mercury, versatility, multiple career trials, quick intellect); Cooper matrix (commercial acumen and rapid thought); Webster pp. 44-47 (Center stability and freedom of movement); Craze pp. 26-27 (adventurous adaptability)."
            },
            "psychology": {
                "summary": "Core cognitive vitality is stimulated by novelty, exploration, and mental autonomy. Confinement, routine repetition, or heavy micro-management triggers severe claustrophobic anxiety. To preserve personal agency, maintains flexible escape options in commitments. When under prolonged stress, can become distractible, restless, or prone to impulsively abandoning projects at the first sign of monotony.",
                "core_need": "Freedom of movement, cognitive variety, and experiential autonomy.",
                "vulnerability_trigger": "Prolonged physical confinement, repetitive bureaucratic paperwork, or forced long-term lock-in.",
                "stress_response": "Restlessness, impulsive sensory escapism, procrastination on detail work, or sudden career pivoting.",
                "source_citations": "Aleka Ghose p. 19 (restless search for vocational fit, susceptibility to temptation); Craze p. 27 (fear of confinement and monotony); Webster p. 45 (need for balanced center amidst motion)."
            },
            "interpretation": {
                "contextual_expression": "In agile, dynamic environments, operates as a brilliant catalyst, diplomat, and market innovator. In rigid, slow-moving hierarchies, can become erratic, impatient, or disengaged.",
                "duality": "Effortless public charisma and social ease coexisting with an internal difficulty maintaining deep roots or enduring boredom."
            },
            "conflicts_and_discrepancies": {
                "discrepancies_recorded": [
                    "Elemental Discrepancy: Chaldean / Vedic associates Mercury 5 with Air and rapid cognitive trade. Lo Shu (Webster) positions 5 in the exact Earth Center representing grounded stability.",
                    "Lifestyle Stability vs. Restlessness: Aleka Ghose (p. 19) highlights that 5 often changes professions multiple times before finding a niche, whereas Lo Shu treats 5 as the essential balance point needed for all other numbers to function."
                ],
                "resolution": "Reconciled without averaging: 5's internal nature is Mercurial Air/motion; its architectural role in the chart is providing the necessary transitional balance between physical and spiritual planes."
            },
            "validation": {
                "status": "untested",
                "notes": "Hypothesis catalogued from reviewed literature. Requires correlation against verified case cohort."
            },
            "prediction": {
                "status": "blocked",
                "notes": "Deterministic predictions based on Mulank 5 are prohibited under NV THINK™ governance."
            }
        },
        "6": {
            "mulank": 6,
            "title": "Mulank 6 — The Protective Guardian",
            "logic": {
                "cosmological_principle": "The Hexad; harmony, symmetry, domestic sanctuary, communal responsibility, and beauty.",
                "tradition_attribution": "Chaldean: Venus (Shukra). Lo Shu: North-West coordinate, Metal element (Helpful Mentors, Father Figure & Home Protection). Pythagorean: Two interlocking triangles, equilibrium.",
                "provenance": "Aleka Ghose pp. 19-20; Webster pp. 48-51; Craze pp. 28-29; Cooper matrix."
            },
            "observation": {
                "natal_criteria": "Born on the 6th, 15th, or 24th of any calendar month.",
                "chart_manifestation": "Single 6 in Lo Shu marks protective family instinct and aesthetic care; multiple 6s (66, 666) indicate intense caregiving focus with potential for over-involvement in others' lives.",
                "compound_sub_variants": {
                    "6": "Pure Venusian harmony; devotion to family, beauty, and domestic sanctuary.",
                    "15": "The Magician / Alchemical Magnetism; powerful personal charm and creative eloquence, with a warning against misuse of influence.",
                    "24": "The Fortunate Alliance; success achieved through loyal partnerships, family harmony, and supportive patrons."
                }
            },
            "behaviour": {
                "summary": "Tends to focus attention on household comfort, team wellbeing, and aesthetic order in environments. Naturally assumes responsibility for protecting dependents, resolving interpersonal friction, and providing hospitality. Invests significant effort in creating appealing, harmonious surroundings. In professional settings, champions customer care, ethical standards, and cultural cohesion.",
                "workplace_patterns": "Excels in healthcare administration, interior design, culinary arts, hospitality, law, community counseling, and luxury brand stewardship.",
                "delegation_habits": "Delegates cautiously when personal standards of quality or care are at stake; tends to step in and fix details themselves.",
                "source_citations": "Aleka Ghose pp. 19-20 (Venus, refined things, magnetic charm, protective domestic responsibility); Cooper matrix (artistic generosity and familial care); Webster pp. 48-51 (North-West helpful mentors and paternal duty); Craze pp. 28-29 (nurturing responsibility)."
            },
            "psychology": {
                "summary": "Core emotional worth is intimately linked to being needed, trusted, and appreciated by close circles. Vulnerable to boundary absorption, taking on emotional burdens belonging to others and experiencing guilt when stepping back. When relationships fracture or when assistance is unacknowledged, can feel profound grief or slip into martyr-like resentment.",
                "core_need": "Harmonious belonging, aesthetic beauty, and feeling protective utility.",
                "vulnerability_trigger": "Domestic acrimony, betrayal of family loyalty, or feeling unappreciated after heavy personal sacrifice.",
                "stress_response": "Perfectionism, boundary over-extension, intrusive caregiving, or passive-aggressive resentment.",
                "source_citations": "Aleka Ghose p. 20 (high expectations of love and loyalty); Craze p. 29 (difficulty saying no and fear of domestic discord); Webster p. 49 (protective instinct extending to community)."
            },
            "interpretation": {
                "contextual_expression": "In appreciative, healthy family and work environments, operates as a pillar of grace, generosity, and community strength. In codependent or ungrateful settings, can become controlling, anxious, or exhausted.",
                "duality": "Deep capacity to create refuge and unconditional comfort for others coexisting with severe self-critical standards regarding one's own worth."
            },
            "conflicts_and_discrepancies": {
                "discrepancies_recorded": [
                    "Sensory Indulgence vs. Austere Duty: Chaldean sources (Ghose p. 20, Cooper) emphasize Venus 6's love of luxury, fine dining, and romantic attraction. Lo Shu (Webster p. 48) emphasizes North-West Metal's stern, paternal authority and moral duty to family.",
                    "Compound 15: Chaldean highlights 15 as an occult magnetic power capable of extreme commercial or personal persuasion, whereas Western sources treat 15 as a standard familial caregiver."
                ],
                "resolution": "Recorded as dual facets: Venusian aesthetic refinement and Lo Shu paternal duty represent the external and internal faces of Number 6."
            },
            "validation": {
                "status": "untested",
                "notes": "Hypothesis catalogued from reviewed literature. Requires correlation against verified case cohort."
            },
            "prediction": {
                "status": "blocked",
                "notes": "Deterministic predictions based on Mulank 6 are prohibited under NV THINK™ governance."
            }
        },
        "7": {
            "mulank": 7,
            "title": "Mulank 7 — The Contemplative Analyst",
            "logic": {
                "cosmological_principle": "The Heptad; spiritual completion, inner investigation, mystical inquiry, and analytical distillation.",
                "tradition_attribution": "Chaldean: Neptune / Ketu (South Node). Lo Shu: West coordinate, Metal element (Children, Creativity & Introspection). Pythagorean: The sacred number of spiritual perfection.",
                "provenance": "Aleka Ghose pp. 21-22; Webster pp. 52-55; Craze pp. 30-31; Cooper matrix."
            },
            "observation": {
                "natal_criteria": "Born on the 7th, 16th, or 25th of any calendar month.",
                "chart_manifestation": "Single 7 in Lo Shu indicates analytical and introspective inclinations; multiple 7s (77, 777) indicate profound need for solitude with potential detachment from material affairs.",
                "compound_sub_variants": {
                    "7": "Philosophical discernment; quiet investigation and spiritual independence.",
                    "16": "The Shattered Citadel / Tower; intense dismantling of false ego and illusions to reveal durable metaphysical truth.",
                    "25": "The Discriminating Mind; wisdom cultivated through technical study, research, and quiet observation."
                }
            },
            "behaviour": {
                "summary": "Tends to observe situations thoroughly before speaking, preferring deep analysis over surface banter. Asks probing questions aimed at discovering underlying causal mechanisms. Values personal solitude, quiet workspaces, and unhurried intellectual inquiry. Skeptical of unexamined popular opinions; insists on independently testing facts and philosophical theories.",
                "workplace_patterns": "Excels in academic research, forensic data analysis, strategic intelligence, specialized philosophy, software architecture, and spiritual inquiry.",
                "delegation_habits": "Prefers independent research projects; when collaborating, requires collaborators to meet high standards of intellectual rigor.",
                "source_citations": "Aleka Ghose pp. 21-22 (Neptune, analysis, understanding, independent original thought); Cooper matrix (philosophical mysticism and analytical depth); Webster pp. 52-55 (West Metal introspection and learning through life); Craze pp. 30-31 (investigative seeker)."
            },
            "psychology": {
                "summary": "Core mental peace requires uninterrupted solitude, intellectual integrity, and deep existential understanding. Small talk, noisy environments, and superficial social posturing drain cognitive stamina rapidly. Under high stress, tends to detach emotionally and retreat into silent isolation, using intellectual analysis as a protective shield against emotional vulnerability.",
                "core_need": "Intellectual autonomy, truth, quiet reflection, and metaphysical depth.",
                "vulnerability_trigger": "Being crowded, forced into loud superficial networking, or having personal privacy invaded.",
                "stress_response": "Emotional withdrawal, cynical detachment, hyper-critical skepticism, or complete silence.",
                "source_citations": "Aleka Ghose p. 21 (need for quiet contemplation, distinct individuality); Craze p. 31 (fear of emotional exposure and mental shallowness); Webster p. 53 (introverted processing)."
            },
            "interpretation": {
                "contextual_expression": "In peaceful, academically stimulating environments, operates as a brilliant researcher, philosopher, and profound advisor. In intrusive, loud, or chaotic settings, can present as aloof, eccentric, or unapproachable.",
                "duality": "Profound intellectual and spiritual discernment coexisting with difficulty navigating mundane everyday logistics and emotional vulnerability."
            },
            "conflicts_and_discrepancies": {
                "discrepancies_recorded": [
                    "Planetary Rulership: Chaldean systems (Cheiro, Ghose p. 21, Cooper) assign 7 to Neptune (or Ketu in Vedic astrology), highlighting spiritual detachment, psychic sensitivity, and research. Western Pythagorean (Craze) frequently assigns 7 to the Moon/Saturn harmonics of introspection.",
                    "Material Disinterest: Aleka Ghose (p. 22) notes that pure 7s often care little for material accumulation unless it aids research, whereas Lo Shu (Webster p. 52) notes 7's placement in the West Metal plane connects it to creative output that can bear physical fruit."
                ],
                "resolution": "Reconciled without averaging: Neptune/Ketu governs the introspective philosophical impulse; Lo Shu West coordinates explain the creative and analytical output."
            },
            "validation": {
                "status": "untested",
                "notes": "Hypothesis catalogued from reviewed literature. Requires correlation against verified case cohort."
            },
            "prediction": {
                "status": "blocked",
                "notes": "Deterministic predictions based on Mulank 7 are prohibited under NV THINK™ governance."
            }
        },
        "8": {
            "mulank": 8,
            "title": "Mulank 8 — The Strategic Realist",
            "logic": {
                "cosmological_principle": "The Ogdoad; equilibrium between material and spiritual forces, karmic accountability, and executive endurance.",
                "tradition_attribution": "Chaldean: Saturn (Shani). Lo Shu: North-East coordinate, Earth element (Knowledge, Wisdom, Quiet Discipline). Pythagorean: Double square, cosmic justice.",
                "provenance": "Aleka Ghose p. 23; Webster pp. 56-59; Craze pp. 32-33; Cooper matrix."
            },
            "observation": {
                "natal_criteria": "Born on the 8th, 17th, or 26th of any calendar month.",
                "chart_manifestation": "Single 8 in Lo Shu marks methodical financial discipline and structured ambition; multiple 8s (88, 888) indicate heavy administrative burdens and intense karmic responsibility.",
                "compound_sub_variants": {
                    "8": "Direct Saturnine responsibility; disciplined executive stewardship and perseverance.",
                    "17": "The Star of the Magi; public recognition, moral elevation, and enduring spiritual legacy.",
                    "26": "The Heavy Stewardship; commercial and partnership responsibility accompanied by acute lessons in financial prudence."
                }
            },
            "behaviour": {
                "summary": "Tends to view endeavors through the lens of long-term durability, structural feasibility, and return on investment. Exercises disciplined patience, preferring gradual, permanent consolidation over rapid, speculative windfalls. Possesses high endurance in demanding situations. In leadership, holds team members and themselves to rigorous standards of accountability and fair execution.",
                "workplace_patterns": "Excels in corporate governance, financial asset stewardship, large-scale enterprise leadership, judicial law, and industrial management.",
                "delegation_habits": "Delegates based on proven competence; expects transparent reporting and zero excuses regarding deadlines.",
                "source_citations": "Aleka Ghose p. 23 (Saturn, career, finance, discipline, balance of material and spiritual); Cooper matrix (executive realism and karmic endurance); Webster pp. 56-59 (North-East Earth discipline and quiet wisdom); Craze pp. 32-33 (executive mastery)."
            },
            "psychology": {
                "summary": "Core emotional calm is anchored in self-mastery, material stability, and practical control over life conditions. Deeply respects structural law and karmic cause-and-effect. Intensely uncomfortable with dependency or vulnerability. When overwhelmed by responsibility, rarely complains openly; instead, doubles down on effort, potentially exhausting physical vitality while maintaining an impassive exterior.",
                "core_need": "Self-mastery, durable accomplishment, financial autonomy, and structural order.",
                "vulnerability_trigger": "Financial helplessness, institutional betrayal, or being perceived as incompetent or dependent.",
                "stress_response": "Emotional hardening, intense hyper-work, pessimistic realism, and strict control of resources.",
                "source_citations": "Aleka Ghose p. 23 (often misunderstood as cold, yet deeply driven by fairness); Craze p. 33 (fear of vulnerability and economic loss); Webster p. 57 (endurance through quiet discipline)."
            },
            "interpretation": {
                "contextual_expression": "In ethical, meritocratic environments, serves as a fair-minded, formidable leader who constructs enduring institutions. In unfair or corrupt environments, may become cynical, authoritarian, or overly guarded.",
                "duality": "Outward aura of unyielding authority and stoic competence coexisting with an internal sensitivity to early struggles and an acute awareness of mortality."
            },
            "conflicts_and_discrepancies": {
                "discrepancies_recorded": [
                    "Material Power vs. Heavy Karma: Commercial Western numerology (Craze p. 32) frequently brands 8 as purely 'the number of money and power'. In stark contrast, Chaldean sources (Ghose p. 23, Cooper) warn that 8 is fundamentally Saturnine—demanding rigorous moral integrity, where greed triggers severe karmic restitution.",
                    "Elemental Placement: Lo Shu (Webster p. 56) positions 8 in the North-East Earth plane governing contemplative knowledge and spiritual wisdom, not mere commercial trade."
                ],
                "resolution": "Zero averaging. Saturn's karmic balance (material responsibility paired with spiritual integrity) is maintained as the primary interpretive authority."
            },
            "validation": {
                "status": "untested",
                "notes": "Hypothesis catalogued from reviewed literature. Requires correlation against verified case cohort."
            },
            "prediction": {
                "status": "blocked",
                "notes": "Deterministic predictions based on Mulank 8 are prohibited under NV THINK™ governance."
            }
        },
        "9": {
            "mulank": 9,
            "title": "Mulank 9 — The Universal Humanitarian",
            "logic": {
                "cosmological_principle": "The Ennead; the completion of the single-digit cycle, universal synthesis, humanitarian consciousness, and catalytic transformation.",
                "tradition_attribution": "Chaldean: Mars (Mangal). Lo Shu: South coordinate, Fire element (Illumination, Reputation, Fame). Pythagorean: The boundary limit containing all preceding vibrations.",
                "provenance": "Aleka Ghose pp. 23-24; Webster pp. 60-63; Craze pp. 34-35; Cooper matrix."
            },
            "observation": {
                "natal_criteria": "Born on the 9th, 18th, or 27th of any calendar month.",
                "chart_manifestation": "Single 9 in Lo Shu marks idealism, ambition, and social conscience; multiple 9s (99, 999) suggest passionate crusading energy with potential for emotional exhaustion.",
                "compound_sub_variants": {
                    "9": "Pure crusading energy; high moral courage and universal empathy.",
                    "18": "The Spiritual Conflict / Internal Warfare; high worldly ambition tested through deceptive alliances and deep emotional trials.",
                    "27": "The Scepter / Command; courageous intellectual leadership dedicated to higher communal principles."
                }
            },
            "behaviour": {
                "summary": "Tends to orient actions toward broad social impact, moral causes, or institutional reform. Demonstrates spontaneous courage when defending perceived underdogs. Expresses strong opinions directly and passionately. In operational tasks, moves with decisive energy and impatience for petty details. Often struggles to step away from situations that have naturally reached completion.",
                "workplace_patterns": "Excels in social enterprise, legal advocacy, military or emergency leadership, healthcare reform, international NGOs, and high-impact arts.",
                "delegation_habits": "Delegates freely when trusted comrades share the ideological mission; impatient with self-serving or transactional collaborators.",
                "source_citations": "Aleka Ghose pp. 23-24 (Mars, global consciousness, humanitarian reach, non-judgmental empathy); Cooper matrix (fighter energy, moral courage); Webster pp. 60-63 (South Fire illumination and ambition); Craze pp. 34-35 (universal compassion)."
            },
            "psychology": {
                "summary": "Core emotional driver is a commitment to a cause larger than oneself. Deeply empathetic toward collective human suffering, yet can struggle with intimate one-on-one emotional maintenance. Intensely uncomfortable with pettiness, greed, or moral cowardice. When ideals are frustrated, can experience fiery righteous indignation or retreat into disillusioned fatigue.",
                "core_need": "Universal purpose, moral alignment, and broad constructive impact.",
                "vulnerability_trigger": "Witnessing systemic injustice, feeling petty personal greed around them, or having their integrity questioned.",
                "stress_response": "Righteous anger, emotional exhaustion from over-giving, impulsive confrontation, or sudden dramatic closures.",
                "source_citations": "Aleka Ghose p. 24 (least judgmental number, universal empathy); Craze p. 35 (difficulty letting go and personal disillusionment); Webster p. 61 (fiery drive for recognition and purpose)."
            },
            "interpretation": {
                "contextual_expression": "In purposeful, mission-driven environments, acts as an inspiring, courageous reformer who mobilizes collective action. In petty or cynical environments, can become combative, frustrated, or alienated.",
                "duality": "Boundless compassion and crusading generosity for humanity at large coexisting with personal difficulty setting boundaries and managing private vulnerability."
            },
            "conflicts_and_discrepancies": {
                "discrepancies_recorded": [
                    "Planetary Rulership (Mars vs. Universal Compassion): Chaldean and Vedic traditions (Ghose p. 24, Cooper) attribute 9 strictly to Mars (Mangal), highlighting the fierce warrior, fighter, and combative courage. Western traditions (Craze p. 34) describe 9 almost exclusively as a gentle, self-sacrificing humanitarian.",
                    "Elemental Discrepancy: Lo Shu (Webster p. 60) places 9 in the South Fire plane of fame and recognition, reflecting high public visibility rather than private martyrdom."
                ],
                "resolution": "Both traditions recorded explicitly: Mars explains the fiery courage and combativeness; the Ennead completion explains the broad humanitarian perspective."
            },
            "validation": {
                "status": "untested",
                "notes": "Hypothesis catalogued from reviewed literature. Requires correlation against verified case cohort."
            },
            "prediction": {
                "status": "blocked",
                "notes": "Deterministic predictions based on Mulank 9 are prohibited under NV THINK™ governance."
            }
        }
    }
}

def main():
    json_path = 'data/knowledge_base/nv_think_mulank_pilot_cards.json'
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(PILOT_RULE_CARDS, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated {len(PILOT_RULE_CARDS['cards'])} Pilot Rule Cards at {json_path}")

    # Generate Markdown documentation
    md_path = 'docs/NV_THINK_MULANK_PILOT_RULE_CARDS.md'
    os.makedirs(os.path.dirname(md_path), exist_ok=True)
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# NUMEROS VISION — NV THINK™ PILOT RULE CARDS (MULANK 1 TO 9)\n\n")
        f.write("**Version:** 1.0.0  \n")
        f.write("**Effective Date:** 2026-11-08  \n")
        f.write("**Validation Status:** `untested`  \n")
        f.write("**Prediction Eligibility:** `blocked`  \n\n")
        f.write("### Governing Principles\n")
        f.write("- **Zero Model Training / Fine-tuning**: Strictly deterministic and literature-backed.\n")
        f.write("- **Zero Embeddings Generated**: Rule cards are symbolic logic-to-psychology schemas.\n")
        f.write("- **Short Phrases Only**: All behaviour and psychology texts are original syntheses.\n")
        f.write("- **Zero Silent Averaging**: All tradition conflicts are recorded verbatim.\n\n")
        f.write("---\n\n")

        for num_str, card in PILOT_RULE_CARDS['cards'].items():
            f.write(f"## {card['title']}\n\n")
            f.write(f"### 1. LOGIC\n")
            f.write(f"- **Cosmological Principle:** {card['logic']['cosmological_principle']}\n")
            f.write(f"- **Tradition & Astrological Attribution:** {card['logic']['tradition_attribution']}\n")
            f.write(f"- **Provenance:** {card['logic']['provenance']}\n\n")

            f.write(f"### 2. OBSERVATION\n")
            f.write(f"- **Natal Chart Criteria:** {card['observation']['natal_criteria']}\n")
            f.write(f"- **Grid & Repetition Manifestation:** {card['observation']['chart_manifestation']}\n")
            f.write(f"- **Compound Sub-Variants:**\n")
            for k, v in card['observation']['compound_sub_variants'].items():
                f.write(f"  - **Number {k}:** {v}\n")
            f.write("\n")

            f.write(f"### 3. BEHAVIOUR (Observable Operational Expression)\n")
            f.write(f"- **Operational Summary:** {card['behaviour']['summary']}\n")
            f.write(f"- **Workplace & Vocational Patterns:** {card['behaviour']['workplace_patterns']}\n")
            f.write(f"- **Delegation & Execution Style:** {card['behaviour']['delegation_habits']}\n")
            f.write(f"- **Source Citations:** {card['behaviour']['source_citations']}\n\n")

            f.write(f"### 4. PSYCHOLOGY (Cognitive & Emotional Drivers)\n")
            f.write(f"- **Psychological Summary:** {card['psychology']['summary']}\n")
            f.write(f"- **Core Emotional Need:** {card['psychology']['core_need']}\n")
            f.write(f"- **Vulnerability / Threat Trigger:** {card['psychology']['vulnerability_trigger']}\n")
            f.write(f"- **Stress & Defensive Response:** {card['psychology']['stress_response']}\n")
            f.write(f"- **Source Citations:** {card['psychology']['source_citations']}\n\n")

            f.write(f"### 5. INTERPRETATION & CONTEXT\n")
            f.write(f"- **Contextual Expression:** {card['interpretation']['contextual_expression']}\n")
            f.write(f"- **NV THINK™ Duality:** {card['interpretation']['duality']}\n\n")

            f.write(f"### 6. CONTRADICTIONS & DISCREPANCIES (No Silent Averaging)\n")
            for disc in card['conflicts_and_discrepancies']['discrepancies_recorded']:
                f.write(f"- {disc}\n")
            f.write(f"- **Resolution:** {card['conflicts_and_discrepancies']['resolution']}\n\n")

            f.write(f"### 7. VALIDATION & PREDICTION STATUS\n")
            f.write(f"- **Validation Status:** `{card['validation']['status']}` ({card['validation']['notes']})\n")
            f.write(f"- **Prediction Eligibility:** `{card['prediction']['status']}` ({card['prediction']['notes']})\n\n")
            f.write("---\n\n")

    print(f"Successfully generated Markdown documentation at {md_path}")

    # Copy to artifact directory
    artifact_path = r"C:\Users\Bhaskr Singh\.gemini\antigravity\brain\c1ea3ed7-b9d2-437a-b7aa-f0cb4004681b\NV_THINK_MULANK_PILOT_RULE_CARDS.md"
    with open(artifact_path, 'w', encoding='utf-8') as f:
        with open(md_path, 'r', encoding='utf-8') as src:
            f.write(src.read())
    print(f"Copied artifact to {artifact_path}")

if __name__ == '__main__':
    main()
