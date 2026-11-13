"""
Integrates the Unified Marketing Funnel (v1.5.0) component across all calculators.
Replaces legacy locked strips with the responsive 3-Step Curiosity Bridge and Upgrade Panel.
"""

import os
import re

def update_life_path():
    path = os.path.join("app", "static", "tools", "life-path-calculator.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = "<!-- Consecrated Remedies Locked Strip -->"
    if marker in content:
        pos = content.find(marker)
        end_marker = "      </div>\n    `;"
        end = content.find(end_marker, pos)
        if end != -1:
            end += len(end_marker)
            replacement = (
                "<!-- Step 2 & 3: Unified Curiosity Bridge & Standard Upgrade Panel -->\n"
                "      <div id=\"res-funnel-offer\"></div>\n"
                "    `;\n\n"
                "    if (window.nvFunnel && typeof window.nvFunnel.renderOfferBridge === 'function') {\n"
                "      window.nvFunnel.renderOfferBridge('res-funnel-offer', {\n"
                "        productId: 'life_path',\n"
                "        personName: personName,\n"
                "        askCharmUrl: `/charm-ai/?name=${encodeURIComponent(personName)}&day=${d}&month=${m}&year=${y}&q=What+is+the+deep+meaning+of+my+Life+Path+${lp}+and+how+does+it+harmonize+with+Driver+${driver}%3F&auto=true`\n"
                "      });\n"
                "    }"
            )
            content = content[:pos] + replacement + content[end:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("Updated life-path-calculator.html")


def update_lo_shu_grid():
    path = os.path.join("app", "static", "tools", "lo-shu-grid.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = "<!-- Consecrated Remedies Locked Strip -->"
    if marker in content:
        pos = content.find(marker)
        end_idx = content.find("</div>\n      </div>`;", pos)
        if end_idx != -1:
            end_idx += len("</div>\n      </div>`;")
            replacement = (
                "<!-- Step 2 & 3: Unified Curiosity Bridge & Standard Upgrade Panel -->\n"
                "      <div id=\"res-funnel-offer\"></div>\n"
                "    `;\n\n"
                "    if (window.nvFunnel && typeof window.nvFunnel.renderOfferBridge === 'function') {\n"
                "      window.nvFunnel.renderOfferBridge('res-funnel-offer', {\n"
                "        productId: 'lo_shu_grid',\n"
                "        askCharmUrl: `/charm-ai/?q=How+do+I+harmonize+my+Lo+Shu+Grid+missing+numbers%3F&auto=true`\n"
                "      });\n"
                "    }"
            )
            content = content[:pos] + replacement + content[end_idx:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("Updated lo-shu-grid.html")


def update_name_numerology():
    path = os.path.join("app", "static", "tools", "name-numerology.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = "<!-- Consecrated Remedies Locked Strip -->"
    if marker in content:
        pos = content.find(marker)
        end_idx = content.find("</div>\n  </div>\n  <div id=\"nameSaveProfileContainer\">", pos)
        if end_idx != -1:
            end_idx += len("</div>\n  </div>")
            replacement = (
                "<!-- Step 2 & 3: Unified Curiosity Bridge & Standard Upgrade Panel -->\n"
                "  <div id=\"res-funnel-offer\" style=\"margin-top:20px;\"></div>\n"
                "  <script>\n"
                "    document.addEventListener('DOMContentLoaded', function() {\n"
                "      if (window.nvFunnel && typeof window.nvFunnel.renderOfferBridge === 'function') {\n"
                "        window.nvFunnel.renderOfferBridge('res-funnel-offer', { productId: 'name_numerology' });\n"
                "      }\n"
                "    });\n"
                "  </script>"
            )
            content = content[:pos] + replacement + content[end_idx:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("Updated name-numerology.html")


def update_mobile_numerology():
    path = os.path.join("app", "static", "tools", "mobile-numerology.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = "<!-- Consecrated Remedies Locked Strip -->"
    if marker in content:
        pos = content.find(marker)
        end_idx = content.find("</div>\n      </div>\n    </div>\n  </div>\n\n  <!-- FAQ Section", pos)
        if end_idx != -1:
            end_idx += len("</div>\n      </div>")
            replacement = (
                "<!-- Step 2 & 3: Unified Curiosity Bridge & Standard Upgrade Panel -->\n"
                "      <div id=\"res-funnel-offer\" style=\"margin-top:20px;\"></div>\n"
                "      <script>\n"
                "        document.addEventListener('DOMContentLoaded', function() {\n"
                "          if (window.nvFunnel && typeof window.nvFunnel.renderOfferBridge === 'function') {\n"
                "            window.nvFunnel.renderOfferBridge('res-funnel-offer', { productId: 'mobile_numerology' });\n"
                "          }\n"
                "        });\n"
                "      </script>"
            )
            content = content[:pos] + replacement + content[end_idx:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("Updated mobile-numerology.html")


def update_lucky_number():
    path = os.path.join("app", "static", "tools", "lucky-number.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = "<!-- Consecrated Remedies Locked Strip -->"
    if marker in content:
        pos = content.find(marker)
        end_marker = "      </div>\n    `;"
        end = content.find(end_marker, pos)
        if end != -1:
            end += len(end_marker)
            replacement = (
                "<!-- Step 2 & 3: Unified Curiosity Bridge & Standard Upgrade Panel -->\n"
                "      <div id=\"res-funnel-offer\"></div>\n"
                "    `;\n\n"
                "    if (window.nvFunnel && typeof window.nvFunnel.renderOfferBridge === 'function') {\n"
                "      window.nvFunnel.renderOfferBridge('res-funnel-offer', {\n"
                "        productId: 'birth_number',\n"
                "        askCharmUrl: `/charm-ai/?q=What+are+my+lucky+numbers+and+planetary+harmonics%3F&auto=true`\n"
                "      });\n"
                "    }"
            )
            content = content[:pos] + replacement + content[end:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print("Updated lucky-number.html")


def update_static_strip(filename, product_id):
    path = os.path.join("app", "static", "tools", filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern for static HTML locked box:
    # <div style="background:#FFFDF7; ... box-shadow:0 8px 24px ...> ... Anveil Master Dossier ... </div>\s*</div>
    pattern = r'<div style="background:#FFFDF7;[^>]*box-shadow:0 8px 24px[^>]*>[\s\S]*?Anveil Master Dossier[\s\S]*?</div>\s*</div>'
    match = re.search(pattern, content)
    if match:
        replacement = (
            f'<div id="res-funnel-offer-{product_id}"></div>\n'
            f'<script>\n'
            f'  document.addEventListener("DOMContentLoaded", function() {{\n'
            f'    if (window.nvFunnel && typeof window.nvFunnel.renderOfferBridge === "function") {{\n'
            f'      window.nvFunnel.renderOfferBridge("res-funnel-offer-{product_id}", {{ productId: "{product_id}" }});\n'
            f'    }}\n'
            f'  }});\n'
            f'</script>'
        )
        content = content[:match.start()] + replacement + content[match.end():]
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated static strip in {filename}")


def update_birth_number_calculator():
    path = os.path.join("app", "static", "birth_number_calculator.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'id="res-funnel-offer"' not in content:
        # Insert funnel container right inside resultDisplay before closing div
        target = '</div>\n\n  <!-- Bottom CTA Strip -->'
        replacement = (
            '  <!-- Step 2 & 3: Unified Curiosity Bridge & Standard Upgrade Panel -->\n'
            '  <div id="res-funnel-offer" style="margin-top:20px;"></div>\n'
            '</div>\n\n  <!-- Bottom CTA Strip -->'
        )
        if target in content:
            content = content.replace(target, replacement)
        
        # In script, after disp.style.display = "block", render offer bridge
        script_target = 'disp.style.display = "block";'
        script_replacement = (
            'disp.style.display = "block";\n'
            '      if (window.nvFunnel && typeof window.nvFunnel.renderOfferBridge === "function") {\n'
            '        window.nvFunnel.renderOfferBridge("res-funnel-offer", {\n'
            '          productId: "birth_number",\n'
            '          askCharmUrl: `/charm-ai/?day=${dayInput}&q=What+are+the+core+strengths+and+remedies+for+my+Birth+Number+${n}%3F&auto=true`\n'
            '        });\n'
            '      }'
        )
        if script_target in content:
            content = content.replace(script_target, script_replacement)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("Updated birth_number_calculator.html with Funnel Offer Bridge")


def main():
    update_life_path()
    update_lo_shu_grid()
    update_name_numerology()
    update_mobile_numerology()
    update_lucky_number()
    update_birth_number_calculator()

    update_static_strip("baby-naming.html", "name_numerology")
    update_static_strip("blessing-years.html", "personal_year")
    update_static_strip("compatibility-calculator.html", "compatibility")
    update_static_strip("profession-calculator.html", "life_path")
    update_static_strip("property-numerology.html", "name_numerology")
    update_static_strip("vehicle-numerology.html", "mobile_numerology")

    print("All calculator funnel integrations complete.")

if __name__ == "__main__":
    main()
