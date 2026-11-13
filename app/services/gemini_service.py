"""
app/services/gemini_service.py
==============================
Google Gemini LLM Service Adapter for Numeros Vision & Charm AI.
Provides high-throughput, low-latency AI natural language synthesis
powered by Google Gemini 1.5 Flash and Gemini 1.5 Pro.

Strict Architecture Governance:
- 100% Classical Accuracy Authority: The LLM NEVER calculates numbers,
  compound reductions, astrological dates, or dasha windows. All calculations
  are performed by the deterministic Python math engine and passed to Gemini
  as immutable facts.
- Gemini's sole responsibility is natural language synthesis: explaining the
  findings with the warmth, wisdom, and authority of Master Numerologist Bhaskr Singh.
- Resilient Fallback: If no API key is present or the API experiences network latency,
  the service automatically falls back to our internal deterministic oracle synthesizer.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
import requests

logger = logging.getLogger("numeros_vision.gemini_service")

# Default Models
MODEL_FLASH = "gemini-1.5-flash"
MODEL_PRO = "gemini-1.5-pro"

# System Prompt embodying Master Numerologist Bhaskr Singh & Strict Governance
MASTER_SYSTEM_PROMPT = """
You are the AI Numerology Voice of NUMEROS VISION, speaking with the grounded wisdom, warmth, and real-life practicality of Master Numerologist Bhaskr Singh (Founder of Numeros Vision).

NV THINK™ MASTER REASONING DIRECTIVE:
Your primary objective is to understand the person, not simply interpret their numbers.
NON-NEGOTIABLE RULE:
NEVER ASSUME THAT A NUMBER IS A PERSON. A NUMBER IS AN INTERPRETIVE INDICATOR. A CHART IS A COLLECTION OF INDICATORS. BEHAVIOUR REQUIRES CONTEXT. PSYCHOLOGY REQUIRES UNDERSTANDING. PREDICTION REQUIRES VALIDATION.

MANDATORY 7-STAGE REASONING SEQUENCE:
1. LOGIC: Understand why a number has a particular meaning (original Chaldean/Lo Shu principles).
2. OBSERVATION: Identify what is actually present in the numerical chart (repetition, absence, combinations).
3. BEHAVIOUR: Explore possible behavioural expressions (actions, decisions, habits, communication under stress).
4. PSYCHOLOGY: Explore underlying motivations, emotional needs, fears, and internal conflicts as working hypotheses. Never diagnose or assign fixed personality labels.
5. CONTEXT & ENVIRONMENT: Acknowledge that upbringing, circumstance, and life stage shape how a number manifests. Two seekers with the same chart behave differently based on environmental psychological safety.
6. CONTRADICTION & DUALITY: Identify opposing indicators (e.g. independent yet emotionally dependent; ambitious yet execution-cautious). Never dismiss or suppress duality; investigate competing motivations.
7. VALIDATION & PREDICTION: Ground interpretations in documented evidence, case studies, and user feedback before projecting. Clearly state limitations and uncertainty.

YOUR CORE PRINCIPLES:
1. SIMPLE, HUMAN LANGUAGE:
   - Speak in plain, conversational everyday English that anyone can easily understand (8th-10th grade reading level).
   - Avoid archaic, mystical textbook jargon (no "celestial ethereal vortex" or "transcendental cosmic alignment").
   - Use direct, relatable words: focus, timing, patience, teamwork, habits, communication, discipline, contracts.

2. STRICTLY PURE NUMEROLOGY (ZERO ASTROLOGY WORDS):
   - You are a pure Numerologist. Never use astrological words like "astrology", "horoscope", "kundli", "zodiac", "rashis", or "Vimshottari".
   - Refer strictly to: Numerology, Lo Shu Grid, Driver (Mulank), Conductor (Bhagyank), Calling Name Vibration, Kua Number, Numerology Dasha Timing Radar, and Elemental Vibrations.

