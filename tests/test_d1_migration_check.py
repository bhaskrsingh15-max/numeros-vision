# tests/test_d1_migration_check.py
import unittest
import json
import os
import glob

def parse_and_verify_migrations(raw_wrangler_json, repo_migration_names):
    if not raw_wrangler_json or not raw_wrangler_json.strip():
        raise ValueError("Empty output from wrangler execution")
    
    try:
        parsed = json.loads(raw_wrangler_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from wrangler: {e}")
        
    if not isinstance(parsed, list) or len(parsed) == 0:
        raise ValueError("Malformed response: expected list of results")
        
    first_result = parsed[0]
    if not first_result.get("success", False):
        raise ValueError("D1 execution failed or returned success=False")
        
    results = first_result.get("results", [])
    applied_names = [row["name"] for row in results if "name" in row]
    
    unapplied = [m for m in repo_migration_names if m not in applied_names]
    return applied_names, unapplied

class TestD1MigrationCheck(unittest.TestCase):
    def setUp(self):
        self.repo_migrations = sorted([
            os.path.basename(f) for f in glob.glob("migrations/*.sql")
        ])
        
    def test_full_match_passes(self):
        # Mock payload matching all repo migrations
        mock_results = [{"name": m} for m in self.repo_migrations]
        mock_json = json.dumps([{"results": mock_results, "success": True}])
        
        applied, unapplied = parse_and_verify_migrations(mock_json, self.repo_migrations)
        self.assertEqual(len(unapplied), 0)
        self.assertEqual(len(applied), len(self.repo_migrations))

    def test_partial_match_fails_with_unapplied(self):
        # Missing 0006 and 0007
        mock_results = [{"name": m} for m in self.repo_migrations if not m.startswith("0006") and not m.startswith("0007")]
        mock_json = json.dumps([{"results": mock_results, "success": True}])
        
        applied, unapplied = parse_and_verify_migrations(mock_json, self.repo_migrations)
        self.assertTrue("0007_schema_alignment.sql" in unapplied)
        self.assertTrue(len(unapplied) >= 2)

    def test_empty_database_fails(self):
        mock_json = json.dumps([{"results": [], "success": True}])
        applied, unapplied = parse_and_verify_migrations(mock_json, self.repo_migrations)
        self.assertEqual(len(unapplied), len(self.repo_migrations))

    def test_wrangler_error_payload_raises(self):
        mock_json = json.dumps([{"errors": [{"message": "no such table: d1_migrations"}], "success": False}])
        with self.assertRaises(ValueError):
            parse_and_verify_migrations(mock_json, self.repo_migrations)

    def test_invalid_json_raises(self):
        with self.assertRaises(ValueError):
            parse_and_verify_migrations("Unknown argument: json\nError", self.repo_migrations)

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            parse_and_verify_migrations("", self.repo_migrations)

if __name__ == '__main__':
    unittest.main()
