# clean_all_legacy_consultation_prices.py
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

updated_files = 0

for root, dirs, files in os.walk('app/static'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            new_content = content
            # 1. 1-on-1 Consultation price
            new_content = new_content.replace('1-on-1 Consultation (₹1,499)', '1-on-1 Consultation (₹1,050)')
            new_content = new_content.replace('1-on-1 Consultation Call (₹1,499)', '1-on-1 Consultation Call (₹1,050)')
            new_content = new_content.replace('1-on-1 Consultation Call</span>\n              <span>₹1,499</span>', '1-on-1 Consultation Call</span>\n              <span>₹1,050</span>')
            new_content = new_content.replace('Book 1-on-1 Name Balancing Consultation (₹1,499)', 'Book 1-on-1 Name Balancing Consultation (₹1,050)')
            new_content = new_content.replace('package of ₹1,499', 'package of ₹1,050')
            new_content = new_content.replace('"priceRange": "₹199 - ₹1,499"', '"priceRange": "₹199 - ₹1,050"')
            new_content = new_content.replace('<span>₹1,499</span>', '<span>₹1,050</span>')

            # 2. View Reports from ₹510 -> from ₹199 (since Basic is ₹199)
            new_content = new_content.replace('View Reports &amp; Pricing (from ₹510)', 'View Reports &amp; Pricing (from ₹199)')
            new_content = new_content.replace('View Reports & Pricing (from ₹510)', 'View Reports & Pricing (from ₹199)')

            # 3. Logo intelligence strike
            new_content = new_content.replace('<span style="font-size:1.05rem; text-decoration:line-through; color:var(--text-muted, #7A654D);">₹1,499</span>\n        ', '')

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_files += 1
                print(f"Updated: {filepath}")

print(f"\nTotal files updated: {updated_files}")
