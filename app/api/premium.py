"""
Premium Subscriber Experience — Charm AI
POST /api/v1/premium/questionnaire/save  → save post-payment questionnaire answers
GET  /api/v1/premium/dashboard           → return personal blueprint (layman language)
POST /api/v1/premium/ask                 → premium AI chat with memory + probing
"""

import os
import json
import time
import hashlib
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/premium", tags=["premium"])

# ── In-memory profile store (Phase 3 will swap to PostgreSQL) ─────────────
_profiles: Dict[str, Dict] = {}

# ── Number meanings — layman language only, NO technical labels ───────────
_LIFE_PATH_MEANING = {
    1: {"theme": "The Pioneer", "energy": "You are a natural leader. You were born to start things, not just manage them. You carry an inner fire that pushes you toward independence and originality. The universe set you on a path where your greatest growth comes from trusting your own instincts."},
    2: {"theme": "The Peacemaker", "energy": "You have a rare gift — the ability to sense what others feel before they say a word. Your path is one of harmony, partnership, and deep emotional intelligence. Your greatest power is not force, it is patience and genuine care."},
    3: {"theme": "The Creative Soul", "energy": "Joy, expression, and creativity are your birthright. You are meant to create — art, ideas, conversation, connection. When you allow yourself to fully express, doors open for you that stay closed for everyone else."},
    4: {"theme": "The Builder", "energy": "You are the foundation that everything else rests on. Stability, loyalty, and hard work are your strengths. The universe asks you to build — slowly, solidly, and with intention. What you build lasts."},
    5: {"theme": "The Explorer", "energy": "Freedom and variety are not just preferences for you — they are necessities. You are at your best when life keeps changing, offering new experiences and new people. Your path is one of constant evolution."},
    6: {"theme": "The Nurturer", "energy": "Love, home, family, and beauty are your natural domain. You carry a deep responsibility energy — you feel happiest when the people around you are well. The universe placed you on Earth to heal, to comfort, and to beautify."},
    7: {"theme": "The Seeker", "energy": "Depth, wisdom, and solitude are your closest companions. You are drawn to understand things at a level most people never reach. Your path is one of inner discovery, and what you find there is more valuable than anything the outside world can offer."},
    8: {"theme": "The Powerhouse", "energy": "Ambition, authority, and abundance are your energy signature. You are meant to accomplish things at scale. Success is not something that happens to you — it is something you build, brick by brick, through focused effort and bold decisions."},
    9: {"theme": "The Visionary", "energy": "You carry the energy of all numbers — wisdom, compassion, and a desire to serve something larger than yourself. Your path is one of completion and contribution. When you give generously, the universe returns it multiplied."},
}

_PERSONALITY_MEANING = {
    1: "You come across as confident, decisive, and self-assured. People instinctively look to you for direction.",
    2: "You appear gentle, approachable, and deeply empathetic. People feel safe sharing their troubles with you.",
    3: "You radiate warmth and charm. People are drawn to your energy — you light up any room you enter.",
    4: "You seem dependable and grounded. People trust you naturally because you are consistent and reliable.",
    5: "You appear vibrant and magnetic. People sense your restless intelligence and find you endlessly interesting.",
    6: "You come across as warm, caring, and responsible. People feel nurtured in your presence.",
    7: "You appear thoughtful and a little mysterious. People sense depth in you even before you speak.",
    8: "You project authority and confidence. People recognise your ambition and respect your drive.",
    9: "You appear compassionate and wise. People come to you with their problems because they trust your perspective.",
}

_LUCKY_COLORS = {
    1: {"primary": "Gold, Orange, Copper", "avoid": "Black, Dark Grey"},
    2: {"primary": "White, Silver, Cream", "avoid": "Deep Red, Black"},
    3: {"primary": "Yellow, Golden Yellow, Purple", "avoid": "Dark Brown"},
    4: {"primary": "Blue-Grey, Electric Blue, Khaki", "avoid": "Bright Red"},
    5: {"primary": "Light Green, Sky Blue, White", "avoid": "Dark Colours in General"},
    6: {"primary": "Pink, Cream, Baby Blue, Pale Green", "avoid": "Dark Black, Maroon"},
    7: {"primary": "Lavender, Violet, Pale White", "avoid": "Dark Red, Orange"},
    8: {"primary": "Dark Blue, Black, Deep Purple", "avoid": "Pale Yellow"},
    9: {"primary": "Red, Crimson, Rose, Coral", "avoid": "Green in Business"},
}

