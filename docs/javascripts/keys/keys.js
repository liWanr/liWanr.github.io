(function () {
    const init = () => {
        const $ = (s, ctx = document) => ctx.querySelector(s),
            box = $('[data-mdx-component="keysearch"]'),
            input = $('[data-mdx-component="keysearch-query"]');
        if (!input || !box) return;

        if (!$('#ks-style')) {
            const s = document.createElement('style');
            s.id = 'ks-style';
            s.innerHTML = `.mdx-copy-target{transition:0.2s}:hover.mdx-copy-target{color:var(--md-accent-fg-color)!important;background:var(--md-accent-fg-color--transparent)!important}.mdx-search-results::-webkit-scrollbar{width:4px}.mdx-search-results::-webkit-scrollbar-thumb{background:var(--md-default-fg-color--lighter);border-radius:10px}:hover.mdx-search-results::-webkit-scrollbar-thumb{background:var(--md-accent-fg-color)}`;
            document.head.append(s);
        }

        let res = box.querySelector('.mdx-search-results') || (() => {
            const el = Object.assign(document.createElement('div'), { className: 'mdx-search-results md-typeset' });
            Object.assign(el.style, { maxHeight: '330px', overflowY: 'auto', borderBottom: '1px solid var(--md-default-fg-color--lightest)', scrollBehavior: 'smooth' });
            return box.appendChild(el);
        })();

        let data = {};
        const t = $('script[src*="keys.js"]');
        fetch(t ? t.src.replace('.js', '.json') : '/javascripts/keys/keys.json').then(r => r.json()).then(d => data = d);

        const render = (val) => {
            const q = val.toLowerCase(), isSym = val.length === 1 && !/[a-z0-9]/i.test(val);
            const m = Object.entries(data).map(([k, c]) => {
                const l = k.toLowerCase(), id = c[0];
                let w = l === q ? 100 : (id.startsWith('num') && k.replace(/^num/i, '').toLowerCase() === q) ? 95 : l.includes(q) ? 50 : (!isSym && c.some(v => v.toLowerCase().includes(q))) ? 10 : -1;
                return { k, c, id, w };
            }).filter(i => i.w > 0).sort((a, b) => b.w - a.w);

            res.innerHTML = m.map(({ k, c, id }) => `
                <div style="display:flex;align-items:center;padding:8px 20px;border-bottom:1px solid var(--md-default-fg-color--lightest);">
                    <div style="min-width:100px;flex-shrink:0;display:flex;justify-content:center;padding-right:10px;"><span class="keys"><kbd class="key-${id}">${k}</kbd></span></div>
                    <div style="display:flex;flex-wrap:wrap;align-items:center;flex:1;">
                        ${c.map(v => `<code style="cursor:pointer;margin-left:25px" data-clipboard-text="++${v}++" class="mdx-copy-target">++${v}++</code>`).join('')}
                    </div>
                </div>`).join('');
            res.scrollTop = 0;

            // 保持 data-clipboard-text 属性，MkDocs 监听器会自动处理复制弹窗
            res.querySelectorAll('.mdx-copy-target').forEach(e => {
                e.onclick = () => navigator.clipboard.writeText(e.getAttribute('data-clipboard-text'));
            });
        };

        input.oninput = () => { const v = input.value.trim(); v ? render(v) : res.innerHTML = ''; };
    };
    document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", init) : init();
})();