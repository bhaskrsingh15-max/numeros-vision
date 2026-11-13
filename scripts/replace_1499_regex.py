# replace_1499_regex.py
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

count = 0
for root, dirs, files in os.walk('app/static'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                c = f.read()

            if '1,499' in c:
                # Replace any Consultation (₹1,499) or variations with (₹1,050)
                new_c = re.sub(r'₹1,499', '₹1,050', c)
                new_c = re.sub(r'1,499', '1,050', new_c)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_c)
                count += 1
                print(f"Updated {filepath}")

print(f"Total files updated: {count}")
