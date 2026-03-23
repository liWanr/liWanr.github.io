---
icon: lucide/badge
title: GitHub 徽章
# date:
#     created: 2025-03-23
tags:
    - Tech
comments: true
---

## 前言

- [**生成网站**](https://shields.io/)

## 技术栈徽

1.  

    ```markdown { linenums="0" }
    ![Docker](https://img.shields.io/badge/Docker-Ready-blue)

    ![Nginx](https://img.shields.io/badge/Nginx-ReverseProxy-green)

    ![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange)

    ![OpenWrt](https://img.shields.io/badge/OpenWrt-Supported-green)
    ```

    <div class="result" markdown>

    ![Docker](https://img.shields.io/badge/Docker-Ready-blue)
    ![Nginx](https://img.shields.io/badge/Nginx-ReverseProxy-green)
    ![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange)
    ![OpenWrt](https://img.shields.io/badge/OpenWrt-Supported-green)

    </div>

1.  

    ```markdown { linenums="0" }
    <img src="https://skillicons.dev/icons?i=linux,apple,windows,markdown,docker,nginx,git,python,cloudflare">
    ```

    <div class="result" markdown>

    <img src="https://skillicons.dev/icons?i=linux,apple,windows,markdown,docker,nginx,git,python,cloudflare">

    </div>

## 实用组

1.  

    ```markdown { linenums="0" }
    ![Stars](https://img.shields.io/github/stars/用户名/仓库名)
    ![Forks](https://img.shields.io/github/forks/用户名/仓库名)
    ![Release](https://img.shields.io/github/v/release/用户名/仓库名)
    ![License](https://img.shields.io/github/license/用户名/仓库名)

    ![File Count](https://img.shields.io/github/directory-file-count/用户名/仓库名)
    ![Repo Size](https://img.shields.io/github/repo-size/用户名/仓库名)
    ![Last Commit](https://img.shields.io/github/last-commit/用户名/仓库名)
    ![Downloads](https://img.shields.io/github/downloads/用户名/仓库名/total)
    ![Commit Activity](https://img.shields.io/github/commit-activity/m/用户名/仓库名)

    ![Created](https://img.shields.io/github/created-at/用户名/仓库名)
    ![Release](https://img.shields.io/github/v/release/用户名/仓库名)
    ![Tags](https://img.shields.io/github/v/tag/用户名/仓库名)
    ![Contributors](https://img.shields.io/github/contributors/用户名/仓库名)
    ```

    <div class="result" markdown>

    ![Stars](https://img.shields.io/github/stars/krahets/hello-algo)
    ![Forks](https://img.shields.io/github/forks/krahets/hello-algo)
    ![Followers](https://img.shields.io/github/followers/liWanr?style=social)

    ![Release](https://img.shields.io/github/v/release/krahets/hello-algo)
    ![License](https://img.shields.io/github/license/krahets/hello-algo)
    ![Last Commit](https://img.shields.io/github/last-commit/liWanr/liWanr.github.io)

    ![File Count](https://img.shields.io/github/directory-file-count/liWanr/liWanr.github.io)
    ![Repo Size](https://img.shields.io/github/repo-size/liWanr/liWanr.github.io)
    ![Downloads](https://img.shields.io/github/downloads/krahets/hello-algo/total)
    ![Commit Activity](https://img.shields.io/github/commit-activity/m/liWanr/liWanr.github.io)

    ![Created](https://img.shields.io/github/created-at/krahets/hello-algo)
    ![Tags](https://img.shields.io/github/v/tag/krahets/hello-algo)
    ![Contributors](https://img.shields.io/github/contributors/krahets/hello-algo)

    </div>

2. 代码行数，会显示：commits / repos / stars / PR

    ```markdown { linenums="0" }
    ![Stats](https://github-readme-stats.vercel.app/api?username=用户名)
    ```

    <div class="result" markdown>

    ![Stats](https://github-readme-stats.vercel.app/api?username=liWanr)

    </div>

3. 最常用语言，会生成语言统计图。

    ```markdown { linenums="0" }
    ![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=用户名)
    ```

    <div class="result" markdown>

    ![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=liWanr)

    </div>

4. 连续提交统计，显示连续提交天数

    ```markdown { linenums="0" }
    ![Streak](https://streak-stats.demolab.com/?user=用户名)
    ```

    <div class="result" markdown>

    ![Streak](https://streak-stats.demolab.com/?user=liWanr)

    </div>

5. 贪吃蛇吃贡献图, 这个需要在 `用户名仓库/.github/workflows/snake.yml` 中使用 Action 生成

    ```markdown { linenums="0" }
    ![snake](https://raw.githubusercontent.com/用户名/用户名/output/github-contribution-grid-snake.svg)
    ```

    <div class="result" markdown>

    ![snake](https://raw.githubusercontent.com/liWanr/liWanr/output/github-contribution-grid-snake.svg)

    </div>

    ```yml
    name: Generate Snake

    on:
    schedule:
        - cron: "0 */01 * * *"      # 每 1 小时运行一次
    workflow_dispatch:              # 允许手动运行

    jobs:
    generate:
        runs-on: ubuntu-latest

        steps:
        - name: Generate snake
            uses: Platane/snk@v3
            with:
            github_user_name:       # 用户名
            outputs: |
                dist/github-contribution-grid-snake.svg
                dist/github-contribution-grid-snake-dark.svg?palette=github-dark

        - name: Push to output branch
            uses: crazy-max/ghaction-github-pages@v3
            with:
            target_branch: output   # 分支
            build_dir: dist
            env:
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    ```

## 好玩组

1.  

    ```markdown { linenums="0" }
    ![views](https://views.whatilearened.today/views/github/用户名/仓库名.svg)
    ![Coffee](https://img.shields.io/badge/Buy%20Me%20a-Coffee-yellow)
    ![Website](https://img.shields.io/badge/Website-Online-brightgreen)
    ```

    <div class="result" markdown>

    ![views](https://views.whatilearened.today/views/github/liWanr/liWanr.svg)
    ![Coffee](https://img.shields.io/badge/Buy%20Me%20a-Coffee-yellow)
    ![Website](https://img.shields.io/badge/Website-Online-brightgreen)

    </div>

2. 打字动画

    ```markdown { linenums="0" }
    ![Typing SVG](https://readme-typing-svg.demolab.com/?lines=Heelo,+I'm+liWanr!;Welcome+to+my+Website.;Every+nobody+is+somebody.)
    ```

    <div class="result" markdown>

    ![Typing SVG](https://readme-typing-svg.demolab.com/?lines=Heelo,+I'm+liWanr!;Welcome+to+my+Website.;Every+nobody+is+somebody.)

    </div>

3. 活动图

    ```markdown { linenums="0" }
    ![Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=用户名)
    ```

    <div class="result" markdown>

    ![Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=liWanr)

    </div>