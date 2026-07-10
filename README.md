# 这是我个人博客的源码仓库

![views](https://views.whatilearened.today/views/github/liWanr/liWanr.github.io.svg)

## 地址矩阵

[**Myself**](https://liwanr.com) ｜
[**LocalSite**](http://local.liwanr.com:24) ｜
[**GitHub Page**](https://liwanr.github.io/)

## 构建方式

### Netlify（弃用）

- Netlify 的构建命令
  
  ```Bash
  pip install zensical && zensical build --clean && python custom_fixes.py
  ```

### Vercel（弃用）

- Vercel 的构建命令
  
  ```Bash
  python -m venv .venv && . .venv/bin/activate && pip install zensical && zensical build --clean && python custom_fixes.py
  ```

### 本地构建

- 激活方式 `source ../.env/zensical/bin/activate`
  
  退出激活 `deactivate`

- 边写边预览 `zensical serve`

- 编译 `zensical build`

  - 清除缓存并编译 `zensical build -c`
    
  - 指定编译目录 `zensical build -f`

## 脚本说明

- **`build.sh`**: 预览、部署及更新架构三合一脚本，并且部署后允许将站点文件复制到 Nginx 指定目录

- **`custom_fixes.py`**（原 `change.py`）

  - 功能1：删除主页面 `index.html` 中的文档地址按钮、标题锚点图标 `headerlink`、二级标题的锚点 `id`，以及一级标题整体

  - 功能2：将所有页面中 GitHub 仓库地址里的 `raw/master/docs` 统一替换为 `raw/main/docs`

  - 功能3：根据 `.gitignore` 文件中列出的 Markdown 文件路径，删除对应生成页面并同步从 `search.json` 搜索索引中移除，实现指定文章的隐藏及屏蔽站内搜索

  - 功能5：扫描 `docs/` 目录下全部 Markdown 文件（可通过 front matter `rss: no` 单篇排除）生成 rss.xml，站点信息取自 zensical.toml 的 project 配置；发布时间优先取 Git 首次提交时间，仅当文章 front matter 里的 created 早于等于 2026-01-26 23:46（北京时间）这一分界点时才直接采用该值，Git 查不到时依次回退到 created、本地文件创建时间

  - 功能6：为 `essays/` 目录下的页面，给导航栏和侧边栏中 "Essays" 对应的标签项加上高亮 `--active` 样式
  
## 博客仓库提交说明

|		类型		| 场景	|
|-----------|-------------|
|		feat		| 发布一篇新文章	|
|		update  | 更新文章内容、README	|
|		fix			| 修正文章里的错误：事实错误、代码错误	|
|		style		| 调整博客样式、布局、字体等	|
|	refactor	| 重新整理文章结构，内容不变	|
|		chore		| 更新依赖、改配置文件、加插件	|
|		perf		| 优化图片大小、加载速度等	|
|		revert	| 撤回某篇文章或某次改动	|