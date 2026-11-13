with open('app/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '@app.get("/blog/chaldean-vs-pythagorean-numerology", include_in_schema=False)\ndef blog_chaldean_vs_pythagorean():'
replacement = '@app.get("/blog/chaldean-vs-pythagorean-numerology", include_in_schema=False)\n@app.get("/blog/chaldean-vs-pythagorean-numerology/", include_in_schema=False)\ndef blog_chaldean_vs_pythagorean():'

is_crlf = '\r\n' in content
content_lf = content.replace('\r\n', '\n')
if target in content_lf:
    content_lf = content_lf.replace(target, replacement, 1)
    if is_crlf:
        content_lf = content_lf.replace('\n', '\r\n')
    with open('app/main.py', 'w', encoding='utf-8') as f:
        f.write(content_lf)
    print('Updated app/main.py with trailing slash route successfully!')
else:
    print('Target not found')
