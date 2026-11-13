import os

changes = {
    'app/api/readings.py': [
        ('unlock your Full Master Dossier', 'access your Full Master Dossier')
    ],
    'app/engine/bnn_numerology_engine.py': [
        ('Revolutionary technological builder', 'Transformative technological builder')
    ],
    'app/engine/diplomatic_narrative_engine.py': [
        ('and unlock your highest potential', 'and achieve your highest potential')
    ],
    'app/engine/naming_engine.py': [
        ('elevate market reach', 'expand market reach')
    ],
    'app/engine/package_report_generator.py': [
        ('To unlock in-depth milestone timelines', 'To access in-depth milestone timelines'),
        ('To unlock personalized, step-by-step', 'To access personalized, step-by-step')
    ],
    'app/engine/unified_planetary_numerology_engine.py': [
        ('Revolutionary ideas', 'Pioneering ideas')
    ],
    'app/static/reports_catalogue.html': [
        ('Unlock Essential Dossier', 'Order Essential Dossier'),
        ('Unlock Master Dossier', 'Order Master Dossier'),
        ('Unlock Sovereign Roadmap', 'Order Sovereign Roadmap')
    ],
    'app/static/sample2.html': [
        ('Unlock comprehensive dossier', 'Access comprehensive dossier')
    ],
    'app/static/blog/gemstone-remedies.html': [
        ('<span>✦</span> Unlock Access', '<span>✦</span> View Plans'),
        ('href="/#plans">Unlock Access</a>', 'href="/#plans">View Plans</a>')
    ],
    'app/static/blog/life-path-numbers-explained.html': [
        ('<span>✦</span> Unlock Access', '<span>✦</span> View Plans'),
        ('href="/#plans">Unlock Access</a>', 'href="/#plans">View Plans</a>')
    ],
    'app/static/blog/vedic-gemstone-remedies.html': [
        ('<span>✦</span> Unlock Access', '<span>✦</span> View Plans'),
        ('href="/#plans">Unlock Access</a>', 'href="/#plans">View Plans</a>')
    ],
    'app/static/blog/what-is-numerology.html': [
        ('<span>✦</span> Unlock Access', '<span>✦</span> View Plans'),
        ('href="/#plans">Unlock Access</a>', 'href="/#plans">View Plans</a>')
    ],
    'app/static/tools/life-path-calculator.html': [
        ('<span>✦</span> Unlock Access', '<span>✦</span> View Plans'),
        ('href="/#plans">Unlock Access</a>', 'href="/#plans">View Plans</a>')
    ],
    'app/static/tools/lo-shu-grid.html': [
        ('<span>✦</span> Unlock Access', '<span>✦</span> View Plans'),
        ('href="/#plans">Unlock Access</a>', 'href="/#plans">View Plans</a>')
    ],
    'app/static/tools/lucky-number.html': [
        ('<span>✦</span> Unlock Access', '<span>✦</span> View Plans'),
        ('href="/#plans">Unlock Access</a>', 'href="/#plans">View Plans</a>')
    ],
    'app/static/tools/name-numerology.html': [
        ('<span>✦</span> Unlock Access', '<span>✦</span> View Plans'),
        ('href="/#plans">Unlock Access</a>', 'href="/#plans">View Plans</a>')
    ]
}

def main():
    for filepath, repls in changes.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        for src, dst in repls:
            if src not in content:
                print(f"WARNING: '{src}' not found in {filepath}")
            else:
                content = content.replace(src, dst)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully processed {filepath}")

if __name__ == '__main__':
    main()
