class Resize {
    constructor(leftMargin, lmOnlyItems, lmOffset) {
        this.lmOnlyItems = lmOnlyItems;
        this.lmOffset = lmOffset;
        this.styles = new Map();
        let lm = leftMargin;
        let rm = window.innerWidth / 24.0;
        const m = (window.innerWidth / 2) - 640;
        if (m > 0) {
            rm += m;
            if (lmOffset === 0) {
                lm += m;
            }
        }
        this.leftMargin = lm;
        this.rightMargin = rm;
    }

    setStyle(e, s) {
        if (!this.styles.has(e)) {
            this.styles.set(e, []);
        }
        (this.styles.has(e) ? this.styles.get(e) : this.styles.set(key, initialize()).get(key)).push(s);
    }

    margins() {
        this.setStyle(document.getElementById("links"), "margin-right:" + this.rightMargin.toFixed(2) + "px");
        this.setStyle(document.getElementById("links"), "margin-left:" + this.leftMargin.toFixed(2) + "px");
        Object.entries(this.lmOnlyItems).forEach(([id, get]) => {
            const e = get(id);
            if (e) {
                this.setStyle(e, "margin-left:" + (this.leftMargin + this.lmOffset).toFixed(2) + "px");
            }
        });
        return this;
    }

    fonts() {
        const pxRatio = (function() {
            if (window.devicePixelRatio === 1.0) {
                return 1.0;
            }
            const isHorizontal = (window.innerWidth / window.innerHeight) > 1.0;
            return Math.max(1.0, window.devicePixelRatio * 0.7 * (isHorizontal ? 0.5 : 1.0));
        })();

        const ratios = {
            "when": 150,
            "post-heading": 150,
            "post-text": 100,
            "previous-year": 100,
            "current-year": 100,
            "page-heading": 240
        };
        Object.entries(ratios).forEach(([c, r]) => {
            Array.from(document.getElementsByClassName(c)).forEach(t => {
                this.setStyle(t, "font-size: " + (r * pxRatio) + "%");
            });
        });
        return this;
    }

    render() {
        for (let [e, ss] of this.styles) {
            e.setAttribute("style", Array.from(ss).join("; "));
        }
    }
}
