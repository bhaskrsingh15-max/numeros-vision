import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def ingest_market_correlation():
    corpus_file = BASE_DIR / "data" / "knowledge_base" / "numeros_vision_corpus.json"
    data_file = BASE_DIR / "data" / "numerobuilder_extracted_data.json"

    if not corpus_file.exists():
        print(f"Error: Corpus file not found at {corpus_file}")
        return

    with open(corpus_file, "r", encoding="utf-8") as f:
        corpus = json.load(f)

    # Check if already ingested
    existing_sources = set(p.get("source", "") for p in corpus.get("passages", []))
    if "Market Correlation Engine: NumeroBuilder Benchmark" in existing_sources:
        print("Market correlation passages already present in corpus. Skipping addition.")
        return

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    passages = []
    planets = data.get("PLANET_BY_NUMBER", {})

    # 1. 81 Mulank-Bhagyank Combinations
    stars = data.get("MULANK_BHAGYANK_STARS", {})
    compat = data.get("COMPAT_PERCENT", {})

    for m in range(1, 10):
        sm = str(m)
        combo_dict = data.get(f"MULANK{m}_COMBO_TEXT", {})
        for b in range(1, 10):
            sb = str(b)
            text = combo_dict.get(sb, "")
            st = stars.get(sm, {}).get(sb, "3")
            pct = compat.get(f"{sm}-{sb}", "N/A")
            if text and isinstance(text, str):
                passages.append({
                    "source": "Market Correlation Engine: NumeroBuilder Benchmark",
                    "location": f"Combination Matrix - Driver {m} ({planets.get(sm)}) & Conductor {b} ({planets.get(sb)})",
                    "provenance": "verified_numeros_vision_market_correlation",
                    "content": f"Mulank {m} (Ruled by {planets.get(sm)}) with Bhagyank {b} (Ruled by {planets.get(sb)}) Combination: "
                               f"Compatibility: {pct}%, Rating: {st} Stars. Core Predictive Trajectory: {text.strip()}"
                })

    # 2. 9 Missing Number Remedies
    missing = data.get("LOSHU_MISSING_REMEDIES", {})
    for num in range(1, 10):
        s = str(num)
        rem = missing.get(s, {})
        if rem:
            passages.append({
                "source": "Market Correlation Engine: NumeroBuilder Benchmark",
                "location": f"Lo Shu Grid Missing Number Remedies - Digit {num} ({planets.get(s)})",
                "provenance": "verified_numeros_vision_market_correlation",
                "content": f"Lo Shu Missing Number {num} Protocol ({rem.get('title', '')}): {rem.get('body', '').strip()} "
                           f"Numeros Vision Correlation Note: Classical verification requires checking Driver-Conductor planetary harmony before applying Sun/Mars/Saturn remedies."
            })

    # 3. Health & Body Chemistry
    for num in range(1, 10):
        s = str(num)
        h = data.get(f"HEALTH_MULANK{num}", {})
        if h:
            passages.append({
                "source": "Market Correlation Engine: NumeroBuilder Benchmark",
                "location": f"Health & Body Chemistry - Mulank {num} ({planets.get(s)})",
                "provenance": "verified_numeros_vision_market_correlation",
                "content": f"Health and Body Chemistry for Mulank {num} ({planets.get(s)}): {h.get('body', '').strip()} "
                           f"Healing Mantra: {h.get('mantra', '')} - Chanting Instructions: {h.get('chantInstructions', '')}"
            })

    # 4. Career & Industry Classifications
    careers = data.get("BHAGYANK_CAREER_DATA", {})
    for num in range(1, 10):
        s = str(num)
        c_list = careers.get(s, [])
        if c_list:
            passages.append({
                "source": "Market Correlation Engine: NumeroBuilder Benchmark",
                "location": f"Career & Industry Classifications - Bhagyank {num} ({planets.get(s)})",
                "provenance": "verified_numeros_vision_market_correlation",
                "content": f"Recommended Professional Industries for Bhagyank {num} ({planets.get(s)}): {', '.join(c_list)}. "
                           f"Vocational orientation combines executive leadership, structured compounding, and karmic alignment."
            })

    # 5. Personal Year Forecasts (Mulank 1-9 x Personal Year 1-9)
    py = data.get("PERSONAL_YEAR_PREDICTIONS", {})
    for m_num in range(1, 10):
        sm = str(m_num)
        m_py = py.get(sm, {})
        years = m_py.get("years", {})
        for y_num, y_data in years.items():
            tag = y_data.get("tag", "")
            text = y_data.get("text", "")
            passages.append({
                "source": "Market Correlation Engine: NumeroBuilder Benchmark",
                "location": f"Personal Year Cycle - Mulank {m_num} in Personal Year {y_num}",
                "provenance": "verified_numeros_vision_market_correlation",
                "content": f"Mulank {m_num} ({planets.get(sm)}) experiencing Personal Year {y_num} ({tag}): {text.strip()} "
                           f"Energy Cycle Analysis: Transition from ideation to compounding and spiritual recalibration."
            })

    # 6. Mobile Numerology Pairs
    mn = data.get("MN_COMBO_MEANINGS", {})
    for pair, info in mn.items():
        passages.append({
            "source": "Market Correlation Engine: NumeroBuilder Benchmark",
            "location": f"Mobile Numerology 2-Digit Combination - Pair {pair}",
            "provenance": "verified_numeros_vision_market_correlation",
            "content": f"Mobile Number Pair '{pair}' Vibration [{info.get('type', 'neutral').upper()}]: {info.get('text', '')}. "
                       f"Reveals financial flow, relationship stability, court/legal risk, or sudden career shifts."
        })

    # 7. Born Special Day Traits (1 to 31)
    born = data.get("BORN_SPECIAL_1_31", {})
    for day in range(1, 32):
        s = str(day)
        trait = born.get(s, "")
        if trait:
            passages.append({
                "source": "Market Correlation Engine: NumeroBuilder Benchmark",
                "location": f"Born Special Day Traits - Birth Day {day}",
                "provenance": "verified_numeros_vision_market_correlation",
                "content": f"Birth Day {day} Psychic Vibration and Specific Personality Traits: {trait.strip()}"
            })

    # 8. Ishta Devata & Fasting Rituals
    deities = data.get("DEITY_BY_MULANK", {})
    fasting = data.get("FASTING_BY_MULANK", {})
    bracelets = data.get("BRACELET_BY_MULANK", {})
    yantras = data.get("YANTRA_BY_MULANK", {})
    mantras = data.get("MANTRA_BY_MULANK", {})

    for num in range(1, 10):
        s = str(num)
        d_obj = deities.get(s, {})
        f_obj = fasting.get(s, {})
        b_obj = bracelets.get(s, {})
        passages.append({
            "source": "Market Correlation Engine: NumeroBuilder Benchmark",
            "location": f"Spiritual Remedies & Sacred Geometry - Mulank {num} ({planets.get(s)})",
            "provenance": "verified_numeros_vision_market_correlation",
            "content": f"Spiritual Prescriptions for Mulank {num} ({planets.get(s)}): "
                       f"Ishta Devata: {d_obj.get('heading', '')} - {d_obj.get('body', '')[:300]} "
                       f"Fasting (Vrat) Ritual: {f_obj.get('heading', '')} - {f_obj.get('body', '')[:300]} "
                       f"Prescribed Healing Bracelet: {', '.join(b_obj.get('items', []))} (Benefit: {b_obj.get('benefit', '')}). "
                       f"Sacred Yantra: {yantras.get(s, '')}. Vedic Beej Mantra: {mantras.get(s, '')} (108x daily)."
        })

    # 9. Kua Directional Formulas (1 to 9)
    kua = data.get("KUA_DIRECTIONS_TEXT", {})
    for num in range(1, 10):
        s = str(num)
        text = kua.get(s, "")
        if text:
            passages.append({
                "source": "Market Correlation Engine: NumeroBuilder Benchmark",
                "location": f"Kua Feng Shui Directional Compass - Kua {num}",
                "provenance": "verified_numeros_vision_market_correlation",
                "content": f"Feng Shui Kua Number {num} Directional Alignment: {text.strip()}"
            })

    # 10. Zodiac Rudraksha
    rudraksha = data.get("RUDRAKSH_BY_ZODIAC", {})
    for sign, r in rudraksha.items():
        passages.append({
            "source": "Market Correlation Engine: NumeroBuilder Benchmark",
            "location": f"Astrological Rudraksha Prescriptions - Western Zodiac {sign}",
            "provenance": "verified_numeros_vision_market_correlation",
            "content": f"Rudraksha Prescription for Western Sun Sign {sign}: Recommended {r}. Helps balance planetary transit pressures and align cosmic vitality."
        })

    # 11. Compound Numbers (10 to 71)
    compounds = data.get("COMPOUND_NUMBER_DATA", {})
    for c_num, c_data in compounds.items():
        if isinstance(c_data, dict):
            c_text = f"Archetype: {c_data.get('title', '')}. Meaning: {c_data.get('body', '')}"
        else:
            c_text = str(c_data)
        passages.append({
            "source": "Market Correlation Engine: NumeroBuilder Benchmark",
            "location": f"Chaldean Compound Numbers - Number {c_num}",
            "provenance": "verified_numeros_vision_market_correlation",
            "content": f"Chaldean Compound Number {c_num} Occult Significance: {c_text.strip()[:800]}"
        })

    # Append to corpus
    corpus["passages"].extend(passages)
    corpus["total_passages"] = len(corpus["passages"])
    all_sources = set(p.get("source", "") for p in corpus["passages"])
    corpus["sources_count"] = len(all_sources)

    with open(corpus_file, "w", encoding="utf-8") as f:
        json.dump(corpus, f, indent=2, ensure_ascii=False)

    print(f"Successfully appended {len(passages)} market correlation passages to {corpus_file}!")
    print(f"New total passages: {corpus['total_passages']}, Sources: {corpus['sources_count']}")

if __name__ == "__main__":
    ingest_market_correlation()
