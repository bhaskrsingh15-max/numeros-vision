# -*- coding: utf-8 -*-
import os

path = os.path.join("app", "main.py")
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

start_marker = "# ── SEO & AEO: llms.txt & robots.txt ─────────────────────────"
end_marker = "# ── Digital Asset Links (for Play Store TWA) ─────────────────"

start_idx = text.find(start_marker)
end_idx = text.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f"Error: markers not found. start={start_idx}, end={end_idx}")
else:
    new_seo_routes = '''# ── SEO & AEO: llms.txt, llms-full.txt & robots.txt ─────────────────────────
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
    return Response(content="49bf97a1d74343ce951918a3a0e676d4\\n", media_type="text/plain")

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

'''
    new_text = text[:start_idx] + new_seo_routes + text[end_idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("SUCCESS: app/main.py updated with production SEO & verification routes.")
