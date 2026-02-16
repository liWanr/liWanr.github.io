---
icon: lucide/folder-archive
title: 压缩与解压
tags:
    - Server
---

- **FileName** 代表压缩包的名称

- **DirName** 代表目录的名称, 也就是准备压缩的文件夹的名称

=== "`*.tar.gz / *.tgz`"

    <div class="grid cards" markdown>

    - :material-folder-open-outline: **解压**

        ---

        ```Bash title=""
        tar -zxvf FileName.tar.gz
        ```

    - :material-folder-zip-outline: **压缩**

        ---

        ```Bash title=""
        tar -zcvf FileName.tar.gz DirName
        ```
        
    </div>

=== "`*.zip`"

    <div class="grid cards" markdown>

    - :material-folder-open-outline: **解压**

        ---

        ```bash title=""
        unzip FileName.zip -d DirName
        ```

    - :material-folder-zip-outline: **压缩**

        ---

        ```bash title=""
        zip FileName.zip DirName
        ```

    </div>

    <small>
    :octicons-light-bulb-16:
    **安装命令:** `sudo apt install zip unzip`
    </small>

=== "`*.7z`"
    
    <div class="grid cards" markdown>

    - :material-folder-open-outline: **解压**

        ---

        ```bash title=""
        7z -x FileName.7z -o/
        ```

    - :material-folder-zip-outline: **压缩**

        ---

        ```bash title=""
        7z -a FileName.7z DirName
        ```

    </div>

    <small>
    :octicons-light-bulb-16:
    **安装命令:** `sudo apt update & sudo apt install p7zip-full`
    </small>

=== "`*.rar`"

    <div class="grid cards" markdown>

    - :material-folder-open-outline: **解压**

        ---

        ```bash title=""
        rar -x FileName.rar
        ```

    - :material-folder-zip-outline: **压缩**

        ---

        ```bash title=""
        rar -a FileName.rar DirName
        ```

    </div>

    <small>
    :octicons-light-bulb-16:
    **安装方式 :** [**下载 rar**](https://www.rarlab.com/){target="_blank"}, 下载解压后将 **rar_static** 拷贝到 `/usr/bin` 目录, 其他由 **$PATH** 环境变量指定的目录也可以
    </small>

=== "`*.tar`"

    <div class="grid cards" markdown>

    - :material-folder-open-outline: **解压**

        ---

        ```bash title=""
        tar -xvf FileName.tar
        ```

    - :material-folder-zip-outline: **压缩**

        ---

        ```bash title=""
        tar -cvf FileName.tar DirName
        ```

    </div>

=== "`*.tar.xz`"

    <div class="grid cards" markdown>

    - :material-folder-open-outline: **解压**

        ---

        - 先解压 `.xz` 文件

            ```Bash title=""
            xz -d FileName.tar.xz
            ```

        - 再先解压 `.tar.xz` 文件解压出来的 `.tar`

            ```Bash title=""
            tar -xvf FileName.tar
            ```

    - :material-folder-zip-outline: **压缩**

        ---

        - 先创建 `.tar` 文件

            ```Bash title=""
            tar -cvf FileName.tar DirName
            ```

        - 再创建 `.tar.xz` 文件

            ```Bash title=""
            xz -z FileName.tar
            ```
    </div>

=== "`*.deb`"
        
    <div class="grid cards" markdown>

    - :material-folder-open-outline: **解包**

        ---

        ```bash title=""
        sudo dpkg -i FileName.deb
        ```

    </div>
