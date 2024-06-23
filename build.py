#!/usr/bin/python

from xml.dom import minidom
import json
import datetime
import sys
from random import randint


class TemplateDoc:
    def __init__(self, template_fn, out_fn):
        self.document = minidom.parse(template_fn)
        self.out_fn = out_fn
        for n in self.document.getElementsByTagName("*"):
            if n.hasAttribute("id"):
                n.setIdAttribute("id")

    def _add_yt_to(self, add_to, t, scale):
        yt_id = t["youtube"]
        y = self.document.createElement("iframe")
        y.setAttribute("width", str(int(302 * scale)))
        y.setAttribute("height", str(int(198 * scale)))
        y.setAttribute("allowfullscreen", "true")
        y.setAttribute("class", "iframe-yt")
        y.setAttribute("src", f"https://www.youtube.com/embed/{yt_id}?{randint(100000, 999999)}")
        y.appendChild(self.document.createTextNode(""))
        add_to.appendChild(y)

    def add_resize_script(self):
        pass

    def add_timeline(self, t):
        pass

    def add_about(self, t):
        pass

    def dump(self):
        page = self.document.documentElement.toprettyxml(indent="  ", encoding=None)
        page = page.replace("&quot;","\"")
        page = page.replace("&lt;", "<")
        page = page.replace("&gt;", ">")

        with open(self.out_fn, "w") as out:
            out.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n")
            out.write(page)


class MainPage(TemplateDoc):
    def __init__(self):
        TemplateDoc.__init__(self, "template.xhtml", "index.html")
        self.container = self.document.getElementById("content")
        self.recent = self.document.getElementById("recent-contents")

    def add_resize_script(self):
        scr = """
function resize() {
    const fh = Math.min(1000, 0.8 * window.innerWidth);
    const ft = Math.min(180, 0.3 * window.innerWidth);
    document.getElementById("heading").setAttribute("style", "font-size: " + fh + "%");
    document.getElementById("tagline").setAttribute("style", "font-size: " + ft + "%");

    let lm =  Math.min(62, window.innerWidth / 24.0);
    let rm = window.innerWidth / 24.0
    const m = (window.innerWidth / 2) - 640;
    if (m > 0) {
        lm += m;
        rm += m;
    }
    ["recent-contents", "flickr"].forEach(id => {
        document.getElementById(id).setAttribute("style", "margin-left:" + lm + "px;");
    });
    document.getElementById("links").setAttribute("style", "margin-right:" + rm + "px; margin-left:" + lm + "px;");
    const pxRatio = Math.max(1.0, window.devicePixelRatio * 0.7);
    Array.from(document.getElementsByClassName("when")).forEach(t => {
        t.setAttribute("style", "font-size: " + (150 * pxRatio) + "%");
    });
    Array.from(document.getElementsByClassName("post-heading")).forEach(t => {
        t.setAttribute("style", "font-size: " + (150 * pxRatio) + "%");
    });
    Array.from(document.getElementsByClassName("post-text")).forEach(t => {
        t.setAttribute("style", "font-size: " + (100 * pxRatio) + "%");
    });
}
resize();
window.onresize = resize;
"""

        script = self.document.getElementsByTagName("script")[0]
        script.appendChild(self.document.createTextNode(scr))

    def add_timeline(self, t):
        if self.recent is not None and len(self.recent.childNodes) < 5:
            d = self.document.createElement("div")
            a = self.document.createElement("a")
            a.setAttribute("href", "#%s" % t["when"])
            a.appendChild(self.document.createTextNode(t["heading"]))

            d.appendChild(a)
            self.recent.appendChild(d)

        row = self.document.createElement("div")
        row.setAttribute("class", "content-item")
        head = self.document.createElement("div")
        head.setAttribute("class", "content-header")
        body = self.document.createElement("div")
        body.setAttribute("class", "content-main")
        
        h = self.document.createElement("div")
        h.setAttribute("class", "post-heading")
        h.appendChild(self.document.createTextNode(t["heading"]))

        when = self.document.createElement("div")
        when.setAttribute("class", "when")
        if "when" in t:
            w = datetime.datetime.strptime(t["when"], "%Y-%m-%d").strftime('%d %b %Y')
            whenAnchor = self.document.createElement("a")
            whenAnchor.appendChild(self.document.createTextNode(w))
            whenAnchor.setAttribute("id", t["when"])
            when.appendChild(whenAnchor)
        else:
            when.appendChild(self.document.createTextNode(""))

        head.appendChild(when)
        head.appendChild(h)

        i = self.document.createElement("div")
        
        if "youtube" in t:
            self._add_yt_to(i, t, 1.0)
            i.setAttribute("class", "post-image")

        elif "image" in t:
            landscape = t["orientation"] != "portrait" if "orientation" in t else True;
            img = self.document.createElement("img")
            img.setAttribute("src", t["image"])
            img.setAttribute("width", str(320
 if landscape else 180))
            img.setAttribute("height", str(320 if not landscape else 180))

            a = self.document.createElement("a")
            imageId = t["image"].split("/")[-1].split("_")[0]
            a.setAttribute("href", "https://flickr.com/photos/90938695@N06/%s/in/album-72157716077356826/" % imageId)
            a.setAttribute("target", "_blank")
            a.appendChild(img)

            i.setAttribute("class", "post-image")
            i.appendChild(a)

        body.appendChild(i)

        txt = self.document.createElement("div")
        txt.appendChild(self.document.createTextNode(t["text"]))
        txt.setAttribute("class", "post-text")
        body.appendChild(txt)

        row.appendChild(head)
        row.appendChild(body)
        self.container.appendChild(row)


