class Resize {
    constructor(leftMargin, lmOnlyItems, lmOffset) {
        this.leftMargin = leftMargin;
        this.lmOnlyItems = lmOnlyItems;
        this.lmOffset = lmOffset;
        this.styles = new Map();
    }

    setStyle(e, s) {
        if (!this.styles.has(e)) {
            this.styles.set(e, []);
        }
        (this.styles.has(e) ? this.styles.get(e) : this.styles.set(key, initialize()).get(key)).push(s);
    }

    margins() {
        let lm = this.leftMargin;
        let rm = window.innerWidth / 24.0;
        const m = (window.innerWidth / 2) - 640;
        if (m > 0) {
            lm += m;
            rm += m;
        }
        this.setStyle(document.getElementById("links"), "margin-right:" + rm + "px");
        this.setStyle(document.getElementById("links"), "margin-left:" + lm + "px;");
        Object.entries(this.lmOnlyItems).forEach(([id, get]) => {
            const e = get(id);
            if (e) {
                this.setStyle(e, "margin-left:" + (lm + this.lmOffset) + "px;");
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
