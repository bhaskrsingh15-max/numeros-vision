import re

with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func_pattern = r'    def draw_page_decorations\(self, total_pages: int\):[\s\S]*?self\.restoreState\(\)'

new_func = '''    def draw_page_decorations(self, total_pages: int):
        self.saveState()
        w, h = A4

        # Dual Jupiter Gold Border (Outer: 1.4pt, Inner: 0.6pt)
        self.setStrokeColor(COLOR_GOLD)
        self.setLineWidth(1.4)
        self.rect(20, 20, w - 40, h - 40, fill=0, stroke=1)

        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.rect(23.5, 23.5, w - 47, h - 47, fill=0, stroke=1)

        # 4 Royal L-Bracket Corner Ornaments
        arm = 12
        self.setStrokeColor(COLOR_GOLD_DARK)
        self.setLineWidth(1.8)
        # Top-Left
        self.line(20, h - 20, 20 + arm, h - 20)
        self.line(20, h - 20, 20, h - 20 - arm)
        # Top-Right
        self.line(w - 20, h - 20, w - 20 - arm, h - 20)
        self.line(w - 20, h - 20, w - 20, h - 20 - arm)
        # Bottom-Left
        self.line(20, 20, 20 + arm, 20)
        self.line(20, 20, 20, 20 + arm)
        # Bottom-Right
        self.line(w - 20, 20, w - 20 - arm, 20)
        self.line(w - 20, 20, w - 20, 20 + arm)

        # Running Top Header on Page 2+
        if self._pageNumber > 1:
            self.setStrokeColor(COLOR_GOLD)
            self.setLineWidth(0.8)
            self.line(36, h - 38, w - 36, h - 38)

            self.setFont("Times-Bold", 8)
            self.setFillColor(COLOR_GOLD_DARK)
            self.drawString(36, h - 32, "NUMEROS VISION")

            self.setFont("Times-Italic", 7.5)
            self.setFillColor(COLOR_INK_MUTED)
            self.drawRightString(w - 36, h - 32, "ANVEIL EVERY CHARM  ·  NUMEROS VISION")

        # Running Footer on all pages
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(36, 42, w - 36, 42)

        self.setFont("Times-Roman", 7.5)
        self.setFillColor(COLOR_INK_MUTED)
        self.drawString(36, 30, "Numeros Vision © 2026 | Numeros Vision (+91 9818418039) | Confidential Destiny Dossier")

        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.setFont("Times-Bold", 8)
        self.setFillColor(COLOR_GOLD_DARK)
        self.drawRightString(w - 36, 30, page_str)

        self.restoreState()'''

content, count = re.subn(old_func_pattern, new_func, content)
print(f"Replaced {count} occurrences of draw_page_decorations.")

with open('app/services/pdf_report_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated app/services/pdf_report_generator.py successfully.")
