import sys

def verify():
    sys.stdout.reconfigure(encoding='utf-8')
    path = 'app/static/tools/life-path-calculator.html'
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    checks = [
        ("<title>Life Path Number Calculator & Meaning | Numeros Vision</title>", "Title"),
        ('name="description" content="Discover your Life Path Number using your date of birth. Explore its traditional numerology meaning and see step-by-step arithmetic without pseudoscientific claims."', "Meta description"),
        ('<h1 class="tool-title">Life Path Number Calculator</h1>', "H1"),
        ('Discover your Life Path Number using your date of birth.', "Lead copy"),
        ('Calculate My Life Path Number', "Button text"),
        ('How Is Your Life Path Number Calculated?', "Heading 1"),
        ('Example: 15 June 1990', "Worked example"),
        ('This example uses component reduction.', "Component reduction note"),
        ('What Does Your Life Path Number Mean?', "Heading 2"),
        ('In numerology, each number is associated with traditional symbolic meanings.', "Meaning copy"),
        ('Explore Your Detailed Life Path Report', "Heading 3"),
        ('Basic Report', "Basic report tier"),
        ('Advanced Report', "Advanced report tier"),
        ('Premium Report', "Premium report tier"),
        ('What is a Life Path Number?', "FAQ 1"),
        ('How is my Life Path Number calculated?', "FAQ 2"),
        ('Do Life Path Numbers have scientifically proven meanings?', "FAQ 3"),
        ('Does the calculation method affect my result?', "FAQ 4"),
        ('What does a detailed Life Path report include?', "FAQ 5"),
        ('res-calc-steps', "JS calculation steps container"),
        ('Classical Component Reduction', "Calculation steps method header"),
    ]

    all_passed = True
    for needle, label in checks:
        found = needle in text
        if not found:
            all_passed = False
        print(f"[{'PASS' if found else 'FAIL'}] {label}: {found}")

    print(f"\nLife Path Calculator verification: {'ALL PASSED' if all_passed else 'SOME FAILED'}")

if __name__ == '__main__':
    verify()
