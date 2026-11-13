import sys
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

c = canvas.Canvas('test_frame.pdf', pagesize=A4)
w, h = A4

# Outer border
c.setStrokeColor(colors.HexColor('#C9A227'))
c.setLineWidth(1.2)
c.rect(20, 20, w - 40, h - 40)

# Inner border
c.setStrokeColor(colors.HexColor('#E2B84B'))
c.setLineWidth(0.6)
c.rect(23, 23, w - 46, h - 46)

# Footer
c.setFont("Times-Roman", 8)
c.setFillColor(colors.HexColor('#7A654D'))
c.drawString(34, 30, "Numeros Vision — ANVEIL EVERY CHARM")
c.setFont("Times-Bold", 8)
c.setFillColor(colors.HexColor('#8B6914'))
c.drawCentredString(w / 2.0, 30, "✦ VERIFIED ROYAL SEAL ✦")
c.drawRightString(w - 34, 30, "Page 1 of 3")

c.showPage()
c.save()

print("Frame generated successfully. Size:", os.path.getsize('test_frame.pdf'))
os.remove('test_frame.pdf')
