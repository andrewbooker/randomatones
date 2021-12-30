from xml.dom import minidom
import json

tl = open("timeline.js", "r")
timeline = json.load(tl)
tl.close()

doc = minidom.parse("template.xhtml")
c = doc.getElementsByTagName("tbody")[0]

for t in timeline:
	row = doc.createElement("tr")
	h = doc.createElement("td")
	h.appendChild(doc.createTextNode(t["when"]))
	row.appendChild(h)
	c.appendChild(row)

print(c)
with open("out.html", "w") as out:
	out.write(doc.toprettyxml(indent="  "))
