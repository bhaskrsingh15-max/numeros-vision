from typing import Dict, Any, List
from app.engine.rag_retriever import rag_engine

PLANETARY_RULERS = {
    1: "Sun (Surya)",
    2: "Moon (Chandra)",
    3: "Jupiter (Guru)",
    4: "Rahu (North Node)",
    5: "Mercury (Budh)",
    6: "Venus (Shukra)",
    7: "Ketu (South Node)",
    8: "Saturn (Shani)",
    9: "Mars (Mangal)"
}

FRIENDLY_NUMBERS = {
    1: [1, 2, 3, 5, 9],
    2: [1, 2, 3, 5],
    3: [1, 2, 3, 5, 7, 9],
    4: [1, 5, 6, 7],
    5: [1, 2, 3, 5, 6],
    6: [5, 6, 8],
    7: [1, 3, 4, 5],
    8: [5, 6],
    9: [1, 3, 5, 9]
}

ENEMY_NUMBERS = {
    1: [8],
    2: [8, 4, 9],
    3: [6],
    4: [2, 8, 9],
    5: [],
    6: [3],
    7: [8],
    8: [1, 2, 4, 8],
    9: [2, 4]
}

def reduce_to_single_digit(num: int) -> int:
    while num > 9:
        num = sum(int(digit) for digit in str(num))
    return num

def calculate_mulank(day: int) -> int:
    """Mulank (Driver Number): derived from the day of birth."""
    return reduce_to_single_digit(day)

def calculate_bhagyank(day: int, month: int, year: int) -> int:
    """Bhagyank (Conductor Number): derived from full DD/MM/YYYY."""
    total = day + month + sum(int(d) for d in str(year))
    return reduce_to_single_digit(total)

def get_numeros_vision_insights(driver: int, conductor: int) -> List[Dict[str, Any]]:
    query_str = f"Driver {driver} Conductor {conductor} combination career health personality"
    passages = rag_engine.query(query_str, top_k=3)
    return passages

def analyze_vedic_numerology(day: int, month: int, year: int) -> Dict[str, Any]:
    from app.engine.cheiro_engine import analyze_birth_day_cheiro, analyze_dob_conductor_cheiro
    
    driver = calculate_mulank(day)
    conductor = calculate_bhagyank(day, month, year)
    
    cheiro_day = analyze_birth_day_cheiro(day)
    cheiro_cond = analyze_dob_conductor_cheiro(day, month, year)
    
    insights = get_numeros_vision_insights(driver, conductor)
    
    return {
        "driver_number": driver,
        "driver_planet": PLANETARY_RULERS[driver],
        "conductor_number": conductor,
        "conductor_planet": PLANETARY_RULERS[conductor],
        "cheiro_day_compound": cheiro_day,
        "cheiro_conductor_compound": cheiro_cond,
        "friendly_numbers": FRIENDLY_NUMBERS[driver],
        "enemy_numbers": ENEMY_NUMBERS[driver],
        "combination_key": f"{driver}-{conductor}",
        "grounded_passages": [
            {
                "source": p["source"],
                "location": p["location"],
                "content": p["content"]
            } for p in insights
        ]
    }

if __name__ == "__main__":
    # Test with birth date 15/08/1995 -> Day 15 (Mulank 6), Month 8, Year 1995 -> Total 15+8+24=47 -> 11 -> 2
    res = analyze_vedic_numerology(15, 8, 1995)
    print("Vedic Numerology Analysis:")
    print(f"Driver: {res['driver_number']} ({res['driver_planet']})")
    print(f"Conductor: {res['conductor_number']} ({res['conductor_planet']})")
    print(f"Retrieved Numeros Vision Passages: {len(res['grounded_passages'])}")
