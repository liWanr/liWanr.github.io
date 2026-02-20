---
icon: simple/openvpn
title: 使用 OpenVPN Client
# date:
#     created: 2025-03-16
tags:
    - Factoid
---

## :simple-linux: **Linux**

1. :fontawesome-solid-download: **安装**

    ```Bash
    sudo apt install openvpn
    ```

2. :material-lan-connect: **使用**

    ```Bash
    sudo openvpn --config *.ovpn
    ```

## :fontawesome-brands-windows: **Windows**

1. :fontawesome-solid-cloud-download: **下载：** 在 [**OpenVPN Connect 官网**](https://openvpn.net/client/) 下载官方现代 GUI 客户端, 支持Windows 10 / 11。有 64-bit 和 32-bit 版, 界面简洁、自动更新、支持最新协议。

2. :fontawesome-solid-download: **安装：** 下载安装完后打开 **OpenVPN Connect 客户端** 。

3. :material-lan-connect: **使用：** 打开后点击 `Import Profile` 或将 `*.ovpn` 拖拽进窗口进行导入, 然后点击 Connect 连接即可。

## :simple-apple: **macOS**

1. :fontawesome-solid-cloud-download: **下载：** 在 [**OpenVPN Connect 官网**](https://openvpn.net/client/) 下载官方现代 GUI 客户端, 支持 macOS Big Sur (11) 到最新的 Sonoma/Sequoia/Tahoe。官方维护、界面友好、支持 Apple Silicon (M 系列) 和 Intel。

2. :fontawesome-solid-download: **安装：** 下载 .dmg 文件后, 打开并拖到 Applications 文件夹安装。

3. :material-lan-connect: **使用：** 打开后点击 `Import Profile` 或将 `*.ovpn` 拖拽进窗口进行导入, 然后点击 Connect 连接即可。