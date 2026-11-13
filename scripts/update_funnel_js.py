with open('app/static/js/funnel_journey.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('price_inr: 249,', 'price_inr: 199,')
text = text.replace('original_price_inr: 499,', 'original_price_inr: 399,')

with open('app/static/js/funnel_journey.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated funnel_journey.js successfully!")
