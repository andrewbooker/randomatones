#!/usr/bin/env python

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A6, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def add_rhs_address(canvas, size):
    canvas.setLineWidth(0.5)
    canvas.setStrokeColor("grey")
    half_x = size[0] / 2
    y_margin = 10
    canvas.line(half_x, y_margin, half_x, size[1] - y_margin)

    canvas.setStrokeColor("lightgrey")
    addr_margin = 30
    for p in [0.6, 0.48, 0.36, 0.24]:
        canvas.line(half_x + addr_margin, size[1] * p, size[0] - addr_margin, size[1] * p)

    canvas.setFillColorCMYK(0, 0, 0, 0.05)
    w, h = (50, 60)
    canvas.rect(size[0] - (w + y_margin), size[1] - (h + y_margin), w, h, stroke=0, fill=1)


def add_heading(canvas, size):
    t = canvas.beginText()
    pdfmetrics.registerFont(TTFont("Impact", "/usr/local/share/fonts/impact.ttf"))
    margin = 10
    font_size = 14
    t.setTextOrigin(margin, size[1] - (margin + font_size))
    t.setFont("Impact", font_size)
    t.setFillColorCMYK(0, 0, 0, 0.8)
    t.textLine("Randomatones")

    canvas.drawText(t)


size = landscape(A6)
canvas = Canvas("postcard_reverse.pdf", pagesize=size)
add_heading(canvas, size)
add_rhs_address(canvas, size)
canvas.save()
