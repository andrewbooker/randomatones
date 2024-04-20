#!/usr/bin/python

import json

def yt_ref(i, h):
    return f"Randomatones video ({h}): https://www.youtube.com/watch?v={i}"

tl = open("timeline.js", "r")
timeline = json.load(tl)
tl.close()

tubes = []
for t in timeline:
    if "youtube" in t:
        yt_id = t["youtube"]
        tubes.append((yt_id, t["heading"]))

for i in range(len(tubes)):
    yt_id, heading = tubes[i]
    print("")
    print(heading)
    if i > 0:
        print("Next", yt_ref(*tubes[i - 1]))
    if i < len(tubes) - 1:
        print("Previous", yt_ref(*tubes[i + 1]))