_LUCKY_DAYS = {
    1: "Sunday — the day of the Sun, which fuels your leadership energy",
    2: "Monday — the day of the Moon, which deepens your emotional clarity",
    3: "Thursday — the day of Jupiter, which amplifies your creative expression",
    4: "Saturday and Sunday — both carry stability energy that supports your patient nature",
    5: "Wednesday — the day of Mercury, which sharpens your quick mind and communication",
    6: "Friday — the day of Venus, which enhances your natural warmth and attractiveness",
    7: "Monday — the day of the Moon, which deepens your intuitive and spiritual gifts",
    8: "Saturday — the day of Saturn, which rewards your discipline and hard work",
    9: "Tuesday — the day of Mars, which fuels your courage and drive",
}

_GEMSTONES = {
    1: {"stone": "Ruby or Red Garnet", "benefit": "Boosts your confidence, leadership energy, and vitality. Wear on the ring finger of your right hand.", "day": "Sunday morning"},
    2: {"stone": "Pearl or Moonstone", "benefit": "Brings emotional clarity, inner peace, and stability in relationships. Wear on the little finger.", "day": "Monday morning"},
    3: {"stone": "Yellow Sapphire or Citrine", "benefit": "Attracts wisdom, abundance, and positive opportunities. Wear on the index finger.", "day": "Thursday morning"},
    4: {"stone": "Hessonite (Gomed) or Brown Zircon", "benefit": "Removes obstacles, reduces confusion, and creates mental clarity. Wear on the middle finger.", "day": "Saturday morning"},
    5: {"stone": "Emerald or Green Tourmaline", "benefit": "Sharpens your mind, improves communication, and supports business success. Wear on the little finger.", "day": "Wednesday morning"},
    6: {"stone": "Diamond or White Sapphire", "benefit": "Amplifies love, beauty, prosperity, and grace. Wear on the ring finger.", "day": "Friday morning"},
    7: {"stone": "Cat's Eye or Labradorite", "benefit": "Deepens intuition, spiritual awareness, and protects from negative energy. Wear on the middle finger.", "day": "Monday morning"},
    8: {"stone": "Blue Sapphire (Neelam) or Amethyst", "benefit": "Brings discipline, focus, and long-term financial gains. Only wear after confirming it suits you.", "day": "Saturday morning"},
    9: {"stone": "Red Coral or Carnelian", "benefit": "Ignites courage, drive, and physical energy. Excellent for overcoming delays. Wear on the ring finger.", "day": "Tuesday morning"},
}

_YEAR_THEMES = {
    1: "The Year of New Beginnings — A seed you plant this year will define the next 9 years. Bold new starts are favoured.",
    2: "The Year of Partnerships — Relationships, collaboration, and patience are your themes. What you nurture this year flourishes.",
    3: "The Year of Expression — Creativity, joy, and social connection are at peak energy. Say yes to new experiences.",
    4: "The Year of Building — Hard work brings real, lasting results this year. Focus on foundations, not quick wins.",
    5: "The Year of Change — Expect unexpected shifts — in career, location, or relationships. Embrace, don't resist.",
    6: "The Year of Home and Heart — Family, love, and home matters take centre stage. Service and beauty are your keywords.",
    7: "The Year of Inner Work — Retreat, reflect, and study. The answers you seek are inside, not outside.",
    8: "The Year of Harvest — Financial and professional recognition arrives for work done in the past. Step into your power.",
    9: "The Year of Completion — What no longer serves you must be released. Endings create space for the new cycle ahead.",
}

# ── Probing question sequence (conversational, one at a time) ──────────────
PROBE_QUESTIONS = [
    {
        "id": "birth_place",
        "text": "To give you your most accurate and complete reading, I need a little more from you. Where were you born? Just the city name is perfect.",
        "field": "birth_city"
    },
    {
        "id": "birth_time",
        "text": "Do you know your approximate time of birth? Even a rough range like 'morning', 'afternoon', or 'evening' helps. If you know the actual time, even better.",
        "field": "birth_time"
    },
    {
        "id": "current_city",
        "text": "Where are you based right now? Your current city helps me understand the energy of your present environment.",
        "field": "current_city"
    },
    {
        "id": "life_focus",
        "text": "What area of life feels most pressing for you right now — career, relationships, finances, health, or something else?",
        "field": "topic_priority"
    },
    {
        "id": "life_events",
        "text": "In the last 2 years, has anything major shifted in your life — a job change, a move, a relationship beginning or ending, or a significant health event? You can describe it simply.",
        "field": "life_events_raw"
    },
    {
        "id": "contact",
        "text": "Last thing — your mobile number and email so I can send your complete personal blueprint report and WhatsApp you any time-sensitive guidance.",
        "field": "contact"
    }
]

