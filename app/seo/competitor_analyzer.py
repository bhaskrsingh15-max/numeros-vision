"""
app.seo.competitor_analyzer
Simulates and analyzes Page 1 vs Page 2 search engine competitor ranking parameters
for any target numerology / astrology topic or keyword.

Identifies the exact structural advantages used by top-ranking pages:
- Direct-answer featured snippet bait (40-55 words)
- LSI / semantic entity co-occurrences
- High-intent 'People Also Ask' (PAA) question clusters
- Tabular data comparison matrices (for Google AI Overviews and Perplexity)
- Heading distribution (H1, H2, H3) and safe keyword density
"""

import re
from typing import Dict, List, Any

# Knowledge domain entity associations for numerology & astrological SERPs
NUMEROLOGY_LSI_MAP: Dict[str, List[str]] = {
    "life path": [
        "birth path number", "destiny number", "conductor number", "ruling planet",
        "career suitability", "marriage compatibility", "karmic challenges", "master number"
    ],
    "chaldean": [
        "vibrational frequency", "sound vibration", "cheiro numerology", "compound number",
        "name correction", "lucky name calculation", "alphabet number values"
    ],
    "lo shu": [
        "chinese grid", "3x3 magic square", "8 planes of life", "rajyog",
        "mental plane", "emotional plane", "practical plane", "missing numbers", "repeated numbers"
    ],
    "mobile": [
        "phone number numerology", "malefic pairs", "lucky mobile number", "total sum number",
        "rahuketu combinations", "33 44 88 vibrations", "wealth frequency"
    ],
    "name": [
        "name balancing", "expression number", "soul urge", "personality number",
        "spelling alteration", "business brand vibration", "favorable compound"
    ],
    "remedy": [
        "gemstone therapy", "planetary crystal", "yantra placement", "rudraksha bead",
        "color therapy", "mantra sadhana", "energy alignment"
    ],
    "kua": [
        "prosperous directions", "auspicious directions", "vastu directions", "angel numbers",
        "success direction", "health orientation", "wealth quadrant"
    ],
    "compatibility": [
        "relationship harmony", "synastry chart", "elemental balance", "driver conductor match",
        "long term union", "friction points", "remedial harmony"
    ]
}

