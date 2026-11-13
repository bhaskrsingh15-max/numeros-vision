import subprocess
import os
import shutil
from PIL import Image

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SVG_PATH = os.path.join(ROOT_DIR, "app", "static", "logos", "nv-logo-mark.svg")
ICONS_DIR = os.path.join(ROOT_DIR, "app", "static", "icons")
STATIC_DIR = os.path.join(ROOT_DIR, "app", "static")

os.makedirs(ICONS_DIR, exist_ok=True)

# 1. Create a minimal HTML page to render the SVG with transparent background at 512x512
html_tmp = os.path.join(ROOT_DIR, "temp_render.html")
out_png_512 = os.path.join(ICONS_DIR, "icon-512.png")

with open(html_tmp, "w", encoding="utf-8") as f:
    f.write(f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{
  width: 512px;
  height: 512px;
  background: transparent !important;
  overflow: hidden;
}}
img {{
  width: 512px;
  height: 512px;
  display: block;
}}
</style>
</head>
<body>
  <img src="file:///{SVG_PATH.replace(os.sep, '/')}" />
</body>
</html>""")

chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
]
browser_exe = None
for p in chrome_paths:
    if os.path.exists(p):
        browser_exe = p
        break

if not browser_exe:
    raise RuntimeError("No Chrome or Edge browser found for rendering SVG.")

print(f"Rendering 512x512 PNG using {browser_exe}...")
cmd = [
    browser_exe,
    "--headless",
    "--disable-gpu",
    "--no-sandbox",
    "--default-background-color=00000000",
    "--window-size=512,512",
    f"--screenshot={out_png_512}",
    f"file:///{html_tmp.replace(os.sep, '/')}"
]
res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(html_tmp):
    os.remove(html_tmp)

if not os.path.exists(out_png_512) or os.path.getsize(out_png_512) == 0:
    raise RuntimeError(f"Screenshot failed: {res.stderr}")

print(f"Successfully rendered 512x512 PNG ({os.path.getsize(out_png_512)} bytes)")

# 2. Use Pillow to resize into standard favicon sizes with high-quality LANCZOS filtering
master_img = Image.open(out_png_512).convert("RGBA")
print(f"Master image loaded: mode={master_img.mode}, size={master_img.size}")
print(f"Corner alpha (transparent): {master_img.getpixel((5, 5))}")
print(f"Center pixel: {master_img.getpixel((256, 256))}")

# icon-192.png (PWA & Android touch)
out_png_192 = os.path.join(ICONS_DIR, "icon-192.png")
im192 = master_img.resize((192, 192), Image.Resampling.LANCZOS)
im192.save(out_png_192, "PNG")
print(f"Saved: {out_png_192}")

# apple-touch-icon.png (180x180 for iOS)
out_apple = os.path.join(ICONS_DIR, "apple-touch-icon.png")
im180 = master_img.resize((180, 180), Image.Resampling.LANCZOS)
im180.save(out_apple, "PNG")
print(f"Saved: {out_apple}")

# Also copy to root static for standard iOS lookup
shutil.copyfile(out_apple, os.path.join(STATIC_DIR, "apple-touch-icon.png"))

# favicon-32x32.png
out_png_32 = os.path.join(ICONS_DIR, "favicon-32x32.png")
im32 = master_img.resize((32, 32), Image.Resampling.LANCZOS)
im32.save(out_png_32, "PNG")
print(f"Saved: {out_png_32}")

# favicon-16x16.png
out_png_16 = os.path.join(ICONS_DIR, "favicon-16x16.png")
im16 = master_img.resize((16, 16), Image.Resampling.LANCZOS)
im16.save(out_png_16, "PNG")
print(f"Saved: {out_png_16}")

# Multi-resolution ICO: 16x16, 32x32, 48x48
im48 = master_img.resize((48, 48), Image.Resampling.LANCZOS)
ico_path_icons = os.path.join(ICONS_DIR, "favicon.ico")
ico_path_static = os.path.join(STATIC_DIR, "favicon.ico")

master_img.save(
    ico_path_icons,
    format="ICO",
    sizes=[(16, 16), (32, 32), (48, 48)]
)
shutil.copyfile(ico_path_icons, ico_path_static)
print(f"Saved multi-resolution ICO to {ico_path_static} and {ico_path_icons}")

print("\nALL FAVICONS AND BRAND TOUCH ICONS REGENERATED WITH 100% UNIFORM GOLD SEAL LOGO!")
