import sqlite3
import os

def test_migration_syntax_and_tables():
    conn = sqlite3.connect(':memory:')
    conn.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Run Migration 0001
    mig1 = os.path.join("migrations", "0001_initial_schema.sql")
    with open(mig1, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

    # 2. Run Migration 0002
    mig2 = os.path.join("migrations", "0002_invoices_refunds_audit.sql")
    with open(mig2, "r", encoding="utf-8") as f:
        conn.executescript(f.read())

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
        "sessions",
        "invoices",
        "refunds",
        "audit_log",
        "charm_answers",
        "report_insights"
    }

    assert expected.issubset(tables), f"Missing tables: {expected - tables}"
    
    # 3. Test Unique Constraints
    # Test users email uniqueness
    cursor.execute("INSERT INTO users (id, email, phone_hash, created_at) VALUES ('u1', 'test@example.com', 'p1_hash', 1000);")
    try:
        cursor.execute("INSERT INTO users (id, email, phone_hash, created_at) VALUES ('u2', 'test@example.com', 'p2_hash', 1001);")
        assert False, "Should have thrown UNIQUE constraint violation on users.email"
    except sqlite3.IntegrityError:
        pass # Expected

    # Test users phone_hash uniqueness
    try:
        cursor.execute("INSERT INTO users (id, email, phone_hash, created_at) VALUES ('u3', 'other@example.com', 'p1_hash', 1002);")
        assert False, "Should have thrown UNIQUE constraint violation on users.phone_hash"
    except sqlite3.IntegrityError:
        pass # Expected

    # Test orders rzp_order_id uniqueness
    cursor.execute("INSERT INTO orders (id, user_id, pack_id, amount_paise, rzp_order_id, created_at) VALUES ('o1', 'u1', 'pack_test', 19900, 'rzp_order_unique_99', 1000);")
    try:
        cursor.execute("INSERT INTO orders (id, user_id, pack_id, amount_paise, rzp_order_id, created_at) VALUES ('o2', 'u1', 'pack_test', 19900, 'rzp_order_unique_99', 1001);")
        assert False, "Should have thrown UNIQUE constraint violation on orders.rzp_order_id"
    except sqlite3.IntegrityError:
        pass # Expected

    print(f"Verified all {len(tables)} tables and unique constraints successfully across migrations 0001 & 0002!")

if __name__ == "__main__":
    test_migration_syntax_and_tables()
