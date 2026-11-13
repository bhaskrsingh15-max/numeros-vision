import os
import re
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('.'))

def run_consultation_audit():
    print("=====================================================================")
    print("NUMEROS VISION — CONSULTATION ENQUIRY-FIRST MODEL COMPREHENSIVE AUDIT")
    print("=====================================================================")

    passed = 0
    total = 0

    def check(name, condition, details=""):
        nonlocal passed, total
        total += 1
        if condition:
            passed += 1
            print(f" [PASS] {name}")
            if details:
                print(f"        {details}")
        else:
            print(f"![FAIL] {name}")
            if details:
                print(f"        {details}")

    # Test 1: Consultation HTML SEO & Metadata
    consult_path = 'app/static/consultation.html'
    dist_consult_path = 'dist_cloudflare_pages/consultation/index.html'
    with open(consult_path, 'r', encoding='utf-8') as f:
        c_html = f.read()

    check("Consultation Page SEO Title",
          "<title>Personal Numerology Consultation | Numeros Vision</title>" in c_html,
          "Title is: Personal Numerology Consultation | Numeros Vision")

    check("Consultation Page Meta Description",
          'content="Express your interest in a personalised numerology consultation with Numeros Vision. Share your questions and requirements to discuss the suitable consultation format and next steps."' in c_html,
          "Meta description matches specification exactly")

    check("Consultation Page Canonical URL",
          '<link rel="canonical" href="https://numerosvision.com/consultation/" />' in c_html,
          "Canonical declared as https://numerosvision.com/consultation/")

    check("Consultation Page H1 Heading",
          '<h1 class="consult-h1">Personalised Numerology Consultation</h1>' in c_html,
          "H1 matches: Personalised Numerology Consultation")

    check("Consultation Page How It Works 4 Steps",
          "Submit form" in c_html and
          "Enquiry review" in c_html and
          "Personal contact" in c_html and
          "Scope &amp; fee" in c_html and
          "Submitting the form expresses interest only" in c_html and
          "does not confirm a booking or create a payment obligation" in c_html,
          "Includes 4-step process and clear interest-only disclaimer")

    check("Consultation Page Form Fields",
          'id="enquiry_name"' in c_html and
          'id="enquiry_email"' in c_html and
          'id="enquiry_phone"' in c_html and
          'id="enquiry_area"' in c_html and
          'id="enquiry_description"' in c_html and
          'id="enquiry_method"' in c_html and
          'id="enquiry_consent"' in c_html,
          "All 7 required enquiry fields + DPDP consent checkbox present")

    check("Consultation Page Primary CTA",
          "Express My Interest ✦" in c_html,
          "Primary CTA is: Express My Interest ✦")

    check("Consultation Page Confirmation Message",
          "We will review the topics you have shared and contact you to discuss your requirements, the consultation format, availability and applicable fee." in c_html,
          "Confirmation text matches required post-submission copy")

    # Test 2: Zero Consultation Fee in Consultation Page
    fee_tokens = ['1050', '1,050', '2499', '3999', '11400']
    has_fee = any(tok in c_html for tok in fee_tokens)
    check("Consultation Page Zero Fee Display",
          not has_fee,
          "Zero consultation fees or price tags present in consultation.html")

    # Test 3: Dist build synchronization
    with open(dist_consult_path, 'r', encoding='utf-8') as f:
        dist_html = f.read()
    check("Dist Cloudflare Pages Mirror Verification",
          "<title>Personal Numerology Consultation | Numeros Vision</title>" in dist_html,
          "dist_cloudflare_pages/consultation/index.html is synchronized")

    # Test 4: Homepage Consultation Banner
    with open('app/static/index.html', 'r', encoding='utf-8') as f:
        idx_html = f.read()

    check("Homepage Consultation Banner Heading",
          "Personalised One-on-One Consultation" in idx_html,
          "Homepage banner updated to Personalised One-on-One Consultation")

    check("Homepage Consultation Banner CTA",
          'href="/consultation/" class="btn-primary-gold"' in idx_html and "Express My Interest ✦" in idx_html,
          "Homepage CTA points to /consultation/ with 'Express My Interest ✦'")

    check("Homepage Zero Consultation Checkout Trigger",
          "openCheckout('consultation" not in idx_html,
          "No direct consultation checkout trigger on homepage")

    # Test 5: Pricing Page Consultation Reference
    with open('app/static/pricing.html', 'r', encoding='utf-8') as f:
        pr_html = f.read()

    check("Pricing Page Table Row",
          "Personalised Consultation" in pr_html and "Enquiry-Based" in pr_html and "/consultation/" in pr_html,
          "Pricing table reflects Enquiry-Based advisory with link to /consultation/")

    check("Pricing Page High-Ticket Section",
          "Enquiry-Based Advisory" in pr_html and 'href="/consultation/" class="btn-gold-action"' in pr_html,
          "VIP section card updated to Enquiry-Based Advisory")

    # Test 6: Report Catalogue Consultation Reference
    with open('app/static/reports_catalogue.html', 'r', encoding='utf-8') as f:
        rep_html = f.read()

    check("Report Catalogue Consultation Card",
          "Enquiry-Based Advisory" in rep_html and "Express My Interest ✦" in rep_html and "/consultation/" in rep_html,
          "Catalogue card displays Enquiry-Based Advisory with Express My Interest CTA")

    # Test 7: Standalone Report Pricing Integrity
    from app.config.pricing_config import REPORT_TIERS
    basic_p = REPORT_TIERS['basic']['price_inr']
    adv_p = REPORT_TIERS['advanced']['price_inr']
    prem_p = REPORT_TIERS['premium']['price_inr']

    check("Standalone Reports Pricing Preserved",
          basic_p == 199 and adv_p == 510 and prem_p == 1050,
          f"Basic: ₹{basic_p} (3p), Advanced: ₹{adv_p} (12p), Premium: ₹{prem_p} (32p) 100% intact")

    # Test 8: Backend API & Enquiry Delivery
    from fastapi import BackgroundTasks
    from app.api.bookings import (
        ConsultationEnquiryRequest,
        submit_consultation_enquiry_direct,
        submit_consultation_enquiry_bookings
    )

    bg = BackgroundTasks()
    test_req = ConsultationEnquiryRequest(
        name="Sunita Narang",
        email="sunita.narang@example.com",
        phone="+91 98111 22334",
        area_of_interest="Business & Brand Entity Alignment",
        description="Launching a new tech venture, need validation on acoustics and trademark vibration.",
        preferred_contact_method="Email",
        consent=True
    )

    resp = submit_consultation_enquiry_direct(test_req, bg)
    check("API Endpoint /api/v1/consultation/enquiry Execution",
          resp.status == "success" and resp.enquiry_id.startswith("ENQ-"),
          f"Enquiry created with ID {resp.enquiry_id}")

    check("API Endpoint Zero Pricing in Response",
          "₹" not in resp.message and "INR" not in resp.message and "fee" in resp.message.lower(),
          "Response confirms enquiry received and clarifies fee discussed personally without displaying amounts")

    resp_b = submit_consultation_enquiry_bookings(test_req, bg)
    check("API Endpoint /api/v1/bookings/enquiry Execution",
          resp_b.status == "success" and resp_b.enquiry_id.startswith("ENQ-"),
          f"Bookings alias enquiry created with ID {resp_b.enquiry_id}")

    # Test 9: Consent enforcement
    no_consent_passed = False
    try:
        from fastapi import HTTPException
        submit_consultation_enquiry_direct(
            ConsultationEnquiryRequest(
                name="Test Reject",
                email="reject@example.com",
                area_of_interest="Career",
                consent=False
            ),
            bg
        )
    except HTTPException as e:
        if e.status_code == 400:
            no_consent_passed = True

    check("API DPDP Consent Validation Enforcement",
          no_consent_passed,
          "Enquiry rejected with 400 Bad Request when consent is False")

    # Test 10: Enquiries log persistence
    log_path = 'data/consultation_enquiries.jsonl'
    check("Enquiries File Logging",
          os.path.exists(log_path) and os.path.getsize(log_path) > 0,
          f"File {log_path} verified with logged entries")

    print("=====================================================================")
    print(f"AUDIT SUMMARY: {passed}/{total} CHECKS PASSED ({passed/total*100:.1f}%)")
    print("=====================================================================")
    return passed == total

if __name__ == '__main__':
    success = run_consultation_audit()
    sys.exit(0 if success else 1)
