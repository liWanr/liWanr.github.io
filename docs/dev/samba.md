---
icon: lucide/database
title: Samba
# date:
#     created: 2026-02-13
tags:
    - Factoid
comments: true
---

## :simple-linux: Ubuntu 端配置 {id="ubuntu-config"}

///html | div.step

1. 安装 Samba 之后 **修改 samba 配置**, 并在末尾 **添加挂载信息**

    ```Bash
    sudo apt update
    sudo apt install samba -y
    ```

    ```Bash
    sudo vim /etc/samba/smb.conf
    ```

    ```conf title="挂载信息"
    [UbuntuShare]
        path = /home/ubuntu/shareDir # (1)!
        available = yes
        browsable = yes
        public = yes
        writable = yes
        read only = no
    ```

    1. 要挂载的目录地址，最好是绝对地址

    添加完成之后按键盘左上角的 ++esc++ 退出编辑模式，再按 ++colon++ 进入命令模式后输入 `wq!` 保存并退出。

2. 设置密码后 **重启 samba** 服务

    ``` Bash
    sudo smbpasswd -a ubuntu # (1)!
    sudo systemctl restart smbd
    ```

    1. ubuntu 代表用户名

///

## :fontawesome-brands-windows: Windows 端挂载 {id="windows-mount"}

///html | div.step

1. 添加位置: 打开 **此电脑** -> **右键空白处** -> **添加一个网络位置**

2. 路径格式:

    ```st { linenums="0" }
    \\192.168.1.2"# (1)!"\UbuntuShare
    ```

    1. 需要挂载的 Ubuntu 的 IP

3. 凭据登录: 输入设置的 **Ubuntu 用户名** 与 **Samba 密码** 就好了

///

## :material-apple-finder: MacOS 端挂载

///html | div.step

1. 打开 Finder, 在顶部菜单点击 「前往 - 连接服务器」 或者使用快捷键 ++command+k++

2. 在服务器地址输入： `smb://服务器IP/共享名`, `smb://192.168.1.10/share` 或者 `smb://username@192.168.1.10/share` 都可以

3. 然后就是连接、输入密码之类的了

///