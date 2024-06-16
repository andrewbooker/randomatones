#!/usr/bin/env python

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A6, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import cm
import os
from PIL import Image
import requests
import io


bleed = 0.3 * cm
size = (tuple([t + (bleed * 2) for t in landscape(A6)]))
canvas = Canvas("postcard_front.pdf", pagesize=size)

w_imgs = [
    ("https://live.staticflickr.com/65535/53794930691_7fe02bc0dc_b.jpg", 0.2, "Walthamstow Forest"),
    ("https://live.staticflickr.com/65535/53795241949_051ecc1248_b.jpg", 0.9, "South Woodford"),
    ("https://live.staticflickr.com/65535/53795150323_693d6768b7_b.jpg", 0.1, "Snarestone Tunnel"),
    ("https://live.staticflickr.com/65535/53795241979_b0e61dd7f7_b.jpg", 1.0, "Woolwich Foot Tunnel"),
]

x_2 = size[0] / 2
y_2 = size[1] / 2
ratio = size[0] / size[1]

for i in range(4):
    get_resp = requests.get(w_imgs[i][0])
    if get_resp.status_code != 200:
        break

    pil_img = Image.open(io.BytesIO(get_resp.content))
    required_width = int(pil_img.height * ratio)
    surplus_width = pil_img.width - required_width

    top = 0
    bottom = pil_img.height
    left = surplus_width * w_imgs[i][1]
    right = left + required_width
    cr = (left, top, right, bottom)
    print(pil_img.size, required_width, cr)

    img = ImageReader(pil_img.crop(cr))
    canvas.drawImage(img, (i % 2) * x_2, (int(0.5 * i) % 2) * y_2, width=x_2, height=y_2, mask="auto")

canvas.save()
