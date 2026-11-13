import os

path = os.path.join('app', 'api', 'readings.py')
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

target = '''        # High-stakes topics consultation recommendation
        if any(w in ql for w in ["child", "conceive", "autism", "divorce", "court", "lawsuit", "dispute", "partner"]):
            orchestrator_output["master_consultation_option"] = {
                "title": "1-on-1 Master Personal Consultation",
                "price_inr": 11400,
                "original_price_inr": 24000,
                "duration": "90 Minutes Private Master Session",
                "benefit": "Private multi-chart synthesis, Birth Epoch Verification, custom yantra preparation, and 30-day priority WhatsApp guidance."
            }'''

replacement = '''        # High-stakes topics consultation recommendation (Enquiry-First Model)
        if any(w in ql for w in ["child", "conceive", "autism", "divorce", "court", "lawsuit", "dispute", "partner"]):
            orchestrator_output["master_consultation_option"] = {
                "title": "1-on-1 Master Personal Consultation",
                "duration": "Private Master Session",
                "benefit": "Private multi-chart synthesis, Birth Epoch Verification, custom yantra preparation, and tailored practitioner guidance.",
                "booking_url": "/consultation/"
            }'''

norm_text = text.replace('\r\n', '\n')
norm_target = target.replace('\r\n', '\n')
norm_replacement = replacement.replace('\r\n', '\n')

if norm_target in norm_text:
    norm_text = norm_text.replace(norm_target, norm_replacement, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(norm_text)
    print('Updated readings.py successfully!')
else:
    print('Target not found in readings.py')
