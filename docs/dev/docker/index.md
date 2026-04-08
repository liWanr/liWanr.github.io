---
icon: simple/docker
title: Docker
comments: true
# date:
#     craeted: 2026-03-04
tags:
    - Tech
---

## 支持系统的安装说明 { id="installation-procedures-for-supported-platforms" }

点击对应系统的链接即可查看具体的安装步骤。

| 平台 | x86_64<br>/ amd64 | arm64<br>/ aarch64 | arm-32bit | ppc64le | s390x |
| :-: | :-: | :--: | :-: | :-: | :-: |
| [**Ubuntu 22.04+**](/dev/docker/install/#ubuntu){ data-preview } | ✅ | ✅ | ✅ | ✅ | ✅ |
| [**Debian 11+**](https://docs.docker.com/engine/install/debian/) | ✅ | ✅ | ✅ | ✅ | - |
| [**CentOS 9+**](https://docs.docker.com/engine/install/centos/) | ✅ | ✅ | - | ✅ | - |
| [二进制包](https://docs.docker.com/engine/install/binaries/) | ✅ | ✅ | ✅ | - | - |
| [Fedora](https://docs.docker.com/engine/install/fedora/) |✅|✅| - |✅| - |
| [Raspberry Pi OS<br>(32-bit)](https://docs.docker.com/engine/install/raspberry-pi-os/) | - | - | - | ⚠️ | - | 
| [RHEL](https://docs.docker.com/engine/install/rhel/) | - | ✅ | ✅ | - | - | ✅ |
| [SLES](https://docs.docker.com/engine/install/sles/) | - | - | - | - | ❌ |


### 其他 Linux 发行版 { id="other-linux-distributions" }

> [!note] 这些方法在某些情况下可能可用, 但 Docker 并不会对这些衍生发行版进行专门测试或验证。
> - **如果是 Debian 的衍生版本**, 例如 「BunsenLabs Linux」、「Kali Linux」 或 「LMDE」（基于 Debian 的 Linux Mint）, 可以参考 Debian 的安装说明。安装时, 将文档中的 Debian 版本替换为你当前发行版所对应的 Debian 版本, 具体对应关系可查阅你所用发行版的官方文档。
> - 同样地, **如果是 Ubuntu 的衍生版本**, 例如 「Kubuntu」、「Lubuntu」 或 「Xubuntu」, 可以参考 Ubuntu 的安装说明, 并将版本号替换为与你发行版对应的 Ubuntu 版本。对应关系请查看发行版文档。
> - 有些 Linux 发行版会在自己的软件仓库中提供 Docker 软件包。这些软件包由发行版的维护者构建和维护, 可能在配置上有所不同, 或基于修改过的源码构建。Docker 官方不参与这些软件包的发布与维护。如果遇到相关问题, 请向对应发行版的 issue 跟踪系统反馈。

Docker 还提供了用于手动安装的二进制文件, 这些二进制文件采用静态链接方式构建, 理论上可以在任意 Linux 发行版上使用。

## 报告安全问题 { id="reporting-security-issues" }

如果发现安全漏洞, 请第一时间 **私发邮件至[官方邮箱](mailto:security@docker.com)**, 请不要在公开的 `issue` 中提交相关信息。