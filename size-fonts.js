function sizeFonts() {
    const pxRatio = Math.max(1.0, window.devicePixelRatio * 0.7);
    const ratios = {
        "when": 150,
        "post-heading": 150,
        "post-text": 100
    };
    Object.entries(ratios).forEach(([c, r]) => {
        Array.from(document.getElementsByClassName(c)).forEach(t => {
            t.setAttribute("style", "font-size: " + (r * pxRatio) + "%");
        });
    });
}
