---
title: 关于
created: 2025-02-22T08:30:16
hide:
    # - navigation
    - path
    # - feedback
---

///html | style
.md-nav--lifted {
    display: none !important;
}
///

<link rel="stylesheet" href="/assets/stylesheets/about.css">

///html | div.grid[style="text-align: center;"]
[**隐私政策**](/about/privacy-policy/)

[**许可证授权**](/about/LICENSE/)
///

## :lucide-megaphone: 关于博客

记录「**技术与思考**」的个人空间，也是我在数字世界中圈出的三分地。

建立站点的初衷是为避免技术重复踩坑。很多复杂问题在初遇时往往需要耗费大量时间翻阅文档、反复尝试；若不及时记录，当再遇类似境遇时仍需从头开始。因此我选择在此标记我曾深耕过的坐标，把经验悉数种进这片地里，固化脚下的寸土。

随着站点的逐步完善，内容亦不再局限于冰冷的逻辑。那些万籁俱寂时的自省、现实的挣扎、乃至尚未成熟的偏见，也想贪心成文。虽凌乱，却也证明这片空间是有温度的活物。

故搭建站点不仅是备份代码，更是在备份灵魂。在这个算法比我们更了解自己的时代，唯有亲手写下的文字，能在大数据的洪流中，拓出名为「**我**」的岛。

## :lucide-ev-charger: 提供动力

