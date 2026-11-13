import os
import sys

# Ensure current working directory is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

def test_routes():
    sys.stdout.reconfigure(encoding='utf-8')
    client = TestClient(app, follow_redirects=False)

    routes_to_test = [
        "/",
        "/about",
        "/about/",
        "/about-us",
        "/about-us/",
        "/contact",
        "/contact/",
        "/privacy",
        "/privacy/",
        "/privacy-policy",
        "/privacy-policy/",
        "/terms",
        "/terms/",
        "/terms-of-service",
        "/terms-of-service/",
        "/disclaimer",
        "/disclaimer/",
        "/pricing",
        "/pricing/",
        "/refund",
        "/refund/",
        "/shipping",
        "/shipping/",
        "/grievance",
        "/grievance/",
        "/tools/life-path-calculator",
        "/tools/life-path-calculator/",
        "/blog/what-is-numerology",
        "/blog/what-is-numerology/",
        "/blog/chaldean-compound-numbers-meanings",
        "/blog/chaldean-compound-numbers-meanings/",
    ]

    for r in routes_to_test:
        resp = client.get(r)
        print(f"{r:45} -> Status: {resp.status_code}")

if __name__ == '__main__':
    test_routes()
