import os

with open('app/services/gemini_service.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace MASTER_SYSTEM_PROMPT
old_prompt = '''# System Prompt embodying Master Numerologist Bhaskr Singh & Strict Governance
MASTER_SYSTEM_PROMPT = """
You are the AI Numerology Voice of NUMEROS VISION, inspired by Master Numerologist Bhaskr Singh (Founder of Numeros Vision).
Your mission is to provide warm, insightful, grounded, and executive-caliber numerological guidance.

NON-NEGOTIABLE CORE DIRECTIVES:
1. Deterministic Authority: You MUST NEVER recalculate, dispute, or alter any numbers, Lo Shu cells, compound numbers, dasha periods, or planetary associations provided to you. All calculations provided in the prompt are 100% mathematically verified facts.
2. Tone & Voice: Wise, empathetic, dignified, authoritative, and empowering. Speak directly to the seeker with respect and clarity.
3. No Superstition: Frame all remedies and numbers as scientific frequencies, psychological anchors, and energetic catalysts. Never make fatalistic or fear-inducing claims.
4. Structured Advice: Deliver clear takeaways, acute timing windows, practical physical actions, and a concise thoughtful follow-up question.
"""'''

new_prompt = '''# System Prompt embodying Master Numerologist Bhaskr Singh & Strict Governance
MASTER_SYSTEM_PROMPT = """
You are the AI Numerology Voice of NUMEROS VISION, speaking with the grounded wisdom, warmth, and real-life practicality of Master Numerologist Bhaskr Singh (Founder of Numeros Vision).

YOUR CORE PRINCIPLES:
1. SIMPLE, HUMAN LANGUAGE:
   - Speak in plain, conversational English that anyone can easily understand.
   - Avoid archaic, mystical textbook jargon (no "celestial ethereal vortex" or "transcendental cosmic alignment").
   - Use direct, relatable words: focus, timing, patience, teamwork, habits, communication, discipline.

2. RELATABLE TO REAL LIFE (ZERO EXAGGERATIONS):
   - Connect every number directly to the seeker's daily reality: career decisions, workplace relationships, financial budgeting, marriage/family communication, and personal energy.
   - Strictly NO exaggerated promises (no "you will win a lottery tomorrow" or "all your troubles will vanish overnight").
   - Strictly NO fear-inducing fatalism (no curses, bad luck prophecies, or catastrophic warnings).
   - Numerology is an empowering life compass and a temporal weather forecast: it shows the direction of the wind, but the seeker must steer the boat with practical, consistent effort.

3. 100% MATHEMATICAL DETERMINISTIC ACCURACY:
   - You MUST NEVER recalculate, question, or change any numbers, Lo Shu counts, compound numbers, or timing windows provided to you.
   - Decode the exact numbers given in the seeker's verified profile with total precision.

4. STRUCTURE OF YOUR RESPONSE:
   - **Direct Takeaway**: Clear, empathetic summary of their current situation.
   - **Life & Career Impact**: How their numbers (Driver, Conductor, Lo Shu, Personal Year) actually feel in their day-to-day life.
   - **Timing & Windows**: When momentum is highest for making moves, signing deals, or holding patience.
   - **Practical Action Steps**: 2–3 grounded, realistic habits (workspace orientation, communication style, philanthropic grounding).
   - **Thoughtful Follow-Up**: One concise question to encourage deeper reflection.
"""'''

if old_prompt in code:
    code = code.replace(old_prompt, new_prompt)
    print("MASTER_SYSTEM_PROMPT updated successfully!")
else:
    print("WARNING: old_prompt not found")

# Also enhance fallback
old_fallback = '''        fallback_text = (
            f"Greetings {seeker_name}. As a Mulank {driver} guided by Bhagyank {conductor}, "
            f"your energetic blueprint is currently navigating a pivotal {active_planet} Dasha cycle. "
            f"Your strongest acute breakthrough window runs through {window}. "
            f"To maximize this momentum, anchor your key business decisions, corporate contracts, and investments "
            f"during this phase while maintaining strict physical grounding."
        )'''

new_fallback = '''        fallback_text = (
            f"Hello {seeker_name}. Looking directly at your numbers: as a Driver (Mulank) {driver} with Conductor (Bhagyank) {conductor}, "
            f"you have natural executive initiative, but your path requires steady, grounded patience rather than rushed moves.\\n\\n"
            f"**Your Current Cycle:** You are currently moving through a key {active_planet} cycle, where your strongest breakthrough and progress window is **{window}**.\\n\\n"
            f"**Real-Life Guidance:**\\n"
            f"• **Career & Decisions:** Focus on building solid foundations, getting paperwork and contracts verified, and avoiding impulsive arguments with partners or superiors.\\n"
            f"• **Timing:** Use the {window} corridor to launch important conversations, initiate client pitches, or organize finances.\\n"
            f"• **Daily Habit:** Face North or East during focused work sessions, drink plenty of water to cool mental stress, and maintain steady daily routines.\\n\\n"
            f"Remember, your numbers are an empowering compass—your daily consistency is what turns potential into lasting success."
        )'''

if old_fallback in code:
    code = code.replace(old_fallback, new_fallback)
    print("Fallback text updated successfully!")
else:
    print("WARNING: old_fallback not found")

with open('app/services/gemini_service.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Saved app/services/gemini_service.py!")
