import subprocess
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_html = os.path.join(root_dir, 'dist_cloudflare_pages', 'your-reading.html')
render_html = os.path.join(root_dir, 'dist_cloudflare_pages', 'your-reading-render.html')

with open(src_html, 'r', encoding='utf-8') as f:
    html = f.read()

# Pre-populate reading content for visual evidence
html = html.replace('id="missing-reading-state" class="empty-state-notice"', 'id="missing-reading-state" class="empty-state-notice" style="display:none;"')
html = html.replace('id="reading-content" style="display:none;"', 'id="reading-content" style="display:block;"')
html = html.replace('id="summary-seeker-name">Seeker Profile<', 'id="summary-seeker-name">Bhaskr Singh<')
html = html.replace('id="summary-seeker-dob">--<', 'id="summary-seeker-dob">1981-11-28<')
html = html.replace('id="summary-driver">-<', 'id="summary-driver">1<')
html = html.replace('id="summary-driver-planet">Ruling Planet<', 'id="summary-driver-planet">Sun · Leadership &amp; Purpose<')
html = html.replace('id="summary-conductor" style="color:var(--emerald);">-<', 'id="summary-conductor" style="color:var(--emerald);">4<')
html = html.replace('id="summary-conductor-planet">Destiny Trajectory<', 'id="summary-conductor-planet">Rahu · Structure &amp; Unconventional Mind<')

with open(render_html, 'w', encoding='utf-8') as f:
    f.write(html)

print("Generated your-reading-render.html")

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_dir = os.path.join(root_dir, "app", "static", "screenshots")
os.makedirs(out_dir, exist_ok=True)

viewports = [
    ("stage_a_1440.png", 1440, 900),
    ("stage_a_768.png", 768, 1024),
    ("stage_a_375.png", 375, 812),
]

for filename, width, height in viewports:
    out_file = os.path.join(out_dir, filename)
    file_url = "file:///" + render_html.replace("\\", "/")
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        f"--window-size={width},{height}",
        "--hide-scrollbars",
        f"--screenshot={out_file}",
        file_url
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(out_file) and os.path.getsize(out_file) > 0:
        print(f"PASS: Screenshot saved: {filename} ({width}px) [{os.path.getsize(out_file)} bytes]")
    else:
        print(f"FAIL: {filename} not generated. {res.stderr}")

if os.path.exists(render_html):
    os.remove(render_html)
