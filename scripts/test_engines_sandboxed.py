import sys
import json
import traceback

sys.stdout.reconfigure(encoding='utf-8')

print('=== 1. TESTING PLANETARY PACKAGE REPORTS ===')
try:
    from app.engine.planetary_package_reports import generate_planetary_package_report
    rep = generate_planetary_package_report(
        package_slug='report_authority_master',
        day=18, month=10, year=1990,
        full_name='Alexander Vance'
    )
    print('Planetary Package Report Success! Keys:', list(rep.keys())[:8])
    if 'error' in rep:
        print('Error in report:', rep['error'])
except Exception as e:
    print('Planetary Package Report Exception:', e)
    traceback.print_exc()

print('\n=== 2. TESTING PACKAGE REPORT GENERATOR ===')
try:
    from app.engine.package_report_generator import generate_package_report
    rep2 = generate_package_report(
        package_id='report_master',
        day=18, month=10, year=1990,
        name='Alexander Vance'
    )
    print('Package Report Generator Success! Keys:', list(rep2.keys())[:8])
    if 'error' in rep2:
        print('Error in report 2:', rep2['error'])
except Exception as e:
    print('Package Report Generator Exception:', e)
    traceback.print_exc()

print('\n=== 3. TESTING PDF GENERATOR ===')
try:
    from app.services.pdf_report_generator import generate_celestial_master_pdf
    pdf_bytes = generate_celestial_master_pdf(
        name='Alexander Vance',
        day=18, month=10, year=1990,
        tier='MASTER'
    )
    print(f'PDF Generator Success! Generated {len(pdf_bytes)} bytes.')
except Exception as e:
    print('PDF Generator Exception:', e)
    traceback.print_exc()

print('\n=== 4. TESTING READINGS ENGINE ===')
try:
    from app.engine.lo_shu import analyze_lo_shu_grid
    loshu = analyze_lo_shu_grid(18, 10, 1990)
    print('Lo Shu Grid Success! Missing:', loshu['missing_numbers'], 'Planes:', loshu['completed_planes'])
except Exception as e:
    print('Lo Shu Grid Exception:', e)
    traceback.print_exc()
