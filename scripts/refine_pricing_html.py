import os
import re

PRICING_PATH = os.path.abspath("app/static/pricing.html")

def refine_pricing():
    content = open(PRICING_PATH, 'r', encoding='utf-8').read()

    # 1. Update Title and Meta Description if needed
    content = re.sub(
        r'<title>.*?</title>',
        '<title>Plans &amp; Auspicious Pricing Packages | Numeros Vision</title>',
        content,
        count=1
    )
    content = re.sub(
        r'<meta\s+name="description"\s+content=".*?"\s*/>',
        '<meta name="description" content="Transparent, unified pricing for personalised PDF numerology reports (Basic ₹199, Advanced ₹510, Premium ₹1,050), bundles, Charm AI passes, and 1-on-1 consultations." />',
        content,
        count=1
    )

    # 2. Update the static summary table in pricing.html:
    # Replace the table rows with the unified 4 product families
    table_target = '''            <tr style="border-bottom:1px solid rgba(180,155,110,0.2);">
              <td style="padding:14px 16px; font-weight:700; color:#2C2214;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="color:#C9A227;">✦</span> Charm AI Starter Pack
                </div>
              </td>
              <td style="padding:14px 16px; color:#523E28;">5 Question Predictions</td>
              <td style="padding:14px 16px; font-weight:800; color:#8B6914; font-size:1.15rem; font-weight:800;">₹95</td>
              <td style="padding:14px 16px; text-decoration:line-through; color:rgba(139,105,20,0.55);">₹199</td>
              <td style="padding:14px 16px; text-align:right;">
                <a href="/#charm-ai" class="btn-gold-action" style="padding:6px 16px; font-size:0.78rem; text-decoration:none; display:inline-block; border-radius:8px;">
                  Get 5 Questions (₹95)
                </a>
              </td>
            </tr>'''

    # Let's inspect where 11,400 or ₹95 is in the file and replace with unified prices
    content = content.replace('₹11,400', '₹1,050')
    content = content.replace('₹24,000', '₹1,499')
    content = content.replace('₹95', '₹199')
    content = content.replace('₹5,100', '₹1,050')
    content = content.replace('₹5,999', '₹1,050')
    content = content.replace('₹5,500', '₹1,050')
    content = content.replace('₹4,800', '₹1,050')
    content = content.replace('₹14,000', '₹1,999')
    content = content.replace('₹10,500', '₹1,999')
    content = content.replace('₹10,900', '₹1,999')
    content = content.replace('₹12,000', '₹1,999')
    content = content.replace('₹105', '₹199')
    content = content.replace('₹120', '₹199')
    content = content.replace('₹149', '₹199')
    content = content.replace('₹330', '₹399')
    content = content.replace('₹370', '₹399')
    content = content.replace('₹390', '₹399')
    content = content.replace('₹410', '₹399')
    content = content.replace('₹550', '₹510')
    content = content.replace('₹570', '₹510')
    content = content.replace('₹599', '₹510')
    content = content.replace('₹1,450', '₹999')
    content = content.replace('₹1,500', '₹999')

    # Update JS pricing data object in pricing.html so all domains use 199, 510, 1050
    # Search for DOMAIN_DATA
    # In JS: tripwire price: '₹199', master price: '₹510', sovereign price: '₹1,050'
    content = re.sub(r"tripwire:\s*\{\s*name:\s*([^,]+),\s*price:\s*'₹[^']+',\s*strike:\s*'₹[^']+'", r"tripwire: { name: \1, price: '₹199', strike: '₹399'", content)
    content = re.sub(r"master:\s*\{\s*name:\s*([^,]+),\s*price:\s*'₹[^']+',\s*strike:\s*'₹[^']+'", r"master: { name: \1, price: '₹510', strike: '₹999'", content)
    content = re.sub(r"sovereign:\s*\{\s*name:\s*([^,]+),\s*price:\s*'₹[^']+',\s*strike:\s*'₹[^']+'", r"sovereign: { name: \1, price: '₹1,050', strike: '₹1,999'", content)

    with open(PRICING_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully refined app/static/pricing.html to unified pricing architecture!")

if __name__ == '__main__':
    refine_pricing()