# ── Request models ─────────────────────────────────────────────────────────
class QuestionnaireRequest(BaseModel):
    premium_token: str
    answers: Dict[str, str]       # field_name → answer string

class PremiumAskRequest(BaseModel):
    premium_token: str
    question: str
    name: Optional[str] = ""
    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None
    conversation_history: Optional[List[Dict]] = []


# ── Endpoints ──────────────────────────────────────────────────────────────

@router.post("/questionnaire/save")
async def save_questionnaire(req: QuestionnaireRequest):
    """Save post-payment questionnaire answers. Enriches the user profile."""
    if not req.premium_token:
        raise HTTPException(status_code=401, detail="Premium token required.")

    existing = _profiles.get(req.premium_token, {})
    existing.update(req.answers)
    existing["updated_at"] = int(time.time())
    _profiles[req.premium_token] = existing

    # Persist
    _persist_profile(req.premium_token, existing)

    return {"status": "saved", "message": "Profile enriched. Your reading will now be even more precise."}


@router.get("/dashboard/{premium_token}")
async def get_dashboard(premium_token: str, day: int = 1, month: int = 1, year: int = 1990):
    """
    Return the full Personal Blueprint in pure layman language.
    NO engine names, NO technical terms — only human-readable insights.
    """
    # ── Calculate personal numbers ─────────────────────────────────────────
    life_path  = _calc_life_path(day, month, year)
    psychic    = _reduce(day)
    name_data  = _profiles.get(premium_token, {})
    full_name  = name_data.get("full_name", "")

    # Current year personal year number
    current_year = time.localtime().tm_year
    personal_year = _reduce(day + month + _digit_sum(current_year))

    lp_info  = _LIFE_PATH_MEANING.get(life_path, _LIFE_PATH_MEANING[1])
    ps_info  = _PERSONALITY_MEANING.get(psychic, _PERSONALITY_MEANING[1])
    colors   = _LUCKY_COLORS.get(life_path, _LUCKY_COLORS[1])
    lucky_day= _LUCKY_DAYS.get(life_path, _LUCKY_DAYS[1])
    gem_info = _GEMSTONES.get(life_path, _GEMSTONES[1])
    yr_theme = _YEAR_THEMES.get(personal_year, _YEAR_THEMES[1])

    # Name energy (simple: if name provided, check if it vibrates well with life path)
    name_verdict = _check_name_energy(full_name, life_path) if full_name else None

    # Angel Numbers & Prosperous Vastu Directions
    from app.engine.core_matrix_engine import ANGEL_NUMBERS_BY_ROOT, get_kua_profile
    angel_data = ANGEL_NUMBERS_BY_ROOT.get(psychic, ANGEL_NUMBERS_BY_ROOT[1])
    kua_prof = get_kua_profile(year, gender=name_data.get("gender"))
    has_kua_gender = kua_prof.get("kua_number") is not None

    return {
        "blueprint": {
            "life_path": {
                "number":  life_path,
                "theme":   lp_info["theme"],
                "insight": lp_info["energy"],
            },
            "personality": {
                "number":  psychic,
                "insight": ps_info,
            },
            "name_energy": name_verdict,
            "lucky": {
                "day":     lucky_day,
                "colors":  colors["primary"],
                "avoid_colors": colors["avoid"],
                "gemstone": gem_info["stone"],
                "gem_benefit": gem_info["benefit"],
                "gem_wear_day": gem_info["day"],
            },
            "angel_numbers": {
                "sequence": angel_data["angel_sequence"],
                "title": angel_data["title"],
                "message": angel_data["message"],
                "synchronicity_tip": f"Seeing repeating {angel_data['angel_sequence'].split('&')[0].strip()} signifies angelic confirmation that your thoughts are manifesting into tangible reality."
            },
            "vastu_directions": {
                "kua_number": kua_prof.get("kua_number"),
                "kua_display": kua_prof.get("kua_display", "Kua needs gender"),
                "rule_note": kua_prof.get("rule_note", "Calculated from your birth year and gender"),
                "prosperous_wealth": kua_prof["wealth_direction"],
                "vitality_health": kua_prof["health_direction"],
                "relationship_harmony": kua_prof["relationship_direction"],
                "clarity_peace": kua_prof["clarity_direction"],
                "orientation_guidance": (
                    f"As per your personal chart reading (calculated from your birth year and gender), position your primary workspace facing {kua_prof['wealth_direction'].split('(')[0].strip()} to support career momentum, and sleep with your headboard towards {kua_prof['health_direction'].split('(')[0].strip()} for restorative equilibrium."
                    if has_kua_gender
                    else "Kua needs gender. Calculated from your birth year and gender."
                )
            },
            "this_year": {
                "personal_year": personal_year,
                "theme":         yr_theme,
            },
            "topic_priority": name_data.get("topic_priority", ""),
            "life_events_context": _humanise_events(name_data.get("life_events_raw", "")),
        }
    }


