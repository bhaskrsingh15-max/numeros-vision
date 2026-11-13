"""
Verification script for Google Tag Manager (GTM-KW6GQRVZ)
"""
import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATIC_DIR = os.path.join(ROOT_DIR, "app", "static")

files_checked = 0
errors = []

for root, dirs, files in os.walk(STATIC_DIR):
    for file in files:
        if file.endswith(".html"):
            files_checked += 1
            fp = os.path.join(root, file)
            rel_path = os.path.relpath(fp, ROOT_DIR)
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()

            gtm_occurrences = content.count("GTM-KW6GQRVZ")
            if gtm_occurrences != 2:
                errors.append(f"{rel_path}: Expected exactly 2 occurrences of GTM-KW6GQRVZ (head + body noscript), found {gtm_occurrences}")

            # Verify head script is before </head>
            head_close = content.find("</head>")
            gtm_head_pos = content.find("googletagmanager.com/gtm.js?id=")
            if gtm_head_pos == -1 or gtm_head_pos > head_close:
                errors.append(f"{rel_path}: GTM head script missing or placed after </head>")

            # Verify noscript is after <body
            body_open = content.find("<body")
            gtm_body_pos = content.find("googletagmanager.com/ns.html?id=")
            if gtm_body_pos == -1 or gtm_body_pos < body_open:
                errors.append(f"{rel_path}: GTM noscript missing or placed before <body")

print(f"Total files checked: {files_checked}")
if errors:
    print(f"FAILED with {len(errors)} errors:")
    for err in errors[:10]:
        print("  -", err)
else:
    print(f"SUCCESS: All {files_checked} static HTML files have exact, valid GTM (GTM-KW6GQRVZ) head & body implementations!")
