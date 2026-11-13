import sys, urllib.request, re
sys.stdout.reconfigure(encoding='utf-8')

req = urllib.request.urlopen("http://127.0.0.1:8000/about/")
html = req.read().decode('utf-8')

m = re.search(r'<ul[^>]*id=["\']nvNavMenu["\'][\s\S]*?</ul>', html)
if m:
    print(m.group(0))
