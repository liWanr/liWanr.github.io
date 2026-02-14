// ============================================
// 性能优化版本（使用立即执行函数）
// ============================================

(function() {
    'use strict';
    
    // 并行加载依赖
    const modules = Promise.all([
        import('./lunisolar/lunisolar.esm.js'),
        import('./lunisolar/festivals.js'),
        import('./lunisolar/zh-cn.js')
    ]);
    
    // 常量
    const formatNum = num => String(num).padStart(2, '0');
    const WEEK_CHARS = '日一二三四五六';
    const MS_PER_DAY = 86400000;
    
    // DOM 缓存
    let lunar, date, clock;
    
    // 更新函数
    const updateLunar = (lunisolar, now) => {
        let text = now.format('cYcZ年 lMlD lH时').replace(/十二月/g, "腊月");
        if (now.solarTerm) text += ` ${now.solarTerm}`;
        const festival = now.markers.toString();
        if (festival) text += ` ${festival}`;
        lunar.textContent = text;
    };
    
    const updateDate = (lunisolar, now) => {
        let text = now.format('YYYY年MM月DD日ddd');

        const firstDay = new Date(now.year, 0, 1);
        const offset = lunisolar(firstDay).dayOfWeek - 1;
        const daysPassed = Math.floor((now.toDate() - firstDay) / MS_PER_DAY) + 1;
        const weekNum = Math.ceil((daysPassed + offset) / 7);
        
        date.textContent = `${text} 第${weekNum}周`;
        // date.textContent = text;
    };
    
    const updateClock = (lunisolar) => {
        const now = lunisolar();

        const time = `${formatNum(now.hour)}:${formatNum(now.minute)}:${formatNum(now.second)}`;
        
        if (now.hour % 2 === 1 && now.minute === 0 && now.second === 0) {
            updateLunar(lunisolar, now);
        }
        else if (time === "00:00:00") {
            updateDate(lunisolar, now);
        }
        
        clock.textContent = time;
    };
    
    // 初始化
    const init = async () => {
        try {
            const [{ default: lunisolar }, { festivals }] = await modules;
            
            lunisolar.locale(lunisolarLocaleZhCn);
            lunisolar.Markers.add(festivals, "自定义节日");
            
            lunar = document.getElementById('lunar-info');
            date = document.getElementById('date-info');
            clock = document.getElementById('clock');
            
            if (!lunar || !date || !clock) {
                throw new Error('Required DOM elements not found');
            }
            
            const now = lunisolar();
            updateLunar(lunisolar, now);
            updateDate(lunisolar, now);
            updateClock(lunisolar);
            
            setInterval(() => updateClock(lunisolar), 1000);
            
        } catch (error) {
            console.error('Init failed:', error);
        }
    };
    
    // 启动
    document.readyState === 'loading' 
        ? document.addEventListener('DOMContentLoaded', init)
        : init();
        
})();