import os

for tier, filename in [
    ('Basic (3 Pages - Rs 199)', 'Numeros_Vision_Basic_Report_28-11-1981.pdf'),
    ('Advanced (12 Pages - Rs 510)', 'Numeros_Vision_Advanced_Report_28-11-1981.pdf'),
    ('Premium (32 Pages - Rs 1050)', 'Numeros_Vision_Premium_Report_28-11-1981.pdf')
]:
    p1 = os.path.join('app', 'static', 'reports', filename)
    p2 = os.path.join('dist_cloudflare_pages', 'reports', filename)
    print(f"{tier}:")
    print(f"  app/static/reports: exists={os.path.exists(p1)}, size={os.path.getsize(p1) if os.path.exists(p1) else 0}")
    print(f"  dist_cloudflare_pages/reports: exists={os.path.exists(p2)}, size={os.path.getsize(p2) if os.path.exists(p2) else 0}")
    if os.path.exists(p1):
        with open(p1, 'rb') as f:
            header = f.read(8)
            print(f"  header={header}")
