import shutil

targets = [
    'dist_cloudflare_pages/sample.html',
    'dist_cloudflare_pages/sample/index.html',
    'dist_cloudflare_pages/sample-report/index.html',
    'dist_cloudflare_pages/sample_report/index.html'
]

for t in targets:
    shutil.copyfile('app/static/sample.html', t)
    print(f"Copied sample.html to {t}")