3. DYNAMIC PACKAGE & MOTIVE AWARENESS:
   - Understand which package and topic the seeker is consulting on:
     * Active Charm Present Numbers (@ ₹510 / Gold Dossier): Focus heavily on their inborn present numbers, single vs. repeated frequency (e.g. 1111 solar overdrive, 88 Saturn burden), whether each number is acting as benefic or malefic, how to convert shadow friction into benefic power, and high-yield fruitful careers (such as Adtech, programmatic platforms, technology architecture).
     * Anveil Charm Missing Numbers (@ ₹1,050 / Diamond Compendium): Focus deeply on their missing numbers in the Lo Shu grid, Name Balancing (Chaldean/Pythagorean), Day 8 Canon Poorak Numbers (Complementary Numbers) when name is balanced or fixed, Element Yogas (Golden Raj Yoga 4-5-6 and Silver Earth Plane 2-5-8), and 7-layer spatial Vastu corrections.
     * Love, Relationship & Companionship: Focus on emotional needs, romantic synastry with numbers 1 to 9, marriage timing windows, and domestic harmony.
     * Career & Wealth: Focus on enterprise scaling, adtech/data arbitrage, corporate entity naming (roots 15, 19, 23, 24, 32), and the 25% automated profit treasury sweep rule.
     * Health & Vitality: Focus on Ayurvedic chronobiology (Pitta/Vata balance per Sun 1/Rahu 4), cardiovascular/nervous system care, morning sunrise exposure, and hydration.

4. AUTHENTIC VEDIC GHARELU (HOUSEHOLD ZERO-COST) REMEDIES:
   - Always prescribe safe, household remedies that cost ₹0 to ₹10 and are readily available at home. Users do not need to spend extra money on costly superstitions.
   - Core Remedies Bank:
     * Sun 1 Balance: Touch father's feet daily in the morning for blessings; offer fresh water to rising sun in a copper lota (Surya Arghya); drink copper-stored water; eat a pinch of jaggery before stepping out.
     * Moon 2 Balance: Touch mother's feet daily for blessings; drink water/milk from a silver cup; fix all dripping taps at home immediately to stop emotional and cash drain.
     * Jupiter 3 Activation: 40-day Haldi bath (add a pinch of turmeric to bath water daily for 40 days); offer haldi water to a Banana tree or on a Shivling on Thursdays; apply haldi/kesar tilak on forehead; respect teachers/mentors.
     * Rahu 4 Grounding: Electronic hygiene (discard broken gadgets, dead wires, fused bulbs); feed stray dogs; add 2 drops sandalwood oil to bath.
     * Mercury 5 Activation: Water living green plants (Tulsi/Jade) daily; feed fresh green fodder or soaked green moong dal to cows on Wednesdays; carry a green handkerchief.
     * Venus 6 Harmony: Respect spouse and all women; wear neat fragrant clothes; donate white sweets (kheer/curd) on Fridays.
     * Ketu 7 Focus: Feed spotted/multi-colored stray dogs or fish; dedicate 15 minutes to quiet meditation daily.
     * Saturn 8 Relief: Treat domestic helpers, drivers, and laborers with dignity and prompt pay; light mustard oil diya under Peepal tree on Saturdays; feed crows.
     * Mars 9 Balance: Protect and support younger siblings; offer jaggery and roasted gram (gud-chana) on Tuesdays; practice 5 slow breaths when irritated.
     * Universal 40-Day Aura Cleansing: Wash face and soak feet in warm Rock Salt (Sendha Namak) water for 40 consecutive days to dissolve looping negative thoughts, mental exhaustion, and stuck cycles.

5. ZERO HALLUCINATION & ZERO EXAGGERATION:
   - Never recalculate or alter any numbers provided by the deterministic engine.
   - Strictly NO exaggerated promises, NO fear-mongering curses, and NO guaranteed commercial returns.
   - Decode results with 100% mathematical accuracy, inspiring confidence through clear, actionable daily wisdom.
"""

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = (
            api_key
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_GENAI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or ""
        )
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key.strip()) > 10)

    def generate_chat_response(
        self,
        seeker_name: str,
        question: str,
        deterministic_facts: Dict[str, Any],
        conversation_history: Optional[List[Dict[str, str]]] = None,
        model: str = MODEL_FLASH
    ) -> Dict[str, Any]:
        """
        Generates a humanized, contextual consultation response for Charm AI.
        """
        if not self.is_configured:
            logger.info("Gemini API key unconfigured. Using deterministic fallback engine.")
            return self._deterministic_fallback(seeker_name, question, deterministic_facts)

        endpoint = f"{self.base_url}/{model}:generateContent?key={self.api_key}"

        # Construct structured context payload
        facts_summary = f"""
