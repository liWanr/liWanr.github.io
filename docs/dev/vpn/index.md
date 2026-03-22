---
icon: simple/openwrt
title: VPN
# date:
#     created: 2026-03-08
#     uodated: 2026-03-22
tags:
    - Net
    - Factoid
hide:
    - toc
comments: true
---

<h1>
ImmortalWrt
</h1>

去 [**ImmortalWrt 设备搜索地址**](https://firmware-selector.immortalwrt.org/) 中查找支持设备。以下是我用的版本信息

| 项目 | 版本 |
|-|-|
| 硬件 | FriendlyElec NanoPi R4S |
| 架构 | ARMv8 Processor rev 4 (v8l) x 6 (1416MHz 600MHz, 39.4°C) |
| 目标平台 | rockchip/armv8 |
| 固件镜像 | SYSUPGRADE (SQUASHFS) |
| 固件版本 | ImmortalWrt 24.10.5 r33805-7c4e882aaf6f / LuCI openwrt-24.10 branch 26.042.32088~3dc9a84 |
| 内核版本 | 6.6.122 |

以下是我加装的软件包, 可以是其他版本。**「上传」**要按照表从上往下的顺序上传, 比如 `lucky` --> `luci-app-lucky` --> `luci-i18n-lucky-zh-cn`

|软件包|版本|安装方式|备注|
|-|-|:-:|:-:|
| `luci-app-homeproxy` | 25.318.35044~0706fa8 | 『过滤器』 搜索 | - |
| `luci-i18n-homeproxy-zh-cn` | 25.318.34996~d3f7643 | 『过滤器』 搜索 | - |
| `wireguard-tools` | 1.0.20210914-r4 | 『过滤器』 搜索 | - |
| `kmod-wireguard` | 6.6.122-r1 | 『过滤器』 搜索 | - |
| `luci-proto-wireguard` | 26.034.21587~e6b2055 | 『过滤器』 搜索 | - |
| `luci-app-openvpn-server` | 3.0-r0 | 终端下载 | `opkg install luci-app-openvpn-server` |
| `luci-i18n-openvpn-server-zh-cn` | 25.306.51720~a833d72 | 终端下载 | `opkg install luci-i18n-openvpn-server-zh-cn` |
| `lucky` | 2.19.4-1 | 『上传软件包』 | [**GitHub Releases**](https://github.com/gdy666/luci-app-lucky/releases/tag/v2.19.5) \| 文件名 `*_Openwrt_*.ipk` |
| `luci-app-lucky` | 2.2.2-r1 | 『上传软件包』 | 文件名 `luci-app-lucky_2.2.2-r1_all.ipk` |
| `luci-i18n-lucky-zh-cn` | 25.051.13443~e78d498 | 『上传软件包』 | 文件名 `luci-i18n-lucky-zh-cn_*_all.ipk` |