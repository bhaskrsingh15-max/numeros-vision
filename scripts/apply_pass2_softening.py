import json
import re

REPLACEMENTS_PASS2 = [
    # Overviews
    (
        "Personal Year 3 brings an energetic focus on creative expression, communication, and widening your social horizons.",
        "Personal Year 3 often introduces an energetic focus on creative expression, communication, and widening your social horizons."
    ),
    (
        "Consistent discipline and orderly routines provide steady peace of mind throughout the months ahead.",
        "Consistent discipline and orderly routines support a sense of calm and structure throughout the months ahead."
    ),
    (
        "Balancing ambitious pursuits with fair-minded integrity creates enduring stability and respect.",
        "Balancing ambitious pursuits with fair-minded integrity may foster enduring stability and respect."
    ),
    # Life Areas
    (
        "Thoughtful budgeting creates the necessary runway for upcoming independent initiatives.",
        "Thoughtful budgeting can build a supportive runway for upcoming independent initiatives."
    ),
    (
        "Discussing budget allocations with trusted partners or family members promotes shared financial peace of mind.",
        "Discussing budget allocations with trusted partners or family members supports shared financial clarity and calm."
    ),
    (
        "Avoiding overly packed schedules keeps journeys pleasant and refreshing.",
        "Avoiding overly packed schedules tends to keep journeys pleasant and unhurried."
    ),
    (
        "Personal Year 3 brings warmth, conversational vitality, and social cheer to the home front. Adding uplifting decor or creative touches brings an inspiring feeling to your living space.",
        "Personal Year 3 tends to bring warmth, conversational vitality, and social cheer to the home front. Adding uplifting decor or creative touches can add an inspiring feeling to your living space."
    ),
    (
        "Organising your daily tasks prevents scattered energy from delaying key deadlines.",
        "Organising your daily tasks can help avoid scattered energy and delayed deadlines."
    ),
    (
        "Traveling with friends or family often creates memorable shared experiences.",
        "Traveling with friends or family often leads to memorable shared experiences."
    ),
    (
        "Investing effort into making your living space secure and functional brings lasting satisfaction.",
        "Investing effort into making your living space secure and functional can offer lasting satisfaction."
    ),
    (
        "Methodically clearing administrative backlogs and refining workflows builds an enduring foundation for future growth.",
        "Methodically clearing administrative backlogs and refining workflows can build an enduring foundation for future growth."
    ),
    (
        "Personal Year 5 brings a refreshing breeze of change and dynamic activity into domestic life.",
        "Personal Year 5 tends to bring a refreshing sense of change and dynamic activity into domestic life."
    ),
    (
        "Your ability to adapt quickly to shifting demands proves a distinct asset in dynamic environments. Focusing on two or three primary initiatives prevents multitasking from diluting your impact.",
        "Your ability to adapt quickly to shifting demands may prove a distinct asset in dynamic environments. Focusing on two or three primary initiatives can help avoid diluted impact from multitasking."
    ),
    (
        "Engaging in spontaneous conversations and exchanging fresh ideas brings genuine intellectual vitality.",
        "Engaging in spontaneous conversations and exchanging fresh ideas can offer genuine intellectual vitality."
    ),
    (
        "Keeping packing minimal and travel plans adaptable makes journeys especially enjoyable.",
        "Keeping packing minimal and travel plans adaptable can make journeys especially pleasant."
    ),
    (
        "Balancing loving support with healthy respect for individual autonomy keeps family bonds harmonious.",
        "Balancing loving support with healthy respect for individual autonomy supports harmonious family bonds."
    ),
    (
        "Engaging in courses that serve a direct practical or interpersonal purpose brings satisfaction.",
        "Engaging in courses that serve a direct practical or interpersonal purpose tends to bring satisfaction."
    ),
    (
        "Establishing orderly systems for family administration keeps domestic affairs running smoothly.",
        "Establishing orderly systems for family administration tends to keep domestic affairs running smoothly."
    ),
    (
        "Maintaining a balanced perspective prevents material concerns from overshadowing personal priorities.",
        "Maintaining a balanced perspective can help avoid material concerns overshadowing personal priorities."
    ),
    (
        "Working together with partners toward shared goals builds durable alignment.",
        "Working together with partners toward shared goals can build durable alignment."
    ),
    (
        "Vocational studies focused on executive leadership, financial markets, organizational strategy, and governance are highly productive.",
        "Vocational studies focused on executive leadership, financial markets, organizational strategy, and governance are well suited to this cycle."
    ),
    (
        "Setting aside brief moments to rest between appointments keeps your focus sharp.",
        "Setting aside brief moments to rest between appointments tends to keep your focus sharp."
    ),
    (
        "Avoiding speculative commitments supports peace of mind.",
        "Avoiding speculative commitments supports a sense of calm."
    ),
    (
        "Cherishing meaningful connections while honoring healthy boundaries keeps your heart light.",
        "Cherishing meaningful connections while honoring healthy boundaries supports a light and clear perspective."
    ),
    # Sun Signs
    (
        "For Aries, 2027 brings an encouraging climate for pioneering action and decisive leadership.",
        "For Aries, 2027 offers an encouraging climate for pioneering action and decisive leadership."
    ),
    (
        "Balancing caring support for others with healthy personal boundaries supports peace of mind.",
        "Balancing caring support for others with healthy personal boundaries supports a sense of calm."
    ),
    (
        "Leading with inclusive generosity and attentive listening creates lasting loyalty and shared accomplishments.",
        "Leading with inclusive generosity and attentive listening can foster lasting loyalty and shared accomplishments."
    ),
    (
        "For Libra, 2027 brings a harmonious focus to interpersonal diplomacy, aesthetic balance, and collaborative partnerships. Your skill in reconciling differing perspectives proves particularly beneficial in both work and family life.",
        "For Libra, 2027 highlights a harmonious focus on interpersonal diplomacy, aesthetic balance, and collaborative partnerships. Your skill in reconciling differing perspectives may prove particularly beneficial in both work and family life."
    ),
    # Personal Months
    (
        "Fostering mutual understanding in both personal and professional discussions brings quiet harmony.",
        "Fostering mutual understanding in both personal and professional discussions tends to bring quiet harmony."
    ),
    (
        "A Personal Month 3 brings social cheer, creative enthusiasm, and lively communication into focus.",
        "A Personal Month 3 often highlights social cheer, creative enthusiasm, and lively communication."
    ),
    (
        "Your dependable follow-through creates a reassuring sense of order and security.",
        "Your dependable follow-through can build a reassuring sense of order and security."
    ),
    (
        "A Personal Month 5 brings a dynamic pace with opportunities to adapt to new information and unexpected developments. Balancing curious exploration with grounded daily routines keeps your focus clear.",
        "A Personal Month 5 introduces a dynamic pace with opportunities to adapt to new information and unexpected developments. Balancing curious exploration with grounded daily routines tends to keep your focus clear."
    ),
    (
        "Deepening your specialized knowledge during this period brings enduring confidence.",
        "Deepening your specialized knowledge during this period can support enduring confidence."
    ),
    # Mulank Notes
    (
        "In 2027, honoring your intuitive perceptions while maintaining healthy boundaries supports peace of mind.",
        "In 2027, honoring your intuitive perceptions while maintaining healthy boundaries supports a sense of calm."
    ),
    (
        "During 2027, applying your systematic approach to clear milestones builds durable security.",
        "During 2027, applying your systematic approach to clear milestones can build durable security."
    ),
    (
        "Balancing caring devotion with intentional personal downtime keeps your vitality vibrant.",
        "Balancing caring devotion with intentional personal downtime supports steady daily energy."
    ),
    (
        "Pairing bold action with calm composure keeps your efforts centered and sustainable.",
        "Pairing bold action with calm composure tends to keep your efforts centered and sustainable."
    ),
    # Pinnacles
    (
        "Establishing healthy self-reliance during these formative years builds lasting inner confidence.",
        "Establishing healthy self-reliance during these formative years can build lasting inner confidence."
    ),
    (
        "The first pinnacle under vibration 5 brings early experiences of adaptability, diverse interests, and personal freedom.",
        "The first pinnacle under vibration 5 often introduces early experiences of adaptability, diverse interests, and personal freedom."
    ),
    (
        "Learning to pair ambitious focus with integrity creates a solid basis for future success.",
        "Learning to pair ambitious focus with integrity can provide a solid basis for future success."
    ),
    (
        "The second pinnacle under vibration 5 brings dynamic transitions, travel opportunities, and versatile learning experiences. Maintaining a grounded daily foundation keeps adventurous explorations constructive.",
        "The second pinnacle under vibration 5 often introduces dynamic transitions, travel opportunities, and versatile learning experiences. Maintaining a grounded daily foundation tends to keep adventurous explorations constructive."
    ),
    (
        "Cultivating an inclusive and generous outlook brings deep personal fulfillment.",
        "Cultivating an inclusive and generous outlook tends to bring deep personal fulfillment."
    ),
    (
        "The third pinnacle under vibration 3 brings an uplifting period of creative sharing, public communication, and social warmth. Balancing joyful sociability with steady work habits keeps projects on course.",
        "The third pinnacle under vibration 3 often introduces an uplifting period of creative sharing, public communication, and social warmth. Balancing joyful sociability with steady work habits tends to keep projects on course."
    ),
    (
        "The third pinnacle under vibration 5 brings versatile horizons, international connections, and stimulating intellectual shifts.",
        "The third pinnacle under vibration 5 often introduces versatile horizons, international connections, and stimulating intellectual shifts."
    ),
    (
        "Quiet contemplation in natural surroundings brings deep restoration.",
        "Quiet contemplation in natural surroundings can offer deep restoration."
    ),
    (
        "The third pinnacle under vibration 9 brings broad humanitarian perspective, charitable contributions, and graceful completions.",
        "The third pinnacle under vibration 9 often introduces a broad humanitarian perspective, charitable contributions, and graceful completions."
    ),
    (
        "Cultivating your unique outlook keeps your spirit youthful and engaged.",
        "Cultivating your unique outlook tends to keep your perspective fresh and engaged."
    ),
    (
        "The fourth pinnacle under vibration 2 brings gentle companionship, peaceful living, and quiet diplomatic wisdom.",
        "The fourth pinnacle under vibration 2 often highlights gentle companionship, peaceful living, and quiet diplomatic wisdom."
    ),
    (
        "It supports practical peace of mind and preserving accumulated security for future generations.",
        "It supports practical calm and prudent stewardship of accumulated security for future generations."
    ),
    (
        "Maintaining an adaptable attitude keeps your outlook vibrant and open.",
        "Maintaining an adaptable attitude tends to keep your outlook open and engaged."
    ),
    (
        "The fourth pinnacle under vibration 6 brings rich domestic fulfillment, warm relationships with family, and community regard.",
        "The fourth pinnacle under vibration 6 often highlights rich domestic fulfillment, warm relationships with family, and community regard."
    ),
    (
        "Living with an unburdened and grateful heart brings profound peace.",
        "Living with an unburdened and grateful outlook tends to support profound peace."
    ),
    # Remedies
    (
        "Keeping fresh yellow flowers at home brings a gentle feeling of optimism.",
        "Keeping fresh yellow flowers at home can provide a gentle feeling of optimism."
    ),
    (
        "Engaging in deliberate acts of kindness brings emotional warmth and balance.",
        "Engaging in deliberate acts of kindness can offer emotional warmth and balance."
    )
]

