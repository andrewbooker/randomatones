function sizeFonts() {
    const pxRatio = (function() {
        if (window.devicePixelRatio === 1.0) {
            return 1.0;
        }
        const isHorizontal = (window.innerWidth / window.innerHeight) > 1.0;
        return (isHorizontal ? 0.5 : 1.0) * Math.max(1.0, window.devicePixelRatio * 0.7);
    })();

    const ratios = {
        "when": 150,
        "post-heading": 150,
        "post-text": 100,
        "previous-year": 100,
        "current-year": 100
    };
    Object.entries(ratios).forEach(([c, r]) => {
        Array.from(document.getElementsByClassName(c)).forEach(t => {
            t.setAttribute("style", "font-size: " + (r * pxRatio) + "%");
        });
    });
}

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
        const e = get(id);
        if (e) {
            e.setAttribute("style", "margin-left:" + (lm + lmOffset) + "px;");
        }
    });
}
