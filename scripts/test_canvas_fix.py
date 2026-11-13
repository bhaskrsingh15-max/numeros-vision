from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.pdfgen import canvas
import pypdf

COLOR_PEARL_BG = colors.HexColor("#FFFDF7")
COLOR_GOLD_DARK = colors.HexColor("#8B6914")
COLOR_BORDER = colors.HexColor("#EEDDB8")
COLOR_INK_MUTED = colors.HexColor("#7A654D")

class TestCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages: int):
        self.saveState()
        w, h = A4
        # Running header on page 2+
        if self._pageNumber > 1:
            self.setStrokeColor(COLOR_GOLD_DARK)
            self.setLineWidth(0.8)
            self.line(40, h - 42, w - 40, h - 42)
            self.setFont("Times-Bold", 8)
            self.setFillColor(COLOR_GOLD_DARK)
            self.drawString(40, h - 34, "NUMEROS VISION")

        # Running footer
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(40, 44, w - 40, 44)
        self.setFont("Times-Roman", 8)
        self.setFillColor(COLOR_INK_MUTED)
        self.drawString(40, 32, "Numeros Vision © 2026")
        self.drawRightString(w - 40, 32, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()

def draw_bg(c, doc):
    c.saveState()
    w, h = A4
    c.setFillColor(COLOR_PEARL_BG)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.restoreState()

doc = SimpleDocTemplate('test_output.pdf', pagesize=A4, leftMargin=40, rightMargin=40, topMargin=50, bottomMargin=50)
styles = getSampleStyleSheet()
story = [
    Paragraph("<b>Hello World Page 1</b>", styles['Heading1']),
    Paragraph("This is page 1 content that must be visible and NOT covered.", styles['Normal']),
    PageBreak(),
    Paragraph("<b>Hello World Page 2</b>", styles['Heading1']),
    Paragraph("This is page 2 content that must be visible.", styles['Normal'])
]
doc.build(story, canvasmaker=TestCanvas, onFirstPage=draw_bg, onLaterPages=draw_bg)

# Let's inspect the stream of test_output.pdf
reader = pypdf.PdfReader('test_output.pdf')
p1_stream = reader.pages[0].get_contents().get_data().decode('latin1', 'backslashreplace')
print("Page 1 stream starts with bg rect:", p1_stream.find("re f") < p1_stream.find("Hello World"))
print("First re f pos:", p1_stream.find("re f"))
print("Hello World pos:", p1_stream.find("Hello World"))
print("Test completed successfully!")
