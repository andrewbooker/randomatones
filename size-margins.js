

function sizeMargins(lm, rm, lmOnlyItems, lmOffset) {
    document.getElementById("links").setAttribute("style", "margin-right:" + rm + "px; margin-left:" + lm + "px;");
    Object.entries(lmOnlyItems).forEach(([id, get]) => {
        get(id).setAttribute("style", "margin-left:" + (lm + lmOffset) + "px;");
    });
}
