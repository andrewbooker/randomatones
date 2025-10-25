function sizeMargins(lm, rm, lmOnlyItems, lmOffset) {
    document.getElementById("links").setAttribute("style", "margin-right:" + rm + "px; margin-left:" + lm + "px;");
    lmOnlyItems.forEach(id => {
        document.getElementById(id).setAttribute("style", "margin-left:" + (lm + lmOffset) + "px;");
    });
}
