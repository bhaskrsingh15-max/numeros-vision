import fitz

doc = fitz.open('data/reference_books/Chaldean Numerology PDF Numbers Pythagoras.pdf')

for p_num in range(12, 25):
    t = doc[p_num].get_text()
    first_few = [l.strip() for l in t.splitlines() if l.strip()][:5]
    printed = [l.strip() for l in t.splitlines() if 'Page ' in l]
    print(f'PDF {p_num+1} [Printed {printed[:1]}]:')
    print('   ', ' // '.join(first_few))
