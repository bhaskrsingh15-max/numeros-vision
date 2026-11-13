import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    path = 'app/static/about.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Mission Box
    old_box = '''    <!-- The Mission Statement -->
    <div class="mission-box">
      <div class="mission-quote">"ANVEIL EVERY CHARM — To illuminate human potential through sacred numbers, without fatalism or fear."</div>
      <p class="mission-sub">
        For centuries, astrology and numerology were clouded by contradictory claims, generic horoscopes, and fear-based predictions. 
        Numeros Vision replaces guesswork with authentic classical wisdom and mathematical rigor, providing you with honest, grounded perspectives and practical clarity for self-mastery.
      </p>
    </div>'''

    new_box = '''    <!-- The Mission Statement -->
    <div class="mission-box">
      <div class="mission-quote">"ANVEIL EVERY CHARM — To illuminate human potential through traditional numbers, without fatalism or fear."</div>
      <p class="mission-sub">
        Our approach values transparency, responsible interpretation and respect for individual choice. Numerology is a traditional belief system, not a scientifically established way to predict a person's future.
        Numeros Vision replaces guesswork with verified calculation rules and clear explanations, providing honest perspectives and practical clarity for personal reflection.
      </p>
    </div>'''

    if old_box in content:
        content = content.replace(old_box, new_box, 1)
        print("Updated mission box!")
    else:
        # Fallback with regex
        import re
        content = re.sub(
            r'<!-- The Mission Statement -->\s*<div class="mission-box">[\s\S]*?</div>',
            new_box.strip(),
            content,
            1
        )
        print("Updated mission box via regex!")

    # 2. Update JSON-LD in about.html
    new_json_ld = '''  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "AboutPage",
        "@id": "https://numerosvision.com/about/#webpage",
        "url": "https://numerosvision.com/about/",
        "name": "About Numeros Vision | Our Methods & Principles",
        "description": "Discover Numeros Vision, our approach to numerology calculators, name analysis, Lo Shu Grid insights and personalised reports, with transparent methods and responsible interpretation.",
        "isPartOf": {
          "@id": "https://numerosvision.com/#website"
        },
        "about": {
          "@id": "https://numerosvision.com/#organization"
        },
        "breadcrumb": {
          "@id": "https://numerosvision.com/about/#breadcrumb"
        }
      },
      {
        "@type": "BreadcrumbList",
        "@id": "https://numerosvision.com/about/#breadcrumb",
        "itemListElement": [
          {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://numerosvision.com/"
          },
          {
            "@type": "ListItem",
            "position": 2,
            "name": "About Us",
            "item": "https://numerosvision.com/about/"
          }
        ]
      }
    ]
  }
  </script>'''

    import re
    content = re.sub(
        r'<!-- Schema\.org JSON-LD -->\s*<script type="application/ld\+json">[\s\S]*?</script>',
        new_json_ld.strip(),
        content,
        1
    )
    print("Updated JSON-LD schema with consistent /about/ URLs")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("app/static/about.html successfully finalized!")

if __name__ == '__main__':
    main()
