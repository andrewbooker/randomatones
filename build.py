#!/usr/bin/python

from xml.dom import minidom
from xml.dom.minidom import Node
import json
import datetime
import sys
from random import randint


class TemplateDoc:
    def __init__(self, template_fn, out_fn):
        self.document = minidom.parse(f"templates/{template_fn}")
        self.out_fn = out_fn
        for n in self.document.getElementsByTagName("*"):
            if n.hasAttribute("id"):
                n.setIdAttribute("id")
        self.container = self.document.getElementById("content")

    def set_metadata(self, page_name=None, link_name=None):
        head = self.document.getElementsByTagName("head")[0]
        title = self.document.createElement("title")
        t = ["Randomatones"]
        if page_name is not None:
            t.append(page_name)
        title.appendChild(self.document.createTextNode(" | ".join(t)))
        head.appendChild(title)
        og_title = self.document.createElement("meta")
        og_title.setAttribute("property", "og:title")
        og_title.setAttribute("content", " | ".join(t))
        head.appendChild(og_title)

        u = ["http://randomatones.co.uk/", self.out_fn]
        og_url = self.document.createElement("meta")
        og_url.setAttribute("property", "og:url")
        og_url.setAttribute("content", "".join(u))
        head.appendChild(og_url)

        pages = self.document.getElementById("links")
        for p in [n for n in pages.childNodes if n.nodeType != Node.TEXT_NODE]:
            for link in [n for n in p.childNodes if n.nodeType != Node.TEXT_NODE]:
                a = link.getElementsByTagName("a")[0]
                label = a.firstChild.nodeValue
                if (link_name is None and label == "Home") or (label is not None and label == link_name):
                    link.removeChild(a)
                    h = self.document.createElement("h2")
                    h.appendChild(self.document.createTextNode(label))
                    link.appendChild(h)

    def _add_yt_to(self, add_to, yt_id, scale):
        y = self.document.createElement("iframe")
        y.setAttribute("width", str(int(302 * scale)))
        y.setAttribute("height", str(int(198 * scale)))
        y.setAttribute("allowfullscreen", "true")
        y.setAttribute("class", "iframe-yt")
        y.setAttribute("src", f"https://www.youtube.com/embed/{yt_id}?{randint(100000, 999999)}")
        y.appendChild(self.document.createTextNode(""))
        add_to.appendChild(y)

    def add_timeline(self, t):
        pass

    def add_about(self, t):
        pass

    def add_generations(self, t):
        pass

    def add_year(self, t):
        pass

    def add_content(self, t):
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

    def dump(self):
        page = self.document.documentElement.toxml(encoding=None)
        page = page.replace("&quot;","\"")
        page = page.replace("&lt;", "<")
        page = page.replace("&gt;", ">")

        with open(self.out_fn, "w") as out:
            out.write("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\">\n")
            out.write(page)


class MainPage(TemplateDoc):
    def __init__(self, currentYear):
        TemplateDoc.__init__(self, "template.xhtml", "index.html")
        self.set_metadata()
        self.recent = self.document.getElementById("recent-contents")
        self.years = dict()
        self.yearList = self.document.getElementById("content-by-year")
        self.currentYear = currentYear

    def add_year(self, t):
        if "when" in t:
            wd = t["when"]
            year = wd[:4]
            if year not in self.years:
                wasEmpty = len(self.years) == 0
                self.years[year] = wd
                if not wasEmpty:
                    yearLink = self.document.createElement("a")
                    yearLink.appendChild(self.document.createTextNode(year))
                    yearLink.setAttribute("href", f"{year}.html")
                    yearLink.setAttribute("class", "previous-year")
                    self.yearList.appendChild(yearLink)

    def add_timeline(self, t):
        if self.recent is not None and len(self.recent.childNodes) < 5:
            d = self.document.createElement("div")
            a = self.document.createElement("a")
            a.setAttribute("href", "#%s" % t["when"])
            a.appendChild(self.document.createTextNode(t["heading"]))

            d.appendChild(a)
            self.recent.appendChild(d)

        if int(t["when"][:4]) == self.currentYear or len(self.recent.childNodes) < 5:
            TemplateDoc.add_content(self, t)


class PortfolioPage(TemplateDoc):
    def __init__(self):
        TemplateDoc.__init__(self, "template-portfolio.xhtml", "portfolio.html")
        self.set_metadata("Portfolio", "Video portfolio")
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
            "6W2pAlF3pl8",   #armitage
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
        add_to = self.document.getElementById("timeline")
        if "youtube" in t:
            y = t["youtube"]
            if y not in {i for i, _ in self.postcard_items} and y not in self.omit_items:
                if self.feature:
                    if y == self.feature:
                        item = self.document.createElement("div")
                        item.setAttribute("class", "post-yt")
                        self._add_yt_to(item, t["youtube"], 3.2)
                        add_to.appendChild(item)
                else:
                    item = self.document.createElement("div")
                    item.setAttribute("class", "post-yt")
                    self._add_yt_to(item, t["youtube"], 1.3)
                    add_to.appendChild(item)


class AboutPage(TemplateDoc):
    def __init__(self):
        TemplateDoc.__init__(self, "template-common.xhtml", "about.html")
        self.set_metadata("About", "About")
        self.recent = None

    def add_about(self, t):
        TemplateDoc.add_content(self, t)


class GenerationPage(TemplateDoc):
    def __init__(self):
        TemplateDoc.__init__(self, "template-common.xhtml", "generations.html")
        self.set_metadata("Generations", "The many generations")
        self.recent = None

    def add_generations(self, t):
        TemplateDoc.add_content(self, t)


class YearPage(TemplateDoc):
    def __init__(self, year):
        TemplateDoc.__init__(self, "template-common.xhtml", f"{year}.html")
        self.recent = None
        self.year = year
        self.years = dict()
        self.yearList = self.document.getElementById("content-by-year")

    def add_year(self, t):
        if "when" in t:
            wd = t["when"]
            year = wd[:4]
            if year not in self.years:
                self.years[year] = wd
                if int(year) != self.year:
                    yearLink = self.document.createElement("a")
                    yearLink.appendChild(self.document.createTextNode(year))
                    yearLink.setAttribute("href", f"{year}.html")
                    yearLink.setAttribute("class", "previous-year")
                    self.yearList.appendChild(yearLink)
                else:
                    currentYear = self.document.createElement("p")
                    currentYear.appendChild(self.document.createTextNode(year))
                    currentYear.setAttribute("class", "current-year")
                    self.yearList.appendChild(currentYear)

    def add_timeline(self, t):
        if int(t["when"][:4]) == self.year:
            TemplateDoc.add_content(self, t)



currentYear = int(datetime.datetime.now().strftime("%Y"))
pages = [MainPage(currentYear), PortfolioPage(), AboutPage(), GenerationPage()]
for y in range(2020, currentYear + 1):
    pages.append(YearPage(y))

for i in ["timeline", "about", "generations"]:
    jf = open(f"content/{i}.json", "r")
    jfc = json.load(jf)
    jf.close()

    for j in jfc:
        for p in pages:
            getattr(p, f"add_{i}")(j)
            p.add_year(j)

for p in pages:
    p.dump()

