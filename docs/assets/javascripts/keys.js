(function () {
    const init = () => {
        const $ = (s, c = document) => c.querySelector(s),
            box = $('[data-mdx-component="keysearch"]'),
            input = $('[data-mdx-component="keysearch-query"]');
        if (!input || !box) return;

        if (!$('#ks-style')) {
            document.head.insertAdjacentHTML('beforeend', `<style id="ks-style">.mdx-copy-target{transition:0.2s}:hover.mdx-copy-target{color:var(--md-accent-fg-color)!important;background:var(--md-accent-fg-color--transparent)!important}.mdx-search-results::-webkit-scrollbar{width:4px}.mdx-search-results::-webkit-scrollbar-thumb{background:var(--md-default-fg-color--lighter);border-radius:10px}:hover.mdx-search-results::-webkit-scrollbar-thumb{background:var(--md-accent-fg-color)</style>`);
        }

        let res = box.querySelector('.mdx-search-results') || box.appendChild(Object.assign(document.createElement('div'), {
            className: 'mdx-search-results md-typeset',
            style: 'max-height:330px;overflow-y:auto;border-bottom:1px solid var(--md-default-fg-color--lightest);scroll-behavior:smooth'
        }));

        // 使用事件委托，避免每次渲染重复绑定事件
        res.onclick = (e) => {
            const target = e.target.closest('.mdx-copy-target');
            if (target) navigator.clipboard.writeText(target.dataset.clipboardText);
        };

        let data = {};
        const t = $('script[src*="keys.js"]');
        fetch(t ? t.src.replace('.js', '.json') : '/json/keys.json').then(r => r.json()).then(d => data = d);

        const render = (val) => {
            const q = val.toLowerCase(), isSym = val.length === 1 && !/[a-z0-9]/i.test(val);
            res.innerHTML = Object.entries(data).map(([k, c]) => {
                const l = k.toLowerCase(), id = c[0];
                let w = l === q ? 100 : (id.startsWith('num') && k.replace(/^num/i, '').toLowerCase() === q) ? 95 : l.includes(q) ? 50 : (!isSym && c.some(v => v.toLowerCase().includes(q))) ? 10 : -1;
                return { k, c, id, w };
            }).filter(i => i.w > 0).sort((a, b) => b.w - a.w).map(({ k, c, id }) => `
                <div style="display:flex;align-items:center;padding:8px 20px;border-bottom:1px solid var(--md-default-fg-color--lightest);">
                    <div style="min-width:100px;flex-shrink:0;display:flex;justify-content:center;padding-right:10px;"><span class="keys"><kbd class="key-${id}">${k}</kbd></span></div>
                    <div style="display:flex;flex-wrap:wrap;align-items:center;flex:1;">
                        ${c.map(v => `<code style="cursor:pointer;margin-left:25px" data-clipboard-text="++${v}++" class="mdx-copy-target">++${v}++</code>`).join('')}
                    </div>
                </div>`).join('');
            res.scrollTop = 0;
        };

        input.oninput = () => { const v = input.value.trim(); v ? render(v) : res.innerHTML = ''; };
    };
    document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", init) : init();
})();