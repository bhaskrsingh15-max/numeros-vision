import os, re, json

sys_banned = ['luck', 'lucky', 'guaranteed', 'will bring', 'will fix', 'prediction', 'prescription', 'consecrated', 'cure', 'exact']
pattern = re.compile(r'\b(' + '|'.join(re.escape(w) for w in sys_banned) + r')\b', re.IGNORECASE)

p1_entries = []
p2_entries = []

for root, dirs, files in os.walk('app/static'):
    for f in sorted(files):
        if not (f.endswith('.html') or f.endswith('.js')):
            continue
        rel_path = os.path.relpath(os.path.join(root, f), '.').replace('\\', '/')
        
        # Categorize P1 vs P2
        is_p2 = 'blog/' in rel_path or 'amp/' in rel_path
        
        with open(rel_path, 'r', encoding='utf-8', errors='ignore') as fp:
            lines = fp.readlines()
            
        file_hits = []
        for line_idx, line in enumerate(lines):
            matches = pattern.findall(line)
            if matches:
                clean_line = line.strip()
                # Skip comments that are purely internal code comments if needed, but per rule capture all active customer-facing copy
                file_hits.append({
                    'line': line_idx + 1,
                    'words': sorted(list(set(w.lower() for w in matches))),
                    'snippet': clean_line[:140]
                })
                
        if file_hits:
            target_list = p2_entries if is_p2 else p1_entries
            target_list.append({
                'file': rel_path,
                'total_hits': len(file_hits),
                'hits': file_hits
            })

report_data = {
    'summary': {
        'total_p1_files': len(p1_entries),
        'total_p1_occurrences': sum(e['total_hits'] for e in p1_entries),
        'total_p2_files': len(p2_entries),
        'total_p2_occurrences': sum(e['total_hits'] for e in p2_entries),
    },
    'p1_surfaces': p1_entries,
    'p2_surfaces': p2_entries
}

os.makedirs('data', exist_ok=True)
with open('data/banned_words_audit.json', 'w', encoding='utf-8') as out_f:
    json.dump(report_data, out_f, indent=2)

# Also generate a markdown report
os.makedirs('docs/audit', exist_ok=True)
with open('docs/audit/BANNED_WORDS_P1_P2_INVENTORY.md', 'w', encoding='utf-8') as md_f:
    md_f.write('# Exhaustive Banned-Word Inventory: P1 vs P2 Surfaces\n\n')
    md_f.write(f"**Total P1 Hits**: {report_data['summary']['total_p1_occurrences']} in {report_data['summary']['total_p1_files']} files  \n")
    md_f.write(f"**Total P2 Hits**: {report_data['summary']['total_p2_occurrences']} in {report_data['summary']['total_p2_files']} files  \n\n")
    md_f.write('---\n\n')
    
    md_f.write('## P1 Surfaces (Product, Calculators, /your-reading/, Checkout, Home, Dashboard)\n\n')
    for e in p1_entries:
        md_f.write(f"### `{e['file']}` ({e['total_hits']} hits)\n")
        for h in e['hits']:
            md_f.write(f"- **L{h['line']}** `[{', '.join(h['words'])}]`: `{h['snippet']}`\n")
        md_f.write('\n')
        
    md_f.write('---\n\n')
    md_f.write('## P2 Surfaces (Blog, Educational Articles, AMP)\n\n')
    for e in p2_entries:
        md_f.write(f"### `{e['file']}` ({e['total_hits']} hits)\n")
        for h in e['hits']:
            md_f.write(f"- **L{h['line']}** `[{', '.join(h['words'])}]`: `{h['snippet']}`\n")
        md_f.write('\n')

print(f"Generated data/banned_words_audit.json and docs/audit/BANNED_WORDS_P1_P2_INVENTORY.md successfully.")
print(f"P1: {report_data['summary']['total_p1_occurrences']} hits in {len(p1_entries)} files")
print(f"P2: {report_data['summary']['total_p2_occurrences']} hits in {len(p2_entries)} files")
