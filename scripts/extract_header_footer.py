with open('app/static/pricing.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('<header class="nv-header">')
idx2 = text.find('</header>') + len('</header>')
header_html = text[idx1:idx2]

idx3 = text.find('<footer class="nv-footer">')
idx4 = text.find('</footer>') + len('</footer>')
footer_html = text[idx3:idx4]

with open('scripts/extracted_header.html', 'w', encoding='utf-8') as f:
    f.write(header_html)
with open('scripts/extracted_footer.html', 'w', encoding='utf-8') as f:
    f.write(footer_html)

print('Header extracted, length:', len(header_html))
print('Footer extracted, length:', len(footer_html))
