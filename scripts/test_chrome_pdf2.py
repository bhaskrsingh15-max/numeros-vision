import subprocess
import os

chrome_exe = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
html_path = os.path.abspath('app/static/sample.html')
pdf_out = os.path.abspath('test_chrome_render.pdf')

cmd = [
    chrome_exe,
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu',
    '--no-pdf-header-footer',
    f'--print-to-pdf={pdf_out}',
    f'http://127.0.0.1:8000/sample?name=Bhaskr+Singh&dob=1981-11-28&tier=basic'
]

print("Running command:", " ".join(cmd))
res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
print("Exit code:", res.returncode)
print("PDF exists:", os.path.exists(pdf_out))
if os.path.exists(pdf_out):
    print("PDF size:", os.path.getsize(pdf_out))
