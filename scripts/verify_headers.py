import glob
import re

def verify():
    files = glob.glob('app/static/**/*.html', recursive=True)
    anomalies = []
    
    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
            
        m = re.search(r'<ul[^>]*id=["\']nvNavMenu["\'][\s\S]*?</ul>', content)
        if not m:
            anomalies.append((f, "No nvNavMenu found"))
            continue
            
        nav_text = m.group(0)
        # Check if About appears after Contact Us
        contact_pos = nav_text.find('/contact/')
        about_last_pos = nav_text.rfind('/about/')
        if contact_pos != -1 and about_last_pos > contact_pos:
            anomalies.append((f, "About appears after Contact Us!"))

        # Check if About Us is at the top
        about_first_pos = nav_text.find('/about/')
        calc_pos = nav_text.find('Calculators')
        if about_first_pos == -1:
            anomalies.append((f, "No About Us in nav!"))
        elif calc_pos != -1 and about_first_pos > calc_pos:
            anomalies.append((f, "About Us is NOT before Calculators!"))

    print(f"Verified {len(files)} files. Anomalies count: {len(anomalies)}")
    for a in anomalies:
        print("  ->", a)

if __name__ == '__main__':
    verify()
