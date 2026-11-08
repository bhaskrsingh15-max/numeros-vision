import json
import re
import hashlib
import os

REPLACEMENTS = [
    # Overviews
    (
        "A balanced attitude toward giving and receiving ensures that caring for others remains deeply fulfilling.",
        "A balanced attitude toward giving and receiving supports caring for others in a fulfilling way."
    ),
    # Life Areas
    (
        "Keeping realistic timelines ensures steady momentum as fresh projects get underway.",
        "Keeping realistic timelines supports steady momentum as fresh projects get underway."
    ),
    (
        "Steady patience protects you from hasty transactional choices.",
        "Steady patience tends to reduce hasty transactional choices."
    ),
    (
        "Sincere and attentive communication ensures that connections remain meaningful.",
        "Sincere and attentive communication helps keep connections meaningful."
    ),
    (
        "Resisting impulsive financial opportunities ensures steady fiscal footing.",
        "Resisting impulsive financial opportunities can support steady fiscal footing."
    ),
    (
        "Establishing realistic boundaries around work hours protects your personal and family time.",
        "Establishing realistic boundaries around work hours supports your personal and family time."
    ),
    (
        "Thoughtful planning for household improvements ensures expenditures remain within comfortable means.",
        "Thoughtful planning for household improvements can help keep expenditures within comfortable means."
    ),
    (
        "A conservative and analytical approach protects your resources effectively.",
        "A conservative and analytical approach can support prudent resource management."
    ),
    (
        "Grounding your leadership in ethical standards earns enduring professional respect.",
        "Grounding your leadership in ethical standards supports enduring professional respect."
    ),
    (
        "Ensuring that professional ambitions do not crowd out quality personal time preserves warmth.",
        "Making sure professional ambitions do not crowd out quality personal time supports warmth."
    ),
    (
        "Consciously releasing workday stress before entering the home preserves mental peace.",
        "Consciously setting aside workday tasks before entering the home supports a restful evening routine."
    ),
    (
        "Scheduled relaxation breaks during intense work weeks protect your long-term vitality.",
        "Scheduled rest pauses during busy work weeks support steady daily pacing."
    ),
    (
        "Applying structured frameworks directly to current responsibilities accelerates your growth.",
        "Applying structured frameworks directly to current responsibilities can support practical skill development."
    ),
    (
        "Selecting efficient travel arrangements and punctual itineraries ensures productive outcomes.",
        "Selecting efficient travel arrangements and punctual itineraries supports productive outcomes."
    ),
    (
        "Concluding commitments with diligence and professional grace ensures a clean slate ahead.",
        "Concluding commitments with diligence and professional grace supports a clean slate ahead."
    ),
    (
        "Avoiding speculative commitments protects your peace of mind.",
        "Avoiding speculative commitments supports peace of mind."
    ),
    # Sun Signs
    (
        "Staying open to practical modern methods ensures steady progress without unnecessary rigidity.",
        "Staying open to practical modern methods supports steady progress without unnecessary rigidity."
    ),
    (
        "Focusing your lively interests on two or three key goals ensures that your talents yield tangible results.",
        "Focusing your lively interests on two or three key goals can support tangible results."
    ),
    (
        "Balancing caring support for others with healthy personal boundaries preserves your peace of mind.",
        "Balancing caring support for others with healthy personal boundaries supports peace of mind."
    ),
    (
        "Grounding your expansive ideas in practical daily schedules ensures lasting achievements.",
        "Grounding your expansive ideas in practical daily schedules can support lasting achievements."
    ),
    (
        "Maintaining clear practical boundaries ensures your compassionate nature remains an enduring source of strength.",
        "Maintaining clear practical boundaries supports your compassionate nature as an enduring source of strength."
    ),
    # Personal Months
    (
        "Keeping track of daily priorities ensures that vibrant enthusiasm leads to productive completions.",
        "Keeping track of daily priorities supports turning enthusiasm into productive completions."
    ),
    (
        "Balancing caring generosity with personal rest preserves your emotional equilibrium.",
        "Balancing caring generosity with personal rest supports a steady emotional balance."
    ),
    (
        "Grounding your leadership in fairness and accountability ensures lasting success.",
        "Grounding your leadership in fairness and accountability supports lasting progress."
    ),
    # Mulank Notes
    (
        "In 2027, honoring your intuitive perceptions while maintaining healthy boundaries protects your peace of mind.",
        "In 2027, honoring your intuitive perceptions while maintaining healthy boundaries supports peace of mind."
    ),
    (
        "Remaining receptive to adaptable methods ensures your steady work flows with greater ease.",
        "Remaining receptive to adaptable methods supports your steady work flowing with greater ease."
    ),
    # Pinnacles
    (
        "Maintaining focus on core commitments ensures that creative ventures bear fruit.",
        "Maintaining focus on core commitments supports creative ventures bearing fruit."
    ),
    (
        "Your steady capacity for stewardship earns lasting respect and stability.",
        "Your steady capacity for stewardship supports lasting respect and stability."
    ),
    (
        "Cultivating calm patience ensures lasting harmony in all partnerships.",
        "Cultivating calm patience supports lasting harmony in all partnerships."
    ),
    (
        "It is an opportune phase to protect long-term security through prudent systems and reliable management.",
        "It is an opportune phase to support long-term security through prudent systems and reliable management."
    ),
    (
        "Conducting affairs with scrupulous fairness ensures enduring honor.",
        "Conducting affairs with scrupulous fairness supports enduring honor."
    ),
    # Wellbeing Lines: Routines only, no health outcome claims
    (
        "Establishing consistent morning routines and engaging in invigorating physical movement supports your vitality during this busy chapter. Prioritising structured hydration and balanced meals keeps energy steady throughout demanding days. Setting aside quiet moments before sleep helps quiet an active mind.",
        "Establishing consistent morning routines and regular movement habits supports your daily scheduling during this busy chapter. Prioritising structured hydration and balanced meals supports consistent pacing throughout demanding days. Setting aside quiet moments before sleep supports an unhurried evening routine."
    ),
    (
        "Gentle movement such as mindful stretching, swimming, or restorative walking suits your rhythm this year. Maintaining consistent sleep hygiene and soothing evening habits aids in releasing accumulated tension. Mindful breathing pauses throughout the workday provide gentle grounding.",
        "Gentle movement such as light stretching, swimming, or walking suits your rhythm this year. Maintaining consistent sleep hygiene and calming evening habits supports unwinding at the end of the day. Mindful pauses throughout the workday provide gentle grounding."
    ),
    (
        "Active hobbies that blend physical vitality with creative expression, such as dance, light cycling, or group walks, support your wellbeing. Staying mindful of restful downtime balances high social engagement. Incorporating fresh wholesome foods sustains your vibrant energy levels.",
        "Active hobbies that blend physical movement with creative expression, such as dance, light cycling, or group walks, support your daily routine. Staying mindful of restful downtime balances high social engagement. Incorporating fresh wholesome foods supports balanced daily nutrition habits."
    ),
    (
        "Consistent daily routines, regular mealtimes, and disciplined sleep patterns provide the core foundation for physical endurance. Posture-strengthening exercises, mindful core work, and regular walking help manage physical tension. Adequate rest days ensure your focused effort remains sustainable.",
        "Consistent daily routines, regular mealtimes, and disciplined sleep patterns provide a steady structure for daily tasks. Gentle stretching, core exercises, and regular walking support comfortable posture. Scheduled rest days support keeping your focused effort sustainable."
    ),
    (
        "Maintaining physical vitality calls for varied, engaging exercise routines that keep boredom at bay. Outdoor trail walking, functional bodyweight training, and mindful breathing support agility. Establishing a grounding evening routine helps calm your nervous system after lively days.",
        "Maintaining consistent routines calls for varied, engaging exercise habits that keep boredom at bay. Outdoor trail walking, functional bodyweight training, and quiet breathing pauses support daily agility. Establishing a grounding evening routine supports relaxation after lively days."
    ),
    (
        "Wholesome home-cooked meals, mindful nourishment, and rhythmic daily walks support your vitality in Year 6. Creating a peaceful bedtime sanctuary encourages restorative and deep sleep. Gentle stretching and spending time in green outdoor spaces promote emotional grounding.",
        "Wholesome home-cooked meals, mindful nourishment, and rhythmic daily walks support steady daily habits in Year 6. Creating a peaceful bedtime environment supports consistent sleep routines. Gentle stretching and spending time outdoors can encourage personal grounding."
    ),
    (
        "Restorative sleep, quiet meditation, and regular walks in natural surroundings are essential during this introspective cycle. Mindful hydration and minimizing excessive screen time before bed support mental calmness. Gentle yoga or contemplative breathing helps release mental fatigue.",
        "Consistent rest, quiet reflection, and regular walks in natural surroundings support this introspective cycle. Mindful hydration and minimizing screen time before bed support quiet evenings. Gentle stretching or contemplative breathing supports an unhurried daily routine."
    ),
    (
        "Maintaining physical stamina through structured strength training, balanced nutrition, and consistent rest is vital. Consciously releasing workday stress before entering the home preserves mental peace. Scheduled relaxation breaks during intense work weeks protect your long-term vitality.",
        "Maintaining consistent exercise routines, regular meals, and scheduled rest supports steady daily focus. Consciously setting aside workday tasks before entering the home supports a restful evening routine. Scheduled rest pauses during busy work weeks support steady daily pacing."
    ),
    (
        "Engaging in restorative wellness practices, gentle swimming, and regular walks in nature supports your vitality. Establishing intentional habits to release emotional tension before sleep promotes refreshing rest. Nourishing meals and adequate hydration help maintain steady vitality.",
        "Engaging in gentle exercise, light swimming, and regular walks in nature supports steady daily routines. Establishing intentional habits to unwind before sleep supports a calm evening routine. Balanced meals and adequate hydration support consistent daily pacing."
    ),
]

