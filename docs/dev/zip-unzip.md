---
icon: lucide/folder-archive
title: 压缩与解压
# date:
#     created: 2024-10-26
#     updated: 2025-12-22
tags:
    - Factoid
comments: true
---

- **FileName** 代表压缩包的名称

- **DirName** 代表目录的名称, 也就是准备压缩的文件夹的名称


///html | div.grid.cards

-   ## tar.gz / tgz
    
    === ":material-folder-open-outline: **解压**"

        ```Bash
        tar -zxvf FileName.tar.gz
        ```

    === ":material-folder-zip-outline: **压缩**"

        ```Bash
        tar -zcvf FileName.tar.gz DirName
        ```
        
///

///html | div.grid.cards

-   ## zip
    
    === ":material-folder-open-outline: **解压**"

        ```bash
        unzip FileName.zip -d DirName
        ```

    === ":material-folder-zip-outline: **压缩**"

        ```bash
        zip FileName.zip DirName
        ```

    ///html | small
    :octicons-light-bulb-16:
    **安装命令:** `sudo apt install zip unzip`
    ///

///

///html | div.grid.cards

-   ## 7z
    
    === ":material-folder-open-outline: **解压**"

        ```bash
        7z -x FileName.7z -o/
        ```

    === ":material-folder-zip-outline: **压缩**"

        ```bash
        7z -a FileName.7z DirName
        ```
    
    ///html | small
    :octicons-light-bulb-16:
    **安装命令:** `sudo apt update & sudo apt install p7zip-full`
    ///

///

///html | div.grid.cards

-   ## rar
    
    === ":material-folder-open-outline: **解压**"

        ```bash
        rar -x FileName.rar
        ```

    === ":material-folder-zip-outline: **压缩**"

        ```bash
        rar -a FileName.rar DirName
        ```
    
    ///html | small
    :octicons-light-bulb-16:
    **安装方式 :** [**下载 rar**](https://www.rarlab.com/), 下载解压后将 **rar_static** 拷贝到 `/usr/bin` 目录, 其他由 **$PATH** 环境变量指定的目录也可以
    ///

///

///html | div.grid.cards

-   ## tar
    
    === ":material-folder-open-outline: **解压**"

        ```bash
        tar -xvf FileName.tar
        ```

    === ":material-folder-zip-outline: **压缩**"

        ```bash
        tar -cvf FileName.tar DirName
        ```
    
    ///html | small
    :octicons-light-bulb-16:
    **安装命令:** `sudo apt update & sudo apt install p7zip-full`
    ///

///

///html | div.grid.cards

-   ## tar.xz
    
    === ":material-folder-open-outline: **解压**"

        - 先解压 `.xz` 文件

            ```Bash
            xz -d FileName.tar.xz
            ```

        - 再先解压 `.tar.xz` 文件解压出来的 `.tar`

            ```Bash
            tar -xvf FileName.tar
            ```

    === ":material-folder-zip-outline: **压缩**"

        - 先创建 `.tar` 文件

            ```Bash
            tar -cvf FileName.tar DirName
            ```

        - 再创建 `.tar.xz` 文件

            ```Bash
            xz -z FileName.tar
            ```
    
    ///html | small
    :octicons-light-bulb-16:
    **安装命令:** `sudo apt update & sudo apt install p7zip-full`
    ///

///

///html | div.grid.cards

-   ## deb
    
    === ":material-folder-open-outline: **解压**"

        ```bash
        sudo dpkg -i FileName.deb
        ```

///