#!/bin/bash
#sudo apt install xmlstarlet

wget -O image.html $1
grep 'meta property="og:image"' image.html > image.xml
echo '</meta>' >> image.xml
echo $(xmlstarlet sel -t -v '//meta/@content' image.xml)
rm image.html
rm image.xml
