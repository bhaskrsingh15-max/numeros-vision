import os

def check_file(path, checks):
    print(f"Checking {path}:")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for desc, expected in checks.items():
        present = expected in content
        status = "PASS" if present else "FAIL"
        print(f"  [{status}] {desc}")
    print()

check_file('app/static/charm_ai.html', {
    "Bottom center button has inline stroke:#FFFFFF": 'stroke="#FFFFFF"',
    "Bottom center button has !important style": 'stroke:#FFFFFF !important;',
    "CSS version is 5.5.0": 'roadmap_components.css?v=5.5.0',
    "Nav JS version is 5.5.0": 'nav.js?v=5.5.0'
})

check_file('app/static/css/roadmap_components.css', {
    "Active child combinator > svg": '.nv-bottom-nav-item.active > svg',
    "Center button svg !important stroke": '.nv-bottom-center-btn svg',
    "Medallion icon svg !important stroke": '.nv-charm-medallion-icon svg'
})

check_file('app/static/js/nav.js', {
    "Bottom nav injection has #FFFFFF stroke": 'stroke="#FFFFFF"',
    "Bottom nav injection has !important style": 'stroke:#FFFFFF !important;'
})

check_file('dist_cloudflare_pages/charm_ai.html', {
    "Dist bottom center button has inline stroke:#FFFFFF": 'stroke="#FFFFFF"',
    "Dist CSS version is 5.5.0": 'roadmap_components.css?v=5.5.0'
})
