import sys

def verify():
    sys.stdout.reconfigure(encoding='utf-8')
    with open('app/static/index.html', 'r', encoding='utf-8') as f:
        text = f.read()

    checks = [
        ("<title>Numerology Calculators & Reports | Numeros Vision</title>", "Title"),
        ('name="description" content="Explore free numerology calculators for birth dates, names and the Lo Shu Grid. Understand your results and explore detailed numerology reports."', "Meta description"),
        ('<h1 class="hero-h1">Discover What Your Numbers Mean</h1>', "H1"),
        ('Calculate My Numbers Free', "Hero primary CTA"),
        ('Explore Numerology Reports', "Hero secondary CTA"),
        ('Start with Your Numbers', "Calculator title"),
        ('id="f-name" placeholder="Full name (optional)"', "Optional name input"),
        ('How Numeros Vision Works', "How it works"),
        ('Calculate. Understand. Explore.', "How it works sub"),
        ('Explore Your Numbers with Charm AI', "Charm AI heading"),
        ('Basic Numerology Report', "Basic Report card"),
        ('Advanced Numerology Report', "Advanced Report card"),
        ('Premium Numerology Report', "Premium Report card"),
        ('Begin with a Free Calculation', "Closing CTA heading"),
        ('Payment gateway connection error', "Checkout error fix"),
        ('test mode', "Test mode string check (should be gone or minimized)")
    ]

    for needle, label in checks:
        found = needle in text
        print(f"[{'PASS' if found else 'FAIL'}] {label}: {found}")

    # Check if 'test mode' is still anywhere in index.html
    count_test_mode = text.count('test mode')
    print(f"Occurrences of 'test mode': {count_test_mode}")

if __name__ == '__main__':
    verify()
