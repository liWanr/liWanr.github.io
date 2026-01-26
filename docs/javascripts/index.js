(function() {
    function updateClock() {
        const now = new Date();
        const clockEl = document.getElementById('clock');
        if (clockEl) clockEl.textContent = now.toTimeString().split(' ')[0];

        const dateEl = document.getElementById('date-info');
        if (dateEl) {
            const w = ["日", "一", "二", "三", "四", "五", "六"][now.getDay()];
            const d = new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
            d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
            const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
            const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
            dateEl.textContent = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 星期${w} 第${weekNo}周`;
        }
        
        const lunarEl = document.getElementById('lunar-info');
        if (lunarEl) lunarEl.textContent = "乙巳蛇年 腊月初八"; 
    }

    function initSearch() {
        const bar = document.querySelector('.search-bar');
        if (!bar) return;
        const ul = bar.querySelector('ul');
        if (!ul) return;

        const firstA = ul.querySelector('a');
        let currentUrl = firstA ? firstA.href : '';
        const getIcon = (el) => el.querySelector('svg') ? el.querySelector('svg').outerHTML : '';

        const trigger = document.createElement('div');
        trigger.className = 'engine-trigger';
        trigger.innerHTML = `<div id="cur-icon-box">${getIcon(firstA)}</div><span style="font-size:8px;margin-left:6px;opacity:0.4">▼</span>`;

        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'real-input';
        input.placeholder = '搜索...';
        input.spellcheck = false;

        const btn = document.createElement('div');
        btn.className = 'go-btn';
        btn.innerHTML = `<svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"></path></svg>`;

        bar.prepend(trigger);
        bar.insertBefore(input, ul);
        bar.appendChild(btn);

        // 核心修改：使用 setProperty 覆盖 CSS 的 !important 隐藏
        trigger.onclick = (e) => {
            e.stopPropagation();
            const isHidden = window.getComputedStyle(ul).display === 'none';
            if (isHidden) {
                ul.style.setProperty('display', 'block', 'important');
            } else {
                ul.style.setProperty('display', 'none', 'important');
            }
        };

        ul.querySelectorAll('a').forEach(a => {
            a.onclick = (e) => {
                e.preventDefault();
                currentUrl = a.href;
                document.getElementById('cur-icon-box').innerHTML = getIcon(a);
                ul.style.setProperty('display', 'none', 'important');
                input.focus();
            };
        });

        const execSearch = () => {
            const val = input.value.trim();
            if (val) {
                window.open(currentUrl + encodeURIComponent(val), '_blank');
                input.value = '';
            }
        };

        input.onkeypress = (e) => { if (e.key === 'Enter') execSearch(); };
        btn.onclick = execSearch;
        document.addEventListener('click', () => { 
            ul.style.setProperty('display', 'none', 'important'); 
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        updateClock();
        setInterval(updateClock, 1000);
        initSearch();
    });
})();