import subprocess
import re

with open('app/static/sample.html', 'r', encoding='utf-8') as f:
    text = f.read()

scripts = re.findall(r'<script(?![^>]*application/ld\+json)(?![^>]*src=)[^>]*>([\s\S]*?)</script>', text)
print(f"Found {len(scripts)} inline script block(s).")

all_ok = True
for i, s in enumerate(scripts):
    p = subprocess.run(['node', '-c'], input=s.encode('utf-8'), capture_output=True)
    if p.returncode != 0:
        print(f"ERROR in script {i}: {p.stderr.decode('utf-8', errors='ignore')}")
        all_ok = False
    else:
        print(f"Script {i}: Valid JS syntax!")

if all_ok:
    print("ALL INLINE SCRIPTS IN SAMPLE.HTML HAVE ZERO SYNTAX ERRORS!")