def main():
    json_path = 'data/planner_2027_content_library.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        text = f.read()

    flagged = [
        'prevents', 'brings', 'keeps', 'makes', 'creates', 'proves', 'builds',
        'guarantees', 'ensures', 'secures', 'peace of mind', 'mental peace',
        'highly productive', 'greatly', 'always'
    ]

    print("=== PASS 2: COUNTS BEFORE ===")
    before_counts = {}
    for w in flagged:
        c = len(re.findall(rf'\b{re.escape(w)}\b', text, re.IGNORECASE))
        before_counts[w] = c
        print(f"  {w}: {c}")

    applied = 0
    for old_s, new_s in REPLACEMENTS_PASS2:
        if old_s in text:
            text = text.replace(old_s, new_s)
            applied += 1
        else:
            print(f"WARNING: Not found: {old_s[:60]}...")

    print(f"\nApplied {applied} / {len(REPLACEMENTS_PASS2)} replacements.")

    print("\n=== PASS 2: COUNTS AFTER ===")
    after_counts = {}
    for w in flagged:
        c = len(re.findall(rf'\b{re.escape(w)}\b', text, re.IGNORECASE))
        after_counts[w] = c
        print(f"  {w}: {c} (was {before_counts[w]})")

    parsed = json.loads(text)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)
    print(f"\nSaved updated JSON to {json_path}")

    artifact_path = r"C:\Users\Bhaskr Singh\.gemini\antigravity\brain\c1ea3ed7-b9d2-437a-b7aa-f0cb4004681b\planner_2027_content_library.json"
    with open(artifact_path, 'w', encoding='utf-8') as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)
    print(f"Updated artifact copy at {artifact_path}")

if __name__ == '__main__':
    main()
