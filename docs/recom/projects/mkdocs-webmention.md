---
title: MkDocs-Webmention
---

在 MkDocs 站点上接收并展示 Webmention。收件箱用 [webmention.io](https://webmention.io)，插件只负责展示。

## 准备

用你的域名在 [webmention.io](https://webmention.io) 注册。它走 IndieAuth 登录，
需要你的首页有一个 `rel="me"` 链接指向 GitHub 之类的身份提供方，对方主页也要链回你的域名。

```html
<a href="https://github.com/yourname" rel="me">GitHub</a>
```

登录后拿到的 token 不要写进 `mkdocs.yml`，插件配置会被写进公开的 HTML。

## 安装

///tab | `pip`

```bash
pip install mkdocs-webmention
```

///

///tab | `mkdocs.yml`

```yaml
site_url: https://example.com/

plugins:
  - webmention: {}
```
///


`site_url` 必填，插件用它推算每个页面的 target 和收件箱域名。

回应区会自动加到每篇文章正文末尾。

## 配置

```yaml
plugins:
  - webmention:
      show: [replies, mentions, likes, reposts, bookmarks]
      facepile: [likes, reposts, bookmarks]
      content: text
      lazy: true
      exclude: []
      i18n: {}
```

| 选项 | 默认 | 说明 |
|---|---|---|
| `show` | 全部 | 显示哪些类型。不在列表里的不计数 |
| `facepile` | `likes, reposts, bookmarks` | 这些折叠成一排头像。必须是 `show` 的子集 |
| `content` | `text` | 改成 `html` 保留粗体、链接、引用（白名单清洗） |
| `lazy` | `true` | 滚到回应区才发请求 |
| `exclude` | `[]` | 哪些页面不显示回应 |
| `i18n` | 跟随主题语言 | 覆盖文案 |

类型名写 `replies` 或 `in-reply-to` 都可以。

### exclude

路径相对 `docs/`：

```yaml
exclude:
  - index.md        # 单个文件
  - about/          # 整个目录
  - drafts/*.md     # glob
```

只影响显示。被排除的页面仍然有 `<link rel="webmention">`，别人照样能提及它。

### 单页关闭

```yaml
---
webmention: false
---
```

优先于 `exclude`。

用 Material 的 blog 插件时，博客首页、归档页、分类页会自动跳过，不用配置。

### 改文案

```yaml
plugins:
  - webmention:
      i18n:
        title: 网友怎么说
        empty: 还没有人聊过这篇。
```

可覆盖的键见 `mkdocs_webmention/locales.py`。

## 回复别人的文章

在 front matter 里声明，插件会在标题下方生成带 microformats2 标记的链接，
对方站点就会把你这篇算作回复而不是普通提及。

```yaml
---
reply: https://friend.example/posts/hello/
---
```

四个键：`reply`、`like`、`repost`、`bookmark`。值可以是网址或网址列表。

插件不发送通知。写完之后用 [Telegraph](https://telegraph.p3k.io/) 手动发一次。

## 自己摆放容器

想把回应区放到别处（比如塞进选项卡），在主题模板里用 `webmention_container`。
插件会自动撤掉正文末尾自动追加的那个。

```jinja
{% if webmention_enabled %}
  {{ webmention_container }}
{% endif %}
```

| 变量 | 说明 |
|---|---|
| `webmention_enabled` | 本页是否显示回应 |
| `webmention_container` | 容器 HTML |
| `webmention_targets` | 本页的 target 列表（JSON） |
| `webmention_i18n` | 文案字典，放进 HTML 记得过 `\|e` |

### 事件

```js
document.addEventListener("webmention:loaded", function (e) {
  e.detail.state     // "loading" | "ready" | "error"
  e.detail.total     // 3
  e.detail.rendered  // 容器里有没有东西
})
```

判断要不要显示自己的入口时用 `rendered`，不要用 `total`。零回应时容器里还有提交表单，
用 `total > 0` 会把它一起藏掉。

同样的值也在容器的 `data-wm-state` / `data-wm-rendered` / `data-wm-total` 上，
监听器挂晚了可以补读。

## 写样式

插件自带的样式只管提交表单，其余交给你的主题和你自己的 CSS。

```
div.wm
└─ section.wm__inner
   ├─ h2.wm__title
   ├─ form.wm__form            hint / row / status
   ├─ div.wm__facepiles        section.wm__facepile > ul.wm__faces > li.wm__face
   ├─ ol.wm__replies           li.wm__reply > avatar-link + body(meta/content)
   └─ p.wm__status             空状态或错误，错误时含 button.wm__retry
```

写选择器时带上 `.md-typeset` 前缀，并且给 `ul` / `ol` 补上元素选择器：

```css
.md-typeset ul.wm__faces { display: flex; }
```

Material 的 `.md-typeset ul:not([hidden]) { display: flow-root }` 特异度是 (0,0,2,1)，
只写两个类名压不住。

### 建议样式

```css { title="CSS" }
.md-typeset .wm__inner {
    margin-top: 2em;
    padding-top: 1.2em;
    border-top: 1px solid var(--md-default-fg-color--lightest);
    font-size: .75rem;
    line-height: 1.7;
}

.md-typeset .wm__title {
    margin: 0 0 .8em;
    font-size: 1.1rem;
}

.md-typeset .wm__form {
    padding-bottom: 1em;
    margin-bottom: 1.2em;
    border-bottom: 1px solid var(--md-default-fg-color--lightest);
}

.md-typeset .wm__form:last-child {
    padding-bottom: 0;
    margin-bottom: 0;
    border-bottom: none;
}

.md-typeset .wm__form-hint {
    margin: 0 0 .5em;
    color: var(--md-default-fg-color--light);
}

.md-typeset .wm__form-status {
    margin: .6em 0 0;
    color: var(--md-default-fg-color--light);
}

.md-typeset .wm__facepiles {
    display: flex;
    flex-wrap: wrap;
    gap: .8em 2em;
    margin-bottom: 1.2em;
}

.md-typeset .wm__facepile {
    flex: 0 1 auto;
    min-width: 0;
}

.md-typeset .wm__subtitle {
    display: flex;
    align-items: baseline;
    gap: .4em;
    margin: 0 0 .4em;
    font-size: .7rem;
    font-weight: 600;
    color: var(--md-default-fg-color--light);
}

.md-typeset .wm__count {
    font-weight: 400;
    color: var(--md-default-fg-color--light);
}

.md-typeset ul.wm__faces {
    display: flex;
    flex-wrap: wrap;
    gap: .35em;
    margin: 0;
    padding: 0;
    list-style: none;
}

.md-typeset ul.wm__faces li {
    margin: 0;
}

.md-typeset .wm__avatar {
    border-radius: 50%;
    object-fit: cover;
    vertical-align: middle;
}

.md-typeset span.wm__avatar--fallback {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 2em;
    height: 2em;
    font-size: .7rem;
    color: var(--md-default-bg-color);
    background: var(--md-default-fg-color--light);
}

.md-typeset .wm__face--more {
    display: inline-flex;
    align-items: center;
    padding: 0 .6em;
    height: 2em;
    font-size: .7rem;
    color: var(--md-default-fg-color--light);
    background: var(--md-default-fg-color--lightest);
    border-radius: 1em;
}

.md-typeset ol.wm__replies {
    margin: 0;
    padding: 0;
    list-style: none;
}

.md-typeset ol.wm__replies li {
    margin: 0;
}

.md-typeset .wm__reply {
    display: flex;
    gap: .7em;
    padding: .8em 0;
    border-top: 1px solid var(--md-default-fg-color--lightest);
}

.md-typeset .wm__reply:first-child {
    border-top: none;
    padding-top: 0;
}

.md-typeset .wm__avatar-link {
    flex: none;
    line-height: 0;
}

.md-typeset .wm__body {
    flex: 1 1 auto;
    min-width: 0;
}

.md-typeset .wm__meta {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: .5em;
    margin-bottom: .1em;
}

.md-typeset .wm__author {
    font-weight: 600;
    color: var(--md-default-fg-color);
}

.md-typeset .wm__badge {
    padding: 0 .5em;
    font-size: .65rem;
    color: var(--md-default-fg-color--light);
    background: var(--md-default-fg-color--lightest);
    border-radius: 1em;
}

.md-typeset .wm__permalink,
.md-typeset .wm__permalink:hover {
    color: var(--md-default-fg-color--light);
    font-size: .7rem;
}

.md-typeset .wm__content > :first-child { margin-top: 0; }
.md-typeset .wm__content > :last-child { margin-bottom: 0; }

.md-typeset .wm__content p {
    margin: .3em 0;
}

.md-typeset .wm__status {
    margin: 0;
    color: var(--md-default-fg-color--light);
}

.md-typeset [data-talk] [data-talk-wm]:not([data-talk-count=""])::after {
    content: attr(data-talk-count);
    display: inline-block;
    min-width: 1.4em;
    margin-left: .4em;
    padding: 0 .35em;
    border-radius: 1em;
    font-size: .85em;
    line-height: 1.5;
    text-align: center;
    color: var(--md-default-fg-color--light);
    background-color: var(--md-default-fg-color--lightest);
}

.md-typeset .talk--single .tabbed-labels { box-shadow: none; }
.md-typeset .talk--single .tabbed-labels::before { display: none; }

.md-typeset .talk--single .tabbed-labels > label {
    margin: 1.6em 0 .64em;
    padding: 0;
    font-size: 1.5em;
    font-weight: 700 !important;
    line-height: 1.4;
    letter-spacing: -.025em;
    color: var(--md-default-fg-color);
    cursor: default;
}

.md-typeset [data-talk] .wm__title { display: none; }

.md-typeset [data-talk] .wm__inner {
    margin-top: 0;
    padding-top: 0;
    border-top: none;
}

.md-typeset [data-talk].tabbed-alternate.tabbed-set > .tabbed-content > .tabbed-block {
    padding-top: 1.4em;
    padding-bottom: .6em;
}

.md-typeset [data-talk] {
    margin-top: 2.5em;
    margin-bottom: 2em;
}

.md-typeset [data-talk].talk--single {
    margin-top: 0;
    margin-bottom: 1em;
}
```

### 建议脚本

```js { title="JavaScript" }
(function () {
    "use strict";

    var SET_ID = "__tabbed_talk";

    function mentionTitle() {
        var el = document.getElementById("mkdocs-webmention-config");
        try {
            return JSON.parse(el.textContent).i18n.title;
        } catch (e) {
            return "提及";
        }
    }

    function radio(id, checked) {
        var input = document.createElement("input");
        input.type = "radio";
        input.id = id;
        input.name = SET_ID;
        if (checked) input.checked = true;
        return input;
    }

    function positionIndicator(set) {
        var labels = set.querySelector(".tabbed-labels");
        var inputs = set.querySelectorAll("input");
        for (var i = 0; i < inputs.length; i++) {
            if (!inputs[i].checked) continue;
            var label = labels.children[i];
            if (!label || label.hidden) return;
            labels.style.setProperty("--md-indicator-x", label.offsetLeft + "px");
            labels.style.setProperty("--md-indicator-width", label.offsetWidth + "px");
            return;
        }
    }

    function build() {
        var wm = document.querySelector(".wm[data-wm-targets]");
        if (!wm || document.querySelector("[data-talk]")) return;

        var heading = null;
        for (var n = wm.nextSibling; n; n = n.nextSibling) {
            if (n.nodeType === 1 && n.tagName === "H2") { heading = n; break; }
        }
        if (!heading) return;

        var commentNodes = [];
        for (var m = heading.nextSibling; m; m = m.nextSibling) commentNodes.push(m);

        var set = document.createElement("div");
        set.className = "tabbed-set tabbed-alternate";
        set.setAttribute("data-tabs", "1:2");
        set.setAttribute("data-talk", "");
        set.appendChild(radio(SET_ID + "_1", true));
        set.appendChild(radio(SET_ID + "_2", false));

        var labels = document.createElement("div");
        labels.className = "tabbed-labels";

        var commentLabel = document.createElement("label");
        commentLabel.htmlFor = SET_ID + "_1";
        commentLabel.textContent = heading.textContent.trim();
        labels.appendChild(commentLabel);

        var wmLabel = document.createElement("label");
        wmLabel.htmlFor = SET_ID + "_2";
        wmLabel.setAttribute("data-talk-wm", "");
        wmLabel.setAttribute("data-talk-count", "");
        wmLabel.hidden = true;
        wmLabel.textContent = mentionTitle();
        labels.appendChild(wmLabel);

        set.appendChild(labels);

        var content = document.createElement("div");
        content.className = "tabbed-content";
        var pane1 = document.createElement("div");
        pane1.className = "tabbed-block";
        var pane2 = document.createElement("div");
        pane2.className = "tabbed-block";
        content.appendChild(pane1);
        content.appendChild(pane2);
        set.appendChild(content);

        wm.parentNode.insertBefore(set, wm);
        commentNodes.forEach(function (node) { pane1.appendChild(node); });
        pane2.appendChild(wm);
        heading.parentNode.removeChild(heading); 

        set.addEventListener("change", function () { positionIndicator(set); });
        positionIndicator(set);
        return set;
    }

    function sync(detail) {
        var set = document.querySelector("[data-talk]");
        var label = set && set.querySelector("[data-talk-wm]");
        if (!label) return;
        label.hidden = !detail.rendered;
        set.classList.toggle("talk--single", !detail.rendered);
        label.dataset.talkCount = detail.total > 0 ? detail.total : "";
        positionIndicator(set);
    }

    function start() {
        var set = build();
        if (!set) return;
        document.addEventListener("webmention:loaded", function (e) { sync(e.detail); });
        var wm = set.querySelector(".wm[data-wm-state]");
        if (wm) sync({
            rendered: wm.dataset.wmRendered === "1",
            total: Number(wm.dataset.wmTotal || 0),
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", start);
    } else {
        start();
    }
})();
```

## 和评论系统放到一起

回应区在正文末尾，评论区在它后面，默认就是上下堆叠。

想合成选项卡，在主题的评论 partial 里用 Material 的内容选项卡标记，两个面板分别放
评论和 `webmention_container`。

如果容器进了未激活的面板（`display: none`），要加上 `lazy: false`，
否则 `IntersectionObserver` 不会触发。

## 常见问题

> [!question]- **数据存在哪儿？本地和线上是两套数据吗？**
> 在 webmention.io，不在你的仓库里。产物里只有一个空的 `<div class="wm">`。
>
> 同一套。target 取自 `mkdocs.yml` 里写的 `site_url`，跟页面实际被哪个域名访问无关。

> [!question]- **可以提及自己的文章吗？对方把文章删了会怎样？**
> 可以，不要求跨域。
>
> 已经收到的提及不会消失，接收方只在被再次通知时才重新验证。

> [!question]- **回应区一直是空的？**
> 1. `site_url` 是公开地址吗
> 2. `grep -c data-wm-targets site/posts/hello/index.html` 是不是 1
> 3. `ls site/assets/webmention/` 资源落地了吗
> 4. 控制台有没有 `[webmention]` 开头的报错
> 5. 直接查一次 API，确认是不是真的没收到过：
> 
> ```bash
> curl -s "https://webmention.io/api/mentions.jf2?target=https://example.com/posts/hello/"
> ```