@router.post("/ask")
async def premium_ask(req: PremiumAskRequest):
    """
    Premium version of /ask — has memory, probing, and no question limit.
    Calls the main orchestrator and wraps result in full layman language.
    Routes back to the standard readings.ask logic with premium context.
    """
    if not req.premium_token:
        raise HTTPException(status_code=401, detail="Premium token required.")

    profile = _profiles.get(req.premium_token, {})

    # Build enriched context for orchestrator
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from orchestrator import handle_question

        dob_str = f"{req.day or 1:02d}/{req.month or 1:02d}/{req.year or 1990}"
        result = handle_question(
            name=req.name or profile.get("full_name", "User"),
            dob=dob_str,
            question=req.question,
            birth_place=profile.get("birth_city", ""),
            birth_time=profile.get("birth_time", ""),
            life_events=profile.get("life_events_raw", ""),
        )
        result["is_premium"] = True
        result["topic_priority"] = profile.get("topic_priority", "")
        return result
    except Exception as e:
        # Graceful fallback
        return {
            "is_premium": True,
            "classified_topic": "general",
            "synthesis_result": {
                "evidence_summary": [],
                "remedies": [],
                "gemstone_remedies": [],
            },
            "error_handled": True,
        }


# ── Calculation helpers ─────────────────────────────────────────────────────

from app.engine.digit_root import calc_bhagyank, calc_chaldean_name_number, digit_root

def _digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))

def _reduce(n: int) -> int:
    """Reduce strictly to single digit (1–9); master numbers 11, 22, 33 are never retained."""
    return digit_root(n)

def _calc_life_path(day: int, month: int, year: int) -> int:
    """Calculate Life Path / Bhagyank Number from DOB (strict 1–9)."""
    return calc_bhagyank(day, month, year)

def _check_name_energy(name: str, life_path: int) -> dict:
    """
    Check name vibration vs life path.
    Returns layman-language verdict only — no Chaldean table exposed.
    """
    _, name_root = calc_chaldean_name_number(name)
    name_num = name_root if name_root > 0 else life_path

    harmony_pairs = {
        1: [1, 3, 5, 9], 2: [2, 4, 6, 8], 3: [1, 3, 6, 9],
        4: [2, 4, 8],     5: [1, 3, 5, 7], 6: [2, 3, 6, 9],
        7: [2, 5, 7],     8: [2, 4, 6, 8], 9: [1, 3, 6, 9],
    }
    harmonious = name_num in harmony_pairs.get(life_path, [life_path])

    if harmonious:
        verdict = "Balanced"
        detail  = f"Your name carries an energy that flows naturally with your birth energy. This alignment supports you — it adds momentum rather than resistance to your path."
    else:
        verdict = "Opportunity to Strengthen"
        detail  = f"Your name vibrates at a slightly different frequency from your birth energy. A small spelling adjustment could bring these into better alignment and remove subtle friction from your life path."

    return {"verdict": verdict, "detail": detail, "name_number": name_num}

def _humanise_events(raw: str) -> str:
    """Convert raw life events input into a context note (no technical output)."""
    if not raw or len(raw.strip()) < 5:
        return ""
    # Simply acknowledge the context — never expose how it's used internally
    return f"I have noted the recent changes in your life. These events are part of an important transitional cycle, and they give me deeper context for your reading."

def _persist_profile(token: str, data: dict):
    """Save profile to disk."""
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/premium_profiles.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"token": token, **data}) + "\n")
    except Exception:
        pass
