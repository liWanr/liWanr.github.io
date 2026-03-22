---
icon: octicons/desktop-download-16
title: 安装
# date:
#     craeted: 2026-03-04
comments: true
---

在**开发阶段**使用 Windows 或 macOS 运行 Docker 是完全可行的，但在**部署或生产环境中**，一般还是更推荐直接在 Linux 服务器上运行 Docker。

因为在 Windows 或 macOS 上运行 Docker 时的本质是通过虚拟化 Linux 内核来运行容器，相当于「**容器跑在虚拟机里的 Linux 上**」。这种方式虽然对开发者非常友好，但在性能、文件系统 IO、网络等方面通常会有一定损耗。

## Ubuntu

!!! failure "前提"

    1. 容器暴露端口的时候会绕过 ufw 或 firewalld 管理的防火墙规则。所以建议使用 iptables-nft 和 iptables-legacy 来管理服务器的防火墙规则。
    
    2. 仅支持 Ubuntu 22.04 / 24.04 / 25.10。并且都兼容 x86_64/amd64、armhf、arm64、s390x 和 ppc64le(ppc64el)架构。

    3. Linux 可能会自带非官方的 Docker 软件包, 可能会和官方的软件包有冲突, 所以最好卸载官方的软件包。并且 Docker 依赖于 `containerd` 和 `runc`, 并捆绑为 `containerd.io` 包, 如果之前安装过尽量卸载, 一面版本冲突。

        需要卸载的软件包：`docker.io` / `docker-compose` / `docker-compose-v2` / `docker-doc` / `podman-docker` / `containerd` / `runc`

        ```Bash { title="一次性解决所有冲突" }
        sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)
        ```

### 安装方法 { id="installation-methods" }

在全新主机上首次安装 Docker 之前, 您需要设置 Docker apt 仓库。之后, 您可以从该仓库安装和更新 Docker。

#### 方法一：使用 `apt` 安装 { id="install-using-the-repository" }

1. 设置 Docker 的 apt 仓库

    ```Bash { title="添加 Docker 官方 GPG 密钥" }
    sudo apt update
    sudo apt install -y ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    ```

    ```Bash { title="将软件源添加到 apt 源" }
    sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
    Types: deb
    URIs: https://download.docker.com/linux/ubuntu
    Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
    Components: stable
    Signed-By: /etc/apt/keyrings/docker.asc
    EOF
    ```

    ```Bash { title="最后更新一下软件包" }
    sudo apt update
    ```

2. 安装 Docker 软件包。

    === "船新版本"

        ```Bash
        sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        ```

    === "指定版本"

        要安装指定版本的 Docker, 首先在仓库中列出可用的版本：

        ```Bash
        apt list --all-versions docker-ce
        ```

        :   >   docker-ce/noble 5:29.2.1-1\~ubuntu.24.04~noble <arch\> <br>
            >   docker-ce/noble 5:29.2.0-1\~ubuntu.24.04~noble <arch\> <br>
            >   ...

        选择所需版本并安装：

        ```Bash
        VERSION_STRING=5:29.2.1-1~ubuntu.24.04~noble
        sudo apt install -y docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
        ```

#### 方法二：使用软件包安装 { id="install-from-a-package" }

如果无法使用 `apt` 安装 Docker, 可以通过 `.deb` 文件安装。但是升级的时候就需要手动下载新文件。

1. 去[**官网列表**](https://download.docker.com/linux/ubuntu/dists/)中选择 Ubuntu 版本, 并下载安装 `pool/stable/` 目录下对应架构软件包的 `.deb` 文件。

2. 安装完成之后将以下示例中的路径更新为你下载 Docker 软件包的位置。

    ```Bash
    sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
    ./docker-ce_<version>_<arch>.deb \
    ./docker-ce-cli_<version>_<arch>.deb \
    ./docker-buildx-plugin_<version>_<arch>.deb \
    ./docker-compose-plugin_<version>_<arch>.deb
    ```
    
#### 检查 { id="verify" }

1. 安装后, Docker 服务将自动启动。要验证 Docker 是否正在运行, 请使用：

    ```Bash
    sudo systemctl status docker
    ```

    某些系统可能禁用了此功能, 并需要手动启动：

    ```Bash
    sudo systemctl start docker
    ```

2. 通过运行 `hello-world` 镜像来验证安装是否成功

    ```Bash
    sudo docker run hello-world
    ```

    > **能找到有这个就行了**<br>
    > This message shows that your installation appears to be working correctly.

#### 卸载 { id="uninstall" }

1. 卸载软件包

    ```console
    sudo apt purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
    ```

2. 删除数据目录

    ```console
    sudo rm -rf /var/lib/docker
    sudo rm -rf /var/lib/containerd
    ```

3. 删除软件源和密钥

    ```console
    sudo rm /etc/apt/sources.list.d/docker.sources
    sudo rm /etc/apt/keyrings/docker.asc
    ```

!!! tip "如果你修改过配置文件, 需要手动删除。"

