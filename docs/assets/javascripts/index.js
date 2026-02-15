(function() {
    'use strict';

    let clockInterval = null;

    // 核心初始化逻辑
    async function init() {
        const clockEl = document.getElementById('clock');
        // 1. 如果页面上根本没有这个元素，直接退出，不浪费性能
        if (!clockEl) {
            if (clockInterval) clearInterval(clockInterval);
            return;
        }

        // 2. 如果已经加载过了（防止重复初始化），直接退出
        if (clockEl.dataset.initialized === 'true') return;

        try {
            // 动态加载依赖
            const [ls, fest, zh] = await Promise.all([
                import('./lunisolar/lunisolar.esm.js'),
                import('./lunisolar/festivals.js'),
                import('./lunisolar/zh-cn.js')
            ]);

            const lunisolar = ls.default;
            // 配置一次即可
            if (!window.lunarConfigured) {
                lunisolar.locale(lunisolarLocaleZhCn);
                lunisolar.Markers.add(fest.festivals, "自定义节日");
                window.lunarConfigured = true;
            }

            // 这里的获取 DOM 需要实时
            const lunarInfo = document.getElementById('lunar-info');
            const dateInfo = document.getElementById('date-info');
            
            const render = () => {
                const now = lunisolar();
                // 时间显示
                clockEl.textContent = `${String(now.hour).padStart(2, '0')}:${String(now.minute).padStart(2, '0')}:${String(now.second).padStart(2, '0')}`;
                
                // 仅在初始或特定时间更新日期和农历（优化性能）
                if (lunarInfo) {
                    let text = now.format('cYcZ年 lMlD lH时').replace(/十二月/g, "腊月");
                    if (now.solarTerm) text += ` ${now.solarTerm}`;
                    if (now.markers.toString()) text += ` ${now.markers.toString()}`;
                    lunarInfo.textContent = text;
                }
                if (dateInfo) {
                    dateInfo.textContent = now.format('YYYY年MM月DD日ddd');
                }
            };

            render();
            if (clockInterval) clearInterval(clockInterval);
            clockInterval = setInterval(render, 1000);
            
            // 标记已初始化
            clockEl.dataset.initialized = 'true';

        } catch (e) {
            console.error("Clock init error:", e);
        }
    }

    // --- 解决“点进页面不加载”的多重保险 ---

    // 1. 传统的加载完成
    if (document.readyState === 'complete') init();
    else window.addEventListener('load', init);

    // 2. Astro 专用的生命周期（万一它开了 View Transitions）
    document.addEventListener('astro:page-load', init);

    // 3. 暴力兜底：监听全局点击。如果点的是链接，等一会就检查 DOM
    document.addEventListener('click', (e) => {
        if (e.target.closest('a')) {
            setTimeout(init, 100); // 稍微延迟，等框架渲染完 DOM
            setTimeout(init, 500); // 双重确认
            setTimeout(init, 1000); 
        }
    });

    // 4. 监听后退/前进
    window.addEventListener('popstate', () => setTimeout(init, 200));

})();