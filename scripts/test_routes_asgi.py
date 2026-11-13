import os
import sys
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app

async def test_scope(path):
    scope = {
        "type": "http",
        "method": "GET",
        "path": path,
        "raw_path": path.encode("ascii"),
        "query_string": b"",
        "headers": [
            (b"host", b"localhost:8000"),
            (b"accept", b"text/html"),
            (b"user-agent", b"Mozilla/5.0"),
        ],
        "client": ("127.0.0.1", 50000),
        "server": ("127.0.0.1", 8000),
    }
    status = None
    headers = []
    body_chunks = []

    async def receive():
        return {"type": "http.request", "body": b"", "more_body": False}

    async def send(message):
        nonlocal status, headers, body_chunks
        if message["type"] == "http.response.start":
            status = message["status"]
            headers = message.get("headers", [])
        elif message["type"] == "http.response.body":
            body_chunks.append(message.get("body", b""))

    await app(scope, receive, send)
    return status, b"".join(body_chunks)

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    routes = [
        "/about",
        "/about/",
        "/about-us",
        "/about-us/",
        "/about.html",
        "/contact",
        "/contact/",
        "/privacy",
        "/privacy/",
        "/terms",
        "/terms/",
        "/disclaimer",
        "/disclaimer/",
        "/pricing",
        "/pricing/",
        "/refund",
        "/refund/",
        "/faq",
        "/faq/",
        "/cookie-policy",
        "/cookie-policy/",
        "/methodology",
        "/methodology/",
        "/tools/life-path-calculator",
        "/tools/life-path-calculator/",
        "/tools/lo-shu-grid",
        "/tools/lo-shu-grid/",
        "/blog/what-is-numerology",
        "/blog/what-is-numerology/",
        "/blog/chaldean-compound-numbers-meanings",
        "/blog/chaldean-compound-numbers-meanings/",
    ]

    all_passed = True
    for r in routes:
        status, body = asyncio.run(test_scope(r))
        is_ok = status == 200
        if not is_ok:
            all_passed = False
        print(f"[{'PASS' if is_ok else 'FAIL'}] {r:45} -> HTTP {status} (len={len(body)})")

    print(f"\nOverall result: {'ALL PASSED' if all_passed else 'SOME FAILED'}")

if __name__ == '__main__':
    main()
