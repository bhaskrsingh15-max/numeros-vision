import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

targets = [
    r'data/knowledge_base/case_library.json',
    r'data/knowledge_base/day8_complementary_masterkey_twins_rules.json',
    r'data/knowledge_base/missing_number_rules.json',
    r'data/knowledge_base/numerological_mahadasha_rules.json',
    r'data/knowledge_base/numeros_vision_corpus.json',
    r'data/knowledge_base/source_registry.json',
    r'docs/NUMEROS_VISION_MASTER_SPECIFICATION.md'
]

replacements = [
    (re.compile(r'Numeros Vision & Numeros Vision', re.IGNORECASE), 'Numeros Vision'),
    (re.compile(r'Numeros Vision / Numeros Vision', re.IGNORECASE), 'Numeros Vision'),
    (re.compile(r'Numeros Vision / Numeros Vision', re.IGNORECASE), 'Numeros Vision'),
    (re.compile(r'NUMEROS VISION', re.IGNORECASE), 'NUMEROS VISION'),
    (re.compile(r'Numeros Vision', re.IGNORECASE), 'Numeros Vision'),
    (re.compile(r'numeros vision', re.IGNORECASE), 'numeros vision'),
]

for target in targets:
    if os.path.exists(target):
        with open(target, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        orig_len = len(content)
        for pattern, repl in replacements:
            content = pattern.sub(repl, content)
            
        with open(target, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Scrubbed {target}")

print("Knowledge base scrub complete.")
