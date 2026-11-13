with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_s = '''    audit_meta = {
        "report_id": calc_data["report_id"],
        "tier": tier_clean,
        "topic_id": topic_id,
        "engine_version": calc_data["engine_version"],
        "generated_at": calc_data["generated_at"],
        "byte_size": len(pdf_bytes),
        "qa_passed": True,
        "calculation_data": calc_data
    }'''

new_s = '''    actual_pages = len(re.findall(rb'/Type\\s*/Page\\b', pdf_bytes))

    audit_meta = {
        "report_id": calc_data["report_id"],
        "tier": tier_clean,
        "topic_id": topic_id,
        "engine_version": calc_data["engine_version"],
        "generated_at": calc_data["generated_at"],
        "byte_size": len(pdf_bytes),
        "pages_count": actual_pages,
        "qa_passed": True,
        "calculation_data": calc_data
    }'''

# Normalize newlines for matching
text_crlf = '\r\n' in text
if text_crlf:
    old_s = old_s.replace('\n', '\r\n')
    new_s = new_s.replace('\n', '\r\n')

if old_s in text:
    text = text.replace(old_s, new_s)
    with open('app/services/pdf_report_generator.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Updated pdf_report_generator.py with pages_count')
else:
    print('old_s not found')
