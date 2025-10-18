function resize() {
    let lm =  Math.max(10, (window.innerWidth * 0.3) - (302 + (18 * 2)));
    let rm = window.innerWidth / 24.0
    const m = (window.innerWidth / 2) - 640;
    if (m > 0) {
        rm += m;
    }

    document.getElementById("links").setAttribute("style", "margin-right:" + rm + "px; margin-left:" + lm + "px;");
    document.getElementsByTagName("h1")[0].setAttribute("style", "margin-right:" + rm + "px; margin-left:" + (lm + 20) + "px;");
    ["content-by-year"].forEach(id => {
        document.getElementById(id).setAttribute("style", "margin-left:" + (lm + 20) + "px;");
    });
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
