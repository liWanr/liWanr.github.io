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

///html | div.step

1.  

    ```markdown { linenums="0" }
    ![Docker](https://img.shields.io/badge/Docker-Ready-blue)

    ![Nginx](https://img.shields.io/badge/Nginx-ReverseProxy-green)

    ![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange)

    ![OpenWrt](https://img.shields.io/badge/OpenWrt-Supported-green)
    ```

    ///html | div.result

    ![Docker](https://img.shields.io/badge/Docker-Ready-blue)
    ![Nginx](https://img.shields.io/badge/Nginx-ReverseProxy-green)
    ![Linux](https://img.shields.io/badge/Linux-Ubuntu-orange)
    ![OpenWrt](https://img.shields.io/badge/OpenWrt-Supported-green)

    ///

1.  

    ```markdown { linenums="0" }
    <img src="https://skillicons.dev/icons?i=linux,apple,windows,markdown,docker,nginx,git,python,cloudflare">
    ```

    ///html | div.result

    <img src="https://skillicons.dev/icons?i=linux,apple,windows,markdown,docker,nginx,git,python,cloudflare">

    ///

///

///html | div.step

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

    ///html | div.result

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

    ///

2. 代码行数，会显示：commits / repos / stars / PR。[**GitHub 仓库地址**](https://github.com/anuraghazra/github-readme-stats)

    ```yaml
    name: Generate stats card

    on:
    schedule:
      - cron: "0 */01 * * *"      # 每 1 小时运行一次
    workflow_dispatch:            # 允许手动运行

    jobs:
    generate:
      runs-on: ubuntu-latest

      steps:
        - name: Checkout repo
          uses: actions/checkout@v4

        - name: Create dist folder
          run: mkdir -p dist

        - name: Generate stats card
          uses: readme-tools/github-readme-stats-action@v1
          with:
            card: stats
            options: username=liWanr&show_icons=true
            path: dist/stats.svg
            token: ${{ secrets.GITHUB_TOKEN }}

        # 输出到仓库
        - name: Push to output branch
          uses: crazy-max/ghaction-github-pages@v3
          with:
            target_branch: output
            build_dir: dist
          env:
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    ```

    ///html | div.result

    ![Stats](https://raw.githubusercontent.com/liWanr/liWanr/output/stats.svg)

    ///

3. 最常用语言，会生成语言统计图。

    ```yaml
    # ...

      steps:
        - name: Generate languages card
          uses: readme-tools/github-readme-stats-action@v1
          with:
            card: top-langs
            github_user_name: username=liWanr&layout=compact
            path: dist/top-langs.svg
            token: ${{ secrets.GITHUB_TOKEN }}

        # ... 输出到仓库
    ```

    ///html | div.result

    ![Top Langs](https://raw.githubusercontent.com/liWanr/liWanr/output/language.svg)

    ///

4. 连续提交统计，显示连续提交天数。 [**GitHub 仓库地址**](https://github.com/DenverCoder1/github-readme-streak-stats)

    ```markdown { linenums="0" }
    ![Streak](https://streak-stats.demolab.com/?user=用户名)
    ```

    ///html | div.result

    ![GitHub Streak](https://raw.githubusercontent.com/liWanr/liWanr/output/streak.svg)

    ///

5. 贪吃蛇吃贡献图, 这个需要在 `用户名仓库/.github/workflows/snake.yml` 中使用 Action 生成

    ```yaml
    # ...

      steps:
        - name: Generate snake
          uses: Platane/snk@v3
          with:
            github_user_name: liWanr
            outputs: |
              dist/snake.svg
              dist/snake-dark.svg?palette=github-dark

        # ... 输出到仓库
    ```

    ///html | div.result

    ![snake](https://raw.githubusercontent.com/liWanr/liWanr/output/snake.svg#only-light)
    ![snake](https://raw.githubusercontent.com/liWanr/liWanr/output/snake-dark.svg#only-dark)

    ///


///

///html | div.step

## 好玩组

1.  

    ```markdown { linenums="0" }
    ![views](https://views.whatilearened.today/views/github/用户名/仓库名.svg)
    ![Coffee](https://img.shields.io/badge/Buy%20Me%20a-Coffee-yellow)
    ![Website](https://img.shields.io/badge/Website-Online-brightgreen)
    ```

    ///html | div.result

    ![views](https://views.whatilearened.today/views/github/liWanr/liWanr.svg)
    ![Coffee](https://img.shields.io/badge/Buy%20Me%20a-Coffee-yellow)
    ![Website](https://img.shields.io/badge/Website-Online-brightgreen)

    ///

2. 打字动画

    ```markdown { linenums="0" }
    ![Typing SVG](https://readme-typing-svg.demolab.com/?lines=Heelo,+I'm+liWanr!;Welcome+to+my+Website.;Every+nobody+is+somebody.)
    ```

    ///html | div.result

    ![Typing SVG](https://readme-typing-svg.demolab.com/?lines=Heelo,+I'm+liWanr!;Welcome+to+my+Website.;Every+nobody+is+somebody.)

    ///

3. 活动图

    ```markdown { linenums="0" }
    ![Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=用户名)
    ```

    ///html | div.result

    ![Activity Graph](https://github-readme-activity-graph.vercel.app/graph?username=liWanr)

    ///

///