class PortfolioPage(TemplateDoc):
    def __init__(self):
        TemplateDoc.__init__(self, "template-portfolio.xhtml", "portfolio.html")
        self.container = self.document.getElementById("timeline")

    def add_timeline(self, t):
        if "youtube" in t:
            item = self.document.createElement("div")
            item.setAttribute("class", "post-yt")
            self._add_yt_to(item, t, 1.3)
            self.container.appendChild(item)

    def add_resize_script(self):
        pass


class AboutPage(TemplateDoc):
    def __init__(self):
        TemplateDoc.__init__(self, "about.xhtml", "about.html")
        self.container = self.document.getElementById("content")
        self.recent = None

    def add_about(self, t):
        MainPage.add_timeline(self, t)

    def add_resize_script(self):
        scr = """
function resize() {
    let lm =  Math.min(62, window.innerWidth / 24.0);
    let rm = window.innerWidth / 24.0
    const m = (window.innerWidth / 2) - 640;
    if (m > 0) {
        lm += m;
        rm += m;
    }

    document.getElementById("links").setAttribute("style", "margin-right:" + rm + "px; margin-left:" + lm + "px;");
    const pxRatio = Math.max(1.0, window.devicePixelRatio * 0.7);
    Array.from(document.getElementsByClassName("when")).forEach(t => {
        t.setAttribute("style", "font-size: " + (150 * pxRatio) + "%");
    });
    Array.from(document.getElementsByClassName("post-heading")).forEach(t => {
        t.setAttribute("style", "font-size: " + (150 * pxRatio) + "%");
    });
    Array.from(document.getElementsByClassName("post-text")).forEach(t => {
        t.setAttribute("style", "font-size: " + (100 * pxRatio) + "%");
    });
}
resize();
window.onresize = resize;
"""
        script = self.document.getElementsByTagName("script")[0]
        script.appendChild(self.document.createTextNode(scr))


pages = [MainPage(), PortfolioPage(), AboutPage()]

for i in ["timeline", "about"]:
    jf = open(f"{i}.js", "r")
    jfc = json.load(jf)
    jf.close()

    for j in jfc:
        for p in pages:
            getattr(p, f"add_{i}")(j)

for p in pages:
    p.add_resize_script()
    p.dump()

