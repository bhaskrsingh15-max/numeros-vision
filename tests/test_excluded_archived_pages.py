"""
Verification Suite: Item 5 — Archive & Exclude demo.html, sample2.html, and logo-preview.html
==============================================================================================
Proves:
1. All three pages are preserved in archive/excluded_pages/.
2. None of demo.html, sample2.html, logo-preview.html or their directory routes exist in
   app/static/ or dist_cloudflare_pages/.
3. FastAPI (app.main:app) returns HTTP 404 on /demo*, /sample2*, /logo-preview*.
4. Cloudflare Worker (app/static/_worker.js) returns HTTP 404 on /demo*, /sample2*, /logo-preview*
   in both production and preview environments.
"""

import os
import subprocess
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

from app.main import app


REPO_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_DIR = REPO_ROOT / "archive" / "excluded_pages"
STATIC_DIR = REPO_ROOT / "app" / "static"
DIST_DIR = REPO_ROOT / "dist_cloudflare_pages"

EXCLUDED_FILES = ("demo.html", "sample2.html", "logo-preview.html")
EXCLUDED_ROUTES = (
    "/demo",
    "/demo/",
    "/demo.html",
    "/sample2",
    "/sample2/",
    "/sample2.html",
    "/logo-preview",
    "/logo-preview/",
    "/logo-preview.html",
)


class TestExcludedArchivedPages(unittest.TestCase):
    def test_01_archived_in_source_and_absent_from_static_and_dist(self):
        for fname in EXCLUDED_FILES:
            archived_path = ARCHIVE_DIR / fname
            self.assertTrue(archived_path.is_file(), f"Archived source missing: {archived_path}")
            self.assertGreater(archived_path.stat().st_size, 1000)
            self.assertFalse((STATIC_DIR / fname).exists(), f"{fname} must not remain in app/static")
            self.assertFalse((DIST_DIR / fname).exists(), f"{fname} must not exist in dist_cloudflare_pages")
            self.assertFalse((DIST_DIR / "static" / fname).exists(), f"{fname} must not exist in dist_cloudflare_pages/static")

        for slug in ("demo", "sample2", "sample-2", "logo-preview"):
            self.assertFalse((DIST_DIR / slug).exists(), f"Route dir {slug}/ must not exist in dist_cloudflare_pages")

    def test_02_fastapi_returns_404_on_all_excluded_routes(self):
        client = TestClient(app)
        for route in EXCLUDED_ROUTES:
            resp = client.get(route, follow_redirects=False)
            self.assertEqual(resp.status_code, 404, f"FastAPI route {route} returned {resp.status_code} instead of 404")

    def test_03_worker_returns_404_in_production_and_preview(self):
        node_check = """
import assert from 'node:assert/strict';
import worker from './app/static/_worker.js';

const routes = [
  '/demo', '/demo/', '/demo.html',
  '/sample2', '/sample2/', '/sample2.html',
  '/logo-preview', '/logo-preview/', '/logo-preview.html'
];

for (const envName of ['production', 'preview']) {
  const host = envName === 'production' ? 'https://numerosvision.com' : 'https://preview.numeros-vision.pages.dev';
  const env = {
    ENVIRONMENT: envName,
    ASSETS: { fetch: async () => new Response('SHOULD_NEVER_REACH_ASSETS', { status: 200 }) }
  };
  for (const r of routes) {
    const res = await worker.fetch(new Request(host + r), env, { waitUntil: () => {} });
    assert.equal(res.status, 404, `${envName} ${r} returned ${res.status}`);
  }
}
"""
        proc = subprocess.run(
            ["node", "--input-type=module", "-e", node_check],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, f"Worker 404 check failed:\n{proc.stderr}\n{proc.stdout}")


if __name__ == "__main__":
    unittest.main()
