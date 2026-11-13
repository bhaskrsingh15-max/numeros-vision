import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    path = 'app/static/about.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update JSON-LD structured data
    old_json_ld = '''  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "AboutPage",
        "name": "About Numeros Vision",
        "url": "https://numerosvision.com/about",
        "description": "The mission, methodology, and ethical standards of Numeros Vision Technologies.",
        "publisher": {
          "@type": "Organization",
          "name": "Numeros Vision",
          "logo": { "@type": "ImageObject", "url": "https://numerosvision.com/static/icons/icon-512.png" }
        }
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://numerosvision.com" },
          { "@type": "ListItem", "position": 2, "name": "About Us", "item": "https://numerosvision.com/about" }
        ]
      }
    ]
  }
  </script>'''

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

    assert old_json_ld in content, "old_json_ld missing"
    content = content.replace(old_json_ld, new_json_ld, 1)

    # 2. Update Mission Box
    old_mission_box = '''    <!-- The Mission Statement -->
    <div class="mission-box">
      <div class="mission-quote">"ANVEIL EVERY CHARM — To illuminate human potential through sacred numbers, without fatalism or fear."</div>
      <p class="mission-sub">
        For centuries, astrology and numerology were clouded by contradictory claims, generic horoscopes, and fear-based predictions.
        Numeros Vision replaces guesswork with authentic classical wisdom and mathematical rigor, providing you with honest, grounded perspectives and practical clarity for self-mastery.
      </p>
    </div>'''

    new_mission_box = '''    <!-- The Mission Statement -->
    <div class="mission-box">
      <div class="mission-quote">"ANVEIL EVERY CHARM — To illuminate human potential through traditional numbers, without fatalism or fear."</div>
      <p class="mission-sub">
        Our approach values transparency, responsible interpretation and respect for individual choice. Numerology is a traditional belief system, not a scientifically established way to predict a person's future.
        Numeros Vision replaces guesswork with verified calculation rules and clear explanations, providing honest perspectives and practical clarity for personal reflection.
      </p>
    </div>'''

    assert old_mission_box in content, "old_mission_box missing"
    content = content.replace(old_mission_box, new_mission_box, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully updated JSON-LD and Mission box in about.html!")

if __name__ == '__main__':
    main()
