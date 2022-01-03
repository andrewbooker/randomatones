#!/usr/bin/python

from xml.dom import minidom
import json

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

    whenAnchor = document.createElement("a")
    when = document.createElement("td")
    #d = new Date(t.when)
    #when.innerHTML = (d.getDate() < 10 ? "0" : "") + d.getDate() + " " + months[d.getMonth()] + " " + d.getFullYear()
    when.appendChild(document.createTextNode(t["when"]))
    when.setAttribute("style", "color: grey; font-size: 150%; font-weight: bold; float: right; margin-right: 30px;")
    whenAnchor.setAttribute("id", t["when"])
    whenAnchor.appendChild(when)

    h = document.createElement("td")
    h.setAttribute("style", "font-size: 150%; color: white; font-weight: bold; text-align: left;")
    h.appendChild(document.createTextNode(t["heading"]))
    head.appendChild(whenAnchor)
    head.appendChild(h)

    i = document.createElement("td")
    if "youtube" in t["image"]:
        y = document.createElement("iframe")
        y.setAttribute("width", str(302))
        y.setAttribute("height", str(198))
        y.setAttribute("allowfullscreen", "true")
        y.setAttribute("style", "border: none; margin-right: 30px; float: right;")
        y.setAttribute("src", "https://www.youtube.com/embed/" + t["href"].split("=")[1])
        y.appendChild(document.createTextNode(""))
        i.appendChild(y)
    else:
        landscape = t["orientation"] == "landscape" if "orientation" in t else False;
        img = document.createElement("img")
        img.setAttribute("src", t["image"])
        img.setAttribute("width", str(320 if landscape else 180))
        img.setAttribute("height", str(320 if not landscape else 180))

        img.setAttribute("style", "float: right; margin: 4px 30px 20px 0;")
        a = document.createElement("a")
        a.setAttribute("href", t["href"] if "href" in t else t["image"])
        a.setAttribute("target", "_blank")
        a.appendChild(img)

        i.appendChild(a)

    body.appendChild(i)

    txt = document.createElement("div")
    txt.appendChild(document.createTextNode(t["text"]))
    txt.setAttribute("style", "font-size: 90%; text-align: left; margin-bottom: 20px; color: rgb(221,234,234)")
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
    document.getElementById("recent-contents").setAttribute("style", "margin-left:" + lm + "px;");
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

with open("out.html", "w") as out:
    out.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n")
    out.write(page)

