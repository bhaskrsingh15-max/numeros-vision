import pypdf

reader = pypdf.PdfReader('app/static/reports/Numeros_Vision_Basic_Report_28-11-1981.pdf')
print('Number of pages in Basic report:', len(reader.pages))

for idx, page in enumerate(reader.pages):
    print(f'=== PAGE {idx+1} ===')
    txt = page.extract_text()
    for line in txt.split('\n'):
        print(line.encode('ascii', 'backslashreplace').decode('ascii'))
