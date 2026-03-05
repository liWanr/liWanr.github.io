---
icon: lucide/arrow-down-to-line
title: 安装
# date:
#     craeted: 2026-03-04
---

## Ubuntu

!!! failure "前提"

    1. 容器暴露端口的时候会绕过 ufw 或 firewalld 管理的防火墙规则。所以建议使用 iptables-nft 和 iptables-legacy 来管理服务器的防火墙规则。
    
    2. 仅支持 Ubuntu 22.04 / 24.04 / 25.10。并且都兼容 x86_64/amd64、armhf、arm64、s390x 和 ppc64le(ppc64el)架构。

    3. Linux 可能会自带非官方的 Docker 软件包, 可能会和官方的软件包有冲突, 所以最好卸载官方的软件包。并且 Docker 依赖于 `containerd` 和 `runc`, 并捆绑为 `containerd.io` 包, 如果之前安装过尽量卸载, 一面版本冲突。

        需要卸载的软件包：`docker.io` / `docker-compose` / `docker-compose-v2` / `docker-doc` / `podman-docker` / `containerd` / `runc`

        ```Bash { title="一次性解决所有冲突" }
        sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)
        ```

### 安装方法 { id="installation-methods-for-ubuntu" }

在全新主机上首次安装 Docker 之前, 您需要设置 Docker apt 仓库。之后, 您可以从该仓库安装和更新 Docker。

#### 方法一：使用 `apt` 安装 { id="install-using-the-repository-for-ubuntu" }

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

#### 方法二：使用软件包安装 { id="install-from-a-package-for-ubuntu" }

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
    
#### 检查 { id="verify-for-ubuntu" }

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

#### 卸载 { id="uninstall-for-ubuntu" }

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

## Debian

!!! failure "前提"

    1. 容器暴露端口的时候会绕过 ufw 或 firewalld 管理的防火墙规则。所以建议使用 iptables-nft 和 iptables-legacy 来管理服务器的防火墙规则。
    
    2. 仅支持 Ubuntu 11 / 12 / 13。并且都兼容 x86_64(amd64)、armhf(arm/v7)、arm64 和 ppc64le(ppc64el)架构。

    3. Linux 可能会自带非官方的 Docker 软件包, 可能会和官方的软件包有冲突, 所以最好卸载官方的软件包。并且 Docker 依赖于 `containerd` 和 `runc`, 并捆绑为 `containerd.io` 包, 如果之前安装过尽量卸载, 一面版本冲突。

        需要卸载的软件包：`docker.io` / `docker-compose` /  `docker-doc` / `podman-docker` / `containerd` / `runc`

        ```Bash { title="一次性解决所有冲突" }
        sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-doc podman-docker containerd runc | cut -f1)
        ```

### 安装方法 { id="installation-methods-for-debian" }

在全新主机上首次安装 Docker 之前, 您需要设置 Docker apt 仓库。之后, 您可以从该仓库安装和更新 Docker。

#### 方法一：使用 `apt` 安装 { id="install-using-the-repository-for-debian" }

1. 设置 Docker 的 apt 仓库

    ```Bash { title="添加 Docker 官方 GPG 密钥" }
    sudo apt update
    sudo apt install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc
    ```

    ```Bash { title="将软件源添加到 apt 源" }
    sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
    Types: deb
    URIs: https://download.docker.com/linux/debian
    Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
    Components: stable
    Signed-By: /etc/apt/keyrings/docker.asc
    EOF
    ```

    ```Bash { title="最后更新一下软件包" }
    sudo apt update
    ```

    !!! tip

        如果你使用衍生发行版, 例如 `Kali Linux`, 你可能需要替换掉这个命令中预期打印版本代号的部分, 将此部分替换为相应 Debian 版本的代号, 例如 bookworm。

        ```Bash
        (. /etc/os-release && echo "$VERSION_CODENAME")
        ```

2. 安装 Docker 软件包。

    === "船新版本"

        ```Bash
        sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        ```

    === "指定版本"

        要安装指定版本的 Docker, 首先在仓库中列出可用的版本：

        ```Bash
        apt list --all-versions docker-ce
        ```

        :   >   docker-ce/bookworm 5:29.2.1-1~debian.12~bookworm <arch> <br>
            >   docker-ce/bookworm 5:29.2.0-1~debian.12~bookworm <arch> <br>
            >   ...

        选择所需版本并安装：

        ```Bash
        VERSION_STRING=5:29.2.1-1~debian.12~bookworm
        sudo apt install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
        ```

#### 方法二：使用软件包安装 { id="install-from-a-package-for-debian" }

