function resize() {
    let lm =  Math.max(10, (window.innerWidth * 0.3) - (302 + (18 * 2)));
    let rm = window.innerWidth / 24.0
    const m = (window.innerWidth / 2) - 640;
    if (m > 0) {
        rm += m;
    }

    sizeMargins(lm, rm, {
        "content-by-year": (i) => document.getElementById(i),
        "h1": (t) => document.getElementsByTagName(t)[0]
    }, 20);
    sizeFonts();
}
