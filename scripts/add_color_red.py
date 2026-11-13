with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = 'COLOR_CARD_BG    = colors.HexColor("#FFFFFF")'
replacement = 'COLOR_CARD_BG    = colors.HexColor("#FFFFFF")\nCOLOR_RED_ALERT  = colors.HexColor("#A13030")'

text = text.replace(target, replacement)

with open('app/services/pdf_report_generator.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("COLOR_RED_ALERT added to palette successfully.")
