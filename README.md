# 这是我个人博客的源码仓库

![views](https://views.whatilearened.today/views/github/liWanr/liWanr.github.io.svg)
[![Netlify Status](https://api.netlify.com/api/v1/badges/c9edb010-2489-4b9e-8062-dcfaf9495e9e/deploy-status)](https://app.netlify.com/projects/liwanr/deploys)
![Website](https://img.shields.io/badge/Vercel-Online-brightgreen)

## 地址矩阵

[**Myself**](https://liwanr.com) ｜
[**LocalSite**](http://local.liwanr.com:24) ｜
[**GitHub Page**](https://liwanr.github.io/) ｜
[**Netlify**](https://liwanr.netlify.app/) ｜
[**Vercel**](https://liwanr.vercel.app/)

## 构建方式

### Netlify

- Netlify 的构建命令
  
  ```Bash
  pip install zensical && zensical build --clean && python custom_fixes.py
  ```

### Vercel

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

- **`change.py`** --> **`custom_fixes.py`**

  - **功能1**: 删除主页面中的文档地址按钮、标题锚点以及一级标题
 
  - **功能2**: 将所有页面中 GitHub 仓库地址的 `master` 分支路径统一替换为 `main` 分支

  - **功能3**: 为所有带有 `class="only-dark"` 或 `class="only-light"` 的图片元素，在其 src 地址后追加对应的 `#only-dark` 或 `#only-light` 哈希值

  - **功能4**: 根据 `.gitignore` 文件中列出的 Markdown 文件路径，删除对应生成页面，实现指定文章的隐藏功能

## 博客仓库提交说明

|		类型		| 场景	|
|-----------|-------------|
|		feat		| 发布一篇新文章	|
|		docs		| 更新文章内容、README	|
|		fix			| 修正文章里的错误：事实错误、代码错误	|
|		style		| 调整博客样式、布局、字体等	|
|	refactor	| 重新整理文章结构，内容不变	|
|		chore		| 更新依赖、改配置文件、加插件	|
|		perf		| 优化图片大小、加载速度等	|
|		revert	| 撤回某篇文章或某次改动	|