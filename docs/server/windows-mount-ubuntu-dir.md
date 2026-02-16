---
icon: material/cloud-upload-outline
title: Win 挂载 Ubuntu 目录
tags:
    - Server
---

## :simple-linux: **Ubuntu 端配置** {id="ubuntu-config"}

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
        path = # (1)!
        available = yes
        browsable = yes
        public = yes
        writable = yes
        read only = no
    ```

    1. 要挂载的目录地址，最好是绝对地址, 比如 `/home/ubuntu/shareDir`

    添加完成之后按键盘左上角的 ++esc++ 退出编辑模式，再按 ++colon++ 进入命令模式后输入 `wq!` 保存并退出。

2. 设置密码后 **重启 samba** 服务

    ``` Bash
    sudo smbpasswd -a # (1)!
    sudo systemctl restart smbd
    ```

    1. 用户名

## :fontawesome-brands-windows: **Windows 端挂载** {id="windows-mount"}

1. 添加位置: 打开 **此电脑** -> **右键空白处** -> **添加一个网络位置**

2. 路径格式:

    ```st
    \\"# (1)!"\UbuntuShare
    ```

    1. 需要挂载的 Ubuntu 的 IP, 比如 `\\192.168.1.2\UbuntuShare`

3. 凭据登录: 输入设置的 **Ubuntu 用户名** 与 **Samba 密码** 就好了