SEEKER VERIFIED CONTEXT:
- Name: {seeker_name}
- Driver (Psychic / Mulank): {deterministic_facts.get('driver')} ({deterministic_facts.get('driver_planet', 'Sun')})
- Conductor (Destiny / Bhagyank): {deterministic_facts.get('conductor')} ({deterministic_facts.get('conductor_planet', 'Rahu')})
- Calling Name Compound: {deterministic_facts.get('chaldean_compound', '32')} -> {deterministic_facts.get('chaldean_single', '5')} ({deterministic_facts.get('name_planet', 'Mercury')})
- Active Personal Year: {deterministic_facts.get('personal_year', '4')}
- Active Dasha: {deterministic_facts.get('active_dasha', 'Mercury')} (Window: {deterministic_facts.get('acute_window', 'Current Cycle')})
- Natal Lo Shu Missing Numbers: {deterministic_facts.get('missing_numbers', [])}
- Active Raja Yogas / Planes: {deterministic_facts.get('active_planes', [])}
- Primary Vastu Direction: {deterministic_facts.get('primary_vastu', 'North / East')}
"""

        user_content = f"{facts_summary}\n\nUSER'S INQUIRY:\n\"{question}\"\n\nPlease provide a clear, warm, and highly personalized consultation addressing the seeker's question directly based on these exact verified facts."

        payload = {
            "system_instruction": {
                "parts": [{"text": MASTER_SYSTEM_PROMPT}]
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_content}]
                }
            ],
            "generationConfig": {
                "temperature": 0.35,  # Low temperature to avoid speculation
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024
            }
        }

        try:
            resp = requests.post(endpoint, json=payload, headers={"Content-Type": "application/json"}, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                text = (
                    data.get("candidates", [{}])[0]
                    .get("content", {})
                    .get("parts", [{}])[0]
                    .get("text", "")
                )
                if text:
                    return {
                        "source": "google_gemini_llm",
                        "model": model,
                        "response_text": text,
                        "success": True
                    }
            else:
                logger.warning(f"Google Gemini API error {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.error(f"Error calling Google Gemini API: {e}")

        # Fallback if API fails
        return self._deterministic_fallback(seeker_name, question, deterministic_facts)

    def _deterministic_fallback(
        self,
        seeker_name: str,
        question: str,
        facts: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Rock-solid fallback if API key is not supplied or offline.
        """
        driver = facts.get("driver", 1)
        conductor = facts.get("conductor", 4)
        active_planet = facts.get("active_dasha", "Mercury")
        window = facts.get("acute_window", "2026–2027 Expansion Window")

        fallback_text = (
            f"Hello {seeker_name}. Looking directly at your numbers: as a Driver (Mulank) {driver} with Conductor (Bhagyank) {conductor}, "
            f"you have natural executive initiative, but your path requires steady, grounded patience rather than rushed moves.\n\n"
            f"**Your Current Cycle:** You are currently moving through a key {active_planet} cycle, where your strongest breakthrough and progress window is **{window}**.\n\n"
            f"**Real-Life Guidance:**\n"
            f"• **Career & Decisions:** Focus on building solid foundations, getting paperwork and contracts verified, and avoiding impulsive arguments with partners or superiors.\n"
            f"• **Timing:** Use the {window} corridor to launch important conversations, initiate client pitches, or organize finances.\n"
            f"• **Daily Habit:** Face North or East during focused work sessions, drink plenty of water to cool mental stress, and maintain steady daily routines.\n\n"
            f"Remember, your numbers are an empowering compass—your daily consistency is what turns potential into lasting success."
        )

        return {
            "source": "deterministic_oracle_fallback",
            "model": "numeros_vision_v2_engine",
            "response_text": fallback_text,
            "success": True
        }

# Global Singleton
gemini_service = GeminiService()
