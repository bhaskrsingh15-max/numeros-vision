# -*- coding: utf-8 -*-
import os

path = os.path.join("app", "static", "charm_ai.html")
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace("localStorage.setItem('nv_premium_token', 'test_master_pass');", "// User starts with default free tier")
text = text.replace("const premiumToken = localStorage.getItem('nv_premium_token') || 'test_master_pass';", "const premiumToken = localStorage.getItem('nv_premium_token') || '';")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: charm_ai.html updated.")
