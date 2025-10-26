function resize() {
    const lm =  Math.max(10, (window.innerWidth * 0.3) - (302 + (18 * 2)));
    new Resize(lm, {
        "content-by-year": (i) => document.getElementById(i),
        "h1": (t) => document.getElementsByTagName(t)[0]
    }, 20).margins().fonts().render();
}
