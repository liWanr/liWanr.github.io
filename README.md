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

## 杀掉被占用的进程

- `sudo lsof -i :8000`

- `sudo kill -9` PID