///html | div.grid.cards
-   :lucide-bug-play: **框架生成**

    基于静态网站生成器
    [MaterialX](https://jaywhj.github.io/mkdocs-materialx/)。
    <!-- [Zensical](https://zensical.org/) -->

-   :lucide-cloud-upload: **托管平台**

    [Local](https://local.liwanr.com:24)
    / [OuluCloud](https://yun.oulucloud.com/aff/WMOMVMPX)
    / [GitHub Pages](https://docs.github.com/pages)
    
-   :lucide-code-xml: **编码存储**

    - 代码通过 [VS Code](https://code.visualstudio.com/) 编写
    - 存储在本地及 [GitHub](https://github.com/github) 公开仓库中。

-   :lucide-type-outline: **字体样式**

    - 常规文字采用 [MiSans](https://hyperos.mi.com/font)
    - 等宽文字采用 [JetBrains Mono](https://www.jetbrains.com/lp/mono/)
    - [ESSAYS](http://localhost:8000/essays/)正文采用
    [Noto Serif SC](https://fonts.google.com/noto/specimen/Noto+Serif+SC?preview.layout=grid&query=Noto+Serif+SC&preview.script=Hans)。
///

## :lucide-newspaper: 新闻简报

<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>

<form id="rss-ring-form">
  <div style="display: flex; gap: 8px; align-items: center;">
    <input class="mdx-form__input mdx-form__input--stretch" type="email" name="email" id="bd-email" style="flex: 1;"  placeholder="your-email@example.com" autocomplete="email" required/>
    <button class="md-button md-button--primary" type="submit" id="rss-ring-submit" disabled>订阅</button>
  </div>
  <div class="cf-turnstile"
       data-sitekey="0x4AAAAAADwZnEQiPgcV_V17"
       data-callback="rssRingOnVerified"
       data-expired-callback="rssRingOnExpired"
       data-error-callback="rssRingOnExpired"></div>
</form>

<p id="rss-ring-message">内容更新不会等你，但订阅可以。</p>

<script src="/assets/javascripts/about.js"></script>

## :lucide-history: 历程轨迹

///tab | **2026年初**

- 框架使用[**Zensical**](https://zensical.org/)，本地服务器部署 + [GitHub Pages](https://liwanr.github.io/) + [Vercel](https://liwanr.vercel.app/) + [Netlify](https://liwanr.netlify.app/)

- 域名更为**liWanr.com**，网站更名**liWanr**

- 迁移并整理之数据，继续写技术内容和经验分享

- 26/03/22，增加评论功能，次日发表第一篇文

- 26/07/06，增加订阅功能，并移除了 Vercel 和 Netlify 部署

- 26/07/13，Zensical是半成品...所以复古了Mkdocs-material的大佬变更版[**MaterialX**](https://jaywhj.github.io/mkdocs-materialx/)

///

///tab | **2024年底**

- 框架使用[**Material for MkDocs**](https://squidfunk.github.io/mkdocs-material/)，本地服务器部署 + [GitHub Pages](https://liwanr.github.io/mkdocs/)

- 域名未做更改，但中期将网站更名为**Easton**

- 迁移并整理之前的数据，开始大量记录技术内容

- 用[**Ngxin**](https://nginx.org/)部署静态文件服务

- 后期个人原因较少写笔记，但一直热衷于修改样式

///

///tab | **2024年中**

- 框架使用[**Poetize**](https://poetize.cn/)(现在被开发者卖了)，在阿里云上部署

- 域名更新为**liiiiy.cn**，后期网站更名**Yearn**

- 少量记录技术经验，主要更新网站书签

- 框架愈发臃肿，感觉偏离博客初衷，就放弃这个框架了，数据保留

///

///tab | **2023年初**

- 框架使用[**Halo**](https://www.halo.run/)，主题使用过[Hao](https://www.halo.run/store/apps/app-MgZJX)、[PIX](https://www.halo.run/store/apps/app-TUSTB)，在腾讯云和阿里云均有部署使用

- 域名依旧是**liy666.cn**，网站依旧为**LiY**

- 主要用于记录个人学习经验笔记

- 服务器过期没续费，数据全部丢失，主要是也没有多少东西

///

///tab | **2021年初**

- 框架使用[**Notion**](https://www.notion.com/)，未使用服务器，使用的是官方云存档，有会员

- 域名使用**liy666.cn**，网站取名为**LiY**

- 主要用于记录比赛笔记与经验

- 后续会员过期不给看笔记，跟客服沟通妄想导出，但客服不通人性，遂注销账号，属于是一怒之下怒了一下，数据全部丢失

///

## :lucide-computer: 战机可查

<div class="divider">编程机 · Dev Machine</div>

///html | div.grid.cards[style='font-family: JetBrains Mono;']
-   <small>:material-apple-finder: MacOS</small><br>
    **M3Pro MacBook Pro 14" 2023**<br>
    <span class="badge theme">18GB RAM</span>
    <span class="badge">512GB SSD</span>

-   <small>:simple-linux: Linux</small><br>
    **RTX 3060 ROG M16  2021**<br>
    <span class="badge theme">i7-11800H</span>
    <span class="badge">16GB RAM</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://rog.asus.com.cn/laptops/rog-zephyrus/2021-rog-zephyrus-m16-series/)</small>
///

<div class="divider">
游戏主机
<span class="dot"></span>
System Specs
</div>

///html | div.grid.cards[style='grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr)); font-family: JetBrains Mono;']
-   <small>:lucide-layout-dashboard: 主板</small><br>
    **ASUS TUF GAMING B650M-PLUS**<br>
    <span class="badge theme">光环同步</span>
    <span class="badge">WIFI 6E</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://www.asus.com/us/motherboards-components/motherboards/tuf-gaming/tuf-gaming-b850m-plus-wifi/)</small>

-   <small>:lucide-cpu: CPU</small><br>
    **AMD Ryzen™ 7 7800X3D**<br>
    <span class="badge theme">3D V-Cache</span>
    <span class="badge">8 核心</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://www.amd.com/en/products/processors/desktops/ryzen/7000-series/amd-ryzen-7-7800x3d.html)</small>

-   <small>:lucide-gpu: GPU</small><br>
    **GeForce RTX 4070 Ti SUPER**<br>
    <span class="badge theme">16 GB</span>
    <span class="badge">iGame Advanced OC</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://www.colorful.cn/home/product?mid=102&id=951619eb-5066-4258-810e-c5ec2bbd32be)</small>

-   <small>:lucide-memory-stick: RAM</small><br>
    **XPG D300 16 GB × 2**<br>
    <span class="badge theme">6000 MHz</span>
    <span class="badge">DDR5</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://xpg.adata.com.cn/cn/xpg/dram-modules-lancer-rgb-ddr5?tab=desc)</small>

-   <small>:lucide-hard-drive: 存储</small><br>
    **Predator GM7000  1 TB**<br>
    <span class="badge theme">PCIe4.0</span>
    <span class="badge">M.2 SSD</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://www.predatorstorage.com/products/pcie-m-2-ssd/predator-gm7000-pcie-4-ssd/)</small>

-   <small>:lucide-hard-drive: 存储</small><br>
    **WesternDigital Blue 2 TB**<br>
    <span class="badge theme">256MB</span>
    <span class="badge">7200RPM</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://www.westerndigital.com/products/internal-drives/wd-blue-desktop-sata-hdd?sku=WD20EZBX)</small>

-   <small>:lucide-thermometer-snowflake: 散热器</small><br>
    **TCOMAS SJ-A090 360**<br>
    <span class="badge theme">水冷</span>
    <span class="badge">35.7dB</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://cougargaming.com/products/cases/mx600-rgb/)</small>

-   <small>:lucide-zap: 电源</small><br>
    **GreatWall F-850BL (92+) F8MP**<br>
    <span class="badge theme">850W</span>
    <span class="badge">92%效率</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://www.gwpst.cn/product/detail/301.html)</small>

-   <small>:lucide-pc-case: 机箱</small><br>
    **GOUGAR MX600 RGB Black**<br>
    <span class="badge theme">全塔</span>
    <span class="badge">风扇≦9</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://cougargaming.com/products/cases/mx600-rgb/)</small>

-   <small>:lucide-fan: 风扇</small><br>
    **Jungle Leopard PRISM 4 MAX × 6**<br>
    <span class="badge theme">神光同步</span>
    <span class="badge">≦20dBA</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://www.jlcpucooler.com/prism-4-max-black-edition-product/)</small>
///

<div class="divider">外设 · Peripherals</div>

///html | div.grid.cards[style='font-family: JetBrains Mono;']

-   <small>:lucide-monitor: 显示器</small><br>
    **SANC G73 2K**<br>
    <span class="badge theme">240Hz</span>
    <span class="badge">27"</span>
    <small>[:lucide-mouse-pointer-click:去看看](http://www.ccclcd.com/high-end-esports-g-series/537233)</small>

-   <small>:lucide-keyboard: 键盘</small><br>
    **Keychron K3 Max 专供版复古灰**<br>
    <span class="badge theme">矮轴</span>
    <span class="badge">三模</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://www.keychron.com/products/keychron-k3-max-qmk-via-wireless-custom-mechanical-keyboard?variant=42752630915161)</small>

-   <small>:lucide-headset: 耳机</small><br>
    **Bose QC35 II Gaming**<br>
    <span class="badge theme">降噪</span>
    <span class="badge">无线</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://support.bose.com/s/product/quietcomfort-35-ii-gaming-headset/01t8c00000OydAGAAZ?language=en_US)</small>

-   <small>:lucide-mouse: 鼠标</small><br>
    **ROG Gladius III Wireless AimPoint**<br>
    <span class="badge theme">79g</span>
    <span class="badge">119h+</span>
    <small>[:lucide-mouse-pointer-click:去看看](https://rog.asus.com/mice-mouse-pads/mice/ergonomic-right-handed/rog-gladius-iii-wireless-aimpoint-model/)</small>
///