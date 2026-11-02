---
title: MkDocs-feed
---

给 MkDocs 站点生成 RSS 2.0 订阅源的插件。**开源地址**：[liWanr/mkdocs-feed](https://github.com/liWanr/mkdocs-feed)

## 安装并启用

///tab | **安装**

```bash
pip install mkdocs-feed
```
///

///tab | **更新**

```bash
pip install --upgrade mkdocs-feed
```
///

///tab | **`mkdocs.yml`**
```yaml
site_url: https://example.com/

plugins:
  - feed
```
///

///html | small
:octicons-light-bulb-16: 
**`site_url` 是必填的。** RSS 条目里的链接必须是绝对地址，订阅源在你站点之外被读取，相对路径会解析到阅读器身上。缺少它时插件直接中止构建。
///

构建后不仅会生成 `site/feed.xml`，同时每个页面的 `<head>` 里会多出一行订阅源被发现的方式，用户把网址粘进阅读器，阅读器读这一行找到真正的 feed 地址:

```html
<link rel="alternate" type="application/rss+xml" title="站点名" href="https://example.com/feed.xml" />
```

## 配置项速查

### 快速配置

大多数站点写到这个程度就够了：

```yaml
plugins:
  - feed:
      filename: rss.xml          # 默认 feed.xml
      length: 15                 # 保留最新多少条，默认 20
      timezone: Asia/Shanghai    # 默认 UTC，不改会差 8 小时
      exclude: [about]           # 路径前缀，一条覆盖整棵子树
```

### 更多配置

| 选项 | 类型 | 默认值 | 作用 |
| --- | --- | --- | --- |
| `enabled` | bool | `true` | 关掉后不写文件、不注入 `<head>` 链接，等于插件不存在。可配合 `!ENV` 按环境开关 |
| `filename` | str | `feed.xml` | 输出文件名，相对 `site_dir`。改名不影响内容格式，始终是 RSS 2.0 |
| `length` | int | `20` | 保留最新多少条。排序后截断 |
| `pretty_print` | bool | `true` | 输出带缩进的 XML。关掉省体积，两种都是合法 XML |
| `include_last_build_date` | bool | `true` | 是否输出 `<lastBuildDate>`。|
| `full_content` | bool | `false` | 是否把完整 HTML 写进 `<content:encoded>` |
| `abstract_chars_count` | int | `300` | 自动提取的摘要截断长度。**只对自动提取生效** |
| `timezone` | IANA 时区名 | `UTC` | 写错在配置阶段就报错 |
| `date_priority` | list | `[meta, git, mtime]` | 依次尝试的日期来源，先命中的赢 |
| `git_history_valid_after` | ISO 8601 | 无 | 迁移仓库的截断点 |
| `sort_by` | `created` \| `updated` | `created` | 排序依据。不影响 `<pubDate>` 的语义 |
| `exclude` | list[str] | `[]` | 排除路径前缀列表 |

### Meta 键

这几个写在页面里，不是配置项：

| 键 | 值 | 作用 |
| --- | --- | --- |
| `feed` / `rss` | `false` | 排除该页面 |
| `description` | 字符串 | 直接作为摘要 |

## feed 筛选

默认所有页面都是候选。命中下列任意一条就被排除：

1. 页面的 `feed` 或 `rss` meta 键设为 `false`
2. 匹配 `exclude` 里的某个路径前缀
3. 是 blog 插件生成的列表页（首页、归档、分类、分页）
4. 是 tags 插件的标签索引页，或 MkDocs 的 `404` 页
5. 在 `date_priority` 的所有来源里都取不到日期

## 日期读取顺序

`date_priority` 列出依次尝试的来源，**先命中的赢**：

///html | div.step

1. `meta`: 取 meta 里的 `date` 或 `created`。写在页面里，作者的意图最明确。

2. `git`: 取文件首次提交的 git blob 哈希的时间戳。真实的时刻，编辑后不变，重命名后不变。

3. `mtime`: 取文件的修改时间。真实的时刻，编辑后会变，重命名后不变。

///

## 时区规则

同一个 `timezone` 设置，对不同来源的日期做的事**不一样**。

///tab | **git / mtime - 换算**

```
commit -> 2026-04-03T10:00:00+00:00
timezone: Asia/Shanghai
feed -> Fri, 03 Apr 2026 18:00:00 +0800 <-- 小时数变了
```
///

///tab | **meta - 贴标签**
```
date: 2026-04-03T12:00:00+00:00
timezone: Asia/Shanghai
feed -> Fri, 03 Apr 2026 12:00:00 +0800 <-- 小时数不变
```
///

> [!quete]- **第二条规则为什么这样定？**
> 
> meta 里的时间是手动的，一般作者都会下意识写当地时区或者常用时区，所以如果把 meta 里面的时间也加入时区换算会让所有手动标记时间的文章日期集体偏移。

> [!quete]- **Git 历史**
>
> git 日志只扫**一遍**，不是每个页面调一次 git，几千页的站点上，按页 spawn 进程的开销会直接主导构建时间。
>
> 重命名会被跟随（等价于批量的 `git log --follow`），移动过位置的文章保留原始创建日期。
>
> 浅克隆（`--depth 1`）里没有真实的首次提交，所有文件看起来都是同一天创建的。插件检测到时会告警。CI 里加上：
>
> ```yaml
> - uses: actions/checkout@v4
>   with:
>     fetch-depth: 0
> ```
>
> 不在 git 仓库里、或文件还没提交过时，自动回退到下一个来源。

## 整体迁移的仓库

如果仓库是把已有内容一次性导入建起来的，git 历史对「什么时候写的」一无所知。所有文件的首次提交都是那一次导入。所以加入了 `git_history_valid_after` 配置项，用于指定**截断点**，满足**任意一条**时就丢弃 git 给出的创建日期：

- 页面 meta 里**声明**的日期早于或等于截断点，是旧内容，只是很晚才提交
- 文件的**首次提交**早于或等于截断点，它是随导入一起进来的

```yaml
plugins:
  - feed:
      date_priority: [git, meta]
      git_history_valid_after: 2026-01-26T23:19:30+00:00
```

两条都需要。只看提交时间，会漏掉一篇 2023 年写、迁移一年后才提交的文章；只看声明日期，会漏掉一个根本没写日期的导入文件。

Git 被丢弃后，解析继续走下一个来源。最后一次提交仍然用于 `updated`，但不允许顶替创建时间，那会悄悄把截断规则撤销掉。

**截断点怎么取。** 查你的导入提交：

```bash
git log --reverse --format=%aI | head -1
```

设成**刚好晚于**它的时刻。假设查出来是 `2026-01-26T23:19:20+00:00`：

| 写法 | 结果 |
| --- | --- |
| `2026-01-26T23:19:30+00:00` | ✅ 正确 |
| `2026-01-26T23:19:30+08:00` | ❌ 早了 8 小时，一条都匹配不到 |

`+00:00` 换成 `+08:00` 是**另一个时刻**，不是同一时间的另一种写法。不写偏移量时按 `timezone` 解释。

## 分类

`<category>` 取自 meta 的 `categories` 和 `tags`，前者是 blog 插件用的，后者是 tags 插件用的。标量和列表都可以，重复值会去掉。

```yaml
---
categories: [Nginx]
tags: [运维, 反向代理]
---
```

```xml
<category>Nginx</category>
<category>运维</category>
<category>反向代理</category>
```

## 频道图标

`<image>` 是阅读器在订阅源旁边显示的图标。取自 `theme.logo`；如果 logo 配的是图标名而不是路径，退回 `theme.favicon`。两个都没配就不输出。

```xml
<image>
  <url>https://example.com/assets/avatar.png</url>
  <title>站点名</title>
  <link>https://example.com/</link>
</image>
```

> [!quete]- **image 元素里的 title 和 link 跟 channel 重复了？**
>
> 这是 RSS 2.0 规范要求的，不是冗余。规范原文：
>
> *"Note, in practice the image `<title>` and `<link>` should have the same value as the channel's `<title>` and `<link>`."*
>
> 设计意图是让 `<image>` 成为可以独立取出来渲染的完整单元，阅读器把它当作「点图跳站点」的一块。删掉这两个子元素会让 `<image>` 变成非法结构。

## 多语言站点

配合 [mkdocs-static-i18n](https://github.com/ultrabug/mkdocs-static-i18n) 时，每种语言得到自己的一份 feed，不需要额外配置：

```
site/
├── rss.xml          # 默认语言（发布在站点根目录的那个）
├── en/
│   └── rss.xml      # 其他语言各一份
```

每份 feed 里 `<language>`、`<atom:link rel="self">`、`<link>` 各自正确，条目只包含该语言的页面。每个页面 `<head>` 里注入的链接也指向同语言的那一份。

排除规则跨语言生效，匹配前会剥掉语言前缀，一条 `exclude: [about/legal]` 同时覆盖 `en/about/legal/` 和 `zh/about/legal/`。

## GUID

阅读器判断「这条我读过没有」的唯一依据。用的是**文件首次提交时的 git blob 哈希**，`isPermaLink="false"`。

为什么不是别的：

- **不用 commit 哈希**: 一次提交经常同时新增好几个页面，它们会拿到相同的 guid，阅读器会合并成一条。实测某真实站点：50 篇文章只有 35 个不同的 commit 哈希，20 篇碰撞，其中 12 篇共享同一个导入提交
- **不用当前的 blob 哈希**: 每编辑一次就变一次，等于每次改错别字都向全体订阅者重新推送
- **不用 URL**: 一改 slug 或 `post_url_format`，所有旧条目失效、全部重新通知

首次提交的 blob 哈希同时满足：每个页面唯一、编辑后不变、重命名后不变。