def main():
    json_path = 'data/planner_2027_content_library.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        text = f.read()

    flagged_words = ['ensures', 'ensuring', 'earns', 'preserves', 'protect', 'protects', 'accelerates', 'guarantee', 'guarantees', 'guaranteed', 'always', 'definitely']
    
    print("=== WORD COUNTS BEFORE ===")
    before_counts = {}
    for w in flagged_words:
        c = len(re.findall(rf'\b{w}\b', text, re.IGNORECASE))
        before_counts[w] = c
        print(f"  {w}: {c}")

    applied_changes = []
    for old_s, new_s in REPLACEMENTS:
        if old_s in text:
            text = text.replace(old_s, new_s)
            applied_changes.append((old_s, new_s))
        else:
            print(f"WARNING: String not found: {old_s[:60]}...")

    print(f"\nApplied {len(applied_changes)} / {len(REPLACEMENTS)} replacements.")

    print("\n=== WORD COUNTS AFTER ===")
    after_counts = {}
    for w in flagged_words:
        c = len(re.findall(rf'\b{w}\b', text, re.IGNORECASE))
        after_counts[w] = c
        print(f"  {w}: {c} (was {before_counts[w]})")

    # Validate JSON syntax
    parsed = json.loads(text)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)
    print(f"\nSuccessfully wrote formatted JSON to {json_path}")

    # Copy to artifact dir as well
    artifact_path = r"C:\Users\Bhaskr Singh\.gemini\antigravity\brain\c1ea3ed7-b9d2-437a-b7aa-f0cb4004681b\planner_2027_content_library.json"
    with open(artifact_path, 'w', encoding='utf-8') as f:
        json.dump(parsed, f, indent=2, ensure_ascii=False)
    print(f"Updated artifact copy at {artifact_path}")

if __name__ == '__main__':
    main()
