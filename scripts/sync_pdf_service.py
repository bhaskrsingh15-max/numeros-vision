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

    for sub in ('config', 'data', 'engine', 'services'):
        d = dest / sub
        d.mkdir(parents=True, exist_ok=True)
        (d / '__init__.py').write_text('', encoding='utf-8')
    (dest / '__init__.py').write_text('', encoding='utf-8')

    needed_files = [
        'app/assets/nv-logo-mark.png',
        'app/assets/nv-icon.png',
        'app/assets/nv-report-watermark-12pct-4096.png',
        'app/assets/nv-header-lockup-transparent-2x.png',
        'app/config/packs.json',
        'app/config/pricing_config.py',
        'app/data/birth_subdates_registry.json',
        'app/data/basic_report_content_library.json',
        'app/data/terminology_geo.json',
        'app/engine/kua.py',
        'app/engine/core_matrix_engine.py',
        'app/engine/complementary_poorak_engine.py',
        'app/engine/vedic_gharelu_remedies.py',
        'app/engine/forecast_engine.py',
        'app/engine/number_characteristics_registry.py',
        'app/engine/cheiro_engine.py',
        'app/engine/professional_numerology_engine.py',
        'app/engine/asset_numerology_engine.py',
        'app/services/pdf_report_generator.py',
        'app/services/internal_pdf_worker_service.py',
    ]

    for rel in needed_files:
        src_path = root / rel
        dst_path = root / 'pdf_service' / rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)

    print(f"Populated pdf_service/app/ with {len(needed_files)} files.")

if __name__ == '__main__':
    sync_pdf_service()
