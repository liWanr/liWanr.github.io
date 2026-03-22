---
icon: simple/markdown
title: 激活 Typora
# date:
#   created: 2026-03-21
hide:
    - toc
---

!!! warning "仅适用于 `1.0.3` 版本的 Typora"

    - [**通用激活文件**](https://liwanr.com/public/Tec/app.asar) | [**Typora v1.0.3 For Ubuntu/Debian**](https://liwanr.com/public/Tec/typora_1.0.3_amd64.deb) | [官网下载地址](https://typora.io/releases/all) | [Windows 绿色版](https://liwanr.com/public/Tec/Typora%201.4.8.7z)

    - 本教程 Ubuntu/Debian 可以无脑 CV，其他 Linux/Mac 按流程激活, Windows 直接下载即可使用

1. 安装

    ```Bash
    sudo dpkg -i typora_1.0.3_amd64.deb
    ```

2. 备份原文件

    ```Bash
    sudo cp /usr/share/typora/resources/app.asar /usr/share/typora/resources/app.asar.bak
    ```

3. 替换文件

    ```Bash
    sudo cp ./app.asar /usr/share/typora/resources/app.asar
    ```

4. 打开 Typora 软件, 在「帮助 - 我的许可证 - 序列号激活」中**随便填写邮箱**, 填 `a@a.a` 都可以, 然后序列号从以下几个中随便挑一个粘贴激活就行了

    <div class="grid cards" markdown>

    ```Bash
    DZTX2H-6MCQZT-QL4GCT-5EBWFX
    ```

    </div>

    <div class="grid cards" markdown>

    ```Bash
    G7LPKN-HP4NLD-FA3BGF-6JDQ5R
    ```

    ```Bash
    3MH4Y8-YJWT37-G5JL9Y-UHNQDJ
    ```

    ```Bash
    85ZPHY-ELQ9FQ-94J3VP-D92YLU
    ```

    ```Bash
    VEZ7NV-USYN3G-8TL2N3-DADUG4
    ```

    </div>