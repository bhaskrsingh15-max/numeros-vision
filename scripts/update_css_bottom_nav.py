with open('app/static/css/roadmap_components.css', 'r', encoding='utf-8') as f:
    text = f.read()

target = '  .nv-bottom-nav-item {\n    display: flex;'
replacement = '  .nv-bottom-nav-item,\n  .nv-bottom-item {\n    display: flex !important;'

if target in text:
    text = text.replace(target, replacement)
    print("Added .nv-bottom-item alias to .nv-bottom-nav-item rule")

target2 = '  .nv-bottom-nav-item * {\n    pointer-events: none !important;\n  }'
replacement2 = '''  .nv-bottom-nav-item *,
  .nv-bottom-item * {
    pointer-events: none !important;
  }

  .nv-bottom-icon {
    font-size: 1.15rem;
    line-height: 1;
    margin-bottom: 2px;
  }

  .nv-bottom-label {
    font-size: 0.68rem;
    font-weight: 500;
  }'''

if target2 in text:
    text = text.replace(target2, replacement2)
    print("Added .nv-bottom-icon and .nv-bottom-label support")

target3 = '  .nv-bottom-nav-item.active {\n    color: var(--gold-dark, #8B6914);\n    font-weight: 700;\n  }'
replacement3 = '  .nv-bottom-nav-item.active,\n  .nv-bottom-item.active {\n    color: var(--gold-dark, #8B6914);\n    font-weight: 700;\n  }'

if target3 in text:
    text = text.replace(target3, replacement3)
    print("Added active state support for .nv-bottom-item")

with open('app/static/css/roadmap_components.css', 'w', encoding='utf-8') as f:
    f.write(text)

print("Finished updating roadmap_components.css")
