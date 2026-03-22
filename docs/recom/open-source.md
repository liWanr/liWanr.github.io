---
icon: lucide/star
title: 屌爆了的开源项目
# date:
#     created: 2025-12-16
#     updated: 2026-03-11
comments: true
---

<style>
hr {
    height: 0.125rem;
    border-radius: 5px;
    background-color: var(--md-accent-fg-color);
}
</style>

## 网络

### Nexttrace

:lucide-mouse-pointer-click: [**GitHub地址**](https://github.com/nxtrace/NTrace-core) | [**发布页**](https://github.com/nxtrace/NTrace-core/releases) | [**官网地址**](https://www.nxtrace.org/)

现代化的**网络路径追踪**工具, 主要用来查看数据包从你的设备到目标服务器之间经过了哪些节点, 以及每一跳的延迟情况。

- 支持平台: Windows / macOS / Linux

- 开源协议: GPL-3.0 license

<div class="grid" markdown>

```Bash { title="Linux 常见的一键安装" }
curl nxtrace.org/nt | bash
```

```Bash { title="Mac Homebrew 安装" }
brew install nexttrace
```

</div>

```Bash { title="案例运行" }
nexttrace google.com
```

### enhanced-FaaS-in-China

:lucide-mouse-pointer-click: [**GitHub 仓库地址**](https://github.com/xingpingcn/enhanced-FaaS-in-China)

只需将 CNAME 记录从官方记录更改为我制作的记录, 即可提高托管在 Cloudflare、Vercel 或 Netlify 上的网页在中国的访问速度和稳定性。

提升部署在 cloudflare、vercel 或 netlify 的网页在中国的访问速度和稳定性

- 开源协议: MIT license

---

## AI 工具

### Vibe Coding cn

:lucide-mouse-pointer-click: [**GitHub 仓库地址**](https://github.com/2025Emma/vibe-coding-cn)
| [**TG 交流群**](https://t.me/glue_coding)
| [**TG 频道**](https://t.me/tradecat_ai_channel)

Vibe Coding = 规划驱动 + 上下文固定 + AI 结对执行, 让「从想法到可维护代码」变成一条可审计的流水线, 而不是一团无法迭代的巨石文件。旨在帮助开发者丝滑地将想法变为现实。本指南详细介绍了从项目构思、技术选型、实施规划到具体开发、调试和扩展的全过程, 强调以规划驱动和模块化为核心, 避免让 AI 失控导致项目混乱。

- 开源协议: Security & MIT license

---

## 代理

### gh-proxy

:lucide-mouse-pointer-click: [**GitHub 仓库地址**](https://github.com/hunshcn/gh-proxy)

用于加速 GitHub 资源访问和下载的开源代理项目, 主要通过代理或缓存 GitHub 的文件、发布包、源码归档等内容来提升访问速度和稳定性。

- 开源协议: MIT license

### sing-box 一键安装 & 管理脚本

:lucide-mouse-pointer-click: [**GitHub 仓库地址**](https://github.com/233boy/sing-box) ｜ [**作者教程**](https://233boy.com/sing-box/sing-box-script/)

基于 sing-box 的「一键安装 & 管理脚本」, 自动完成安装、更新、配置等工作。脚本会自动创建 REALITY 配置, 适合新手快速搭建多协议并存的科学上网节点。

设计理念强调「高效率、超快速、极易用」, 能自动处理 TLS 证书（Caddy 实现）, 并内置伪装网站反代（如访问域名时显示正常网页）。兼容所有sing-box原生命令, 还提供BBR一键开启、日志管理、核心/脚本更新等功能。

- 开源协议: GPL-3.0 license

- 支持平台: **Ubuntu** / Debian / CentOS(慎用, 可能无法正常运行)

- 支持协议: Vless / Hysteria2 / Shadowsocks / Socks 等20个协议

```Bash
bash <(wget -qO- -o- https://github.com/233boy/sing-box/raw/main/install.sh)
```

### Clash Verge Rev

:lucide-mouse-pointer-click: [**GitHub 仓库地址**](https://github.com/clash-verge-rev/clash-verge-rev)
| [**发布页**](https://github.com/clash-verge-rev/clash-verge-rev/releases)
| [**TG 频道**](https://t.me/clash_verge_re)

基于开源的 Clash Verge（项目已归档）重开发的跨平台代理客户端, 采用现代化图形界面和增强功能。它由社区持续维护更新, 继承了原版的易用性, 同时集成了最新的 Clash Meta 内核和高级配置管理, 适合 Windows、macOS 和 Linux 平台用户使用。

- 开源协议: GNU GPL‑3.0

- 支持平台: Windows / macOS / Linux 等桌面操作系统（跨平台）

- 核心内核: 基于 Clash Meta（mihomo） 内核, 支持切换到 Alpha 版本内核, 提供现代网络协议和规则处理能力

- 支持协议: 兼容主流代理协议, 包括 Shadowsocks（SS）、ShadowsocksR（SSR）、SOCKS、Snell、V2Ray（VMess/VLESS）、Trojan 等；具体支持视内核版本和构建而定

### Clash Meta for Android
    
:lucide-mouse-pointer-click: [**GitHub 仓库地址**](https://github.com/MetaCubeX/ClashMetaForAndroid)
| [**发布页**](https://github.com/MetaCubeX/ClashMetaForAndroid/releases)


基于开源的 Clash Meta（又名 Mihomo） 内核开发的 Android 客户端, 提供图形化界面和丰富的网络代理功能。它持续维护更新, 相比原版 Clash for Android（已停止维护）, 兼容性更强、协议支持更丰富, 并且支持复杂的流量分流规则。

- 开源许可证: GNU GPL‑3.0

- 支持平台: Android （通常需要 Android 5.0 或更高版本）

- 核心内核: 基于 Clash Meta（Mihomo）开发, 提供更强的现代网络协议支持

- 支持协议: 兼容包括 V2Ray（VMess/VLESS）、Shadowsocks / ShadowsocksR、Trojan、SOCKS 以及其它现代或扩展协议（如 Hysteria 等）。具体支持情况取决于内核版本和构建配置

---

## 通信

### LocalSend

:lucide-mouse-pointer-click: [**GitHub 仓库地址**](https://github.com/localsend/localsend)
| [**官网地址**](https://localsend.org/)
| [**发布页**](https://github.com/localsend/localsend/releases)
| [**Discord**](https://discord.gg/GSRWmQNP87)

跨平台应用程序, 使用 REST API 和 HTTPS 加密实现设备之间的安全通信。与依赖外部服务器的其他消息应用程序不同, LocalSend 不需要互联网连接或第三方服务器, 因此成为本地通信的快速可靠解决方案。

- 开源协议: Apache License 2.0

- 支持平台: Android / iOS / macOS / Windows / Linux（跨平台）

---

## 娱乐

### XiaoMusic

:lucide-mouse-pointer-click: [**GitHub 仓库地址**](https://github.com/hanxi/xiaomusic)
| [**官方网站**](http://xdocs.hanxi.cc/)
| [**发布页**](https://github.com/hanxi/xiaomusic/releases)

专为「无限听歌」打造, 旨在通过摆脱对单一音响设备的依赖, 解放 小爱音响 等智能音响设备。无论你是喜欢在家中沉浸式听歌, 还是需要通过不同平台享受音乐, XiaoMusic 都能够提供一个无缝的音乐播放体验, 真正做到 随时随地、畅享音乐。

- 开源协议: MIT license

- 核心功能: 播放控制、播放模式、歌单管理、收藏功能等

- 支持格式: mp3 / flac / wav / ape / ogg / m4a
