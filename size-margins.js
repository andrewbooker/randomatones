function sizeMargins(leftMargin, lmOnlyItems, lmOffset) {
    let lm = leftMargin;
    let rm = window.innerWidth / 24.0;
    const m = (window.innerWidth / 2) - 640;
    if (m > 0) {
        lm += m;
        rm += m;
    }
    document.getElementById("links").setAttribute("style", "margin-right:" + rm + "px; margin-left:" + lm + "px;");
    Object.entries(lmOnlyItems).forEach(([id, get]) => {
        get(id).setAttribute("style", "margin-left:" + (lm + lmOffset) + "px;");
    });
}
