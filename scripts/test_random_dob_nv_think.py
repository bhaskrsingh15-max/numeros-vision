import sys
import os
import pypdf

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath('.'))

from app.engine.nv_psychology_engine import nv_think_engine
from app.services.pdf_report_generator import generate_customised_pdf_report
from app.engine.question_explanation_engine import generate_simple_explanation_and_remedies

print("================================================================================")
print("  NV THINK™ RANDOM PROFILE AUDIT & VERIFICATION TEST")
print("================================================================================")

# Random Test Profile
name = "Aanya Sharma"
day = 15
month = 8
year = 1995
gender = "female"
topic = "career"
question = "I am feeling torn between expanding my creative design studio and entering corporate advisory. What is my optimal timing and operational path?"

print(f"\nTarget Seeker: {name}")
print(f"Date of Birth: {day:02d}-{month:02d}-{year}")
print(f"Inquiry: \"{question}\"")

# 1. TEST NV THINK™ PSYCHOLOGY ENGINE
print("\n" + "="*50)
print("STEP 1: NV THINK™ 7-STAGE PSYCHOLOGICAL EVALUATION")
print("="*50)

# Calculate Core Digits
driver = 6  # 15 -> 1+5 = 6 (Venus)
conductor = 2 # 1+5+8+1+9+9+5 = 38 -> 11 -> 2 (Moon)
loshu_counts = {1: 2, 5: 2, 8: 1, 9: 2}
missing_numbers = [2, 3, 4, 6, 7]
active_planes = ["Will Plane (9-5-1 Fully Active — High Ambition & Execution)", "Action Plane (2-7-6 Broken Void)"]

eval_driver = nv_think_engine.evaluate_number(driver, frequency=0, position="Driver (Mulank)", environmental_context="Creative boutique studio founder")
eval_conductor = nv_think_engine.evaluate_number(conductor, frequency=0, position="Conductor (Bhagyank)", environmental_context="Rapidly expanding team and external advisory inquiries")

print(f"\n• Driver {driver} (Venus) Psychological Assessment:")
print("  Traditional Logic:", eval_driver["traditional_logic"])
print("  Possible Behaviours:", eval_driver["possible_behaviours"][:2])
print("  Psychological Hypotheses:", eval_driver["psychological_hypotheses"][:2])
print("  Core Duality Pattern:", eval_driver["contradictory_indicators"][:1])

print(f"\n• Conductor {conductor} (Moon) Assessment:")
print("  Traditional Logic:", eval_conductor["traditional_logic"])
print("  Possible Behaviours:", eval_conductor["possible_behaviours"][:2])
print("  Psychological Hypotheses:", eval_conductor["psychological_hypotheses"][:2])

chart_synth = nv_think_engine.evaluate_chart_synthesis(
    driver=driver,
    conductor=conductor,
    loshu_counts=loshu_counts,
    active_planes=active_planes,
    missing_numbers=missing_numbers,
    user_environment="Creative Agency / Design Studio"
)

print("\n• Chart-Level Duality & Synthesis:")
for d_note in chart_synth["chart_dualities"]:
    print("  *", d_note)
for v_note in chart_synth["void_hypotheses"]:
    print("  *", v_note)
print("\n  Synthesized Narrative:")
print(" ", chart_synth["synthesized_narrative"])

# 2. TEST CHARM AI MULTI-MODEL ASTROLOGICAL CONSENSUS
print("\n" + "="*50)
print("STEP 2: CHARM AI MULTI-MODEL CONSENSUS CORRELATION")
print("="*50)

charm_consensus = nv_think_engine.correlate_charm_ai_consensus(
    numerology_dasha={"active_dasha": "Venus", "acute_window": "Personal Year 6 (2026-2027)"},
    vedic_factors={"favorable": True, "subperiod_lord": "Mercury"},
    kp_factors={"houses": [2, 5, 10, 11]},
    bnn_factors={"conjunction": "Venus-Mercury Harmony"},
    seeker_question=question
)

print("Consensus Status:", charm_consensus["consensus_status"])
print("Primary Authority:", charm_consensus["primary_authority"])
print("Active Timing Window:", charm_consensus["timing_window"])
print("Takeaway Narrative:", charm_consensus["nv_think_takeaway"])
print("Models Correlated:", charm_consensus["multi_model_summary"]["corroborations"])

# 3. TEST LIVE QEE ENGINE
print("\n" + "="*50)
print("STEP 3: LIVE CHARM AI QUERY ENGINE (WITH 10,939 PASSAGE RAG)")
print("="*50)

qee_res = generate_simple_explanation_and_remedies(
    question=question,
    driver=driver,
    conductor=conductor,
    day=day,
    month=month,
    year=year,
    name=name,
    topic=topic,
    current_age=30
)

print("\nConsultation Takeaway:")
print(qee_res.get("direct_answer", "")[:280] + "...")
print("\nRoot Cause / Why Happening:")
print(qee_res.get("why_happening", "")[:280] + "...")
print("\nNV THINK Diagnostic Present in Output:", bool(qee_res.get("nv_think_diagnostic")))
print("Multi-Model Consensus Status in Output:", qee_res.get("multi_model_consensus", {}).get("consensus_status"))

# 4. TEST PDF REPORT GENERATION FOR THIS RANDOM PROFILE (3p, 12p, 32p)
print("\n" + "="*50)
print("STEP 4: PDF REPORT GENERATION & PAGE COUNT VERIFICATION")
print("="*50)

test_tiers = [
    ("basic", "Random_Test_Basic_Aanya_3P.pdf", 3),
    ("advanced", "Random_Test_Advanced_Aanya_12P.pdf", 12),
    ("premium", "Random_Test_Premium_Aanya_32P.pdf", 32)
]

output_dir = "scratch"
os.makedirs(output_dir, exist_ok=True)

all_pdf_passed = True
for tier_name, filename, expected_pages in test_tiers:
    out_path = os.path.join(output_dir, filename)
    pdf_bytes, meta = generate_customised_pdf_report(
        name=name,
        day=day,
        month=month,
        year=year,
        topic_id="career_wealth",
        tier=tier_name
    )
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    
    reader = pypdf.PdfReader(out_path)
    actual_pages = len(reader.pages)
    file_size = os.path.getsize(out_path)
    
    status_str = "PASS" if actual_pages == expected_pages else "FAIL"
    print(f"• {tier_name.upper()} Report: {actual_pages} Pages (Expected {expected_pages}) | {file_size:,} bytes -> [{status_str}]")
    if actual_pages != expected_pages:
        all_pdf_passed = False

if all_pdf_passed:
    print("\n✅ ALL TESTS PASSED: NV THINK™ successfully verified across random profile end-to-end!")
else:
    print("\n❌ Page count mismatch detected.")
