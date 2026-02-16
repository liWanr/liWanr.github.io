---
icon: lucide/feather
title: Zensical 的小技巧
status: new
---

<small>
created: 2025-12-16
updated: 2026-01-18
</small>

<script src="../../../assets/javascripts/keys/keys.js"></script>

## 键盘按键格式 {id="Keyboard-key-format"}

<div class="mdx-search" data-mdx-component="keysearch">
    <input
        class="md-input md-input--stretch mdx-search__input"
        placeholder="搜索按键的对应格式"
        data-mdx-component="keysearch-query"
    />
</div>

<small>
:octicons-light-bulb-16:
我这里修改了 a-z & A-Z 的键映射索引, 如果需要可以去
[**PyMdown Extensions**](https://facelessuser.github.io/pymdown-extensions/extensions/keys/#extendingmodifying-key-map-index)
查怎么改
</small>

=== "**`markdown 的使用方法`**"

    ```md 
    ++ctrl+alt+delete++
    ```

    ///html |div.result
    ++ctrl+alt+delete++
    ///

=== "**`HTML 的使用方法`**"

    ```html
    <span class="keys">
        <kbd class="key-ctrl">Ctrl</kbd>
        <span>+</span>
        <kbd class="key-alt">Alt</kbd>
        <span>+</span>
        <kbd class="key-delete">Del</kbd>
    </span>
    ```

    ///html |div.result
    <span class="keys">
        <kbd class="key-ctrl">Ctrl</kbd>
        <span>+</span>
        <kbd class="key-alt">Alt</kbd>
        <span>+</span>
        <kbd class="key-delete">Del</kbd>
    </span>
    ///



## 使用 MiSans 字体 {id="use-MiSans-font"}

### 基础使用 {id="basic-usage"}

**字体选择与下载**

:   首先去 [**MiSans 官网**](https://hyperos.mi.com/font) 下载字体, 有很多选项, 我选择的是第一个 [MiSans](https://hyperos.mi.com/font/details/sc), 下载解压之后有很多目录, 分别代表不同的格式, 选一种来用就行了, 我选的是可变字体, 文件是 **MiSansVF.ttf** 

    |目录名称|格式与特征|
    |-|-|
    |ttf|经典桌面字体格式, 兼容性最强, 几乎所有系统都能直接用, 适合本地安装, 但文件大、没压缩、网页加载慢, 不推荐做网页主字体。|
    |otf|TTF 的升级版, 支持更多高级排版特性, 如连字、SS01、上标、分式等, 质量更高, macOS 表现优秀, 但体积同样大、网页效率低, 主要用于设计和印刷。|
    |woff|网页专用格式, 对 TTF/OTF 进行 zlib 压缩, 体积小 30–50%、保留所有特性、兼容 IE9+, 但压缩不如 WOFF2, 现在多做 fallback。|
    |woff2|WOFF 的升级版, 用 Brotli 压缩, 体积再小 20–30%、加载最快、特性完整、现代浏览器全支持, 是当前网页字体的首选。|
    |**可变字体**|**现代技术, 一个文件就能控制所有字重、宽度、斜体等变化, 体积最小、加载高效、过渡平滑, 适合字重多的字体族, 是简化配置的好选择。**|
    |.DS_Store|这不是字体文件, 是 macOS 系统自动生成的隐藏文件（桌面设置缓存）, 完全无用。直接忽略或删除它即可, 不会影响字体使用。|

**装载与配置**

:   1. 创建 `docs/assets/fonts` 这个目录, 将 `MiSansVF.ttf` 文件放进去。

    2. 在自定义 CSS 文件中添加规则, 让自定义字体覆盖项目字体。
    <small>
    :octicons-light-bulb-16:
    别忘了在项目配置文件中添加自定义 CSS 文件
    </small>

        === "`docs/stylesheets/extra.css`"

            ```css title=""
            @font-face {
                font-family: "MiSansVF";
                src: url("../assets/fonts/MiSansVF.ttf") format("truetype");
                font-weight: 100 900;
                font-style: normal;
                font-display: swap;
            }
            ```

        === "`zensical.toml`"

            ```toml title=""
            [project]
            extra_css = ["stylesheets/extra.css"]
            ```

    3. 然后在自定义 CSS 文件中设置将字体用于特定元素, 例如仅应用于标题、整个网站或者用作常规字体或代码字体。我配置了常规字体, 因为我觉得代码字体用上不好看。

        === "常规字体"

            ```css title=""
            :root {
                --md-text-font: "MiSansVF", sans-serif; /* (1)! */
            }
            ```

            1. 尽量使用 CSS `--md-text-font` 等内置变量去定义字体, 而不是直接使用 font-family, 因为这样做会禁用系统字体的回退。

        === "代码字体"

            ```css title=""
            :root {
                --md-code-font: "MiSansVF", sans-serif;
            }
            ```

### 使用高级特性 {id="enable-OpenType"}

MiSans 包含多种 OpenType 高级排版功能, 也就是可以让字体排版更加精致, 符合实际设计、开发需求, 每个字体功能都有对应的标签, 用于标记功能效果。MiSans 包含 15 种特性以满足不同业务对字体上的不同需求, 提供可选择性。

1. **局部开启(推荐)**, 用内联样式或者自定义类使用, 这样也不会影响其他正常文本, 使用方法如下：

    === "`CSS`"

        ```Css title=""
        .ss01{
            font-feature-settings: 'ss01' on;
        }
        ```

        /// html | div.result
        已开启:
        <span style="font-size: 2em; font-weight:900; font-feature-settings: var(--features), 'ss01' on">
        123,435,400
        </span>
        <br> 未开启:
        <span style="font-size: 2em; font-weight:900;">
        123,435,400
        </span>
        ///

    === "`HTML`"

        ```Html title=""
        未开启 __123,435,400__
        已开启 __123,435,400__{style="font-feature-settings: 'ss01' on"}
        ```

        <div class="result" markdown >

        未开启 __123,435,400__{style="font-size:2em;"}<br>
        已开启 __123,435,400__{style="font-size:2em; font-feature-settings: var(--features), 'ss01' on"}
        
        </div>

    这个特征是数字专用标点, 除了这个还有其他的特征:

    |CSS 底层配置|特征效果|未启用|已启用|
    |:-|:-|:-:|:-:|
    |`'ss01'`|数字专用标点|__:1,234,356__{style="font-size:2em;"}|__:1,234,356__{style="font-size:2em; font-feature-settings: var(--features), 'ss01' on"}|
    |`'ss02'`|单位改为上标|__96% 96℃__{style="font-size:2em;"}|__96% 96℃__{style="font-size:2em; font-feature-settings: var(--features), 'ss02' on"}|
    |`'ss03'`|单位改为下标|__96% 96℃__{style="font-size:2em;"}|__96% 96℃__{style="font-size:2em; font-feature-settings: var(--features), 'ss03' on"}|
    |`'ss04'`|数字等高汉字|__4月21日__{style="font-size:2em; font-feature-settings: var(--features), 'ss04' off"}|__4月21日__{style="font-size:2em;"}|
    |`'ss05'`|将大写的 M<br>改为 [小米](https://www.mi.com/) 图标|__M__{style="font-size:2em;"}|__M__{style="font-size:2em; font-feature-settings: var(--features), 'ss05' on"}|
    |`'ss06'`|将大写的 M<br>改为 [MIUI](https://home.miui.com/) 图标|__M__{style="font-size:2em;"}|__M__{style="font-size:2em; font-feature-settings: var(--features), 'ss06' on"}|
    |`'ss07'`|西文式标点|__“Hi, it’s me”__{style="font-size:2em;"}|__“Hi, it’s me”__{style="font-size:2em; font-feature-settings: var(--features), 'ss07' on"}|
    |`'ss08'`|拨号专用符号|__*0#__{style="font-size:2em;"}|__*0#__{style="font-size:2em; font-feature-settings: var(--features), 'ss08' on"}|
    |`'SS09'`|小字面数字|__359264__{style="font-size:2em;"}|__359264__{style="font-size:2em; font-feature-settings: var(--features), 'ss09' on"}|
    |`'case'`|大中小三个括号<br>与大写字母等高|__(HBCD)__{style="font-size:2em; font-feature-settings: var(--features), 'case' off"}|__(HBCD)__{style="font-size:2em;"}|
    |`'frac'`|分数|__5/9__{style="font-size:2em;"}|__5/9__{style="font-size:2em; font-feature-settings: var(--features), 'frac' on"}|
    |`'sups'`|数字/小写字母<br>全部为上标|__12ABab__{style="font-size:2em;"}|__12ABab__{style="font-size:2em; font-feature-settings: var(--features), 'sups' on"}|
    |`'tnum'`[^1]|数字等宽|__1,234,567,890__{style="font-size:1.5em; font-feature-settings: 'tnum' off,'ss01' on;" }|__1,234,567,890__{style="font-size:1.5em;font-feature-settings: var(--features), 'ss01' on"}|

    [^1]: [__M__{style="font-feature-settings: 'ss05' on"} **MiSans**](https://hyperos.mi.com/font) 官网写错了, 他写的 **`thum`**
    
2. **全局开启**, `font-feature-settings` 属性提供了对 OpenType 字体特性的底层精细控制, 它的设计初衷是让开发者能够访问那些不常用但在特定场景下非常需要的字体特性, 所以在全局状态下使用这个属性浏览器**不一定会渲染**。所以这是我想到一个强制加载的方法, 但是比较麻烦。

    === "`docs/stylesheets/extra.css`"

        ```css title=""
        :root {
            --features: "tnum" on, "ss04" on;
        }

        * {
            font-feature-settings: var(--features);
        }
        ```

    === "`*.md`"

        ```html title=""
        <div style="font-feature-settings: var(--features), 'ss01' on">
        2026年4月21日 15:23
        </div>
        ```

        <div class="result" markdown>
        前:
        <span style="font-size: 2em; font-feature-settings: var(--features), 'ss01' on">
        26年4月21日 15:23
        </span> <br>后:
        <span style="font-size: 2em; font-feature-settings: 'tnum' off, 'ss04' off">
        26年4月21日 15:23
        </span>

        </div>

## 使用 Base64 编码 {id="encoded-using-base64"}

使用 Base64 编码 PNG、JPEG 和 GIF 图像能让整个页面完全**自包含**这类文件, 不需要额外携带图像文件夹。但是会让 HTML 文件体积增加约 33%~37%, 其次图像无法被浏览器缓存, 每次访问都会重新渲染。

<small>
:octicons-light-bulb-16:
如果仅希望分享文档内容, 但不额外提供图像文件, Base64 就能帮到你。但不推荐在普通的网站场景中使用。
</small>

=== "`zensical.toml`"

    ```toml title=""
    [project.markdown_extensions.pymdownx.b64]
    base_path = './docs/'
    ```

    `base_path` 参数指示用于解析相对链接的基本路径的字符串。默认为 `'.'`, 这个不管 images 在哪里都不用更改

=== "`*.md`"

    ```md title=""
    ![1.png](/docs/images/.../*.png)
    ```

    要注意路径, 主要在 **\*.md**  文档和存放图像的 **images** 目录之间的关系上。如果文档和存放图像的目录不在同一目录, 比如 `/docs/blog/test.md`, 那引用就是 `![1.png](/docs/images/.../*.png)`。如果文图在同目录下, 比如 `/docs/index.md`, 那引用就是 `![1.png](./images/.../*.png)`