如果无法使用 `apt` 安装 Docker, 可以通过 `.deb` 文件安装。但是升级的时候就需要手动下载新文件。

1. 去[**官网列表**](https://download.docker.com/linux/debian/dists/)中选择 Debian 版本, 并下载安装 `pool/stable/` 目录下对应架构软件包的 `.deb` 文件。

2. 安装完成之后将以下示例中的路径更新为你下载 Docker 软件包的位置。

    ```Bash
    sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
    ./docker-ce_<version>_<arch>.deb \
    ./docker-ce-cli_<version>_<arch>.deb \
    ./docker-buildx-plugin_<version>_<arch>.deb \
    ./docker-compose-plugin_<version>_<arch>.deb
    ```
    
#### 检查 { id="verify-for-debian" }

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

#### 卸载 { id="uninstall-for-debian" }

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

## CentOS

!!! failure "前提"

    1. 仅支持 CentOS 9 / 10, 并且 `centos-extras` 仓库必须启用, 此仓库默认已启用, 如果你已禁用它, 需要重新启用。

    2. Linux 可能会自带非官方的 Docker 软件包, 可能会和官方的软件包有冲突, 所以最好卸载官方的软件包。

        ```Bash { title="一次性解决所有冲突" }
        sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
        ```

### 安装方法 { id="installation-methods-for-centos" }

在全新主机上首次安装 Docker 之前, 您需要设置 Docker apt 仓库。之后, 您可以从该仓库安装和更新 Docker。

#### 方法一：使用 `rpm` 安装 { id="install-using-the-repository-for-centos" }

1. 安装 `dnf-plugins-core`（用于管理 DNF 仓库）并添加 Docker 仓库。

    ```Bash
    sudo dnf -y install dnf-plugins-core
    sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    ```

2. 安装 Docker 软件包。

    === "船新版本"

        ```Bash
        sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
        ```

        如果提示接受 GPG 密钥, 请验证指纹是否匹配 `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`, 如果是这样, 就接受它。

    === "指定版本"

        要安装指定版本的 Docker, 首先在仓库中列出可用的版本：

        ```Bash
         dnf list docker-ce --showduplicates | sort -r
        ```

        :   >   docker-ce.x86_64    3:29.2.1-1.el9    docker-ce-stable <br>
            >   docker-ce.x86_64    3:29.2.0-1.el9    docker-ce-stable <br>
            >   <...>

        返回的列表取决于启用的仓库, 并且特定于您的 CentOS 版本（在本示例中, 由 .el9 后缀指示）。

        通过完全限定包名安装特定版本, 该包名由包名（ docker-ce）和版本字符串（第 2 列）通过连字符（ -）连接。例如, docker-ce-3:29.2.1-1.el9。

        将 <VERSION_STRING> 替换为所需版本, 然后运行以下命令进行安装：

        ```Bash
        sudo dnf install docker-ce-<VERSION_STRING> docker-ce-cli-<VERSION_STRING> containerd.io docker-buildx-plugin docker-compose-plugin
        ```

    这个命令安装了 Docker, 但它不会启动 Docker。它还会创建 docker 组, 但是, 默认情况下不会将任何用户添加到该组。

#### 方法二：使用软件包安装 { id="install-from-a-package-for-centos" }

如果无法使用 `rpm` 安装 Docker, 可以通过 `.rpm` 文件安装。但是升级的时候就需要手动下载新文件。

1. 去[**官网列表**](https://download.docker.com/linux/centos/)中选择 CentOS 版本, 并下载安装 `x86_64/stable/Packages/` 目录下的 `.rpm` 文件。

2. 安装完成之后将以下示例中的路径更新为你下载 Docker 软件包的位置。

    ```Bash
    sudo dnf install /path/to/package.rpm
    ```
    
#### 检查 { id="verify-for-centos" }

1. 安装后, Docker 服务将自动启动。要验证 Docker 是否正在运行, 请使用：

    ```Bash
    sudo systemctl enable --now docker
    ```

    这配置了 Docker systemd 服务在您启动系统时自动启动。如果您不想让 Docker 自动启动, 请使用 `sudo systemctl start docker`。

2. 通过运行 `hello-world` 镜像来验证安装是否成功

    ```Bash
    sudo docker run hello-world
    ```

#### 卸载 { id="uninstall-for-centos" }

1. 卸载软件包

    ```console
    sudo dnf remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
    ```

2. 删除数据目录

    ```console
    sudo rm -rf /var/lib/docker
    sudo rm -rf /var/lib/containerd
    ```

!!! tip "如果你修改过配置文件, 需要手动删除。"