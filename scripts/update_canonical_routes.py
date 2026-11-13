import re

with open("app/main.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update page_calculator_hub
calc_hub_target = """# ── Canonical Roadmap Hub Pages ─────────────────────────────
@app.get("/calculators", include_in_schema=False)
@app.get("/calculators/", include_in_schema=False)
@app.get("/calculator", include_in_schema=False)
@app.get("/calculator/", include_in_schema=False)
@app.get("/calculator_hub.html", include_in_schema=False)
@app.get("/calculator.html", include_in_schema=False)
def page_calculator_hub():"""

calc_hub_repl = """# ── Canonical Roadmap Hub Pages ─────────────────────────────
@app.get("/numerology-calculators", include_in_schema=False)
@app.get("/numerology-calculators/", include_in_schema=False)
@app.get("/calculators", include_in_schema=False)
@app.get("/calculators/", include_in_schema=False)
@app.get("/calculator", include_in_schema=False)
@app.get("/calculator/", include_in_schema=False)
@app.get("/calculator_hub.html", include_in_schema=False)
@app.get("/calculator.html", include_in_schema=False)
def page_calculator_hub():"""

assert calc_hub_target in content, "calc_hub_target not found"
content = content.replace(calc_hub_target, calc_hub_repl, 1)

# 2. Update page_methodology
method_target = """@app.get("/methodology", include_in_schema=False)
@app.get("/methodology/", include_in_schema=False)
def page_methodology():"""

method_repl = """@app.get("/numerology-methodology", include_in_schema=False)
@app.get("/numerology-methodology/", include_in_schema=False)
@app.get("/methodology", include_in_schema=False)
@app.get("/methodology/", include_in_schema=False)
def page_methodology():"""

assert method_target in content, "method_target not found"
content = content.replace(method_target, method_repl, 1)

# 3. Update page_local_hub (city-name-numerology)
local_target = """@app.get("/local", include_in_schema=False)
@app.get("/local/", include_in_schema=False)
def page_local_hub():"""

local_repl = """@app.get("/city-name-numerology", include_in_schema=False)
@app.get("/city-name-numerology/", include_in_schema=False)
@app.get("/local", include_in_schema=False)
@app.get("/local/", include_in_schema=False)
def page_local_hub():"""

assert local_target in content, "local_target not found"
content = content.replace(local_target, local_repl, 1)

# 4. Update calculator aliases
calc_aliases_target = """# ── Canonical Calculator Route Aliases ───────────────────────
@app.get("/calculators/birth-number", include_in_schema=False)
@app.get("/calculators/birth-number/", include_in_schema=False)
def calc_alias_birth_number():
    path = os.path.join(STATIC_DIR, "birth_number_calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/calculators/life-path-number", include_in_schema=False)
@app.get("/calculators/life-path-number/", include_in_schema=False)
def calc_alias_life_path():
    path = os.path.join(STATIC_DIR, "tools", "life-path-calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/calculators/name-numerology", include_in_schema=False)
@app.get("/calculators/name-numerology/", include_in_schema=False)
def calc_alias_name():
    path = os.path.join(STATIC_DIR, "tools", "name-numerology.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/calculators/chaldean-name-numerology", include_in_schema=False)
@app.get("/calculators/chaldean-name-numerology/", include_in_schema=False)
def calc_alias_chaldean():
    path = os.path.join(STATIC_DIR, "tools", "name-balancing.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/calculators/lo-shu-grid", include_in_schema=False)
@app.get("/calculators/lo-shu-grid/", include_in_schema=False)
def calc_alias_lo_shu():
    path = os.path.join(STATIC_DIR, "tools", "lo-shu-grid.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/calculators/mobile-number-numerology", include_in_schema=False)
@app.get("/calculators/mobile-number-numerology/", include_in_schema=False)
def calc_alias_mobile():
    path = os.path.join(STATIC_DIR, "tools", "mobile-numerology.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/calculators/personal-year", include_in_schema=False)
@app.get("/calculators/personal-year/", include_in_schema=False)
@app.get("/calculators/personal-year-numerology", include_in_schema=False)
@app.get("/calculators/personal-year-numerology/", include_in_schema=False)
def calc_alias_personal_year():
    path = os.path.join(STATIC_DIR, "tools", "blessing-years.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/calculators/business-name-numerology", include_in_schema=False)
@app.get("/calculators/business-name-numerology/", include_in_schema=False)
def calc_alias_business_name():
    path = os.path.join(STATIC_DIR, "tools", "name-balancing.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/calculators/numerology-compatibility", include_in_schema=False)
@app.get("/calculators/numerology-compatibility/", include_in_schema=False)
def calc_alias_compatibility():
    path = os.path.join(STATIC_DIR, "tools", "compatibility-calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()"""

calc_aliases_repl = """# ── Canonical Calculator Route Aliases ───────────────────────
@app.get("/birth-date-numerology", include_in_schema=False)
@app.get("/birth-date-numerology/", include_in_schema=False)
@app.get("/calculators/birth-number", include_in_schema=False)
@app.get("/calculators/birth-number/", include_in_schema=False)
def calc_alias_birth_number():
    path = os.path.join(STATIC_DIR, "birth_number_calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()

@app.get("/life-path-number-calculator", include_in_schema=False)
@app.get("/life-path-number-calculator/", include_in_schema=False)
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
@app.get("/calculators/numerology-compatibility", include_in_schema=False)
@app.get("/calculators/numerology-compatibility/", include_in_schema=False)
def calc_alias_compatibility():
    path = os.path.join(STATIC_DIR, "tools", "compatibility-calculator.html")
    return FileResponse(path, media_type="text/html") if os.path.exists(path) else root()"""

assert calc_aliases_target in content, "calc_aliases_target not found"
content = content.replace(calc_aliases_target, calc_aliases_repl, 1)

# 5. Update tool_lucky_number
lucky_target = """@app.get("/tools/lucky-number", include_in_schema=False)
def tool_lucky_number():"""

lucky_repl = """@app.get("/lucky-number-calculator", include_in_schema=False)
@app.get("/lucky-number-calculator/", include_in_schema=False)
@app.get("/tools/lucky-number", include_in_schema=False)
def tool_lucky_number():"""

assert lucky_target in content, "lucky_target not found"
content = content.replace(lucky_target, lucky_repl, 1)

# 6. Update tool_baby_naming
baby_target = """@app.get("/tools/baby-naming", include_in_schema=False)
@app.get("/tools/baby-naming/", include_in_schema=False)
def tool_baby_naming():"""

baby_repl = """@app.get("/baby-name-numerology", include_in_schema=False)
@app.get("/baby-name-numerology/", include_in_schema=False)
@app.get("/tools/baby-naming", include_in_schema=False)
@app.get("/tools/baby-naming/", include_in_schema=False)
def tool_baby_naming():"""

assert baby_target in content, "baby_target not found"
content = content.replace(baby_target, baby_repl, 1)

# 7. Update tool_business_alignment (direction-alignment)
direction_target = """@app.api_route("/tools/business-alignment", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/tools/business-alignment/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/business-alignment", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/business-alignment/", methods=["GET", "POST"], include_in_schema=False)"""

direction_repl = """@app.api_route("/numerology-direction-alignment", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/numerology-direction-alignment/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/tools/business-alignment", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/tools/business-alignment/", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/business-alignment", methods=["GET", "POST"], include_in_schema=False)
@app.api_route("/business-alignment/", methods=["GET", "POST"], include_in_schema=False)"""

assert direction_target in content, "direction_target not found"
content = content.replace(direction_target, direction_repl, 1)

with open("app/main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully updated app/main.py with all canonical routes!")
