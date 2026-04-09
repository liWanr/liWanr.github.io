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
  pip install zensical && zensical build --clean && python change.py
  ```

### Vercel

- Vercel 的构建命令
  
  ```Bash
  python -m venv .venv && . .venv/bin/activate && pip install zensical && zensical build --clean && python change.py
  ```

### 本地构建

- 激活方式 `source ../.env/zensical/bin/activate`
  
  退出激活 `deactivate`

- 边写边预览 `zensical serve`

- 编译 `zensical build`

  - 清除缓存并编译 `zensical build -c`
    
  - 指定编译目录 `zensical build -f`

## 版本控制

- 升级 `pip install --upgrade --force-reinstall zensical`

- 显示当前版本 `pip show zensical`

## 博客仓库提交说明

| type | 场景 |
|---|---|
| feat | 发布一篇新文章 |
| fix | 修正文章里的错误（事实错误、代码错误） |
| docs | 更新 README 、博客说明页及与博客本身内容无关的文件  |
| style | 调整博客样式、布局、字体等 |
| refactor | 重新整理文章结构，内容不变 |
| chore | 更新依赖、改配置文件、加插件 |
| perf | 优化图片大小、加载速度等 |
| revert | 撤回某篇文章或某次改动 |