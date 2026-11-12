from dotenv import load_dotenv
load_dotenv()
import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("numeros_vision")

# Ensure project root is in sys.path so app can run via python app/main.py or uvicorn
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, Response, RedirectResponse, HTMLResponse
from app.services.city_numerology import get_city_profile, render_city_html
from app.security.cyber_defense import CyberDefenseMiddleware

from app.api.readings import router as readings_router
from app.api.privacy import router as privacy_router
from app.api.b2b import router as b2b_router
from app.api.bookings import router as bookings_router, consultation_router
from app.api.payments import router as payments_router, api_router as payments_api_router
from app.api.premium import router as premium_router
from app.api.numerology_v2 import router as numerology_v2_router
from app.api.cost_governance import router as cost_governance_router
from app.api.auth import router as auth_router
from app.api.cdp import router as cdp_router
from app.api.v1_master_api import router as v1_master_router
from app.api.seo_engine_api import router as seo_engine_router
from app.api.geo import router as geo_router
from app.api.logo_intelligence import router as logo_router
from app.api.business_alignment import router as business_router
from app.api.charm_ai import router as charm_router
from app.api.reports_delivery import router as reports_delivery_router
from app.api.billing import router as billing_router

# ── Environment & Production Gating ──────────────────────────
is_prod = os.environ.get("ENVIRONMENT", "development").lower() == "production"

# ── FastAPI App ──────────────────────────────────────────────
app = FastAPI(
    title="Numeros Vision API",
    description="Numeros Vision Secure Platform API.",
    version="3.9.0",
    docs_url=None if is_prod else "/docs",
    redoc_url=None if is_prod else "/redoc",
    openapi_url=None if is_prod else "/openapi.json"
)

# ── Security Middleware ──────────────────────────────────────
app.add_middleware(CyberDefenseMiddleware)

# --- Logo Studio routes ------------------------------------------------------
from fastapi import Form
from fastapi.responses import HTMLResponse
from app.services.brand_report import generate_brand_report

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

