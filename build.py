#!/usr/bin/python

from xml.dom import minidom
import json
import datetime
import sys
from random import randint

tl = open("timeline.js", "r")
timeline = json.load(tl)
tl.close()

document = minidom.parse("template.xhtml")
recent = document.getElementsByTagName("div")[2]
for t in timeline[:5]:
    d = document.createElement("div")
    a = document.createElement("a")
    a.setAttribute("href", "#%s" % t["when"])
    a.appendChild(document.createTextNode(t["heading"]))

    d.appendChild(a)
    recent.appendChild(d)

container = document.getElementsByTagName("tbody")[0]

for t in timeline:
    head = document.createElement("tr")
    body = document.createElement("tr")
    body.setAttribute("style", "vertical-align: top;")

    w = datetime.datetime.strptime(t["when"], "%Y-%m-%d").strftime('%d %b %Y')
    whenAnchor = document.createElement("a")
    when = document.createElement("td")

    whenAnchor.appendChild(document.createTextNode(w))
    when.setAttribute("class", "when")
    whenAnchor.setAttribute("id", t["when"])
    when.appendChild(whenAnchor)

    h = document.createElement("td")
    h.setAttribute("class", "post-heading")
    h.appendChild(document.createTextNode(t["heading"]))
    head.appendChild(when)
    head.appendChild(h)

    i = document.createElement("td")
    if "youtube" in t:
        y = document.createElement("iframe")
        y.setAttribute("id", str(randint(100000, 999999)))
        y.setAttribute("width", str(302))
        y.setAttribute("height", str(198))
        y.setAttribute("allowfullscreen", "true")
        y.setAttribute("class", "post-yt")
        y.setAttribute("src", "https://www.youtube.com/embed/" + t["youtube"])
        y.appendChild(document.createTextNode(""))
        i.appendChild(y)
    elif "image" in t:
        landscape = t["orientation"] != "portrait" if "orientation" in t else True;
        img = document.createElement("img")
        img.setAttribute("src", t["image"])
        img.setAttribute("width", str(320 if landscape else 180))
        img.setAttribute("height", str(320 if not landscape else 180))

        img.setAttribute("class", "post-image")
        a = document.createElement("a")
        imageId = t["image"].split("/")[-1].split("_")[0]
        a.setAttribute("href", "https://flickr.com/photos/90938695@N06/%s/in/album-72157716077356826/" % imageId)
        a.setAttribute("target", "_blank")
        a.appendChild(img)

        i.appendChild(a)

    body.appendChild(i)

    txt = document.createElement("div")
    txt.appendChild(document.createTextNode(t["text"]))
    txt.setAttribute("class", "post-text")
    td = document.createElement("td")
    td.appendChild(txt)
    body.appendChild(td)

    container.appendChild(head)
    container.appendChild(body)

scr = """
function resize() {
    const fh = Math.min(1000, 0.8 * window.innerWidth);
    const ft = Math.min(180, 0.3 * window.innerWidth);
    document.getElementById("heading").setAttribute("style", "font-size: " + fh + "%");
    document.getElementById("tagline").setAttribute("style", "font-size: " + ft + "%");

    let lm =  Math.min(62, window.innerWidth / 24.0);
    const m = (window.innerWidth / 2) - 640;
    if (m > 0) {
        lm += m;
    }
    ["recent-contents", "flickr"].forEach(id => {
        document.getElementById(id).setAttribute("style", "margin-left:" + lm + "px;");
    });
}
resize();
window.onresize = resize;
"""

script = document.getElementsByTagName("script")[0]
script.appendChild(document.createTextNode(scr))

page = document.documentElement.toprettyxml(indent="  ", encoding=None)
page = page.replace("&quot;","\"")
page = page.replace("&lt;", "<")
page = page.replace("&gt;", ">")

with open("index.html", "w") as out:
    out.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n")
    out.write(page)