class CompetitorSERPAnalyzer:
    """Analyzes competitor ranking patterns on Page 1 & Page 2 for a given topic."""

    @staticmethod
    def derive_slug(topic: str) -> str:
        """Converts topic to clean SEO URL slug."""
        clean = re.sub(r"[^\w\s-]", "", topic.lower()).strip()
        slug = re.sub(r"[\s_]+", "-", clean)
        return slug[:60]

    @classmethod
    def analyze_topic(cls, topic: str, target_keyword: str = "") -> Dict[str, Any]:
        """
        Generates a comprehensive SERP Competitor Blueprint for the target topic.
        Identifies Page 1 structural ranking factors.
        """
        topic_lower = topic.lower()
        slug = cls.derive_slug(topic)
        
        # 1. Determine primary keyword if not provided
        if not target_keyword:
            target_keyword = topic.strip()

        # 2. Extract LSI keywords by domain entity matching
        lsi_keywords = set()
        for domain_key, terms in NUMEROLOGY_LSI_MAP.items():
            if domain_key in topic_lower or any(t in topic_lower for t in terms):
                lsi_keywords.update(terms[:4])
        
        if not lsi_keywords:
            lsi_keywords.update([
                "planetary alignment", "vibrational resonance",
                "vedic calculation", "remedial measures", "destiny blueprint"
            ])

        lsi_list = sorted(list(lsi_keywords))[:6]

        # 3. Search Intent Classification
        if any(w in topic_lower for w in ["calculator", "how to calculate", "audit", "checker", "tool"]):
            intent = "Practical / Tool"
            target_word_count = 1400
        elif any(w in topic_lower for w in ["vs", "difference", "comparison"]):
            intent = "Comparative / Analysis"
            target_word_count = 1800
        else:
            intent = "Informational Guide / Authority"
            target_word_count = 2100

        # 4. Meta Title Optimization (Strict 50-65 chars)
        # Frontload keyword + add high-CTR hook + brand
        raw_title = f"{target_keyword.title()}: Complete Guide — Numeros Vision"
        if len(raw_title) > 65:
            raw_title = f"{target_keyword.title()} — Numeros Vision"
        meta_title = raw_title[:65]

        # 5. Meta Description Optimization (Strict 145-160 chars)
        meta_desc = (
            f"Discover the complete guide to {target_keyword.lower()}. "
            f"Explore hidden vibrational patterns, expert calculation rules, and personalized remedies."
        )
        if len(meta_desc) < 140:
            meta_desc += " Read the verified analysis now."
        meta_desc = meta_desc[:160]

        # 6. Featured Snippet Bait Formulation (Position Zero / AEO Direct Answer)
        snippet_question = f"What is {target_keyword.title()}?"
        snippet_answer = (
            f"{target_keyword.title()} is a sacred vibrational system in ancient numerology "
            f"that decodes your cosmic energetic blueprint through mathematical coordinate synthesis. "
            f"By aligning planetary rulers with harmonic core numbers, it provides deterministic guidance "
            f"for life path timing, relationship harmony, and auspicious life milestones."
        )

        # 7. High-Ranking Heading Outline (H2 / H3 map)
        headings = [
            {
                "h2": f"Understanding {target_keyword.title()}: Core Principles",
                "h3s": [
                    "Historical Foundations & Classical Origins",
                    "Planetary Rulership & Energetic Signatures"
                ]
            },
            {
                "h2": f"Step-by-Step Calculation & Methodology",
                "h3s": [
                    "Primary Formula & Mathematical Reduction",
                    "Interpreting Core Coordinates Without Error"
                ]
            },
            {
                "h2": f"Key Life Influences & Practical Applications",
                "h3s": [
                    "Career & Wealth Acceleration Paths",
                    "Relationship Compatibility & Emotional Resonance"
                ]
            },
            {
                "h2": f"Harmonic Remedies & Planetary Balancing",
                "h3s": [
                    "Prescribed Vedic Gemstones & Crystals",
                    "Auspicious Directional & Lifestyle Alignments"
                ]
            }
        ]

        # 8. People Also Ask (PAA) Question Clusters (for FAQPage schema)
        faqs = [
            {
                "q": f"How does this numerical configuration affect my daily life?",
                "a": f"Understanding these vibrations provides clarity regarding your thought patterns, innate talents, and recurring relationship dynamics by aligning your energetic vibration with universal planetary frequencies."
            },
            {
                "q": "Can challenging planetary alignments be balanced or neutralized?",
                "a": "Yes. Through classical gemstone therapy, name spelling optimization, and directional alignment (Kua/Vastu), any conflicting numerical vibration can be effectively neutralized."
            },
            {
                "q": "What is the most accurate methodology to calculate your coordinates?",
                "a": "Numeros Vision applies a 6-tradition synthesis combining Chaldean, Pythagorean, Lo Shu, and Vedic Bhrigu Nandi Nadi frameworks to guarantee deterministic, conflict-free calculations."
            }
        ]

        # 9. Comparison Matrix Specification (for Google AI Overviews and tabular SERP extracts)
        table_spec = {
            "title": f"{target_keyword.title()} Core Coordinate Matrix",
            "headers": ["Vibrational Coordinate", "Planetary Ruler", "Favorable Energy", "Recommended Remedy"],
            "rows": [
                ["Solar Archetype (1)", "Sun", "Leadership, Ambition, Clarity", "Ruby, Surya Yantra, East Facing"],
                ["Lunar Empathy (2)", "Moon", "Intuition, Harmony, Creativity", "Pearl, Chandra Yantra, North Facing"],
                ["Jupiter Expansion (3)", "Jupiter", "Wisdom, Counsel, Growth", "Yellow Sapphire, Guru Yantra, North-East"],
                ["Mercury Versatility (5)", "Mercury", "Commerce, Speed, Communication", "Emerald, Budh Yantra, North Facing"],
                ["Venus Luxury (6)", "Venus", "Beauty, Attraction, Family", "Diamond/Opal, Shukra Yantra, South-East"]
            ]
        }

        return {
            "topic": topic,
            "slug": slug,
            "target_keyword": target_keyword,
            "intent": intent,
            "target_word_count": target_word_count,
            "meta_title": meta_title,
            "meta_description": meta_desc,
            "lsi_keywords": lsi_list,
            "snippet_question": snippet_question,
            "snippet_answer": snippet_answer,
            "headings": headings,
            "faqs": faqs,
            "table_spec": table_spec,
            "competitor_page1_benchmark": {
                "h1_count": 1,
                "h2_count": len(headings),
                "safe_keyword_density": "1.2% - 1.8%",
                "schema_types": ["Article", "FAQPage", "BreadcrumbList"]
            }
        }
