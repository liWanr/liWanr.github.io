(function () {
    const init = () => {
        const queryInput = document.querySelector('[data-mdx-component="keysearch-query"]');
        const box = document.querySelector('[data-mdx-component="keysearch"]');
        if (!queryInput || !box) return;

        const results = box.querySelector('.mdx-search-results') || (() => {
            const el = document.createElement('div');
            el.className = 'mdx-search-results md-typeset';
            // --- 新增：限制高度并允许滚动 ---
            // 假设单条高度约 55px，6条约为 330px
            Object.assign(el.style, {
                maxHeight: '330px',
                overflowY: 'auto',
                borderBottom: '1px solid var(--md-default-fg-color--lightest)',
                scrollBehavior: 'smooth'
            });
            return box.appendChild(el);
        })();

        let keyData = {};
        const sTag = document.querySelector('script[src*="keys.js"]');
        fetch(sTag ? sTag.src.replace('.js', '.json') : '/javascripts/keys/keys.json')
            .then(r => r.json()).then(d => keyData = d);

        const render = (val) => {
            const q = val.toLowerCase(), isSym = val.length === 1 && !/[a-z0-9]/i.test(val);
            const matches = Object.entries(keyData).map(([key, codes]) => {
                const lowKey = key.toLowerCase(), id = codes[0];
                let w = lowKey === q ? 100 
                        : (id.startsWith('num') && key.replace(/^num/i, '').toLowerCase() === q) ? 95 
                        : lowKey.includes(q) ? 50 
                        : (!isSym && codes.some(c => c.toLowerCase().includes(q))) ? 10 : -1;
                return { key, codes, id, w };
            }).filter(m => m.w > 0).sort((a, b) => b.w - a.w);

            if (!matches.length) return results.innerHTML = '';

            results.innerHTML = matches.map(({ key, codes, id }) => `
                <div style="display:flex; align-items:center; padding:12px 20px; border-bottom:1px solid var(--md-default-fg-color--lightest);">
                    <div style="min-width:100px; flex-shrink:0; display:flex; justify-content:center; padding-right:10px;">
                        <span class="keys"><kbd class="key-${id}">${key}</kbd></span>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; align-items:center; flex:1;">
                        ${codes.map(c => `<code style="cursor:pointer; margin-left:25px;" data-clipboard-text="++${c}++" class="mdx-copy-target">++${c}++</code>`).join('')}
                    </div>
                </div>`).join('');

            // 每次渲染后让滚动条回到顶部
            results.scrollTop = 0;

            results.querySelectorAll('.mdx-copy-target').forEach(el => {
                el.onclick = () => {
                    navigator.clipboard.writeText(el.getAttribute('data-clipboard-text')).then(() => {
                        el.style.opacity = "0.4";
                        setTimeout(() => { el.style.opacity = "1"; }, 150);
                    });
                };
            });
        };

        queryInput.oninput = () => {
            const v = queryInput.value.trim();
            v ? render(v) : results.innerHTML = '';
        };
    };

    document.readyState === "loading" ? document.addEventListener("DOMContentLoaded", init) : init();
})();