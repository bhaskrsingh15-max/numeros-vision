import sqlite3
import glob

def test_migrations():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    files = sorted(glob.glob('migrations/*.sql'))
    for f in files:
        with open(f, 'r', encoding='utf-8') as sql_file:
            c.executescript(sql_file.read())
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in c.fetchall() if not r[0].startswith('sqlite_')]
    print(f"All {len(files)} migrations replayed successfully into SQLite. Tables ({len(tables)}):")
    for t in tables:
        print(f"  - {t}")

if __name__ == '__main__':
    test_migrations()
