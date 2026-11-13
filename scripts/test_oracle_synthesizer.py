import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.engine.charm_oracle_synthesizer import charm_oracle_synthesizer

questions = [
    ('Bhaskr Singh', 'How can I resolve partner issues and bring harmony to my love and married life?'),
    ('Bhaskr Singh', 'I feel stuck in my career and lost opportunities. How can I unblock my professional growth?'),
    ('Ahmad Khan', 'How can I clear trapped debt and unblock steady wealth accumulation?'),
    ('Sarah Jenkins', 'We are praying to conceive a child. What cosmic timing and remedies support progeny blessings?'),
    ('Bhaskr Singh', 'What is the stock market investment outlook for my numbers?'),
    ('Bhaskr Singh', 'I am facing obstacles everywhere in life. How can I clear this stagnation?')
]

for name, q in questions:
    res = charm_oracle_synthesizer.synthesize_consultation(name, 10, 8, 1988, q, is_premium=False)
    topic = res["topic_display"]
    faith = res["faith_detected"]
    preview = res["direct_answer"][:250].encode('ascii', errors='replace').decode('ascii')
    has_cta = 'ANVEIL EVERY CHARM' in res['direct_answer']
    print(f"=== {name} | Topic: {topic} | Faith: {faith} ===")
    print(preview)
    print(f"Includes Curiosity CTA: {has_cta}\n")
