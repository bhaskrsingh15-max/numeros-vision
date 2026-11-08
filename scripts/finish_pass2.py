import json
import re

INDIVIDUAL_SENTENCE_REPLACEMENTS = [
    # PY 3 Home & Family
    (
        "Personal Year 3 brings warmth, conversational vitality, and social cheer to the home front.",
        "Personal Year 3 tends to bring warmth, conversational vitality, and social cheer to the home front."
    ),
    (
        "Adding uplifting decor or creative touches brings an inspiring feeling to your living space.",
        "Adding uplifting decor or creative touches can add an inspiring feeling to your living space."
    ),
    # Personal Month 5
    (
        "A Personal Month 5 brings a dynamic pace with opportunities to adapt to new information and unexpected developments.",
        "A Personal Month 5 introduces a dynamic pace with opportunities to adapt to new information and unexpected developments."
    ),
    (
        "Balancing curious exploration with grounded daily routines keeps your focus clear.",
        "Balancing curious exploration with grounded daily routines tends to keep your focus clear."
    ),
    # Pinnacle 2 - 5
    (
        "The second pinnacle under vibration 5 brings dynamic transitions, travel opportunities, and versatile learning experiences.",
        "The second pinnacle under vibration 5 often introduces dynamic transitions, travel opportunities, and versatile learning experiences."
    ),
    (
        "Maintaining a grounded daily foundation keeps adventurous explorations constructive.",
        "Maintaining a grounded daily foundation tends to keep adventurous explorations constructive."
    ),
    # Pinnacle 3 - 3
    (
        "The third pinnacle under vibration 3 brings an uplifting period of creative sharing, public communication, and social warmth.",
        "The third pinnacle under vibration 3 often introduces an uplifting period of creative sharing, public communication, and social warmth."
    ),
    (
        "Balancing joyful sociability with steady work habits keeps projects on course.",
        "Balancing joyful sociability with steady work habits tends to keep projects on course."
    )
]

def main():
    json_path = 'data/planner_2027_content_library.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        text = f.read()

    applied = 0
    for old_s, new_s in INDIVIDUAL_SENTENCE_REPLACEMENTS:
        if old_s in text:
            text = text.replace(old_s, new_s)
            applied += 1
        else:
            print(f"WARNING: Sentence not found: {old_s[:60]}...")

    print(f"Applied {applied} / {len(INDIVIDUAL_SENTENCE_REPLACEMENTS)} remaining sentences.")

    flagged = [
        'prevents', 'brings', 'keeps', 'makes', 'creates', 'proves', 'builds',
        'guarantees', 'ensures', 'secures', 'peace of mind', 'mental peace',
        'highly productive', 'greatly', 'always'
    ]

    print("\n=== FINAL COUNTS ===")
    for w in flagged:
        c = len(re.findall(rf'\b{re.escape(w)}\b', text, re.IGNORECASE))
        print(f"  {w}: {c}")

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
