#!/usr/bin/python

import qrcode
import sys

www = sys.argv[1]

qr = qrcode.QRCode(version=1, box_size=6, border=2)
qr.add_data(www)
qr.make(fit=True)
img = qr.make_image(fill="black", back_color="white")
img.save("qrcode.png")
