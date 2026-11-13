import os
import re

TARGET_EXTENSIONS = ('.html', '.py', '.js', '.json')

TAGLINE_REPLACEMENTS = [
    # Master exact tagline: "Anveil Every Charm" (A-N-V-E-I-L)
    (re.compile(r'ANVEIL\s+EVERY\s+CHARM', re.IGNORECASE), 'ANVEIL EVERY CHARM'),
    (re.compile(r'Anveil\s+Every\s+Charm', re.IGNORECASE), 'Anveil Every Charm'),
    (re.compile(r'anveil\s+every\s+charm', re.IGNORECASE), 'Anveil every charm'),
    (re.compile(r'ANVEIL', re.IGNORECASE), 'ANVEIL'),
    (re.compile(r'Anveil', re.IGNORECASE), 'Anveil'),
    (re.compile(r'anveil', re.IGNORECASE), 'anveil'),
    (re.compile(r'UNVEIL\s+EVERY\s+CHARM', re.IGNORECASE), 'ANVEIL EVERY CHARM'),
    (re.compile(r'Unveil\s+Every\s+Charm', re.IGNORECASE), 'Anveil Every Charm'),
    (re.compile(r'unveil\s+every\s+charm', re.IGNORECASE), 'Anveil every charm'),
]

# Marketing jargon replacements
JARGON_REPLACEMENTS = [
    (re.compile(r'\bUnlock\s+Your\b', re.IGNORECASE), 'Explore Your'),
    (re.compile(r'\bUnlock\s+Deeper\b', re.IGNORECASE), 'Reveal Deeper'),
    (re.compile(r'\bUnlock\s+Full\b', re.IGNORECASE), 'View Full'),
    (re.compile(r'\bUnlock\s+all\b', re.IGNORECASE), 'Explore all'),
    (re.compile(r'\bUnlock\b', re.IGNORECASE), 'Explore'),
    (re.compile(r'\bunlock\b', re.IGNORECASE), 'explore'),
    (re.compile(r'\bElevate\s+Your\b', re.IGNORECASE), 'Harmonize Your'),
    (re.compile(r'\belevate\s+your\b', re.IGNORECASE), 'harmonize your'),
    (re.compile(r'\bElevate\b', re.IGNORECASE), 'Enhance'),
    (re.compile(r'\belevate\b', re.IGNORECASE), 'enhance'),
    (re.compile(r'\bSeamlessly\b', re.IGNORECASE), 'Smoothly'),
    (re.compile(r'\bseamlessly\b', re.IGNORECASE), 'smoothly'),
    (re.compile(r'\bSeamless\b', re.IGNORECASE), 'Integrated'),
    (re.compile(r'\bseamless\b', re.IGNORECASE), 'integrated'),
    (re.compile(r'\bGame-changer\b', re.IGNORECASE), 'Pivotal shift'),
    (re.compile(r'\bgame-changer\b', re.IGNORECASE), 'pivotal shift'),
    (re.compile(r'\bRevolutionary\b', re.IGNORECASE), 'Advanced'),
    (re.compile(r'\brevolutionary\b', re.IGNORECASE), 'advanced'),
]

modified_files = 0
total_tagline_subs = 0
total_jargon_subs = 0

for root, dirs, files in os.walk('app'):
    for f in files:
        if f.endswith(TARGET_EXTENSIONS):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                original = fp.read()
            
            content = original
            tagline_subs = 0
            for pattern, repl in TAGLINE_REPLACEMENTS:
                content, n = pattern.subn(repl, content)
                tagline_subs += n
            
            jargon_subs = 0
            for pattern, repl in JARGON_REPLACEMENTS:
                content, n = pattern.subn(repl, content)
                jargon_subs += n
            
            if content != original:
                with open(p, 'w', encoding='utf-8') as fp:
                    fp.write(content)
                modified_files += 1
                total_tagline_subs += tagline_subs
                total_jargon_subs += jargon_subs
                print(f"Updated {p}: {tagline_subs} tagline fixes, {jargon_subs} jargon fixes.")

print(f"\nDone. Modified {modified_files} files.")
print(f"Total tagline standardizations: {total_tagline_subs}")
print(f"Total jargon eliminations: {total_jargon_subs}")
