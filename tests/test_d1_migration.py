import sqlite3
import os

def test_migration_syntax_and_tables():
    conn = sqlite3.connect(':memory:')
    conn.execute("PRAGMA foreign_keys = ON;")
    
    migration_file = os.path.join("migrations", "0001_initial_schema.sql")
    with open(migration_file, "r", encoding="utf-8") as f:
        sql = f.read()

    conn.executescript(sql)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = set([r[0] for r in cursor.fetchall()])

    expected = {
        "users",
        "subjects",
        "orders",
        "payments",
        "webhook_events",
        "entitlements",
        "voucher_ledger",
        "credit_ledger",
        "report_jobs",
        "consents",
        "otp_challenges",
        "sessions"
    }

    assert expected.issubset(tables), f"Missing tables: {expected - tables}"
    print(f"Verified all {len(expected)} tables successfully in SQLite/D1 in-memory engine!")

if __name__ == "__main__":
    test_migration_syntax_and_tables()
