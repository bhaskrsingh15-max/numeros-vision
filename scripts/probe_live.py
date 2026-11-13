import urllib.request
import sys

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    req = urllib.request.Request('http://127.0.0.1:8000/', headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            code = resp.getcode()
            body = resp.read().decode('utf-8')
            print('HTTP Status:', code)
            print('Length:', len(body))
            print('Has Title:', '<title>Numerology Calculators & Reports | Numeros Vision</title>' in body)
            print('Has H1:', '<h1 class="hero-h1">Discover What Your Numbers Mean</h1>' in body)
            print('Has Hero CTA 1:', 'Calculate My Numbers Free' in body)
            print('Has Hero CTA 2:', 'Explore Numerology Reports' in body)
            print('Has Optional Name:', 'Full name (optional)' in body)
            print('Has Basic Report:', 'Basic Numerology Report' in body)
            print('Has Advanced Report:', 'Advanced Numerology Report' in body)
            print('Has Premium Report:', 'Premium Numerology Report' in body)
            print('Has Closing CTA:', 'Begin with a Free Calculation' in body)
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    main()
