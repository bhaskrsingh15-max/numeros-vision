"""
Insert AMP routes into app/main.py
"""
import os

MAIN_PY = os.path.join("app", "main.py")
with open(MAIN_PY, "r", encoding="utf-8") as f:
    content = f.read()

target = 'def dynamic_blog_page(slug: str):'
amp_code = '''

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
    return root()'''

if "def amp_hub():" not in content:
    idx = content.find(target)
    if idx != -1:
        # find end of dynamic_blog_page function
        ret_idx = content.find("return root()", idx)
        insert_pos = ret_idx + len("return root()")
        new_content = content[:insert_pos] + amp_code + content[insert_pos:]
        with open(MAIN_PY, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("Successfully added AMP routes to app/main.py")
    else:
        print("Target not found in app/main.py")
else:
    print("AMP routes already present in app/main.py")
