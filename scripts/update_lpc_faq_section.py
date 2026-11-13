import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    path = 'app/static/tools/life-path-calculator.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    idx_start = content.find('  <!-- ───── FAQ SECTION ───── -->')
    idx_end = content.find('  <!-- ───── RELATED TOOLS STRIP ───── -->')

    assert idx_start != -1, "FAQ start missing"
    assert idx_end != -1, "Related tools start missing"

    new_faq_section = '''  <!-- ───── FAQ SECTION ───── -->
  <div class="faq-section">
    <h2 class="faq-title">Frequently Asked Questions</h2>

    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">What is a Life Path Number? <span>+</span></div>
      <div class="faq-a">A Life Path Number is a numerology number calculated from a person's date of birth using a specified method.</div>
    </div>

    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">How is my Life Path Number calculated? <span>+</span></div>
      <div class="faq-a">The calculator applies its stated method to your birth date and shows the calculation steps.</div>
    </div>

    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">Do Life Path Numbers have scientifically proven meanings? <span>+</span></div>
      <div class="faq-a">Numerology is a traditional interpretive practice. Its personality descriptions and predictions are not scientifically established facts.</div>
    </div>

    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">Does the calculation method affect my result? <span>+</span></div>
      <div class="faq-a">It can. Different systems may use different reduction rules, so check which method the calculator follows.</div>
    </div>

    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">What does a detailed Life Path report include? <span>+</span></div>
      <div class="faq-a">The contents depend on the report you select. Review the listed features before purchasing.</div>
    </div>

    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">What are Master Numbers (11, 22, 33)? <span>+</span></div>
      <div class="faq-a">Master numbers are double digits (11, 22, 33) that carry amplified traditional symbolic significance and are preserved without immediate reduction in many traditions.</div>
    </div>

    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">Is this Life Path calculator free? <span>+</span></div>
      <div class="faq-a">Yes. Calculating your number, viewing your calculation steps, and reading the initial interpretation are completely free. Extended multi-page reports are optional purchases.</div>
    </div>
  </div>

'''

    content = content[:idx_start] + new_faq_section + content[idx_end:]

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Updated visible FAQ section cleanly!")

if __name__ == '__main__':
    main()
