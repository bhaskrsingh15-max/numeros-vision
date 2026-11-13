with open('app/static/year_2027.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="sample-preview"')
print(text[idx-20:idx+1500])
