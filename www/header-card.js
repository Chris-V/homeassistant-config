class HeaderCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: 'open'});
    }

    set hass(hass) {
        this._hass = hass;

        if (!this.hasRendered()) {
            this.render();
        }
    }

    setConfig(config) {
        if (!config.title) {
            this._config = undefined;
            throw new Error('You need to define a title');
        }

        this._config = config;
        this.render();
    }

    render() {
        const root = this.shadowRoot;
        while (root.hasChildNodes()) {
            root.removeChild(root.lastChild);
        }

        if (!this._config || !this._hass) {
            return;
        }

        const header = document.createElement("div");
        header.className = "header";
        header.style = `
            font-family: var(--paper-font-headline_-_font-family);
            -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing);
            font-size: var(--paper-font-headline_-_font-size);
            font-weight: var(--paper-font-headline_-_font-weight);
            letter-spacing: var(--paper-font-headline_-_letter-spacing);
            line-height: var(--paper-font-headline_-_line-height);
            text-rendering: var(--paper-font-common-expensive-kerning_-_text-rendering);
            color: var(--primary-text-color);
            padding: 24px 16px 12px 16px;
            display: flex;
            justify-content: space-between;  
        `;
        header.innerHTML = `<div class="name">${this._config.title}</div>`;

        if (this._config.entities) {
            const toggle = document.createElement('hui-entities-toggle');
            toggle.hass = this._hass;
            toggle.entities = Array.isArray(this._config.entities) ? this._config.entities : [this._config.entities];

            header.appendChild(toggle);
        }

        root.appendChild(header);
    }

    hasRendered() {
        return this.shadowRoot.hasChildNodes();
    }

    getCardSize() {
        return 1;
    }
}

customElements.define('header-card', HeaderCard);
