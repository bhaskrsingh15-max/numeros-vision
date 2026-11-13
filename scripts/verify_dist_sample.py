with open('dist_cloudflare_pages/sample.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
fmt3_pages = re.findall(r'id=\"page-(\d+)\"', text)
print(f"Total page IDs found in dist sample.html: {len(fmt3_pages)}")

chap_matches = re.findall(r'Chapter\s+\d+', text)
print(f"Chapter occurrences in dist sample.html: {len(chap_matches)}")

sec_matches = re.findall(r'Section\s+\d+', text)
print(f"Section occurrences in dist sample.html: {len(sec_matches)}")

print("dist_cloudflare_pages/sample.html verification complete!")
