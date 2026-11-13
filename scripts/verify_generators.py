import sys
sys.stdout.reconfigure(encoding='utf-8')

from app.engine.package_report_generator import generate_package_report
from app.services.pdf_report_generator import generate_customised_pdf_report

print('Testing generate_package_report for basic tier...')
res = generate_package_report(
    name='Alexander Vance',
    day=18, month=10, year=1990,
    package_tier='free'
)
print('Free report generated successfully! Keys:', list(res.keys()))

print('\nTesting generate_package_report for master tier...')
res_master = generate_package_report(
    name='Alexander Vance',
    day=18, month=10, year=1990,
    package_tier='complete_report'
)
print('Complete report generated successfully! Keys:', list(res_master.keys()))

print('\nTesting generate_customised_pdf_report for basic (3 pages)...')
pdf_bytes, audit = generate_customised_pdf_report(
    name='Alexander Vance',
    day=18, month=10, year=1990,
    tier='basic'
)
v_status = audit.get("validation_status")
print(f'Basic PDF successfully generated! Bytes: {len(pdf_bytes):,}, Audit: {v_status}')

print('\nTesting generate_customised_pdf_report for advanced (12 pages)...')
pdf_bytes_adv, audit_adv = generate_customised_pdf_report(
    name='Alexander Vance',
    day=18, month=10, year=1990,
    tier='advanced'
)
p_count = audit_adv.get("page_count")
print(f'Advanced PDF successfully generated! Bytes: {len(pdf_bytes_adv):,}, Pages: {p_count}')
