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

    def _add_yt_to(self, add_to, yt_id, scale):
        y = self.document.createElement("iframe")
        y.setAttribute("width", str(int(302 * scale)))
        y.setAttribute("height", str(int(198 * scale)))
        y.setAttribute("allowfullscreen", "true")
        y.setAttribute("class", "iframe-yt")
        y.setAttribute("src", f"https://www.youtube.com/embed/{yt_id}?{randint(100000, 999999)}")
        y.appendChild(self.document.createTextNode(""))
        add_to.appendChild(y)

    def add_common_style(self):
        for s in self.document.getElementsByTagName("style"):
            for p in s.childNodes:
                p.nodeValue += "a:link { color: dodgerblue; }\na:visited { color: mediumslateblue; }\n"

    def add_resize_script(self):
        scr = """
function resize() {
    let lm =  Math.max(10, (window.innerWidth * 0.3) - (302 + (18 * 2)));
    let rm = window.innerWidth / 24.0
    const m = (window.innerWidth / 2) - 640;
    if (m > 0) {
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

    def add_timeline(self, t):
        pass

    def add_about(self, t):
        pass

    def add_generations(self, t):
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
        self.years = dict()
        self.yearList = self.document.getElementById("content-by-year")

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
    ["recent-contents", "content-by-year"].forEach(id => {
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
            wd = t["when"]
            w = datetime.datetime.strptime(wd, "%Y-%m-%d").strftime("%d %b %Y")
            whenAnchor = self.document.createElement("a")
            whenAnchor.appendChild(self.document.createTextNode(w))
            whenAnchor.setAttribute("id", wd)
            when.appendChild(whenAnchor)
            year = wd[:4]
            if year not in self.years:
                wasEmpty = len(self.years) == 0
                self.years[year] = wd
                if not wasEmpty:
                    yearLink = self.document.createElement("a")
                    yearLink.appendChild(self.document.createTextNode(year))
                    yearLink.setAttribute("href", f"#{wd}")
                    yearLink.setAttribute("class", "previous-year")
                    self.yearList.appendChild(yearLink)
        else:
            when.appendChild(self.document.createTextNode(""))

        head.appendChild(when)
        head.appendChild(h)

        i = self.document.createElement("div")
        
        if "youtube" in t:
            self._add_yt_to(i, t["youtube"], 1.0)
            i.setAttribute("class", "post-image")

        elif "image" in t:
            landscape = t["orientation"] != "portrait" if "orientation" in t else True;
            img = self.document.createElement("img")
            img.setAttribute("src", t["image"])
            w = 320 if landscape else 180
            if "image-width" in t:
                w = int(t["image-width"])
            img.setAttribute("width", str(w))
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
        self.postcard = self.document.getElementById("postcard")
        self.postcard_items = [
            ("C7SRY2J_L6c", "53795150323_693d6768b7"),
            ("PmSZrsthFks", "53795241979_b0e61dd7f7"),
            ("k2WSEi149CM", "53794930691_7fe02bc0dc"),
            ("-Iec5qIazRc", "53795241949_051ecc1248")
        ]
        self.feature = "8jH8vtE1S_Q"
        self.omit_items = {
            "eIS7tWrvk-c",   #pumpkin
            "6W2pAlF3pl8",   #armitage,
            "2xTeApzjrQM",   #mcr2
            "7F-Sw6fVl0I",   #mcr1
            "jL1AqcHteug",   #sapperton
            "Ijo-B0MvH2w",   #mimmshall
            "hvtv9qaenxo",   #bow flyover
            "RBprgrceOII",   #curzon
            "_sodYEzFBB0",   #leicester
            "sFGq1ZAaaPE",   #heart of noise
            "3FMnYXOUaEg",   #highams pk
            "sBHxgcOxsO8",   #walthamstow marshians
        }

        item = None
        for i in range(0, 4):            
            a = self.document.createElement("a")
            y, f = self.postcard_items[i]
            if item is None or i % 2 == 0:
                item = self.document.createElement("div")
                item.setAttribute("class", "postcard-row")
                self.postcard.appendChild(item)
            
            item.appendChild(a)
            a.setAttribute("href", f"https://www.youtube.com/watch?v={y}")
            a.setAttribute("target", "_blank")
            img = self.document.createElement("img")
            img.setAttribute("src", f"https://live.staticflickr.com/65535/{f}_b.jpg")
            img.setAttribute("width", "480")
            img.setAttribute("height", "270")
            img.setAttribute("class", "postcard-img")
            a.appendChild(img)

    def add_timeline(self, t):
        if "youtube" in t:
            y = t["youtube"]
            if y not in {i for i, _ in self.postcard_items} and y not in self.omit_items:
                if self.feature:
                    if y == self.feature:
                        item = self.document.createElement("div")
                        item.setAttribute("class", "post-yt")
                        self._add_yt_to(item, t["youtube"], 3.2)
                        self.container.appendChild(item)    
                else:
                    item = self.document.createElement("div")
                    item.setAttribute("class", "post-yt")
                    self._add_yt_to(item, t["youtube"], 1.3)
                    self.container.appendChild(item)


class AboutPage(TemplateDoc):
    def __init__(self):
        TemplateDoc.__init__(self, "template-about.xhtml", "about.html")
        self.container = self.document.getElementById("content")
        self.recent = None

    def add_about(self, t):
        MainPage.add_timeline(self, t)


class GenerationPage(TemplateDoc):
    def __init__(self):
        TemplateDoc.__init__(self, "template-generations.xhtml", "generations.html")
        self.container = self.document.getElementById("content")
        self.recent = None

    def add_generations(self, t):
        MainPage.add_timeline(self, t)



pages = [MainPage(), PortfolioPage(), AboutPage(), GenerationPage()]
for i in ["timeline", "about", "generations"]:
    jf = open(f"{i}.js", "r")
    jfc = json.load(jf)
    jf.close()

    for j in jfc:
        for p in pages:
            getattr(p, f"add_{i}")(j)

for p in pages:
    p.add_common_style()
    p.add_resize_script()
    p.dump()

