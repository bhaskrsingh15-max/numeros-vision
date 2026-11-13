import zipfile

with zipfile.ZipFile('cloudflare_pages_upload.zip', 'r') as zf:
    names = zf.namelist()
    print(f"Total files in zip: {len(names)}")
    report_files = [n for n in names if 'report' in n.lower()]
    print(f"Report files in zip: {report_files}")
    worker_files = [n for n in names if '_worker' in n.lower()]
    print(f"Worker files in zip: {worker_files}")
