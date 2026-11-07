import sqlite3
import json
import glob
import subprocess

# 1. Fresh SQLite from 0001 through 0006
conn = sqlite3.connect(':memory:')
c = conn.cursor()
for f in sorted(glob.glob('migrations/*.sql')):
    with open(f, 'r', encoding='utf-8') as sql_file:
        c.executescript(sql_file.read())

fresh_tables = ['enquiries', 'events', 'cookie_consents']
fresh_schema = {}
for tbl in fresh_tables:
    c.execute(f"PRAGMA table_info({tbl});")
    cols = c.fetchall()
    c.execute(f"PRAGMA index_list({tbl});")
    idxs = c.fetchall()
    fresh_schema[tbl] = {
        'columns': {row[1]: {'type': row[2], 'notnull': row[3], 'dflt': row[4], 'pk': row[5]} for row in cols},
        'indexes': [row[1] for row in idxs if not row[1].startswith('sqlite_autoindex')]
    }

# 2. Preview D1 from remote wrangler execution
cmd = [
    'npx.cmd', 'wrangler', 'd1', 'execute', 'numeros-vision-db-preview',
    '--remote',
    '--command=PRAGMA table_info(enquiries); PRAGMA index_list(enquiries); PRAGMA table_info(events); PRAGMA index_list(events); PRAGMA table_info(cookie_consents); PRAGMA index_list(cookie_consents);',
    '--json'
]
res = subprocess.run(cmd, capture_output=True, text=True, check=True)
data = json.loads(res.stdout)

preview_schema = {}
# data has 6 items: [enquiries_cols, enquiries_idx, events_cols, events_idx, cookie_cols, cookie_idx]
tables = ['enquiries', 'events', 'cookie_consents']
for i, tbl in enumerate(tables):
    cols_res = data[i*2]['results']
    idxs_res = data[i*2+1]['results']
    preview_schema[tbl] = {
        'columns': {row['name']: {'type': row['type'], 'notnull': row['notnull'], 'dflt': row['dflt_value'], 'pk': row['pk']} for row in cols_res},
        'indexes': [row['name'] for row in idxs_res if not row['name'].startswith('sqlite_autoindex')]
    }

print("=== DIFFERENCES (Preview D1 vs Fresh Migrations) ===")
for tbl in tables:
    print(f"\n--- TABLE: {tbl} ---")
    p_cols = set(preview_schema[tbl]['columns'].keys())
    f_cols = set(fresh_schema[tbl]['columns'].keys())
    
    in_preview_not_fresh = p_cols - f_cols
    in_fresh_not_preview = f_cols - p_cols
    common_cols = p_cols & f_cols
    
    print(f"Columns in Preview D1 but NOT in Fresh: {in_preview_not_fresh}")
    print(f"Columns in Fresh but NOT in Preview D1: {in_fresh_not_preview}")
    for col in common_cols:
        p_info = preview_schema[tbl]['columns'][col]
        f_info = fresh_schema[tbl]['columns'][col]
        if p_info != f_info:
            print(f"Column '{col}' definition mismatch: Preview={p_info} vs Fresh={f_info}")
            
    p_idxs = set(preview_schema[tbl]['indexes'])
    f_idxs = set(fresh_schema[tbl]['indexes'])
    print(f"Indexes in Preview D1 but NOT in Fresh: {p_idxs - f_idxs}")
    print(f"Indexes in Fresh but NOT in Preview D1: {f_idxs - p_idxs}")
