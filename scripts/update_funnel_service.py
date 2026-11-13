with open('app/engine/funnel_service.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"price_inr": 249,', '"price_inr": 199,')
text = text.replace('"original_price_inr": 499,', '"original_price_inr": 399,')

with open('app/engine/funnel_service.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated funnel_service.py successfully!")
