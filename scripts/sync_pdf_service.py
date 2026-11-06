"""
NUMEROS VISION — SYNC PDF SERVICE REPOSITORY SCRIPT
===================================================
Synchronizes needed engine and generator files from app/ into pdf_service/app/,
ensuring pdf_service is completely self-contained for isolated Cloud Run deployment.
"""

import pathlib
import shutil

def sync_pdf_service():
    root = pathlib.Path(__file__).resolve().parent.parent
    dest = root / 'pdf_service' / 'app'

    for sub in ('config', 'engine', 'services'):
        d = dest / sub
        d.mkdir(parents=True, exist_ok=True)
        (d / '__init__.py').write_text('', encoding='utf-8')
    (dest / '__init__.py').write_text('', encoding='utf-8')

    needed_files = [
        'app/config/packs.json',
        'app/config/pricing_config.py',
        'app/engine/core_matrix_engine.py',
        'app/engine/complementary_poorak_engine.py',
        'app/engine/vedic_gharelu_remedies.py',
        'app/engine/forecast_engine.py',
        'app/engine/asset_numerology_engine.py',
        'app/services/pdf_report_generator.py',
        'app/services/internal_pdf_worker_service.py',
    ]

    for rel in needed_files:
        src_path = root / rel
        dst_path = root / 'pdf_service' / rel
        shutil.copy2(src_path, dst_path)

    print(f"Populated pdf_service/app/ with {len(needed_files)} files.")

if __name__ == '__main__':
    sync_pdf_service()
