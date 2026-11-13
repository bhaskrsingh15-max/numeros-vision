import sys
import re

def update_main_routes():
    sys.stdout.reconfigure(encoding='utf-8')
    with open('app/main.py', 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original app/main.py length: {len(content)}")

    # 1. Enhance 404 Exception Handler to resolve any existing static HTML file
    old_404_block = '''    if exc.status_code == 404:
        if request.url.path.startswith("/api/"):
            return JSONResponse({"status": "error", "message": "API resource not found", "path": request.url.path}, status_code=404)
        path = os.path.join(STATIC_DIR, "404.html")
        if os.path.exists(path):
            return FileResponse(path, status_code=404, media_type="text/html")'''

    new_404_block = '''    if exc.status_code == 404:
        if request.url.path.startswith("/api/"):
            return JSONResponse({"status": "error", "message": "API resource not found", "path": request.url.path}, status_code=404)
        
        # Automatic static HTML file resolution for any page
        raw = request.url.path.strip("/")
        if raw:
            clean = raw.removesuffix(".html").strip("/")
            candidates = [
                os.path.join(STATIC_DIR, f"{clean}.html"),
                os.path.join(STATIC_DIR, clean, "index.html"),
                os.path.join(STATIC_DIR, f"{clean.replace('-', '_')}.html"),
                os.path.join(STATIC_DIR, f"{clean.replace('_', '-')}.html"),
            ]
            if not clean.startswith(("tools/", "blog/", "amp/")):
                candidates.extend([
                    os.path.join(STATIC_DIR, "tools", f"{clean}.html"),
                    os.path.join(STATIC_DIR, "blog", f"{clean}.html"),
                ])
            for cand in candidates:
                if os.path.exists(cand) and os.path.isfile(cand):
                    return FileResponse(cand, media_type="text/html")

        path = os.path.join(STATIC_DIR, "404.html")
        if os.path.exists(path):
            return FileResponse(path, status_code=404, media_type="text/html")'''

    assert old_404_block in content, "old_404_block missing"
    content = content.replace(old_404_block, new_404_block, 1)
    print("Enhanced 404 exception handler with universal static HTML auto-resolution")

    # 2. Fix page_about decorators
    old_about_block = '''@app.get("/about", include_in_schema=False)
@app.get("/about-us", include_in_schema=False)
def page_about():'''

    new_about_block = '''@app.get("/about", include_in_schema=False)
@app.get("/about/", include_in_schema=False)
@app.get("/about.html", include_in_schema=False)
@app.get("/about-us", include_in_schema=False)
@app.get("/about-us/", include_in_schema=False)
@app.get("/about-us.html", include_in_schema=False)
def page_about():'''

    assert old_about_block in content, "old_about_block missing"
    content = content.replace(old_about_block, new_about_block, 1)
    print("Updated page_about route decorators")

    # 3. Fix institutional routes (contact, privacy, terms, refund, disclaimer, pricing, etc.)
    old_inst_block = '''# ── Institutional & Legal Routes ───────────────────────────
@app.get("/contact", include_in_schema=False)
@app.get("/contact-us", include_in_schema=False)
@app.get("/helpdesk", include_in_schema=False)
def page_contact():
    path = os.path.join(STATIC_DIR, "contact.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/privacy", include_in_schema=False)
@app.get("/privacy-policy", include_in_schema=False)
def page_privacy():
    path = os.path.join(STATIC_DIR, "privacy.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/terms", include_in_schema=False)
@app.get("/terms-and-conditions", include_in_schema=False)
@app.get("/terms-of-service", include_in_schema=False)
def page_terms():
    path = os.path.join(STATIC_DIR, "terms.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/refund", include_in_schema=False)
@app.get("/refund-policy", include_in_schema=False)
@app.get("/cancellation", include_in_schema=False)
@app.get("/cancellation-policy", include_in_schema=False)
def page_refund():
    path = os.path.join(STATIC_DIR, "refund.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/disclaimer", include_in_schema=False)
@app.get("/disclaimers", include_in_schema=False)
def page_disclaimer():
    path = os.path.join(STATIC_DIR, "disclaimer.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/pricing", include_in_schema=False)
@app.get("/payments", include_in_schema=False)
@app.get("/subscription", include_in_schema=False)
def page_pricing():
    path = os.path.join(STATIC_DIR, "pricing.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()'''

    new_inst_block = '''# ── Institutional & Legal Routes ───────────────────────────
@app.get("/contact", include_in_schema=False)
@app.get("/contact/", include_in_schema=False)
@app.get("/contact.html", include_in_schema=False)
@app.get("/contact-us", include_in_schema=False)
@app.get("/contact-us/", include_in_schema=False)
@app.get("/helpdesk", include_in_schema=False)
@app.get("/helpdesk/", include_in_schema=False)
def page_contact():
    path = os.path.join(STATIC_DIR, "contact.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/privacy", include_in_schema=False)
@app.get("/privacy/", include_in_schema=False)
@app.get("/privacy.html", include_in_schema=False)
@app.get("/privacy-policy", include_in_schema=False)
@app.get("/privacy-policy/", include_in_schema=False)
def page_privacy():
    path = os.path.join(STATIC_DIR, "privacy.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/terms", include_in_schema=False)
@app.get("/terms/", include_in_schema=False)
@app.get("/terms.html", include_in_schema=False)
@app.get("/terms-and-conditions", include_in_schema=False)
@app.get("/terms-and-conditions/", include_in_schema=False)
@app.get("/terms-of-service", include_in_schema=False)
@app.get("/terms-of-service/", include_in_schema=False)
def page_terms():
    path = os.path.join(STATIC_DIR, "terms.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/refund", include_in_schema=False)
@app.get("/refund/", include_in_schema=False)
@app.get("/refund.html", include_in_schema=False)
@app.get("/refund-policy", include_in_schema=False)
@app.get("/refund-policy/", include_in_schema=False)
@app.get("/cancellation", include_in_schema=False)
@app.get("/cancellation/", include_in_schema=False)
@app.get("/cancellation-policy", include_in_schema=False)
@app.get("/cancellation-policy/", include_in_schema=False)
def page_refund():
    path = os.path.join(STATIC_DIR, "refund.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/disclaimer", include_in_schema=False)
@app.get("/disclaimer/", include_in_schema=False)
@app.get("/disclaimer.html", include_in_schema=False)
@app.get("/disclaimers", include_in_schema=False)
@app.get("/disclaimers/", include_in_schema=False)
def page_disclaimer():
    path = os.path.join(STATIC_DIR, "disclaimer.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/pricing", include_in_schema=False)
@app.get("/pricing/", include_in_schema=False)
@app.get("/pricing.html", include_in_schema=False)
@app.get("/payments", include_in_schema=False)
@app.get("/payments/", include_in_schema=False)
@app.get("/subscription", include_in_schema=False)
@app.get("/subscription/", include_in_schema=False)
def page_pricing():
    path = os.path.join(STATIC_DIR, "pricing.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()'''

    assert old_inst_block in content, "old_inst_block missing"
    content = content.replace(old_inst_block, new_inst_block, 1)
    print("Updated institutional legal route decorators")

    # 4. Fix grievance, shipping, practitioner, cdp, faq, cookies, reports
    old_post_about = '''@app.get("/grievance", include_in_schema=False)
@app.get("/grievance-redressal", include_in_schema=False)
def page_grievance():
    path = os.path.join(STATIC_DIR, "privacy.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/shipping", include_in_schema=False)
@app.get("/shipping-policy", include_in_schema=False)
def page_shipping():
    path = os.path.join(STATIC_DIR, "refund.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/practitioner", include_in_schema=False)
@app.get("/consultation-desk", include_in_schema=False)
def page_practitioner():
    path = os.path.join(STATIC_DIR, "practitioner.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/cdp", include_in_schema=False)
@app.get("/cdp-console", include_in_schema=False)
def page_cdp():
    path = os.path.join(STATIC_DIR, "cdp.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()'''

    new_post_about = '''@app.get("/grievance", include_in_schema=False)
@app.get("/grievance/", include_in_schema=False)
@app.get("/grievance-redressal", include_in_schema=False)
@app.get("/grievance-redressal/", include_in_schema=False)
def page_grievance():
    path = os.path.join(STATIC_DIR, "privacy.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/shipping", include_in_schema=False)
@app.get("/shipping/", include_in_schema=False)
@app.get("/shipping-policy", include_in_schema=False)
@app.get("/shipping-policy/", include_in_schema=False)
def page_shipping():
    path = os.path.join(STATIC_DIR, "refund.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/practitioner", include_in_schema=False)
@app.get("/practitioner/", include_in_schema=False)
@app.get("/practitioner.html", include_in_schema=False)
@app.get("/consultation-desk", include_in_schema=False)
@app.get("/consultation-desk/", include_in_schema=False)
def page_practitioner():
    path = os.path.join(STATIC_DIR, "practitioner.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/cdp", include_in_schema=False)
@app.get("/cdp/", include_in_schema=False)
@app.get("/cdp.html", include_in_schema=False)
@app.get("/cdp-console", include_in_schema=False)
@app.get("/cdp-console/", include_in_schema=False)
def page_cdp():
    path = os.path.join(STATIC_DIR, "cdp.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/cookie-policy", include_in_schema=False)
@app.get("/cookie-policy/", include_in_schema=False)
@app.get("/cookies", include_in_schema=False)
@app.get("/cookies/", include_in_schema=False)
@app.get("/cookie_policy.html", include_in_schema=False)
def page_cookie_policy():
    path = os.path.join(STATIC_DIR, "cookie_policy.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/reports", include_in_schema=False)
@app.get("/reports/", include_in_schema=False)
@app.get("/reports-catalogue", include_in_schema=False)
@app.get("/reports-catalogue/", include_in_schema=False)
def page_reports_catalogue():
    path = os.path.join(STATIC_DIR, "reports_catalogue.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/faq", include_in_schema=False)
@app.get("/faq/", include_in_schema=False)
@app.get("/faqs", include_in_schema=False)
@app.get("/faqs/", include_in_schema=False)
@app.get("/faq.html", include_in_schema=False)
def page_faq_general():
    path = os.path.join(STATIC_DIR, "faq.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()'''

    assert old_post_about in content, "old_post_about missing"
    content = content.replace(old_post_about, new_post_about, 1)
    print("Updated grievance, shipping, practitioner, cdp, cookies, reports, and faq decorators")

    # 5. Fix tool routes trailing slashes
    content = content.replace(
        '@app.get("/tools/life-path-calculator", include_in_schema=False)\ndef tool_life_path():',
        '@app.get("/tools/life-path-calculator", include_in_schema=False)\n@app.get("/tools/life-path-calculator/", include_in_schema=False)\ndef tool_life_path():'
    )
    content = content.replace(
        '@app.get("/tools/lo-shu-grid", include_in_schema=False)\ndef tool_lo_shu():',
        '@app.get("/tools/lo-shu-grid", include_in_schema=False)\n@app.get("/tools/lo-shu-grid/", include_in_schema=False)\ndef tool_lo_shu():'
    )
    content = content.replace(
        '@app.get("/tools/lucky-number", include_in_schema=False)\ndef tool_lucky_number():',
        '@app.get("/tools/lucky-number", include_in_schema=False)\n@app.get("/tools/lucky-number/", include_in_schema=False)\ndef tool_lucky_number():'
    )
    content = content.replace(
        '@app.get("/tools/name-numerology", include_in_schema=False)\ndef tool_name_numerology():',
        '@app.get("/tools/name-numerology", include_in_schema=False)\n@app.get("/tools/name-numerology/", include_in_schema=False)\ndef tool_name_numerology():'
    )
    content = content.replace(
        '@app.get("/tools/name-balancing", include_in_schema=False)\ndef tool_name_balancing():',
        '@app.get("/tools/name-balancing", include_in_schema=False)\n@app.get("/tools/name-balancing/", include_in_schema=False)\ndef tool_name_balancing():'
    )
    content = content.replace(
        '@app.get("/tools/mobile-numerology", include_in_schema=False)\ndef tool_mobile_numerology():',
        '@app.get("/tools/mobile-numerology", include_in_schema=False)\n@app.get("/tools/mobile-numerology/", include_in_schema=False)\ndef tool_mobile_numerology():'
    )
    content = content.replace(
        '@app.get("/tools/blessing-years", include_in_schema=False)\ndef tool_blessing_years():',
        '@app.get("/tools/blessing-years", include_in_schema=False)\n@app.get("/tools/blessing-years/", include_in_schema=False)\ndef tool_blessing_years():'
    )
    content = content.replace(
        '@app.get("/tools/profession-calculator", include_in_schema=False)\ndef tool_profession_calculator():',
        '@app.get("/tools/profession-calculator", include_in_schema=False)\n@app.get("/tools/profession-calculator/", include_in_schema=False)\ndef tool_profession_calculator():'
    )
    content = content.replace(
        '@app.get("/tools/vehicle-numerology", include_in_schema=False)\ndef tool_vehicle_numerology():',
        '@app.get("/tools/vehicle-numerology", include_in_schema=False)\n@app.get("/tools/vehicle-numerology/", include_in_schema=False)\ndef tool_vehicle_numerology():'
    )
    content = content.replace(
        '@app.get("/tools/compatibility-calculator", include_in_schema=False)\n@app.get("/tools/kundali-milan", include_in_schema=False)\ndef tool_compatibility():',
        '@app.get("/tools/compatibility-calculator", include_in_schema=False)\n@app.get("/tools/compatibility-calculator/", include_in_schema=False)\n@app.get("/tools/kundali-milan", include_in_schema=False)\n@app.get("/tools/kundali-milan/", include_in_schema=False)\ndef tool_compatibility():'
    )
    content = content.replace(
        '@app.get("/tools/business-numerology", include_in_schema=False)\ndef tool_business_numerology():',
        '@app.get("/tools/business-numerology", include_in_schema=False)\n@app.get("/tools/business-numerology/", include_in_schema=False)\ndef tool_business_numerology():'
    )
    content = content.replace(
        '@app.get("/tools/property-numerology", include_in_schema=False)\ndef tool_property_numerology():',
        '@app.get("/tools/property-numerology", include_in_schema=False)\n@app.get("/tools/property-numerology/", include_in_schema=False)\ndef tool_property_numerology():'
    )
    print("Updated tool routes with trailing slashes")

    # 6. Fix dynamic blog route trailing slashes and .html suffix
    old_dyn_blog = '''# ── Dynamic Automated Blog Content Fallback Route ──────────
@app.get("/blog/{slug}", include_in_schema=False)
def dynamic_blog_page(slug: str):
    path = os.path.join(STATIC_DIR, "blog", f"{slug}.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    return root()'''

    new_dyn_blog = '''# ── Dynamic Automated Blog Content Fallback Route ──────────
@app.get("/blog/{slug}", include_in_schema=False)
@app.get("/blog/{slug}/", include_in_schema=False)
def dynamic_blog_page(slug: str):
    clean_slug = slug.strip("/").removesuffix(".html")
    path = os.path.join(STATIC_DIR, "blog", f"{clean_slug}.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    return root()'''

    assert old_dyn_blog in content, "old_dyn_blog missing"
    content = content.replace(old_dyn_blog, new_dyn_blog, 1)
    print("Updated dynamic blog page route")

    # 7. Add top-level page fallback route right before exception handler or at end
    page_fallback_route = '''
# ── Universal Page Fallback Route for Any Static HTML File ──
@app.get("/{page}", include_in_schema=False)
@app.get("/{page}/", include_in_schema=False)
def static_page_fallback(page: str):
    clean = page.strip("/").removesuffix(".html")
    candidates = [
        os.path.join(STATIC_DIR, f"{clean}.html"),
        os.path.join(STATIC_DIR, clean, "index.html"),
        os.path.join(STATIC_DIR, f"{clean.replace('-', '_')}.html"),
        os.path.join(STATIC_DIR, f"{clean.replace('_', '-')}.html"),
        os.path.join(STATIC_DIR, "tools", f"{clean}.html"),
        os.path.join(STATIC_DIR, "blog", f"{clean}.html"),
    ]
    for cand in candidates:
        if os.path.exists(cand) and os.path.isfile(cand):
            return FileResponse(cand, media_type="text/html")
    path_404 = os.path.join(STATIC_DIR, "404.html")
    return FileResponse(path_404, status_code=404, media_type="text/html") if os.path.exists(path_404) else root()
'''

    if 'def static_page_fallback' not in content:
        # Insert before # --- Startup & Diagnostics
        target_startup = '# --- Startup & Diagnostics'
        if target_startup in content:
            content = content.replace(target_startup, page_fallback_route + '\n' + target_startup, 1)
            print("Added universal static_page_fallback route")
        else:
            content += '\n' + page_fallback_route
            print("Appended universal static_page_fallback route")

    with open('app/main.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"app/main.py updated successfully! New length: {len(content)}")

if __name__ == '__main__':
    update_main_routes()
