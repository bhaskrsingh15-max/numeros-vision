# -*- coding: utf-8 -*-
path = "app/static/index.html"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
    ".nv-next-insight-section {\n      margin: 0 auto 48px;\n      max-width: 860px;",
    ".nv-next-insight-section {\n      margin: 0 auto 48px;\n      max-width: 1060px;"
)
text = text.replace(
    ".nv-next-insight-section {\r\n      margin: 0 auto 48px;\r\n      max-width: 860px;",
    ".nv-next-insight-section {\r\n      margin: 0 auto 48px;\r\n      max-width: 1060px;"
)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated nv-next-insight-section.")
