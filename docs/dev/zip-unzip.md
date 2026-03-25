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

///html | div.grid.cards

-   **FileName**

    代表压缩包的名称

-   **DirName**
    
    目录名, 也就是准备压缩的文件夹

///

///html | div.grid.cards

-   ## tar.gz / tgz
    
    ///tab | :material-folder-open-outline: **解压**
    ```Bash { linenums="0" }
    tar -zxvf FileName.tar.gz
    ```
    ///

    ///tab | :material-folder-zip-outline: **压缩**
    ```Bash { linenums="0" }
    tar -zcvf FileName.tar.gz DirName
    ```
    ///

///

///html | div.grid.cards
-   ## zip
    
    ///tab | :material-folder-open-outline: **解压**

    ```Bash { linenums="0" }
    unzip FileName.zip -d DirName
    ```

    ///

    ///tab | :material-folder-zip-outline: **压缩**

    ```Bash { linenums="0" }
    zip FileName.zip DirName
    ```

    ///

    ///html | small

    :octicons-light-bulb-16:
    `sudo apt install zip unzip`

    ///

-   ## 7z
    
    ///tab | :material-folder-open-outline: **解压**

    ```Bash { linenums="0" }
    7z -x FileName.7z -o/
    ```

    ///

    ///tab | :material-folder-zip-outline: **压缩**

    ```Bash { linenums="0" }
    7z -a FileName.7z DirName
    ```

    ///
    
    ///html | small
    :octicons-light-bulb-16:
    `sudo apt update & sudo apt install p7zip-full`
    ///

-   ## rar
    
    ///tab | :material-folder-open-outline: **解压**

    ```Bash { linenums="0" }
    rar -x FileName.rar
    ```

    ///

    ///tab | :material-folder-zip-outline: **压缩**

    ```Bash { linenums="0" }
    rar -a FileName.rar DirName
    ```
    
    ///
    
    ///html | small
    :octicons-light-bulb-16:
    [**下载 rar**](https://www.rarlab.com/), 教程自己找。
    ///

-   ## tar
    
    ///tab | :material-folder-open-outline: **解压**

    ```Bash { linenums="0" }
    tar -xvf FileName.tar
    ```

    ///

    ///tab | :material-folder-zip-outline: **压缩**

    ```Bash { linenums="0" }
    tar -cvf FileName.tar DirName
    ```
    
    ///
    
    ///html | small
    :octicons-light-bulb-16:
    `sudo apt update & sudo apt install p7zip-full`
    ///

///

///html | div.grid.cards

-   ## tar.xz
    
    ///tab | :material-folder-open-outline: **解压**

    ///html | div.step

    1. 先解压 `.xz` 文件

        ```Bash { linenums="0" }
        xz -d FileName.tar.xz
        ```

    2. 再先解压 `.tar.xz` 文件解压出来的 `.tar`

        ```Bash { linenums="0" }
        tar -xvf FileName.tar
        ```

    ///
    
    ///

    ///tab | :material-folder-zip-outline: **压缩**

    ///html | div.step

    1. 先创建 `.tar` 文件

        ```Bash { linenums="0" }
        tar -cvf FileName.tar DirName
        ```

    2. 再创建 `.tar.xz` 文件

        ```Bash { linenums="0" }
        xz -z FileName.tar
        ```

    ///

    ///
    
    ///html | small

    :octicons-light-bulb-16:
    `sudo apt update & sudo apt install p7zip-full`

    ///

///