@app.get("/tools/logo-studio", response_class=HTMLResponse)
@app.get("/tools/logo-studio/", response_class=HTMLResponse)
def get_logo_studio():
    """Render the full production Logo Studio & Brand Intelligence page."""
    path = os.path.join(STATIC_DIR, "tools", "logo-intelligence.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    return root()

@app.post("/tools/logo-studio", response_class=HTMLResponse)
def post_logo_studio():
    path = os.path.join(STATIC_DIR, "tools", "logo-intelligence.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    return root()

# ── CORS ─────────────────────────────────────────────────────
cors_origins = [
    "https://numerosvision.com",
    "https://www.numerosvision.com"
] if is_prod else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── API Routers ──────────────────────────────────────────────
app.include_router(v1_master_router)
app.include_router(readings_router)
app.include_router(privacy_router)
app.include_router(b2b_router)
app.include_router(bookings_router)
app.include_router(consultation_router)
app.include_router(payments_router)
app.include_router(payments_api_router)
app.include_router(premium_router)
app.include_router(numerology_v2_router)
app.include_router(cost_governance_router)
app.include_router(auth_router)
app.include_router(cdp_router)
app.include_router(seo_engine_router)
app.include_router(geo_router)
app.include_router(logo_router)
app.include_router(business_router)
app.include_router(charm_router)
app.include_router(reports_delivery_router)
app.include_router(billing_router)

# ── Automated SEO & SERP Ranking Scanner API ──────────────
@app.get("/api/v1/seo/ranking-scan", include_in_schema=False)
def api_seo_ranking_scan():
    from app.seo.ranking_scanner import RankingScanner
    report = RankingScanner.scan_all_pages()
    return JSONResponse(report)


# ── Static Files ─────────────────────────────────────────────
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
    for subdir in ["logos", "icons", "images", "screenshots"]:
        sub_path = os.path.join(STATIC_DIR, subdir)
        if os.path.exists(sub_path):
            app.mount(f"/{subdir}", StaticFiles(directory=sub_path), name=subdir)

# ── SEO: Serve manifest.json at root level ───────────────────
@app.get("/manifest.json", include_in_schema=False)
def serve_manifest():
    path = os.path.join(STATIC_DIR, "manifest.json")
    return FileResponse(path, media_type="application/manifest+json")

# ── PWA: Serve service worker at root ────────────────────────
@app.get("/sw.js", include_in_schema=False)
def serve_sw():
    path = os.path.join(STATIC_DIR, "sw.js")
    headers = {
        "Service-Worker-Allowed": "/",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache"
    }
    return FileResponse(path, media_type="application/javascript", headers=headers)

# ── Favicon: Serve favicon.ico at root ───────────────────────
@app.get("/favicon.ico", include_in_schema=False)
def serve_favicon():
    path = os.path.join(STATIC_DIR, "favicon.ico")
    return FileResponse(path, media_type="image/x-icon") if os.path.exists(path) else Response(status_code=204)

@app.get("/apple-touch-icon.png", include_in_schema=False)
@app.get("/apple-touch-icon-precomposed.png", include_in_schema=False)
def serve_apple_touch_icon():
    path = os.path.join(STATIC_DIR, "apple-touch-icon.png")
    return FileResponse(path, media_type="image/png") if os.path.exists(path) else Response(status_code=204)

from starlette.exceptions import HTTPException as StarletteHTTPException

# ── 404 Exception Handler (Custom Branded Recovery Page) ─────
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
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
            return FileResponse(path, status_code=404, media_type="text/html")
    elif exc.status_code == 405:
        accept = request.headers.get("accept", "")
        # If user opened an API endpoint in their browser via GET, redirect to the corresponding UI tool
        if "text/html" in accept or "*/*" in accept:
            p = request.url.path
            if "/business" in p:
                return RedirectResponse(url="/tools/business-alignment", status_code=303)
            elif "/logo" in p:
                return RedirectResponse(url="/tools/logo-studio", status_code=303)
            elif "/contact" in p:
                return RedirectResponse(url="/contact", status_code=303)
    return JSONResponse({"status": "error", "message": exc.detail, "detail": exc.detail}, status_code=exc.status_code)

# ── SEO & AEO: llms.txt, llms-full.txt & robots.txt ─────────────────────────
@app.get("/llms.txt", include_in_schema=False)
def serve_llms():
    path = os.path.join(STATIC_DIR, "llms.txt")
    return FileResponse(path, media_type="text/plain") if os.path.exists(path) else Response("Numeros Vision Deterministic AI Numerology", media_type="text/plain")

@app.get("/llms-full.txt", include_in_schema=False)
def serve_llms_full():
    path = os.path.join(STATIC_DIR, "llms-full.txt")
    return FileResponse(path, media_type="text/plain") if os.path.exists(path) else Response("Numeros Vision Deterministic AI Numerology Full Reference", media_type="text/plain")

@app.get("/robots.txt", include_in_schema=False)
def serve_robots():
    path = os.path.join(STATIC_DIR, "robots.txt")
    return FileResponse(path, media_type="text/plain")

# ── Search Engine Verification: Google Search Console, Bing, IndexNow ───────
@app.get("/BingSiteAuth.xml", include_in_schema=False)
def serve_bing_auth():
    path = os.path.join(STATIC_DIR, "BingSiteAuth.xml")
    if os.path.exists(path):
        return FileResponse(path, media_type="application/xml")
    return Response(content='<?xml version="1.0"?><users><user>A84D35D9658E298B2FE5F2DAA418619A</user></users>', media_type="application/xml")

@app.get("/49bf97a1d74343ce951918a3a0e676d4.txt", include_in_schema=False)
def serve_indexnow_key():
    return Response(content="49bf97a1d74343ce951918a3a0e676d4\n", media_type="text/plain")

@app.get("/google{token}.html", include_in_schema=False)
def serve_google_verification(token: str):
    return Response(content=f"google-site-verification: google{token}.html", media_type="text/html")

# ── SEO: sitemap.xml & HTML Sitemap ─────────────────────────────────────────
@app.get("/sitemap.xml", include_in_schema=False)
def serve_sitemap():
    path = os.path.join(STATIC_DIR, "sitemap.xml")
    if os.path.exists(path):
        return FileResponse(path, media_type="application/xml")
    return Response(content='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://numerosvision.com/</loc></url></urlset>', media_type="application/xml")

@app.get("/sitemap", include_in_schema=False)
@app.get("/sitemap/", include_in_schema=False)
def serve_html_sitemap():
    path = os.path.join(STATIC_DIR, "sitemap.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    return RedirectResponse(url="/sitemap.xml")

# ── Digital Asset Links (for Play Store TWA) ─────────────────
@app.get("/.well-known/assetlinks.json", include_in_schema=False)
def asset_links():
    path = os.path.join(STATIC_DIR, ".well-known", "assetlinks.json")
    if os.path.exists(path):
        return FileResponse(path, media_type="application/json")
    return JSONResponse([{
        "relation": ["delegate_permission/common.handle_all_urls"],
        "target": {
            "namespace": "android_app",
            "package_name": "com.numerosvision.app",
            "sha256_cert_fingerprints": [
                "14:6D:E9:01:07:52:07:71:02:85:63:F6:44:9F:65:4F:92:49:EE:12:12:F1:C7:A7:F3:33:43:24:B9:4C:6D:8F"
            ]
        }
    }])

@app.get("/.well-known/apple-app-site-association", include_in_schema=False)
@app.get("/apple-app-site-association", include_in_schema=False)
def apple_app_site_association():
    path = os.path.join(STATIC_DIR, ".well-known", "apple-app-site-association")
    if os.path.exists(path):
        return FileResponse(path, media_type="application/json")
    return JSONResponse({
        "applinks": {
            "apps": [],
            "details": [{"appID": "TEAM_ID.com.numerosvision.app", "paths": ["*"]}]
        },
        "webcredentials": {"apps": ["TEAM_ID.com.numerosvision.app"]}
    })

# ── Schema.org structured data endpoint (for GEO/AIO) ────────
@app.get("/schema.json", include_in_schema=False)
def structured_data():
    return JSONResponse({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": "https://numerosvision.com/#organization",
                "name": "Numeros Vision",
                "url": "https://numerosvision.com",
                "logo": "https://numerosvision.com/static/icons/icon-512.png",
                "description": "Numeros Vision Charm AI platform based on Core Matrix Numerology, Dasha cycles, Elements Balancing, and personalized gemstone and crystal remedies.",
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "Customer Support",
                    "availableLanguage": ["English", "Hindi"]
                },
                "sameAs": [
                    "https://instagram.com/numerosvision",
                    "https://youtube.com/@numerosvision",
                    "https://twitter.com/numerosvision"
                ]
            },
            {
                "@type": "SoftwareApplication",
                "name": "Numeros Vision Charm AI",
                "applicationCategory": "LifestyleApplication",
                "operatingSystem": "Web, Android, iOS",
                "offers": [
                    {
                        "@type": "Offer",
                        "name": "Premium Charm AI",
                        "price": "999",
                        "priceCurrency": "INR",
                        "billingIncrement": "month"
                    },
                    {
                        "@type": "Offer",
                        "name": "Phone Consultation",
                        "price": "2499",
                        "priceCurrency": "INR"
                    }
                ]
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "What is numerology?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Numerology is an ancient system that reveals insights about personality, destiny, and life events through the analysis of numbers derived from a person's name and date of birth. Numeros Vision computes this using Core Matrix Numerology: Driver & Conductor numbers, Dasha cycles, 5 Elements balancing, repeat & missing numbers, karmic debt, and master numbers."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "How accurate is AI numerology?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Numeros Vision uses deterministic mathematical calculations — not AI guesswork — cross-verified through Core Matrix Numerology. The AI ensures all predictions are based on verifiable numerological principles, not hallucinated content."
                        }
                    },
                    {
                        "@type": "Question",
                        "name": "What is a life path number?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Your Life Path Number is calculated from your date of birth and reveals your core personality traits, strengths, challenges, and life purpose. It is the most important number in numerology. Numeros Vision calculates this along with 5 additional number systems for a complete picture."
                        }
                    }
                ]
            }
        ]
    })

# ── Core Routes ──────────────────────────────────────────────
@app.get("/", include_in_schema=False)
def root():
    path = os.path.join(STATIC_DIR, "index.html")
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache"
    }
    return FileResponse(path, headers=headers) if os.path.exists(path) else JSONResponse({"status": "online"})

@app.get("/sample", include_in_schema=False)
@app.get("/sample/", include_in_schema=False)
@app.get("/sample.html", include_in_schema=False)
@app.get("/sample-report", include_in_schema=False)
@app.get("/sample-report/", include_in_schema=False)
@app.get("/sample_report", include_in_schema=False)
@app.get("/sample-reports", include_in_schema=False)
def serve_sample_report():
    path = os.path.join(STATIC_DIR, "sample.html")
    headers = {"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"}
    return FileResponse(path, media_type="text/html", headers=headers) if os.path.exists(path) else root()

@app.get("/sample2", include_in_schema=False)
@app.get("/sample2/", include_in_schema=False)
@app.get("/sample-2", include_in_schema=False)
@app.get("/sample-2/", include_in_schema=False)
@app.get("/sample2.html", include_in_schema=False)
def serve_sample2():
    path = os.path.join(STATIC_DIR, "sample2.html")
    headers = {"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"}
    return FileResponse(path, media_type="text/html", headers=headers) if os.path.exists(path) else root()

