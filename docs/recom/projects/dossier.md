---
icon: lucide/hat-glasses
title: 侦探事务所 · Dossier
# date:
    # created: 2026-06-03
    # updated: 2026-06-06
comments: true
rss: no
---

///html | small
把「爱因斯坦谜题」做成侦探剧情游戏，一次完整的"小游戏当大工程做"复盘。
///

///html | div.grid.cards

- **在线游玩**：[侦探事务所 · Dossier](https://Dossier.liWanr.vercel.app)

- **开源地址**：[liWanr/Dossier](https://github.com/liWanr/Dossier)

///

## 起源

如果你在网上见过这道题：

> 1. 英国人住在红房子里
> 2. 瑞典人养狗
> 3. 丹麦人喝茶
> 4. ……
> 5. **谁养斑马？谁喝水？**

这就是著名的「**爱因斯坦谜题**」（Zebra Puzzle）。一道朴素的逻辑题，没有任何数学知识，只靠**排除法 + 唯一可能性**，纯推理就能解出来。

最近就对这种题着迷，它的迷人之处在于：**每一步都有确定的对错**，没有模糊空间，但全局的解法要等你把所有线索串起来才能浮现。它跟数独像，但比数独有故事感。

## 玩法

- **简单**：4 个侦探，3 个其它类别（案件 / 证物 / 时间）
- **中等**：5 个侦探，4 个其它类别（+ 地点）
- **困难**：6 个侦探，5 个其它类别（+ 嫌疑人）

任务是根据右侧给出的 8 – 19 条线索，在左侧的逻辑网格里推出每个侦探对应的全套属性。

简单模式大概 3–5 分钟、中等 8–15 分钟、困难 20–40 分钟。每天三档共享同一个「世界观主题」，给推理过程一点叙事粘合剂。

## 主题

为了避免审美疲劳，我做了 **5 套主题包**：

| 主题 | 主角色 | 类别 | 调性 |
|---|---|---|---|
| 🕵️ 经典刑侦 | 侦探 | 案件 / 证物 / 嫌疑人 / 时间 / 地点 | 现代都市 |
| 🗡️ 古代刑名 | 捕快 | 案件 / 物证 / 嫌犯 / 时辰 / 坊市 | 古代衙门 |
| 🎒 校园悬案 | 推理社员 | 事件 / 物品 / 同学 / 时段 / 教室 | 轻松日常 |
| 🏴‍☠️ 海盗谜局 | 船长 | 任务 / 物证 / 嫌疑人 / 时段 / 海域 | 大航海冒险 |
| 🚀 太空惊魂 | 宇航员 | 事件 / 物证 / 嫌疑人 / 时段 / 舱段 | 科幻推理 |

每天按日期 hash 选一个主题，同一天三档共享世界观，避免上午做"古代捕快"下午跳"太空惊魂"这种割裂感。

线索文案每个主题独立：
- 经典：「连环纵火案的现场发现了神秘纸条」
- 古代：「钱庄盗银案的现场遗有可疑信笺」
- 海盗：「古地图争夺留下的关键物证是破旧海盗旗」
- 太空：「气闸故障的现场遗留了数据日志副本」

同一类关系（如"案件→证物"）每个主题还有 2 种句式变体，按日期种子随机选，所以即使是同一主题，不同日期的文案也不会一模一样。

## 技术细节

### AC-3 算法

「唯一解」是数学保证：题目数学上只能有一种解。

但「**推理可达**」是更强的承诺：玩家用人类常规的推理手法（排除法、唯一可能性、跨类传递…）一步步就能解出来，**不需要"假设错了反推回来"这种试错**。

这俩不等价。一道题可能数学唯一解，但需要"试一下假设"才能解开。

我用 **AC-3 约束传播算法** 作为生成器的核心校验：

```js
function ambiguousCount(clueList, N, M, timeCatIdx) {
  // 对每个 (类别, 实体) 维护一个候选位图
  // 反复传播 5 类规则直到收敛：
  //   1. naked single（格子里只剩 1 个候选 → 同行同列排除该值）
  //   2. hidden single（一行里只有 1 个格能放某值 → 那就是它）
  //   3. 正向跨类传递（A=B & B=C → A=C）
  //   4. 时序约束（X 早于 Y → X 的时间值要小于 Y）
  //   5. 时段范围（X 在下午 → 排除 X 在所有非下午的时间）
  // 返回剩余不确定的格子数；0 = 完全收敛 = 题可推
}
```

生成器只接受 `ambiguousCount === 0` 的线索集，因为传播规则跟人推理用的方法**逐条对应**：算法能纯传播解出，类就能纯推理解出。

### 多种子 + 多样性优选

生成器从成百上千条可能的线索里贪心挑选最小子集，让题目"刚好可解"。但同一个解可以被很多种不同的线索集编码：

- 13 条直接正向能解
- 8 条直接正向 + 2 条时段范围 + 1 条时序 + 2 条直接负向也能解

第二种显然更有趣，但贪心默认会偏向第一种（因为单条信息密度高）。

我加了两层优化：

1. **20+ 个随机种子**各跑一遍贪心，比较谁的线索集更短
2. **同长度时按多样性 tiebreaker**：能覆盖更多种线索类型（pos / neg / range / ord）的胜出

跑完后 1095 道题里只有 37 道是纯 `direct_positive`，其它都至少 2 种类型，比改之前从「大部分单调」降到 3.4%。

### 服务器时区门控

「每日一题」的核心承诺是：**今天的题只在今天能解锁**。原本的设计是客户端把 `?tz=Asia/Shanghai` 传给服务器，服务器在该时区下算"今天"。

测试自己工程时我发现一个洞，客户端可以传 `?tz=Pacific/Kiritimati`（UTC+14），服务器会以为玩家在地球上时间最早的地方，**提前 14 小时放出第二天的题**。整个"每日"概念瞬间失效。

修复方案：**服务器侧硬编码 `BASE_TZ = 'Asia/Shanghai'`，忽略客户端 tz 参数**。为了照顾海外用户，加 6 小时安全窗，这样美西玩家也能在他们的傍晚就拿到次日题，而不是要等到他们的次日早上。

```ts
const BASE_TZ = 'Asia/Shanghai';
const SAFETY_WINDOW_HOURS = 6;

export function latestPlayableDate(utcMs: number) {
  return todayInTimezone(utcMs + SAFETY_WINDOW_HOURS * 3600_000, BASE_TZ);
}
```

再加一个 `PUZZLE_MAX_DAYS_AHEAD=1` 的环境变量做防御纵深，即便上面的时区计算出 bug，API 也最多放出 today + 1 天的题，整年 1095 道题不会一次性泄漏。

### 数据存储

进度都存在浏览器 IndexedDB 里，刷新不丢，不需要登录。但要做得健壮：

**版本化迁移**：未来 schema 升级（比如加个"提示次数"字段）不能直接 `deleteDatabase` 清掉一年的贡献图。所以我写了一个迁移数组：

```ts
const migrations: Migration[] = [
  // v0 → v1: 初始 schema
  (db) => {
    if (!db.objectStoreNames.contains('history')) db.createObjectStore(...);
    if (!db.objectStoreNames.contains('gameStates')) db.createObjectStore(...);
  },
  // 未来 v1 → v2 在这里 append，绝对不 deleteObjectStore
];
```

### 跨标签同步

**多标签同步**：玩家可能在两个标签里同时开同一道题。用 `BroadcastChannel` 让一个标签写完后通知其它标签重新从 IndexedDB 读，避免静默互相覆盖。Safari < 15.4 没这个 API，所以做了 `localStorage` 的 `storage` 事件兜底。

**乐观锁**：每次写都带 version 号，事务内读+写，保证最近写入版本单调递增。

### 主题包架构

5 套主题如果硬编码在生成器里会很难维护。所以每个主题是一个独立模块：

```js
// scripts/themes/pirate.mjs
export const pirate = {
  id: 'pirate',
  label: '海盗谜局',
  pool: { captain: [...], case: [...], evidence: [...], ... },
  cats: { captain: { name: '船长', icon: '🏴‍☠️', prefix: 'd' }, ... },
  difficulties: {
    easy:   { n: 4, cats: ['captain','case','evidence','time'], desc: n => `...` },
    medium: { n: 5, cats: ['captain','case','evidence','time','location'], ... },
    hard:   { n: 6, cats: ['captain','case','suspect','evidence','time','location'], ... },
  },
  POS: {
    captain_case: [
      (a,b) => `${a}接下的就是${b}这趟差事`,
      (a,b) => `${b}的指挥旗在${a}的桅杆上`,
    ],
    // ... 15+ 种关系
  },
  NEG: { ... }, ORD: { ... }, RANGE: { ... },
};
```

生成器 `themeForDate(date)` 按日期 hash 选一个主题，然后照常跑算法。**加新主题只要再写一个文件 + append 到主题数组**，不用改生成器一行代码。

### 浅/暗色

Tailwind v4 + 内联引导脚本让暗色模式无闪烁：

```html
<script>
  // 在 React 挂载前就把 data-theme 写到 <html>
  // 否则深色用户会看到 200ms 的白色闪屏
  const pref = JSON.parse(localStorage.getItem('settings-v1') || '{}').theme;
  const resolved = pref === 'auto' || !pref
    ? (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
    : pref;
  document.documentElement.dataset.theme = resolved;
  document.documentElement.style.colorScheme = resolved;
</script>
```

`<html suppressHydrationWarning>` 让 React 不要把这种"客户端脚本在 hydration 前改 DOM"当作错误。

## 走过的坑

- **困难模式手机端单元格 38px** — 低于 Apple HIG 44px 最小点击区，玩家在 6 列里频繁误点。最后改成 44px + 横向滚动。

- **重置按钮单击触发** — 半小时推理一键消失是体验灾难。改成"双击才生效，单击弹气泡提示"。

- **完成后 1.5 秒强制跳下一难度** — 玩家刚解完还在欢呼就被切走。改成 8 秒倒计时 + 可取消按钮。

- **教程文案「单击/双击/三击」** — 实际机制是每次点击循环切换状态，跟"双击 = 一个动作"的语义冲突。改成「点一次 → 再点一次 → 再点一次」。

- **首屏暗色闪烁** — 见上面的内联脚本方案。

- **每点一次都同步写 IndexedDB** — 困难题 100+ 次点击 = 100+ 次事务，低端 Android 会卡顿。改成 debounce 300ms 批写。

每个坑都是「我自己玩的时候真的觉得难受」之后才发现的，没有 QA 团队就只能自测。

## 写在最后

这个项目从「我想要一个每天都能玩的爱因斯坦题」开始，最终变成一次完整的AI鞭策：算法（AC-3）+ 后端（API 时区门控 + 数据库迁移）+ 前端（响应式 / 暗色 / 无障碍 / 状态同步）+ 内容创作（5 套主题文案）。

小游戏看起来简单，但只要你真的认真想"上线给陌生人用"，就会发现每一个看似无关紧要的角落都藏着设计决策，重置按钮的二次确认、完成后的倒计时长度、暗色模式的首屏闪烁、移动端的点击区大小、时区怎么算"今天"……

这些都不是我开始时想到的。它们是在我自己玩了二十遍之后、在朋友试玩反馈之后、在让 AI 充当严苛 QA 找茬之后才浮现的。

希望它能给你一点每日推理的小快乐。如果觉得有意思，欢迎在 GitHub 上 star，或者贡献一个新的主题包（提供 15 套素材 + 文案模板就行）。