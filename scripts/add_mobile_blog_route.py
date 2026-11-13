with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '@app.get("/blog/mobile-numerology-malefic-pairs", include_in_schema=False)\ndef blog_mobile_malefics():'
replacement = '@app.get("/blog/mobile-numerology-malefic-pairs", include_in_schema=False)\n@app.get("/blog/mobile-numerology-malefic-pairs/", include_in_schema=False)\ndef blog_mobile_malefics():'

is_crlf = '\r\n' in content
content_lf = content.replace('\r\n', '\n')
if target in content_lf:
    content_lf = content_lf.replace(target, replacement, 1)
    if is_crlf:
        content_lf = content_lf.replace('\n', '\r\n')
    with open('app/main.py', 'w', encoding='utf-8') as f:
        f.write(content_lf)
    print('Added trailing slash route to app/main.py!')
else:
    print('Target not found or already updated')
