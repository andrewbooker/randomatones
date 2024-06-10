#!/usr/bin/env python

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A6, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
import qrcode
from reportlab.lib.utils import ImageReader

def add_rhs_address(canvas, size):
    canvas.setLineWidth(0.5)
    canvas.setStrokeColor("lightgrey")
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
    margin = 10
    font_size = 14
    t.setTextOrigin(margin, size[1] - (margin + font_size))
    t.setFont("Impact", font_size)
    t.setFillColorCMYK(0, 0, 0, 0.8)
    t.textLine("Randomatones")

    canvas.drawText(t)


def add_upper_details(canvas, size):
    t = canvas.beginText()
    margin = 10

    t.setTextOrigin(margin, size[1] - 36)
    t.setFont("Helvetica", 8)
    t.textLine("Pop-up aleatoric music installations")

    t.setFont("Helvetica", 5)
    t.textLine("Clockwise from top left:")
    t.textLine(", ".join([
        "Snarestone",
        "Walthamstow Forest",
        "Lisson Grove",
        "Woolwich Foot Tunnel"
    ]))

    canvas.drawText(t)


def add_lower_details(canvas, size):
    img = qrcode.make("http://randomatones.co.uk/portfolio.html")
    canvas.drawImage(ImageReader(img.get_image()), 5, 5, width=60, height=60, mask="auto")

    t = canvas.beginText()
    x_pos = 70
    t.setFillColorCMYK(0, 0, 0, 0.8)
    t.setTextOrigin(x_pos, 50)
    t.setFont("Impact", 10)
    t.textLine("Andrew Booker")
    t.setFont("Helvetica", 6)
    t.textLine("improvizone@gmail.com")
    t.textLine("randomatones.co.uk")
    t.textLine("youtube.com/@Randomatones")

    t.setTextOrigin(x_pos, 12)
    t.textLine("QR code for video portfolio")

    canvas.drawText(t)


pdfmetrics.registerFont(TTFont("Impact", "/usr/local/share/fonts/impact.ttf"))
size = landscape(A6)
canvas = Canvas("postcard_reverse.pdf", pagesize=size)
items = {
    add_heading,
    add_upper_details,
    add_lower_details,
    add_rhs_address,
}

for i in items:
    i(canvas, size)
canvas.save()
