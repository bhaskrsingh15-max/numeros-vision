import os

with open('app/static/sample.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Read the fmt1_code from the previous file or define directly
start_marker = "function generateFormat1Pages(client) {"
end_marker = "function generateFormat2Pages(client) {"

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

print(f"start_idx: {start_idx}, end_idx: {end_idx}")

# Read fmt1_code
with open('scripts/build_luxury_sample_formats.py', 'r', encoding='utf-8') as f:
    script_text = f.read()

# Extract fmt1_code
s_pos = script_text.find("fmt1_code = '''") + len("fmt1_code = '''")
e_pos = script_text.find("'''\n\n# Replace", s_pos)
fmt1_code = script_text[s_pos:e_pos].strip()

# Replace using string slice
new_html = html[:start_idx] + fmt1_code + "\n\n    " + html[end_idx:]

with open('app/static/sample.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Successfully replaced generateFormat1Pages via string slicing!")
