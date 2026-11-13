with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = "import re\n" + text

with open('app/services/pdf_report_generator.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Added import re")