@app.get("/logo-preview", include_in_schema=False)
@app.get("/logos", include_in_schema=False)
def serve_logo_preview():
    path = os.path.join(STATIC_DIR, "logo-preview.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

# ── Master Website Roadmap: Separate Sample Preview Version ──
@app.get("/sample-roadmap", include_in_schema=False)
@app.get("/sample-roadmap/", include_in_schema=False)
@app.get("/sample_roadmap", include_in_schema=False)
@app.get("/sample_roadmap/", include_in_schema=False)
@app.get("/roadmap-preview", include_in_schema=False)
@app.get("/roadmap-preview/", include_in_schema=False)
def serve_sample_roadmap():
    path = os.path.join(STATIC_DIR, "sample_roadmap.html")
    headers = {"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache"}
    return FileResponse(path, media_type="text/html", headers=headers) if os.path.exists(path) else root()

# ── Canonical Roadmap Hub Pages ─────────────────────────────
@app.get("/numerology-calculators", include_in_schema=False)
@app.get("/numerology-calculators/", include_in_schema=False)
@app.get("/calculators", include_in_schema=False)
@app.get("/calculators/", include_in_schema=False)
@app.get("/calculator", include_in_schema=False)
@app.get("/calculator/", include_in_schema=False)
@app.get("/calculator_hub.html", include_in_schema=False)
@app.get("/calculator.html", include_in_schema=False)
def page_calculator_hub():
    path = os.path.join(STATIC_DIR, "calculator_hub.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

# ── Canonical Compatibility & Redirects ─────────────────────
@app.get("/calculators/gemstone", include_in_schema=False)
def redirect_calc_gemstone():
    return RedirectResponse(url="/blog/gemstone-remedies", status_code=301)

@app.get("/calculators/kp", include_in_schema=False)
def redirect_calc_kp():
    return RedirectResponse(url="/tools/life-path-calculator", status_code=301)

@app.get("/calculators/numerology", include_in_schema=False)
def redirect_calc_numerology():
    return RedirectResponse(url="/tools/name-numerology", status_code=301)

@app.get("/calculators/transit", include_in_schema=False)
def redirect_calc_transit():
    return RedirectResponse(url="/tools/blessing-years", status_code=301)

@app.get("/festivals-and-vrats", include_in_schema=False)
def redirect_festivals():
    return RedirectResponse(url="/daily-panchang", status_code=301)

@app.get("/horoscope/daily", include_in_schema=False)
def redirect_daily_horoscope():
    return RedirectResponse(url="/daily-panchang", status_code=301)

@app.get("/shop", include_in_schema=False)
def redirect_shop():
    return RedirectResponse(url="/pricing", status_code=301)

@app.get("/disclaimer.html", include_in_schema=False)
def redirect_disclaimer():
    return RedirectResponse(url="/disclaimer", status_code=301)

@app.get("/pricing.html", include_in_schema=False)
def redirect_pricing():
    return RedirectResponse(url="/pricing", status_code=301)

@app.get("/privacy.html", include_in_schema=False)
def redirect_privacy_html():
    return RedirectResponse(url="/privacy", status_code=301)

@app.get("/terms.html", include_in_schema=False)
def redirect_terms_html():
    return RedirectResponse(url="/terms", status_code=301)

@app.get("/refund.html", include_in_schema=False)
def redirect_refund_html():
    return RedirectResponse(url="/refund-policy", status_code=301)

@app.get("/reports_catalogue.html", include_in_schema=False)
def redirect_reports_cat():
    return RedirectResponse(url="/reports_catalogue", status_code=301)

@app.get("/numerology", include_in_schema=False)
@app.get("/numerology/", include_in_schema=False)
def page_numerology_overview():
    path = os.path.join(STATIC_DIR, "numerology_overview.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/numerology-methodology", include_in_schema=False)
@app.get("/numerology-methodology/", include_in_schema=False)
@app.get("/methodology", include_in_schema=False)
@app.get("/methodology/", include_in_schema=False)
def page_methodology():
    path = os.path.join(STATIC_DIR, "methodology.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/faq", include_in_schema=False)
@app.get("/faq/", include_in_schema=False)
def page_faq():
    path = os.path.join(STATIC_DIR, "faq.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/accessibility", include_in_schema=False)
@app.get("/accessibility/", include_in_schema=False)
def page_accessibility():
    path = os.path.join(STATIC_DIR, "accessibility.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/cookie-policy", include_in_schema=False)
@app.get("/cookie-policy/", include_in_schema=False)
def page_cookie_policy():
    path = os.path.join(STATIC_DIR, "cookie_policy.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/charm-ai", include_in_schema=False)
@app.get("/charm-ai/", include_in_schema=False)
def page_charm_ai():
    path = os.path.join(STATIC_DIR, "charm_ai.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/charm-ai/chat", include_in_schema=False)
@app.get("/charm-ai/chat/", include_in_schema=False)
@app.get("/chat", include_in_schema=False)
@app.get("/chat/", include_in_schema=False)
def page_chat():
    path = os.path.join(STATIC_DIR, "charm_ai_chat.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/reading", include_in_schema=False)
@app.get("/reading/", include_in_schema=False)
def page_reading():
    path = os.path.join(STATIC_DIR, "sample.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/daily-panchang", include_in_schema=False)
@app.get("/daily-panchang/", include_in_schema=False)
def page_daily_panchang():
    path = os.path.join(STATIC_DIR, "tools", "blessing-years.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/matchmaking", include_in_schema=False)
@app.get("/matchmaking/", include_in_schema=False)
def page_matchmaking():
    path = os.path.join(STATIC_DIR, "tools", "compatibility-calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/cart", include_in_schema=False)
@app.get("/cart/", include_in_schema=False)
def page_cart():
    path = os.path.join(STATIC_DIR, "pricing.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/reports", include_in_schema=False)
@app.get("/reports/", include_in_schema=False)
@app.get("/reports_catalogue", include_in_schema=False)
@app.get("/reports_catalogue/", include_in_schema=False)
@app.get("/report", include_in_schema=False)
@app.get("/report/", include_in_schema=False)
def page_reports_catalogue():
    path = os.path.join(STATIC_DIR, "reports_catalogue.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/consultation", include_in_schema=False)
@app.get("/consultation/", include_in_schema=False)
def page_consultation():
    path = os.path.join(STATIC_DIR, "consultation.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/learn", include_in_schema=False)
@app.get("/learn/", include_in_schema=False)
def page_learn():
    path = os.path.join(STATIC_DIR, "learn.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/blog", include_in_schema=False)
@app.get("/blog/", include_in_schema=False)
@app.get("/insights", include_in_schema=False)
@app.get("/insights/", include_in_schema=False)
def page_insights_hub():
    path = os.path.join(STATIC_DIR, "insights_hub.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/compare", include_in_schema=False)
@app.get("/compare/", include_in_schema=False)
def page_compare_hub():
    path = os.path.join(STATIC_DIR, "compare_hub.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/city-name-numerology", include_in_schema=False)
@app.get("/city-name-numerology/", include_in_schema=False)
@app.get("/local", include_in_schema=False)
@app.get("/local/", include_in_schema=False)
def page_local_hub():
    path = os.path.join(STATIC_DIR, "local_hub.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/local/bangalore", include_in_schema=False)
@app.get("/local/bangalore/", include_in_schema=False)
def page_local_bangalore():
    path = os.path.join(STATIC_DIR, "local_bangalore.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else page_local_hub()

@app.get("/local/mumbai", include_in_schema=False)
@app.get("/local/mumbai/", include_in_schema=False)
def page_local_mumbai():
    path = os.path.join(STATIC_DIR, "local_mumbai.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else page_local_hub()

@app.get("/local/delhi", include_in_schema=False)
@app.get("/local/delhi/", include_in_schema=False)
def page_local_delhi():
    path = os.path.join(STATIC_DIR, "local_delhi.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else page_local_hub()

@app.get("/local/dubai", include_in_schema=False)
@app.get("/local/dubai/", include_in_schema=False)
def page_local_dubai():
    path = os.path.join(STATIC_DIR, "local_dubai.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else page_local_hub()

@app.get("/local/{city_slug}", include_in_schema=False)
@app.get("/local/{city_slug}/", include_in_schema=False)
def page_local_dynamic(city_slug: str):
    static_file = os.path.join(STATIC_DIR, f"local_{city_slug.lower()}.html")
    if os.path.exists(static_file):
        return FileResponse(static_file, media_type="text/html")
    profile = get_city_profile(city_slug)
    html = render_city_html(profile)
    return HTMLResponse(html, status_code=200)

@app.get("/insights/{slug}", include_in_schema=False)
@app.get("/insights/{slug}/", include_in_schema=False)
def page_insights_article(slug: str):
    path = os.path.join(STATIC_DIR, "blog", f"{slug}.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    return page_insights_hub()

# ── AnswerThePublic 30-Day SEO Strategy Guide Routes ────────
@app.get("/guides", include_in_schema=False)
@app.get("/guides/", include_in_schema=False)
def page_guides_hub():
    path = os.path.join(STATIC_DIR, "insights_hub.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/guides/{slug}", include_in_schema=False)
@app.get("/guides/{slug}/", include_in_schema=False)
def page_guides_article(slug: str):
    alias_map = {
        "numerology-guide": "what-is-numerology",
        "chaldean-numerology": "chaldean-numerology",
        "chaldean-vs-pythagorean-numerology": "chaldean-vs-pythagorean-numerology",
        "how-to-calculate-name-numerology": "how-to-calculate-name-numerology",
        "numerology-alphabet-chart": "numerology-alphabet-chart",
        "numerology-number-meanings": "numerology-number-meanings",
        "master-numbers-in-numerology": "master-numbers-11-22-33",
        "life-path-and-birth-numbers": "life-path-numbers-explained",
        "name-vs-date-of-birth-numerology": "name-vs-date-of-birth-numerology",
    }
    target_slug = alias_map.get(slug, slug)
    path = os.path.join(STATIC_DIR, "blog", f"{target_slug}.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    tool_map = {
        "house-number-numerology": "property-numerology",
    }
    if slug in tool_map:
        tool_path = os.path.join(STATIC_DIR, "tools", f"{tool_map[slug]}.html")
        if os.path.exists(tool_path):
            return FileResponse(tool_path, media_type="text/html")
    return page_guides_hub()

# ── Canonical Calculator Route Aliases ───────────────────────
@app.get("/birth-date-numerology", include_in_schema=False)
@app.get("/birth-date-numerology/", include_in_schema=False)
@app.get("/calculators/birth-number", include_in_schema=False)
@app.get("/calculators/birth-number/", include_in_schema=False)
def calc_alias_birth_number():
    path = os.path.join(STATIC_DIR, "birth_number_calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/life-path-number-calculator", include_in_schema=False)
@app.get("/life-path-number-calculator/", include_in_schema=False)
@app.get("/calculators/life-path", include_in_schema=False)
@app.get("/calculators/life-path/", include_in_schema=False)
@app.get("/calculators/life-path-number", include_in_schema=False)
@app.get("/calculators/life-path-number/", include_in_schema=False)
def calc_alias_life_path():
    path = os.path.join(STATIC_DIR, "tools", "life-path-calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/name-numerology-calculator", include_in_schema=False)
@app.get("/name-numerology-calculator/", include_in_schema=False)
@app.get("/calculators/name-numerology", include_in_schema=False)
@app.get("/calculators/name-numerology/", include_in_schema=False)
def calc_alias_name():
    path = os.path.join(STATIC_DIR, "tools", "name-numerology.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/chaldean-numerology", include_in_schema=False)
@app.get("/chaldean-numerology/", include_in_schema=False)
@app.get("/calculators/name-balancing", include_in_schema=False)
@app.get("/calculators/name-balancing/", include_in_schema=False)
@app.get("/calculators/chaldean-name-numerology", include_in_schema=False)
@app.get("/calculators/chaldean-name-numerology/", include_in_schema=False)
def calc_alias_chaldean():
    path = os.path.join(STATIC_DIR, "tools", "name-balancing.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/lo-shu-grid-calculator", include_in_schema=False)
@app.get("/lo-shu-grid-calculator/", include_in_schema=False)
@app.get("/calculators/lo-shu-grid", include_in_schema=False)
@app.get("/calculators/lo-shu-grid/", include_in_schema=False)
def calc_alias_lo_shu():
    path = os.path.join(STATIC_DIR, "tools", "lo-shu-grid.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/mobile-number-numerology", include_in_schema=False)
@app.get("/mobile-number-numerology/", include_in_schema=False)
@app.get("/calculators/mobile-number", include_in_schema=False)
@app.get("/calculators/mobile-number/", include_in_schema=False)
@app.get("/calculators/mobile-number-numerology", include_in_schema=False)
@app.get("/calculators/mobile-number-numerology/", include_in_schema=False)
def calc_alias_mobile():
    path = os.path.join(STATIC_DIR, "tools", "mobile-numerology.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/personal-year-numerology", include_in_schema=False)
@app.get("/personal-year-numerology/", include_in_schema=False)
@app.get("/calculators/personal-year", include_in_schema=False)
@app.get("/calculators/personal-year/", include_in_schema=False)
@app.get("/calculators/personal-year-numerology", include_in_schema=False)
@app.get("/calculators/personal-year-numerology/", include_in_schema=False)
def calc_alias_personal_year():
    path = os.path.join(STATIC_DIR, "tools", "blessing-years.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/business-name-numerology", include_in_schema=False)
@app.get("/business-name-numerology/", include_in_schema=False)
@app.get("/calculators/business-name-numerology", include_in_schema=False)
@app.get("/calculators/business-name-numerology/", include_in_schema=False)
def calc_alias_business_name():
    path = os.path.join(STATIC_DIR, "tools", "business-alignment.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/numerology-compatibility-calculator", include_in_schema=False)
@app.get("/numerology-compatibility-calculator/", include_in_schema=False)
@app.get("/calculators/compatibility", include_in_schema=False)
@app.get("/calculators/compatibility/", include_in_schema=False)
@app.get("/calculators/numerology-compatibility", include_in_schema=False)
@app.get("/calculators/numerology-compatibility/", include_in_schema=False)
def calc_alias_compatibility():
    path = os.path.join(STATIC_DIR, "tools", "compatibility-calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/calculators/pythagorean", include_in_schema=False)
@app.get("/calculators/pythagorean/", include_in_schema=False)
@app.get("/calculators/pythagorean-numerology", include_in_schema=False)
@app.get("/calculators/pythagorean-numerology/", include_in_schema=False)
def calc_alias_pythagorean():
    path = os.path.join(STATIC_DIR, "pythagorean_calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

# ── Member Account Routes ────────────────────────────────────
@app.get("/login", include_in_schema=False)
@app.get("/login/", include_in_schema=False)
def page_login():
    path = os.path.join(STATIC_DIR, "login.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/signup", include_in_schema=False)
@app.get("/signup/", include_in_schema=False)
def page_signup():
    path = os.path.join(STATIC_DIR, "signup.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.post("/api/v1/identity/signup", tags=["Authentication & Access Control"])
async def route_identity_signup(req: Request, response: Response):
    from app.api.auth import api_signup, UserSignupRequest
    body = await req.json()
    signup_req = UserSignupRequest(**body)
    return await api_signup(signup_req, req, response)

@app.post("/api/v1/identity/otp/send", tags=["Authentication & Access Control"])
@app.post("/api/v1/identity/send-otp", tags=["Authentication & Access Control"])
async def route_identity_otp_send(req: Request):
    from app.api.auth import api_send_otp, OTPSendRequest
    body = await req.json()
    otp_req = OTPSendRequest(**body)
    return await api_send_otp(otp_req, req)

@app.post("/api/v1/identity/otp/verify", tags=["Authentication & Access Control"])
@app.post("/api/v1/identity/verify-otp", tags=["Authentication & Access Control"])
async def route_identity_otp_verify(req: Request, response: Response):
    from app.api.auth import api_verify_otp, OTPVerifyRequest
    body = await req.json()
    otp_req = OTPVerifyRequest(**body)
    return await api_verify_otp(otp_req, req, response)

@app.post("/api/v1/identity/otp/login", tags=["Authentication & Access Control"])
async def route_identity_otp_login(req: Request, response: Response):
    from app.api.auth import api_otp_login, OTPLoginRequest
    body = await req.json()
    otp_req = OTPLoginRequest(**body)
    return await api_otp_login(otp_req, req, response)

@app.get("/dashboard", include_in_schema=False)
@app.get("/dashboard/", include_in_schema=False)
def page_dashboard():
    path = os.path.join(STATIC_DIR, "dashboard.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/profile", include_in_schema=False)
@app.get("/profile/", include_in_schema=False)
def page_profile():
    return RedirectResponse(url="/dashboard/", status_code=307)

# ── SEO Tool Pages ─────────────────────────────────────────
@app.get("/tools/life-path-calculator", include_in_schema=False)
@app.get("/tools/life-path-calculator/", include_in_schema=False)
def tool_life_path():
    path = os.path.join(STATIC_DIR, "tools", "life-path-calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/tools/lo-shu-grid", include_in_schema=False)
@app.get("/tools/lo-shu-grid/", include_in_schema=False)
def tool_lo_shu():
    path = os.path.join(STATIC_DIR, "tools", "lo-shu-grid.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/lucky-number-calculator", include_in_schema=False)
@app.get("/lucky-number-calculator/", include_in_schema=False)
@app.get("/tools/lucky-number", include_in_schema=False)
@app.get("/tools/lucky-number/", include_in_schema=False)
def tool_lucky_number():
    path = os.path.join(STATIC_DIR, "tools", "lucky-number.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/tools/name-numerology", include_in_schema=False)
@app.get("/tools/name-numerology/", include_in_schema=False)
def tool_name_numerology():
    path = os.path.join(STATIC_DIR, "tools", "name-numerology.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/tools/name-balancing", include_in_schema=False)
@app.get("/tools/name-balancing/", include_in_schema=False)
def tool_name_balancing():
    path = os.path.join(STATIC_DIR, "tools", "name-balancing.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/tools/mobile-numerology", include_in_schema=False)
@app.get("/tools/mobile-numerology/", include_in_schema=False)
def tool_mobile_numerology():
    path = os.path.join(STATIC_DIR, "tools", "mobile-numerology.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/tools/blessing-years", include_in_schema=False)
@app.get("/tools/blessing-years/", include_in_schema=False)
def tool_blessing_years():
    path = os.path.join(STATIC_DIR, "tools", "blessing-years.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/tools/profession-calculator", include_in_schema=False)
@app.get("/tools/profession-calculator/", include_in_schema=False)
def tool_profession_calculator():
    path = os.path.join(STATIC_DIR, "tools", "profession-calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/tools/vehicle-numerology", include_in_schema=False)
@app.get("/tools/vehicle-numerology/", include_in_schema=False)
def tool_vehicle_numerology():
    path = os.path.join(STATIC_DIR, "tools", "vehicle-numerology.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/tools/compatibility-calculator", include_in_schema=False)
@app.get("/tools/compatibility-calculator/", include_in_schema=False)
@app.get("/tools/kundali-milan", include_in_schema=False)
@app.get("/tools/kundali-milan/", include_in_schema=False)
def tool_compatibility():
    path = os.path.join(STATIC_DIR, "tools", "compatibility-calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/tools/business-numerology", include_in_schema=False)
@app.get("/tools/business-numerology/", include_in_schema=False)
def tool_business_numerology():
    path = os.path.join(STATIC_DIR, "tools", "name-balancing.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/tools/property-numerology", include_in_schema=False)
@app.get("/tools/property-numerology/", include_in_schema=False)
def tool_property_numerology():
    path = os.path.join(STATIC_DIR, "tools", "property-numerology.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/baby-name-numerology", include_in_schema=False)
@app.get("/baby-name-numerology/", include_in_schema=False)
@app.get("/tools/baby-naming", include_in_schema=False)
@app.get("/tools/baby-naming/", include_in_schema=False)
def tool_baby_naming():
    path = os.path.join(STATIC_DIR, "tools", "baby-naming.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.api_route("/numerology-direction-alignment", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/numerology-direction-alignment/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/tools/business-alignment", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/tools/business-alignment/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/business-alignment", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/business-alignment/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/calculators/business-alignment", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/calculators/business-alignment/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/tools/business-direction", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/tools/business-direction/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/business-direction", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/business-direction/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/calculators/business-direction", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/calculators/business-direction/", methods=["GET", "POST"], include_in_schema=False)
def tool_business_alignment():
    path = os.path.join(STATIC_DIR, "tools", "business-alignment.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.api_route("/tools/logo-studio", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/tools/logo-studio/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/logo-studio", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/logo-studio/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/calculators/logo-studio", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/calculators/logo-studio/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/tools/logo-intelligence", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/tools/logo-intelligence/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/logo-intelligence", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/logo-intelligence/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/calculators/logo-intelligence", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/calculators/logo-intelligence/", methods=["GET", "POST"], include_in_schema=False)
def tool_logo_intelligence():
    path = os.path.join(STATIC_DIR, "tools", "logo-intelligence.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

# ── Dynamic Automated Tool Fallback Route ─────────────────
@app.get("/tools/{slug}", include_in_schema=False)
@app.get("/tools/{slug}/", include_in_schema=False)
def dynamic_tool_page(slug: str):
    path = os.path.join(STATIC_DIR, "tools", f"{slug}.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    return root()


# ── Blog Routes ───────────────────────────────────────────
@app.get("/blog/what-is-numerology", include_in_schema=False)
@app.get("/blog/what-is-numerology/", include_in_schema=False)
def blog_what_is_numerology():
    path = os.path.join(STATIC_DIR, "blog", "what-is-numerology.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/blog/life-path-numbers-explained", include_in_schema=False)
def blog_life_path():
    path = os.path.join(STATIC_DIR, "blog", "life-path-numbers-explained.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/blog/gemstone-remedies", include_in_schema=False)
@app.get("/blog/vedic-gemstone-remedies", include_in_schema=False)
def blog_gemstones():
    path = os.path.join(STATIC_DIR, "blog", "gemstone-remedies.html")
    if not os.path.exists(path):
        path = os.path.join(STATIC_DIR, "blog", "vedic-gemstone-remedies.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/blog/master-numbers-11-22-33", include_in_schema=False)
def blog_master_numbers():
    path = os.path.join(STATIC_DIR, "blog", "master-numbers-11-22-33.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/blog/chaldean-vs-pythagorean-numerology", include_in_schema=False)
@app.get("/blog/chaldean-vs-pythagorean-numerology/", include_in_schema=False)
def blog_chaldean_vs_pythagorean():
    path = os.path.join(STATIC_DIR, "blog", "chaldean-vs-pythagorean-numerology.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/blog/lo-shu-grid-8-planes", include_in_schema=False)
def blog_lo_shu_planes():
    path = os.path.join(STATIC_DIR, "blog", "lo-shu-grid-8-planes.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/blog/mobile-numerology-malefic-pairs", include_in_schema=False)
@app.get("/blog/mobile-numerology-malefic-pairs/", include_in_schema=False)
def blog_mobile_malefics():
    path = os.path.join(STATIC_DIR, "blog", "mobile-numerology-malefic-pairs.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

# ── Dynamic Automated Blog Content Fallback Route ──────────
@app.get("/blog/{slug}", include_in_schema=False)
@app.get("/blog/{slug}/", include_in_schema=False)
def dynamic_blog_page(slug: str):
    clean_slug = slug.strip("/").removesuffix(".html")
    path = os.path.join(STATIC_DIR, "blog", f"{clean_slug}.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    return root()

# ── Google AMP (Accelerated Mobile Pages) Routes ───────────
@app.get("/amp", include_in_schema=False)
@app.get("/amp/", include_in_schema=False)
def amp_hub():
    path = os.path.join(STATIC_DIR, "amp", "index.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    return root()

@app.get("/amp/blog/{slug}", include_in_schema=False)
@app.get("/amp/blog/{slug}/", include_in_schema=False)
@app.get("/blog/{slug}/amp", include_in_schema=False)
@app.get("/blog/{slug}/amp/", include_in_schema=False)
def amp_blog_page(slug: str):
    clean_slug = slug.strip("/").lower()
    path = os.path.join(STATIC_DIR, "amp", "blog", f"{clean_slug}.html")
    if os.path.exists(path):
        return FileResponse(path, media_type="text/html")
    fallback = os.path.join(STATIC_DIR, "blog", f"{clean_slug}.html")
    if os.path.exists(fallback):
        return FileResponse(fallback, media_type="text/html")
    return root()



# ── Institutional & Legal Routes ───────────────────────────
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
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/about", include_in_schema=False)
@app.get("/about/", include_in_schema=False)
@app.get("/about.html", include_in_schema=False)
@app.get("/about-us", include_in_schema=False)
@app.get("/about-us/", include_in_schema=False)
@app.get("/about-us.html", include_in_schema=False)
def page_about():
    path = os.path.join(STATIC_DIR, "about.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/grievance", include_in_schema=False)
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

# /cdp route removed per CDP decommission

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
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.post("/api/v1/contact")
async def api_submit_contact(request: Request):
    try:
        body = await request.json()
        name = body.get("name", "").strip()
        email = body.get("email", "").strip()
        message = body.get("message", "").strip()
        phone = body.get("phone", "").strip()
        category = body.get("category", "general")
        order = body.get("order", "").strip()
        if not name or not email or not message:
            return JSONResponse({"status": "error", "message": "Name, email, and message are required."}, status_code=400)
        import random
        ticket_id = f"NV-TICK-{random.randint(100000, 999999)}"
        logger.info(f"[LEAD_INQUIRY] Ticket: {ticket_id} | Name: {name} | Email: {email} | Phone: {phone} | Category: {category} | OrderRef: {order}")

        # Capture and stitch lead into CDP Identity Graph
        try:
            from app.engine.cdp_identity_engine import IdentityPayload, resolve_golden_profile, enrich_audience_taxonomy
            p = IdentityPayload(
                email=email,
                phone=phone,
                client_ip=request.client.host if request.client else "127.0.0.1"
            )
            prof = resolve_golden_profile(p)
            gid = prof["golden_profile_id"]
            enrich_audience_taxonomy(
                golden_profile_id=gid,
                chart_data={"sun_sign": "Aries", "mulank": 5, "bhagyank": 6, "mahadasha": "Mercury"},
                transaction_data={"total_spend_inr": 0.0, "purchase_count": 0},
                behavioral_data={"page_views_career": 2 if category == "career" else 1}
            )
            logger.info(f"[CDP_STITCH] Lead stitched into Golden Profile: {gid}")
        except Exception as cdp_err:
            logger.warning(f"[CDP_STITCH_WARN] {cdp_err}")

        return JSONResponse({
            "status": "success",
            "ticket_id": ticket_id,
            "message": "Your inquiry has been received. Our advisory desk will respond within 24 business hours."
        })
    except Exception as e:
        logger.error(f"[INQUIRY_ERROR] {e}")
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


# ── Enterprise Agentic AI Observability & Gateway Routes ──
@app.get("/api/v1/agent/status")
def api_get_agent_status():
    from app.engine.enterprise_agent_gateway import (
        DATA_PERIMETER_ALLOWED,
        DATA_PERIMETER_RESTRICTED,
        AGENT_TOOL_REGISTRY,
        _TRACE_BUFFER
    )
    return {
        "status": "HEALTHY",
        "gateway": "Enterprise Agentic AI Gateway",
        "version": "4.1.0",
        "agent_identity": {
            "agent_id": "charm-ai-oracle-v4",
            "agent_name": "Charm AI",
            "role": "astrological_advisor",
            "authorized_scopes": [
                "read:astrological_coords",
                "compute:deterministic_matrix",
                "retrieve:sanitized_wisdom",
                "generate:narrative_guidance"
            ]
        },
        "data_perimeter": {
            "status": "AIR_GAPPED_ENFORCED",
            "allowed_domains": list(DATA_PERIMETER_ALLOWED),
            "restricted_domains": list(DATA_PERIMETER_RESTRICTED)
        },
        "tool_registry": {
            "registered_tools_count": len(AGENT_TOOL_REGISTRY),
            "manifest": {k: {"tier": v.tier, "deterministic": v.deterministic} for k, v in AGENT_TOOL_REGISTRY.items()}
        },
        "circuit_breaker": {
            "status": "ACTIVE",
            "filters": ["INTERCEPTED_CRISIS_HITL", "CLINICAL_HEALTH_CARVEOUT", "FINANCIAL_SPECULATION_CARVEOUT"]
        },
        "observability": {
            "buffered_traces_count": len(_TRACE_BUFFER),
            "trace_endpoint": "/api/v1/agent/traces"
        },
        "compliance": {
            "disclaimer_url": "/disclaimer",
            "terms_url": "/terms",
            "privacy_url": "/privacy",
            "refund_policy_url": "/refund-policy"
        }
    }

@app.get("/api/v1/agent/traces")
def api_get_agent_traces(limit: int = 50):
    from app.engine.enterprise_agent_gateway import get_recent_traces
    return {"status": "success", "traces": get_recent_traces(limit)}

@app.post("/api/v1/agent/gateway/turn")
async def api_agent_gateway_turn(request: Request):
    from app.engine.enterprise_agent_gateway import EnterpriseAgentGateway
    body = await request.json()
    prompt = body.get("prompt", "")
    topic = body.get("topic", "general")
    user_id = body.get("user_id", "guest_user")
    session_id = body.get("session_id")
    result = EnterpriseAgentGateway.process_turn(
        user_prompt=prompt,
        topic=topic,
        user_id=user_id,
        session_id=session_id
    )
    return JSONResponse(result)


# ── Logo / Brand Assets ───────────────────────────────────
@app.get("/logos/{filename}", include_in_schema=False)
def serve_logo(filename: str):
    import re
    if not re.match(r'^[\w\-\.]+\.(png|jpg|svg|webp)$', filename):
        return JSONResponse({"error": "invalid"}, status_code=400)
    path = os.path.join(STATIC_DIR, "logos", filename)
    return FileResponse(path) if os.path.exists(path) else JSONResponse({"error": "not found"}, status_code=404)

# ── Logo Preview ──────────────────────────────────────────
@app.get("/logo-preview", include_in_schema=False)
def logo_preview():
    path = os.path.join(STATIC_DIR, "logo-preview.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else JSONResponse({"error": "not found"}, status_code=404)

@app.get("/demo", include_in_schema=False)
def demo_page():
    path = os.path.join(STATIC_DIR, "demo.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else JSONResponse({"error": "not found"}, status_code=404)

# ── Health & System Diagnostics ───────────────────────────
@app.get("/health")
def health_check(request: Request):
    format = request.query_params.get("format", "")
    health_data = {
        "status": "healthy",
        "platform": "Numeros Vision — ANVEIL EVERY CHARM · Powered by AI",
        "version": "3.7.0",
        "waf_security": "active",
        "rag_status": "Active and grounded",
        "engines": ["CoreMatrix", "LoShu", "Dasha", "ElementsBalancing", "Chaldean", "ChaldeanAstro", "NameBalancing", "MobileNumerology", "BlessingYears", "ProfessionBNN", "PractitionerCRM", "AssetNumerology"],
        "pwa": "enabled",
        "play_store_ready": True,
        "features": ["payments", "premium_blueprint", "questionnaire", "voice_input", "seo_tools", "blog", "aeo_geo_optimization", "institutional_compliance", "practitioner_workspace"],
        "tools": [
            "/tools/name-balancing",
            "/tools/mobile-numerology",
            "/tools/life-path-calculator",
            "/tools/lo-shu-grid",
            "/tools/blessing-years",
            "/tools/profession-calculator",
            "/tools/vehicle-numerology",
            "/tools/compatibility-calculator",
            "/tools/property-numerology",
            "/tools/baby-naming",
            "/tools/lucky-number",
            "/tools/name-numerology",
            "/tools/logo-studio"
        ],
        "blog": [
            "/blog/what-is-numerology",
            "/blog/master-numbers-11-22-33",
            "/blog/chaldean-vs-pythagorean-numerology",
            "/blog/lo-shu-grid-8-planes",
            "/blog/mobile-numerology-malefic-pairs",
            "/blog/life-path-numbers-explained",
            "/blog/gemstone-remedies",
            "/blog/vedic-gemstone-remedies"
        ],
        "corporate_and_legal": [
            "/about",
            "/practitioner",
            "/pricing",
            "/contact",
            "/privacy",
            "/terms",
            "/refund-policy"
        ]
    }
    
    # If explicitly requesting JSON, or non-browser API client:
    accept = request.headers.get("accept", "")
    if format == "json" or ("text/html" not in accept and "*/*" not in accept):
        return health_data
    
    # Render rich, branded System Status Dashboard for humans in browser
    tools_html = "".join([f'<a href="{t}" class="badge-link" target="_blank">{t.replace("/tools/", "")}</a>' for t in health_data["tools"]])
    engines_html = "".join([f'<span class="badge-engine">✓ {e}</span>' for e in health_data["engines"]])
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>System Status &amp; Health — Numeros Vision</title>
  <link rel="icon" type="image/svg+xml" href="/logos/nv-logo-mark.svg">
  <link rel="stylesheet" href="/static/css/theme.css?v=4.8.0">
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body {{
      background: #FFFDF7;
      color: #523E28;
      font-family: 'Inter', sans-serif;
      margin: 0;
      padding: 40px 20px;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      box-sizing: border-box;
    }}
    .status-card {{
      background: #FFFFFF;
      border: 1.5px solid rgba(201, 162, 39, 0.35);
      border-radius: 20px;
      padding: 36px 40px;
      max-width: 760px;
      width: 100%;
      box-shadow: 0 16px 48px rgba(82, 62, 40, 0.08);
    }}
    .status-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1.5px solid #F7F3EA;
      padding-bottom: 20px;
      margin-bottom: 24px;
    }}
    .status-brand {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    .status-brand img {{
      width: 50px;
      height: 50px;
    }}
    .status-brand h1 {{
      font-family: 'Cinzel', serif;
      font-size: 1.25rem;
      margin: 0;
      color: #523E28;
      letter-spacing: 1.5px;
    }}
    .status-brand p {{
      margin: 2px 0 0;
      font-size: 0.78rem;
      color: #8B6914;
      font-weight: 600;
      letter-spacing: 1px;
    }}
    .status-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #E8F5E9;
      color: #16835B;
      padding: 6px 16px;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 700;
      border: 1px solid rgba(22, 131, 91, 0.25);
    }}
    .pulse-dot {{
      width: 10px;
      height: 10px;
      background: #16835B;
      border-radius: 50%;
      animation: pulse 1.8s infinite;
    }}
    @keyframes pulse {{
      0% {{ transform: scale(0.95); opacity: 0.8; }}
      50% {{ transform: scale(1.2); opacity: 1; }}
      100% {{ transform: scale(0.95); opacity: 0.8; }}
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .meta-box {{
      background: #FFFDF7;
      border: 1px solid #F7F3EA;
      border-radius: 12px;
      padding: 14px 18px;
    }}
    .meta-label {{
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: #7A654D;
      font-weight: 600;
      margin-bottom: 4px;
    }}
    .meta-value {{
      font-size: 0.95rem;
      font-weight: 700;
      color: #523E28;
    }}
    .section-title {{
      font-family: 'Cinzel', serif;
      font-size: 0.92rem;
      color: #8B6914;
      margin: 20px 0 10px;
      text-transform: uppercase;
      letter-spacing: 1.2px;
    }}
    .badges-wrap {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 20px;
    }}
    .badge-engine {{
      background: #F7F3EA;
      color: #523E28;
      font-size: 0.78rem;
      font-weight: 600;
      padding: 4px 12px;
      border-radius: 8px;
      border: 1px solid rgba(201, 162, 39, 0.2);
    }}
    .badge-link {{
      background: rgba(201, 162, 39, 0.12);
      color: #8B6914;
      font-size: 0.78rem;
      font-weight: 600;
      padding: 5px 12px;
      border-radius: 8px;
      text-decoration: none;
      border: 1px solid rgba(201, 162, 39, 0.3);
      transition: all 0.2s;
    }}
    .badge-link:hover {{
      background: #C9A227;
      color: #FFFFFF;
    }}
    .footer-actions {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 28px;
      padding-top: 18px;
      border-top: 1.5px solid #F7F3EA;
      font-size: 0.8rem;
    }}
    .btn-home {{
      background: #8B6914;
      color: #FFFFFF;
      padding: 10px 22px;
      border-radius: 10px;
      text-decoration: none;
      font-weight: 600;
      transition: background 0.2s;
    }}
    .btn-home:hover {{
      background: #C9A227;
    }}
    .json-link {{
      color: #7A654D;
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <div class="status-card">
    <div class="status-header">
      <div class="status-brand">
        <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Logo">
        <div>
          <h1>NUMEROS VISION</h1>
          <p>SYSTEM HEALTH &amp; ENGINE STATUS</p>
        </div>
      </div>
      <div class="status-pill">
        <span class="pulse-dot"></span>
        <span>ALL SYSTEMS OPERATIONAL</span>
      </div>
    </div>

    <div class="meta-grid">
      <div class="meta-box">
        <div class="meta-label">Release Version</div>
        <div class="meta-value">v3.7.0 (Production)</div>
      </div>
      <div class="meta-box">
        <div class="meta-label">WAF &amp; Cyber Shield</div>
        <div class="meta-value" style="color: #16835B;">Active &amp; Guarded</div>
      </div>
      <div class="meta-box">
        <div class="meta-label">Deterministic AI Core</div>
        <div class="meta-value">12 Engines Online</div>
      </div>
      <div class="meta-box">
        <div class="meta-label">PWA &amp; Mobile Web</div>
        <div class="meta-value">Play Store Ready</div>
      </div>
    </div>

    <div class="section-title">Verified Calculation Engines</div>
    <div class="badges-wrap">
      {engines_html}
    </div>

    <div class="section-title">Online Interactive Tools</div>
    <div class="badges-wrap">
      {tools_html}
    </div>

    <div class="footer-actions">
      <a href="/" class="btn-home">← Return to Homepage</a>
      <a href="/health?format=json" class="json-link">View Raw JSON Endpoint</a>
    </div>
  </div>
</body>
</html>"""
    return HTMLResponse(content=html, status_code=200)

def health_check_legacy():
    return {
        "status": "healthy",
        "platform": "Numeros Vision — ANVEIL EVERY CHARM · Powered by AI",
        "version": "3.7.0",
        "waf_security": "active",
        "rag_status": "Active and grounded",
        "engines": ["CoreMatrix", "LoShu", "Dasha", "ElementsBalancing", "Chaldean", "ChaldeanAstro", "NameBalancing", "MobileNumerology", "BlessingYears", "ProfessionBNN", "PractitionerCRM", "AssetNumerology"],
        "pwa": "enabled",
        "play_store_ready": True,
        "features": ["payments", "premium_blueprint", "questionnaire", "voice_input", "seo_tools", "blog", "aeo_geo_optimization", "institutional_compliance", "practitioner_workspace"],
        "tools": [
            "/tools/name-balancing",
            "/tools/mobile-numerology",
            "/tools/life-path-calculator",
            "/tools/lo-shu-grid",
            "/tools/blessing-years",
            "/tools/profession-calculator",
            "/tools/vehicle-numerology",
            "/tools/compatibility-calculator",
            "/tools/property-numerology",
            "/tools/baby-naming",
            "/tools/lucky-number",
            "/tools/name-numerology"
        ],
        "blog": [
            "/blog/what-is-numerology",
            "/blog/master-numbers-11-22-33",
            "/blog/chaldean-vs-pythagorean-numerology",
            "/blog/lo-shu-grid-8-planes",
            "/blog/mobile-numerology-malefic-pairs",
            "/blog/life-path-numbers-explained",
            "/blog/gemstone-remedies",
            "/blog/vedic-gemstone-remedies"
        ],
        "corporate_and_legal": [
            "/about",
            "/practitioner",
            "/pricing",
            "/contact",
            "/privacy",
            "/terms",
            "/refund-policy"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


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
            status_code = 404 if clean == "404" else 200
            return FileResponse(cand, status_code=status_code, media_type="text/html")
    path_404 = os.path.join(STATIC_DIR, "404.html")
    return FileResponse(path_404, status_code=404, media_type="text/html") if os.path.exists(path_404) else root()
