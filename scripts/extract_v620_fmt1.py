import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('backups/v6.20.0/app/static/sample.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find('function generateFormat1Pages')
pos2 = text.find('function generateFormat2Pages')
print(f"Total length of generateFormat1Pages in v6.20.0: {pos2 - pos1}")

with open('scripts/v620_generateFormat1Pages.js', 'w', encoding='utf-8') as f_out:
    f_out.write(text[pos1:pos2])

print("Written to scripts/v620_generateFormat1Pages.js successfully.")
