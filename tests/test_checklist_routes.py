"""
NUMEROS VISION — CHECKLIST ROUTE VALIDATION TEST
=================================================
Parses docs/PREVIEW_DEPLOYMENT_CHECKLIST.md for all occurrences of `/api/` paths
and verifies that 100% of the paths referenced in the checklist exist as canonical
handled routes inside app/static/_worker.js.
"""

import re
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHECKLIST_PATH = ROOT / "docs" / "PREVIEW_DEPLOYMENT_CHECKLIST.md"
WORKER_PATH = ROOT / "app" / "static" / "_worker.js"


def extract_checklist_api_paths():
    content = CHECKLIST_PATH.read_text(encoding="utf-8")
    # Matches /api/... up to query string, space, backtick, quote, paren, or markdown delimiter
    raw_matches = re.findall(r"(/api/[a-zA-Z0-9_\-\/]+)", content)
    # Strip any trailing punctuation or slashes
    clean_paths = sorted(set(p.rstrip("/").rstrip("`").rstrip(")") for p in raw_matches))
    return clean_paths


def extract_worker_api_routes():
    content = WORKER_PATH.read_text(encoding="utf-8")
    patterns = [
        r'pathname\s*===?\s*[\'"`]([^\'"`]+)[\'"`]',
        r'pathname\.startsWith\([\'"`]([^\'"`]+)[\'"`]\)',
    ]
    routes = set()
    for p in patterns:
        for m in re.finditer(p, content):
            path = m.group(1).rstrip("/")
            if path.startswith("/api"):
                routes.add(path)
    return routes


class TestChecklistRoutes(unittest.TestCase):
    def test_all_checklist_api_routes_exist_in_worker(self):
        self.assertTrue(CHECKLIST_PATH.exists(), f"{CHECKLIST_PATH} does not exist!")
        self.assertTrue(WORKER_PATH.exists(), f"{WORKER_PATH} does not exist!")

        checklist_paths = extract_checklist_api_paths()
        worker_routes = extract_worker_api_routes()

        print(f"\n[Checklist Route Audit] Found {len(checklist_paths)} API paths in checklist:")
        for p in checklist_paths:
            print(f"  - {p}")

        missing = []
        for p in checklist_paths:
            # Check direct match or prefix match (for wildcard endpoints like /api/v1/auth/)
            if p not in worker_routes and not any(p.startswith(r) for r in worker_routes):
                missing.append(p)

        self.assertEqual(
            missing,
            [],
            f"The following /api/ routes in docs/PREVIEW_DEPLOYMENT_CHECKLIST.md do NOT exist in _worker.js: {missing}"
        )
        print("PASS: 100% of API routes in PREVIEW_DEPLOYMENT_CHECKLIST.md match canonical _worker.js routes.")


if __name__ == "__main__":
    unittest.main()
