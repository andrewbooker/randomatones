#!/bin/bash
#sudo apt install xmlstarlet

wget -O image.html $1
echo '<details>' > image.xml
grep 'meta property="og:image"' image.html >> image.xml
echo '</meta>' >> image.xml
grep 'meta property="og:title"' image.html >> image.xml
echo '</meta>' >> image.xml
echo '</details>' >> image.xml
imgUrl=$(xmlstarlet sel -t -v '//details/meta[@property="og:image"]/@content' image.xml)
imgDate=$(echo $(xmlstarlet sel -t -v '//details/meta[@property="og:title"]/@content' image.xml) | sed -E 's/.*(20[0-9]{6}).*/\1/' | sed -E 's/([0-9]{4})([0-9]{2})([0-9]{2})/\1-\2-\3/')

echo "{\"when\":\"${imgDate}\",\"heading\":\"\",\"image\":\"$imgUrl\",\"text\":\"\"}" | jq .

rm image.html
rm image.xml
