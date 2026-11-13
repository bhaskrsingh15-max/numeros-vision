"""
Script: scripts/update_tagline_to_anveil.py
Purpose: Update all occurrences of brand tagline to 'Anveil Every Charm' and 'ANVEIL EVERY CHARM'
         across all website HTML pages, components, templates, SEO registry, and docs.
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Files/Directories to process
TARGET_EXTENSIONS = {'.html', '.py', '.css', '.json', '.md'}

# Files to explicitly skip
EXCLUDE_PATHS = [
    BASE_DIR / ".venv",
    BASE_DIR / ".git",
    BASE_DIR / "backups",
    BASE_DIR / "tests" / "test_claim_validator.py",  # keeps negative test case
    BASE_DIR / "tests" / "test_deep_llm_agents_questions_predictions_remedies.py",  # keeps dirty_text test
    BASE_DIR / "app" / "engine" / "claim_validator.py",  # handled specifically
]

def is_excluded(path: Path) -> bool:
    for exc in EXCLUDE_PATHS:
        try:
            if exc in path.parents or path.resolve() == exc.resolve():
                return True
        except Exception:
            pass
    return False

def update_file(path: Path) -> bool:
    if is_excluded(path):
        return False
    if path.suffix not in TARGET_EXTENSIONS:
        return False
    
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return False
        
    original = content

    # 1. Exact string replacements for both Unveil and Anveil variations to Anveil
    # All-caps
    content = content.replace("UNVEIL EVERY CHARM", "ANVEIL EVERY CHARM")
    content = content.replace("ANVEIL EVERY CHARM", "ANVEIL EVERY CHARM")
    
    # Title-case
    content = content.replace("Unveil Every Charm", "Anveil Every Charm")
    content = content.replace("Anveil Every Charm", "Anveil Every Charm")
    
    # Lowercase
    content = content.replace("unveil every charm", "anveil every charm")
    content = content.replace("anveil every charm", "anveil every charm")
    
    # Logo title and alt attributes
    content = content.replace("Numeros Vision — Unveil Every Charm", "Numeros Vision — Anveil Every Charm")
    content = content.replace("Numeros Vision - Unveil Every Charm", "Numeros Vision - Anveil Every Charm")
    content = content.replace("Numeros Vision — Anveil Every Charm", "Numeros Vision — Anveil Every Charm")
    content = content.replace("Numeros Vision - Anveil Every Charm", "Numeros Vision - Anveil Every Charm")

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    target_dirs = [BASE_DIR / "app", BASE_DIR / "data", BASE_DIR / "docs", BASE_DIR / "tests"]
    updated_files = []

    for d in target_dirs:
        for root, dirs, files in os.walk(d):
            for f in files:
                p = Path(root) / f
                if update_file(p):
                    updated_files.append(p.relative_to(BASE_DIR))

    print(f"Successfully updated tagline to 'Anveil Every Charm' in {len(updated_files)} files:")
    for f in updated_files:
        print(f"  - {f}")

if __name__ == "__main__":
    main()
