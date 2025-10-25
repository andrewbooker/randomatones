function resize() {
    let lm =  Math.max(10, (window.innerWidth * 0.3) - (302 + (18 * 2)));
    let rm = window.innerWidth / 24.0
    const m = (window.innerWidth / 2) - 640;
    if (m > 0) {
        rm += m;
    }

    document.getElementsByTagName("h1")[0].setAttribute("style", "margin-right:" + rm + "px; margin-left:" + (lm + 20) + "px;");
    sizeMargins(lm, rm, ["content-by-year"], 20);
    sizeFonts();
}
