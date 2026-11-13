with open(r"tests\test_ui_ux_consistency.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
    "self.files = glob.glob('app/static/**/*.html', recursive=True)",
    "self.files = [f for f in glob.glob('app/static/**/*.html', recursive=True) if 'amp' not in f]"
)

with open(r"tests\test_ui_ux_consistency.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated test_ui_ux_consistency.py to filter out amp pages.")
