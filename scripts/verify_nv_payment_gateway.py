with open('app/static/js/nv_payment_gateway.js', 'r', encoding='utf-8') as f:
    text = f.read()

print('Contains pay_LIVE_:', 'pay_LIVE_' in text)
print('Contains confirm(:', 'confirm(' in text)
print('Contains NV-REC-:', 'NV-REC-' in text)
print('Contains rzp_test_Tw4QuPjP46Q6dh:', 'rzp_test_Tw4QuPjP46Q6dh' in text)
