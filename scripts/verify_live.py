import urllib.request

req = urllib.request.urlopen('http://127.0.0.1:8000/charm_ai.html')
html = req.read().decode('utf-8')
print("Status:", req.status)
print("Has canonical bottom center svg:", 'style="display:block; stroke:#FFFFFF !important;' in html)
print("Has v=5.5.0:", 'v=5.5.0' in html)

# Also check static CSS
css_req = urllib.request.urlopen('http://127.0.0.1:8000/static/css/roadmap_components.css')
css = css_req.read().decode('utf-8')
print("CSS Status:", css_req.status)
print("CSS has child combinator .nv-bottom-nav-item.active > svg:", '.nv-bottom-nav-item.active > svg' in css)
print("CSS has !important center button stroke:", '.nv-bottom-center-btn svg' in css and 'stroke: #FFFFFF !important;' in css)
print("CSS has !important medallion stroke:", '.nv-charm-medallion-icon svg' in css and 'stroke: #FFFFFF !important;' in css)
