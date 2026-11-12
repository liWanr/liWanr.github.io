---
icon: lucide/feather
title: Zensical 的小技巧
tags: [Wiki]
date:
    created: 2026-01-27T07:19:20
    updated: 2026-07-19
---

[**Mermaid**](https://mermaid.ai/open-source/syntax/flowchart.html "图标")
| [**PyMdown Extensions**](https://facelessuser.github.io/pymdown-extensions/extensions/arithmatex/ "python Markdown 扩展")
| [**Icons**](https://squidfunk.github.io/mkdocs-material/reference/icons-emojis/ "图标和表情")
| [**Lucide**](https://lucide.dev/icons/ "图标")

<script src="/assets/javascripts/keys.js" defer></script>
<link rel="stylesheet" href="/assets/stylesheets/search.css">

## 键盘按键格式

<div class="mdx-search" data-mdx-component="keysearch">
    <input
        class="md-input md-input--stretch mdx-search__input"
        placeholder="搜索按键的对应格式"
        data-mdx-component="keysearch-query"
    />
</div>

///html | small
:octicons-light-bulb-16:
我这里修改了 a-z & A-Z 的键映射索引, 如果需要可以去
[**PyMdown Extensions**](https://facelessuser.github.io/pymdown-extensions/extensions/keys/#extendingmodifying-key-map-index)
查怎么改
///

**使用方法**

```markdown { linenums="0" }
++tab++

++ctrl+alt+delete++
```

///html | div.result

++tab++

++ctrl+alt+delete++

///

## 警告框

```markdown { linenums="0" }
> [!tip]
> tip

> [!info | inline | end] 
> info

> [!success]+
> success

> [!note]-
> note
```

///html | div.result
> [!tip]
> tip

> [!info | inline | end] 
> info

> [!success]+
> success

> [!note]-
> note
///

///html | div.grid.cards

> [!tip]

> [!info]

> [!success]

> [!question]

> [!note]

> [!abstract]

> [!warning]

> [!failure]

> [!danger]

> [!bug]

> [!quote]

> [!example]

///

## 按钮

```markdown { linenums="0"}
[Button](#按钮){ .md-button }
[Button](#按钮){ .md-button .md-button--primary }
```

///html | div.result

[Button](#按钮){ .md-button }
[Button](#按钮){ .md-button .md-button--primary }

///

## 代码块

````markdown { linenums="0" }
```py { title="代码块的所有配置" .yaml .no-copy .no-select hl_lines="2 3" linenums="0" }
def bubble_sort(items): # (1)!
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

1. 这是注释内容, 注释是按照对应语言来的

`#!python range()` / `range()`
````

///html | div.result

```py { title="代码块的所有配置" .yaml .no-copy .no-select hl_lines="2 3" linenums="0" }
def bubble_sort(items): # (1)!
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

1. 这是注释内容, 注释是按照对应语言来的

`#!python range()` / `range()`
///

## 内容标签

```markdown
///tab | `标签1`
标签1里面的内容
///

///tab | `标签2`
标签2里面的内容
///
```

////html | div.result
///tab | 标签1
标签1里面的内容
///

///tab | 标签2
标签2里面的内容
///
////

## 文字

```markdown
- 标记: ==高亮显示==
- 下划线: ^^这不是链接^^
- 删除: ~~我是傻逼~~
- 加粗: __够不够粗__
- 上标: X^2^ + 4x - 8
- 下标: CH~3~CH~2~OH
```

///html | div.result
- 标记: ==高亮显示==
- 下划线: ^^这不是链接^^
- 删除: ~~我是傻逼~~
- 加粗: __够不够粗__
- 上标: X^2^ + 4x - 8
- 下标: CH~3~CH~2~OH
///

## 任务清单

```markdown
-   [X] 任务 1
    *   [X] 任务 A
    *   [ ] 任务 B
        +   [x] 任务 a
        +   [ ] 任务 b
-   [ ] 任务 2
```

///html | div.result
-   [X] 任务 1
    *   [X] 任务 A
    *   [ ] 任务 B
        +   [x] 任务 a
        +   [ ] 任务 b
-   [ ] 任务 2
///

## 使用 MiSans 字体

### 基础使用

#### 字体选择与下载

首先去 [**MiSans 官网**](https://hyperos.mi.com/font) 下载字体, 有很多选项, 我选择的是第一个 [MiSans](https://hyperos.mi.com/font/details/sc), 下载解压之后有很多目录, 分别代表不同的格式, 选一种来用就行了, 我用的是**可变字体**。

|目录名称|格式与特征|
|-|-|
|ttf|经典桌面字体格式, 兼容性最强, 几乎所有系统都能直接用, 适合本地安装, 但文件大、没压缩、网页加载慢, 不推荐做网页主字体。|
|otf|TTF 的升级版, 支持更多高级排版特性, 如连字、SS01、上标、分式等, 质量更高, macOS 表现优秀, 但体积同样大、网页效率低, 主要用于设计和印刷。|
|woff|网页专用格式, 对 TTF/OTF 进行 zlib 压缩, 体积小 30–50%、保留所有特性、兼容 IE9+, 但压缩不如 WOFF2, 现在多做 fallback。|
|woff2|WOFF 的升级版, 用 Brotli 压缩, 体积再小 20–30%、加载最快、特性完整、现代浏览器全支持, 是当前网页字体的首选。|
|**可变字体**|**现代技术, 一个文件就能控制所有字重、宽度、斜体等变化, 体积最小、加载高效、过渡平滑, 适合字重多的字体族, 是简化配置的好选择。**|
|.DS_Store|这不是字体文件, 是 macOS 系统自动生成的隐藏文件（桌面设置缓存）, 完全无用。直接忽略或删除它即可, 不会影响字体使用。|

#### 装载与配置

///html | div.step

1. 创建 `docs/assets/fonts` 这个目录, 将 `MiSans-*.woff2` 文件放进去。

2. 在自定义 CSS 文件中添加规则, 让自定义字体覆盖项目字体。

    ///html | small

    :octicons-light-bulb-16:
    别忘了在项目配置文件中添加自定义 CSS 文件

    ///
    
    ///tab | `docs/stylesheets/extra.css`

    ```css
    @font-face {
    font-family: "MiSans";
    src: url("/assets/fonts/MiSans-Regular.woff2") format("woff2");
    font-weight: 400;
    font-style: normal;
    font-display: swap;
    }
    ```

    ///
    
    ///tab | `zensical.toml`

    ```toml
    [project]
    extra_css = ["stylesheets/extra.css"]
    ```

    ///

3. 然后在自定义 CSS 文件中设置将字体用于特定元素, 例如仅应用于标题、整个网站或者用作常规字体或代码字体。我配置了常规字体, 因为我觉得代码字体用上不好看。
    
    ///tab | 常规字体

    ```css
    :root {
        --md-text-font: "MiSans", sans-serif; 
        /* 尽量使用 --md-text-font 等内置变量去定义字体,
            而不是直接使用 font-family,
            因为这样做会禁用系统字体的回退。 */
    }
    ```

    ///
    
    ///tab | 代码字体

    ```css
    :root {
        --md-code-font: "MiSans", sans-serif;
    }
    ```

    ///

### 使用高级特性

<style>
.big-strong strong { font-size: 2.5em; }
.big-strong table { width: 100%; table-layout: fixed; }
.big-strong th:nth-child(1), .big-strong td:nth-child(1) { width: 10%; }
.big-strong th:nth-child(2), .big-strong td:nth-child(2) { width: 20%; }
.big-strong th:nth-child(3), .big-strong td:nth-child(3) { width: 50%; }
.big-strong th:nth-child(4), .big-strong td:nth-child(4) { width: 20%; }
.font-switch { display: inline-flex; cursor: pointer; vertical-align: middle; }
.font-switch input { display: none; }
.font-switch span { display: inline-block; width: 40px; height: 22px; border-radius: 20px; background: #aaa; position: relative; transition: .25s; }
.font-switch span::after { content: ""; position: absolute; width: 16px; height: 16px; top: 3px; left: 3px; border-radius: 50%; background: white; transition: .25s; }
.font-switch input:checked + span { background: #0d84ff; }
.font-switch input:checked + span::after { transform: translateX(18px); }
#font-a, #font-b, #font-c, #font-d, #font-e, #font-f, #font-g, #font-h, #font-i, #font-j, #font-k, #font-l, #font-m { font-feature-settings: "tnum" off, "ss08" off; }
#font-a.enabled { font-feature-settings: "ss01" on; }
#font-b.enabled { font-feature-settings: "ss02" on; }
#font-c.enabled { font-feature-settings: "ss03" on; }
#font-d.enabled { font-feature-settings: "ss04" on; }
#font-e.enabled { font-feature-settings: "ss05" on; }
#font-f.enabled { font-feature-settings: "ss06" on; }
#font-g.enabled { font-feature-settings: "ss07" on; }
#font-h.enabled { font-feature-settings: "ss08" on; }
#font-i.enabled { font-feature-settings: "ss09" on; }
#font-j.enabled { font-feature-settings: "case" on; }
#font-k.enabled { font-feature-settings: "frac" on; }
#font-l.enabled { font-feature-settings: "sups" on; }
#font-m.enabled { font-feature-settings: "tnum" on; }
</style>

<script>
document.addEventListener("change", event => {
  const input = event.target.closest(".font-switch input[data-target]");
  if (!input) return;
  document.getElementById(input.dataset.target)?.classList.toggle("enabled", input.checked);
});
</script>

MiSans 包含多种 OpenType 高级排版功能, 也就是可以让字体排版更加精致, 符合实际设计、开发需求, 每个字体功能都有对应的标签, 用于标记功能效果。MiSans 包含 15 种特性以满足不同业务对字体上的不同需求, 提供可选择性。

**局部开启(推荐)**, 用内联样式或者自定义类使用, 这样也不会影响其他正常文本, 使用方法如下：
    
///tab | `CSS`

```Css
.ss01{
    font-feature-settings: 'ss01' on;
}
```

///

///tab | `HTML`

```Html
未开启 __123,435,400__
已开启 __123,435,400__{style="font-feature-settings: 'ss01' on"}
```

///

///html | div.grid.cards.big-strong

-   未开启
            
    __123<mark>,</mark>435<mark>.</mark>00__

-   已开启
        
    __123<mark style="font-feature-settings: 'ss01' on">,</mark>435<mark style="font-feature-settings: var(--features), 'ss01' on">.</mark>00__

///

这个特征是数字专用标点, 除了这个还有其他的特征:

///html | div.big-strong

| CSS 属性 | 特征效果 | 效果 | 切换 |
| :- | :- | :-:| :-: |
| `'ss01'` | 数字专用标点 | __<span id="font-a">123,435.00</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-a"><span></span></label> |
| `'ss02'` | 单位改为上标 | __<span id="font-b">96% 96℃</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-b"><span></span></label> |
| `'ss03'` | 单位改为下标 | __<span id="font-c">96% 96℃</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-c"><span></span></label> |
| `'ss04'` | 数字等高汉字 | __<span id="font-d">4月21日</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-d"><span></span></label> |
| `'ss05'` | 将大写的 M<br>改为 [小米](https://www.mi.com/) 图标 | __<span id="font-e">M</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-e"><span></span></label> |
| `'ss06'` | 将大写的 M<br>改为 [MIUI](https://home.miui.com/) 图标 | __<span id="font-f">M</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-f"><span></span></label> |
| `'ss07'` | 西文式标点 | __<span id="font-g">“Hi, it’s.”</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-g"><span></span></label> |
| `'ss08'` | 拨号专用符号 | __<span id="font-h">*0#</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-h"><span></span></label> |
| `'ss09'` | 小字面数字 | __<span id="font-i">359264</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-i"><span></span></label> |
| `'case'` | 英文括号与<br>大写字母等高 | __<span id="font-j">{[(ABC)]}</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-j"><span></span></label> |
| `'frac'` | 分数 | __<span id="font-k">5/9</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-k"><span></span></label> |
| `'sups'` | 数字&小写字母<br>全部为上标 | __<span id="font-l">12ABab</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-l"><span></span></label> |
| `'tnum'`[^1] | 数字等宽 | __<span id="font-m">12345678</span>__ | <label class="font-switch"><input type="checkbox" data-target="font-m"><span></span></label> |
///

**全局开启**, `font-feature-settings` 属性提供了对 OpenType 字体特性的底层精细控制, 它的设计初衷是让开发者能够访问那些不常用但在特定场景下非常需要的字体特性, 所以在全局状态下使用这个属性浏览器**不一定会渲染**。所以这是我想到一个强制加载的方法, 但是比较麻烦。
    
///tab | `docs/stylesheets/extra.css`

```css
:root {
    --features: "tnum" on, "ss04" on;
}

* {
    font-feature-settings: var(--features);
}
```

///

///tab | `*.md`

```html
<span style="font-feature-settings: var(--features), 'ss01' on">
2026年4月21日 15:23
</span>
```

///
///

## 使用 Base64 编码

使用 Base64[^2] 编码 PNG、JPEG 和 GIF 图像能让整个页面完全**自包含**这类文件, 不需要额外携带图像文件夹。但是会让 HTML 文件体积增加约 33%~37%, 其次图像无法被浏览器缓存, 每次访问都会重新渲染。

///html | small
:octicons-light-bulb-16:
如果仅希望分享文档内容, 但不额外提供图像文件, Base64 就能帮到你。但不推荐在普通的网站场景中使用。
///

///tab | `zensical.toml`

```toml
[project.markdown_extensions.pymdownx.b64]
base_path = './docs/'
```

`base_path` 参数指示用于解析相对链接的基本路径的字符串。默认为 `'.'`, 这个不管 images 在哪里都不用更改

///

///tab | `*.md`

```markdown { linenums="0" }
![1.png](/docs/images/.../*.png)
```

要注意路径, 主要在 **\*.md**  文档和存放图像的 **images** 目录之间的关系上。如果文档和存放图像的目录不在同一目录, 比如 `/docs/blog/test.md`, 那引用就是 `![1.png](/docs/images/.../*.png)`。如果文图在同目录下, 比如 `/docs/index.md`, 那引用就是 `![1.png](/assets/images/.../*.png)`

///

[^1]: [__M__{style="font-feature-settings: 'ss05' on"} **MiSans**](https://hyperos.mi.com/font) 官网写错了, 他写的 **`thum`**

[^2]: 官方详细解说 [Base64](https://facelessuser.github.io/pymdown-extensions/extensions/b64/)