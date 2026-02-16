import lunisolar from './lunisolar/lunisolar.esm.js';

// 设置全局使用中文
const locale = import('https://unpkg.com/lunisolar/locale/zh-cn.js');
lunisolar.locale(locale.default);

// 引入节日
import { festivals } from './lunisolar/festivals.js';
lunisolar.Markers.add(festivals, "自定义节日")

// 格式化
function formatNum(num){
    return String(num).padStart(2, '0')
}

// 更新农历
function updateLunar(now) {
    let lunarTime = now.format('cYcZ年 lMlD lH时').replace(/十二月/g, "腊月");;

    if(now.solarTerm != null){
        lunarTime = lunarTime + " " + now.solarTerm.toString();
    }
     
    const festival = now.markers.toString()
    if(festival != "") {
        lunarTime = lunarTime + " " + festival;
    }

    document.getElementById('lunar-info').textContent = lunarTime;
}

// 更新公历
function updateDate(now) {

    const week = '日一二三四五六';

    const nowDay = now.toDate();
    const firstDay = new Date(now.year, 0, 1);
    const offset = lunisolar(firstDay).dayOfWeek-1; // 偏移量，因为如果1月1号不是周一就会有误差

    const allDays = Math.floor((nowDay - firstDay) / 86400000) + 1;
    const weekNum = Math.ceil((allDays+offset) / 7);

    const dateTime = `${now.year}年${formatNum(now.month)}月${formatNum(now.day)}日星期${week[now.dayOfWeek]} 第${weekNum}周`

    document.getElementById('date-info').textContent = dateTime;
}

// 更新钟点
function updateClock(now) {

    const hour = String(now.hour).padStart(2, '0');
    const minute = String(now.minute).padStart(2, '0');
    const second = String(now.second).padStart(2, '0');

    const clock = `${hour}:${minute}:${second}`;

    document.getElementById('clock').textContent = clock;
}

function run() {
    const now = lunisolar(lunisolar());
    updateLunar(now);
    updateDate(now);
    updateClock(now);
}

document.addEventListener('DOMContentLoaded', () => {
    run();
    setInterval(run, 100);
});