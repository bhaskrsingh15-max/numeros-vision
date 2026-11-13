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

    for sub in ('config', 'data', 'engine', 'services', 'logo_intelligence'):
        d = dest / sub
        d.mkdir(parents=True, exist_ok=True)
        init_file = d / '__init__.py'
        if not init_file.exists():
            init_file.write_text('', encoding='utf-8')
    root_init = dest / '__init__.py'
    if not root_init.exists():
        root_init.write_text('', encoding='utf-8')

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
        'app/data/indication_library.json',
        'app/data/remedy_library.json',
        'app/data/neighbour_relations.json',
        'app/data/name_denylist.json',
        'data/knowledge_base/day7_loshu_rules.json',
        'data/knowledge_base/missing_number_rules.json',
        'data/knowledge_base/driver_conductor_81_rules.json',
        'data/knowledge_base/numerological_mahadasha_rules.json',
        'app/engine/kua.py',
        'app/engine/core_matrix_engine.py',
        'app/engine/complementary_poorak_engine.py',
        'app/engine/vedic_gharelu_remedies.py',
        'app/engine/forecast_engine.py',
        'app/engine/number_characteristics_registry.py',
        'app/engine/cheiro_engine.py',
        'app/engine/professional_numerology_engine.py',
        'app/engine/asset_numerology_engine.py',
        'app/engine/digit_root.py',
        'app/engine/indication_validator.py',
        'app/engine/indication_schema_and_loader.py',
        'app/engine/indications_engine.py',
        'app/engine/layer1_golden_snapshot.py',
        'app/engine/charm_oracle_synthesizer.py',
        'app/engine/driver_conductor_81_engine.py',
        'app/engine/five_elements_hygiene_engine.py',
        'app/engine/rule_governance.py',
        'app/services/pdf_report_generator.py',
        'app/services/internal_pdf_worker_service.py',
        'data/logo_rules_v1.json',
        'app/logo_intelligence/__init__.py',
        'app/logo_intelligence/rulebook_v1.py',
    ]

    for rel in needed_files:
        src_path = root / rel
        dst_path = root / 'pdf_service' / rel
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dst_path)

    print(f"Populated pdf_service/app/ with {len(needed_files)} files.")

if __name__ == '__main__':
    sync_pdf_service()
