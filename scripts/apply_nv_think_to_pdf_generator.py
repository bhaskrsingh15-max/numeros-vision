import sys
import re

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

path = 'app/services/pdf_report_generator.py'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update __init__ to attach nv_think
init_target = '''        self.topic_id = self._normalize_topic(topic_id)
        self.styles = _build_styles()
        self.story = []'''

init_repl = '''        self.topic_id = self._normalize_topic(topic_id)
        self.styles = _build_styles()
        self.story = []
        try:
            from app.engine.nv_psychology_engine import nv_think_engine
            self.nv_think = nv_think_engine.evaluate_chart_synthesis(
                driver=self.data.get('driver', 1),
                conductor=self.data.get('conductor', 4),
                loshu_counts=self.data.get('loshu_counts', {}),
                active_planes=self.data.get('active_planes', []),
                missing_numbers=self.data.get('missing_numbers', []),
                user_environment="Executive / Professional Career Context"
            )
        except Exception:
            self.nv_think = {}'''

if init_target in c:
    c = c.replace(init_target, init_repl)
    print("1. Updated NumerosPdfReportBuilder.__init__ with nv_think")
else:
    init_target_crlf = init_target.replace('\n', '\r\n')
    init_repl_crlf = init_repl.replace('\n', '\r\n')
    if init_target_crlf in c:
        c = c.replace(init_target_crlf, init_repl_crlf)
        print("1. Updated NumerosPdfReportBuilder.__init__ with nv_think (CRLF)")

# 2. Update Basic Report Page 2 summary callout
basic_p2_target = '''        summary_p = Paragraph(
            f"<b>Active Present Numbers:</b> <b>[1, 2, 8, 9]</b> (Quadruple 1 solar executive stamina, double 8 financial realism).<br/><b>Karmic Sleeping Charms (To Anveil):</b> <b>[3, 4, 5, 6, 7]</b>. Lacking central 5 is successfully bridged by Calling Name 32 → 5.",
            s['CalloutText']
        )'''

basic_p2_repl = '''        summary_p = Paragraph(
            f"<b>NV THINK™ Cognitive Synthesis:</b> <b>Present Numbers [1, 2, 8, 9]</b> reflect high autonomous drive (1) and grounded endurance (8). Operational duality: tension between rapid executive action and cautious verification is a strategic balance, not an error. <b>Missing Voids [3, 4, 5, 6, 7]</b> represent unpracticed elemental planes, harmonized via Calling Name 32 → 5 and targeted daily routines.",
            s['CalloutText']
        )'''

if basic_p2_target in c:
    c = c.replace(basic_p2_target, basic_p2_repl)
    print("2. Updated Basic Report Page 2 callout")
else:
    b_target_crlf = basic_p2_target.replace('\n', '\r\n')
    b_repl_crlf = basic_p2_repl.replace('\n', '\r\n')
    if b_target_crlf in c:
        c = c.replace(b_target_crlf, b_repl_crlf)
        print("2. Updated Basic Report Page 2 callout (CRLF)")

# 3. Update Advanced Report Page 2 TOC banner
toc_target = '''            self.story.append(Paragraph("✦   MASTER SYNTHESIS DOSSIER · 10 STANDARD SECTIONS ACROSS 12 PAGES   ✦", s['CoverSubtitle']))'''
toc_repl = '''            self.story.append(Paragraph("✦   MASTER SYNTHESIS DOSSIER · NV THINK™ LOGIC-TO-PSYCHOLOGY ARCHITECTURE   ✦", s['CoverSubtitle']))'''

if toc_target in c:
    c = c.replace(toc_target, toc_repl)
    print("3. Updated Advanced Report Page 2 TOC banner")
else:
    toc_target_crlf = toc_target.replace('\n', '\r\n')
    toc_repl_crlf = toc_repl.replace('\n', '\r\n')
    if toc_target_crlf in c:
        c = c.replace(toc_target_crlf, toc_repl_crlf)
        print("3. Updated Advanced Report Page 2 TOC banner (CRLF)")

# 4. Update Advanced Report Page 3 Executive Charter
exec_target = '''        exec_summary_p = Paragraph(
            f"<b>Executive Charter:</b> This dossier is prepared for <b>{d['seeker_name']}</b> born on <b>28-11-1981</b> at 04:15 PM in New Delhi. Combining Driver 1 (Sun), Conductor 4 (Rahu), and Chaldean 32/5 (Mercury), this report maps your inborn present numbers, 5-year Numerology Dasha timing radar, and safe home-accessible Vedic Gharelu remedies with zero ambiguity.",
            s['CalloutText']
        )'''

exec_repl = '''        exec_summary_p = Paragraph(
            f"<b>NV THINK™ Executive Charter:</b> This dossier is prepared for <b>{d['seeker_name']}</b> (DOB: 28-11-1981). Combining Driver 1 (Sun), Conductor 4 (Rahu), and Chaldean 32/5 (Mercury), this report decodes your chart through the 7 stages of intelligence: from deterministic mathematical logic to behavioral observations, psychological motivations, and responsible 5-year Dasha timing.",
            s['CalloutText']
        )'''

if exec_target in c:
    c = c.replace(exec_target, exec_repl)
    print("4. Updated Advanced Report Page 3 Executive Charter")
else:
    exec_target_crlf = exec_target.replace('\n', '\r\n')
    exec_repl_crlf = exec_repl.replace('\n', '\r\n')
    if exec_target_crlf in c:
        c = c.replace(exec_target_crlf, exec_repl_crlf)
        print("4. Updated Advanced Report Page 3 Executive Charter (CRLF)")

# 5. Update Advanced Report Page 12 Governance table with NV THINK row
gov_target = '''            [Paragraph("Interpretive Boundary", s['TableCell']), Paragraph("Traditional numerology offers psychological and spiritual perspectives for self-reflection. It does not replace professional medical, legal, or financial counsel.", s['TableCell'])],'''
gov_repl = '''            [Paragraph("Interpretive Boundary", s['TableCell']), Paragraph("Traditional numerology offers psychological and spiritual perspectives for self-reflection. It does not replace professional medical, legal, or financial counsel.", s['TableCell'])],
            [Paragraph("NV THINK™ Framework", s['TableCell']), Paragraph("Reasoned across 7 stages: Logic → Observation → Behaviour → Psychology → Context → Duality → Validation. A number is an interpretive indicator, not a fixed person.", s['TableCell'])],'''

if gov_target in c:
    c = c.replace(gov_target, gov_repl)
    print("5. Updated Advanced Report Page 12 Governance table")
else:
    gov_target_crlf = gov_target.replace('\n', '\r\n')
    gov_repl_crlf = gov_repl.replace('\n', '\r\n')
    if gov_target_crlf in c:
        c = c.replace(gov_target_crlf, gov_repl_crlf)
        print("5. Updated Advanced Report Page 12 Governance table (CRLF)")

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Finished applying NV THINK™ updates to pdf_report_generator.py")
