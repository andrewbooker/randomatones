function sizeFonts() {
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
