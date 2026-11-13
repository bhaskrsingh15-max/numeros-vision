import sys
import json
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'http://127.0.0.1:8000'

def test_endpoint(name, url, method='GET', data=None):
    print(f'Testing: {name} ({method} {url})...')
    try:
        req_data = json.dumps(data).encode('utf-8') if data else None
        headers = {'Content-Type': 'application/json'} if data else {}
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        with urllib.request.urlopen(req, timeout=10) as resp:
            code = resp.status
            body = resp.read()
            print(f' -> SUCCESS (HTTP {code}, {len(body)} bytes)')
            if 'json' in resp.headers.get('content-type', ''):
                j = json.loads(body.decode('utf-8'))
                print(' -> Sample JSON keys:', list(j.keys())[:8])
            return True, body
    except urllib.error.HTTPError as e:
        print(f' -> HTTP ERROR: {e.code} - {e.reason}')
        try:
            err_body = e.read().decode('utf-8')
            print('    Details:', err_body[:300])
        except Exception:
            pass
        return False, None
    except Exception as e:
        print(f' -> EXCEPTION: {e}')
        return False, None

print('=== 1. TESTING FREE READING & CALCULATOR ===')
test_endpoint('Free Reading', f'{BASE_URL}/api/v1/readings/free', 'POST', {'day': 18, 'month': 10, 'year': 1990})

print('\n=== 2. TESTING REPORTS CATALOG ===')
test_endpoint('Reports Catalog', f'{BASE_URL}/api/v1/reports/catalog', 'GET')

print('\n=== 3. TESTING PACKAGE REPORT (READINGS) ===')
test_endpoint('Package Report Career', f'{BASE_URL}/api/v1/readings/package-report', 'POST', {
    'package_slug': 'report_authority_master',
    'day': 18, 'month': 10, 'year': 1990,
    'full_name': 'Alexander Vance'
})

print('\n=== 4. TESTING REPORTS CALCULATE ===')
test_endpoint('Reports Delivery Calculate', f'{BASE_URL}/api/v1/reports/calculate', 'POST', {
    'day': 18, 'month': 10, 'year': 1990,
    'name': 'Alexander Vance'
})

print('\n=== 5. TESTING SAMPLE PAGES ===')
test_endpoint('Sample Page 1', f'{BASE_URL}/sample', 'GET')
test_endpoint('Sample Page 2', f'{BASE_URL}/sample2', 'GET')
test_endpoint('Pricing Page', f'{BASE_URL}/pricing', 'GET')
test_endpoint('Reports Catalogue Page', f'{BASE_URL}/reports_catalogue', 'GET')
