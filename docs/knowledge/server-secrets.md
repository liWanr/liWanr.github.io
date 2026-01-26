---
tags:
    - Server
---

# 服务器秘籍 {id=" "}



## 压缩与解压 {id="Compression-Decompression"}

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


## :simple-openvpn: OpenVPN Client {id="OpenVPN-client"}

=== ":simple-linux: **Linux**"

    1. :fontawesome-solid-download: **安装**

        ```bash title=""
        sudo apt install openvpn
        ```
    
    2. :material-lan-connect: **使用**

        ```bash title=""
        sudo openvpn --config *.ovpn
        ```

=== ":fontawesome-brands-windows: **Windows**"

    1. :fontawesome-solid-cloud-download: **下载：** 在 [**OpenVPN Connect 官网**](https://openvpn.net/client/){target="_blank"} 下载官方现代 GUI 客户端, 支持Windows 10 / 11。有 64-bit 和 32-bit 版, 界面简洁、自动更新、支持最新协议。

    2. :fontawesome-solid-download: **安装：** 下载安装完后打开 **OpenVPN Connect 客户端** 。
    
    3. :material-lan-connect: **使用：** 打开后点击 `Import Profile` 或将 `*.ovpn` 拖拽进窗口进行导入, 然后点击 Connect 连接即可。

=== ":simple-apple: **macOS**"

    1. :fontawesome-solid-cloud-download: **下载：** 在 [**OpenVPN Connect 官网**](https://openvpn.net/client/){target="_blank"} 下载官方现代 GUI 客户端, 支持 macOS Big Sur (11) 到最新的 Sonoma/Sequoia/Tahoe。官方维护、界面友好、支持 Apple Silicon (M 系列) 和 Intel。

    2. :fontawesome-solid-download: **安装：** 下载 .dmg 文件后, 打开并拖到 Applications 文件夹安装。
    
    3. :material-lan-connect: **使用：** 打开后点击 `Import Profile` 或将 `*.ovpn` 拖拽进窗口进行导入, 然后点击 Connect 连接即可。
