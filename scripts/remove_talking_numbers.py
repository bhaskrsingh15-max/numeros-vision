"""
Removes 'Numeros Vision' across all frontend, backend, engine, reports, and demo files.
Replaces with 'Numeros Vision'.
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

REPLACEMENTS = [
    ("✦ NUMEROS VISION · MASTER NUMEROLOGY MATRIX ✦", "✦ NUMEROS VISION · MASTER NUMEROLOGY MATRIX ✦"),
    ("✦ NUMEROS VISION · SACRED NUMEROLOGY BLUEPRINT ✦", "✦ NUMEROS VISION · ANVEIL EVERY CHARM ✦"),
    ("Numeros Vision & Numeros Vision", "Numeros Vision"),
    ("Numeros Vision &amp; Numeros Vision", "Numeros Vision"),
    ("Numeros Vision / Numeros Vision", "Numeros Vision"),
    ("Numeros Vision or Numeros Vision", "Numeros Vision"),
    ("Numeros Vision, Pages", "Numeros Vision, Pages"),
    ("Numeros Vision Senior Practitioner Archives", "Numeros Vision Senior Practitioner Archives"),
    ("Numeros Vision Commercial Advisory", "Numeros Vision Commercial Advisory"),
    ("Numeros Vision Classical Methodology", "Numeros Vision Classical Methodology"),
    ("Numeros Vision Canon", "Numeros Vision Canon"),
    ("Numeros Vision Professional / Advanced", "Numeros Vision Professional / Advanced"),
    ("Numeros Vision Professional", "Numeros Vision Professional"),
    ("Founder, Numeros Vision", "Founder, Numeros Vision"),
    ("(Founder, Numeros Vision)", "(Founder, Numeros Vision)"),
    ("Bhaskr Singh (Numeros Vision)", "Bhaskr Singh (Numeros Vision)"),
    ("Bhaskr Singh · Numeros Vision", "Bhaskr Singh · Numeros Vision"),
    ("Numeros Vision (+91 9818418039)", "Numeros Vision (+91 9818418039)"),
    ("(Numeros Vision)", "(Numeros Vision)"),
    ("Numeros Vision", "Numeros Vision"),
    ("numeros vision", "numeros vision"),
    ("NUMEROS VISION", "NUMEROS VISION"),
]

def clean_file(filepath):
    if not os.path.isfile(filepath):
        return False
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        original = content
        for old, new in REPLACEMENTS:
            if old in content:
                content = content.replace(old, new)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Scrubbed: {filepath}")
            return True
    except Exception as e:
        pass
    return False

def main():
    skip_dirs = {'.git', 'venv', 'env', 'node_modules', '__pycache__', 'dist', 'backups', '.system_generated', '.user_uploaded'}
    
    cleaned_count = 0
    # Clean app directory
    for root, dirs, files in os.walk('app'):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for f in files:
            if f.endswith(('.html', '.py', '.js', '.json', '.md', '.txt')):
                p = os.path.join(root, f)
                if clean_file(p):
                    cleaned_count += 1

    # Clean root files of artifact directory
    art_dir = r'C:\Users\Bhaskr Singh\.gemini\antigravity\brain\c1ea3ed7-b9d2-437a-b7aa-f0cb4004681b'
    if os.path.exists(art_dir):
        for f in os.listdir(art_dir):
            p = os.path.join(art_dir, f)
            if os.path.isfile(p) and f.endswith(('.html', '.py', '.js', '.json', '.md')):
                if clean_file(p):
                    cleaned_count += 1

    print(f"\nCompleted scrubbing 'Numeros Vision'. Total files updated: {cleaned_count}")

if __name__ == '__main__':
    main()
