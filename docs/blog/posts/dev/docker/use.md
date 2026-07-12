---
icon: octicons/terminal-16
title: 服务与架构
comments: true
# date:
#     craeted: 2026-03-05
tags:
    - Tech
---

由于一般都是用 `sudo` 安装的 docker，所以使用 docker 的时候也需要用管理员权限运行命令，一般开发 / 测试 / 个人服务器环境下推荐将非 root 用户添加进 docker 组里面，这样就不用重复输入 `sudo` 提升权限了。将非 root 用户添加进 docker 组按照这个流程：

///html | div.step

1. 把用户加入 docker 组

    ```Bash { linenums="0" }
    sudo usermod -aG docker $USER
    ```

2. 重新登录

    ```Bash { linenums="0" }
    exit
    ```

3. 重启 Docker

    ```Bash { linenums="0" }
    sudo systemctl restart docker
    ```

4. 再试一下命令
    
    ```Bash { linenums="0" }
    docker images
    ```

///

**但是在生产环境中不建议这样使用**，因为 docker 组的权限几乎等价于「能以 root 权限运行容器」。攻击者只要拿到这个用户的 shell，就可以通过 `docker run -v /:/host ...` 等方式逃逸到宿主机，读写任意文件，甚至提权为 root。

///tab | 启停服务

///html | div.grid.cards

-   启动服务

    ```Bash { linenums="0" }
    systemctl start docker
    ```

-   停止服务

    ```Bash { linenums="0" }
    systemctl stop docker
    ```

///

///

///tab | 重启&重载

///html | div.grid.cards

-   重启服务

    ```Bash { linenums="0" }
    systemctl restart docker
    ```

-   重载服务

    ```Bash { linenums="0" }
    systemctl reload docker
    ```

///

///

///tab | 查看状态

///html | div.grid.cards

-   查看运行状态

    ```Bash { linenums="0" }
    systemctl status docker
    ```

-   查看依赖关系

    ```Bash { linenums="0" }
    systemctl list-dependencies docker.service
    ```

///

///

///tab | 开启自启

///html | div.grid.cards

-   开启开机自启服务

    ```Bash { linenums="0" }
    systemctl enable docker
    ```

-   关闭开机自启服务

    ```Bash { linenums="0" }
    systemctl disable docker
    ```

///

///

## 镜像 { id="images" }

Docker 镜像包含了运行应用所需的所有文件、库和配置，但它是**只读的**。基于镜像就能快速创建容器实例，实现「**一次打包，到处运行**」。

///html | div.grid.cards

-   **查看本地镜像**

    ```Bash { linenums="0" }
    docker images
    ```

-   **在 docker hub 上搜索镜像**

    ```Bash { linenums="0" }
    docker search ubuntu
    ```

-   **拉取镜像**

    ```Bash { linenums="0" }
    docker pull ubuntu
    ```

-   **拉取指定版本的镜像**

    ```Bash { linenums="0" }
    docker pull ubuntu:22.04
    ```

-   **删除镜像**

    ```Bash { linenums="0" }
    docker rmi ubuntu:22.04
    ```

///

## 容器 { id="container" }

容器是「镜像的运行实例」，是一个轻量级、可移植的执行环境。它**共享主机内核，但文件系统、网络和进程空间完全隔离**，轻便高效（秒级启动），无需完整虚拟机。

///html | div.grid.cards

-   创建并**持续在后台**运行的**名为 con1** 的<br> **ubuntu22.04** 容器

    ```Bash { linenums="0" }
    docker run -id --name=con1 ubuntu:22.04
    ```

-   创建并**持续**运行**名为 con2** 的<br> **ubuntu22.04** 容器并**进入终端**

    ```Bash { linenums="0" }
    docker run -it --name=con2 ubuntu:22.04
    ```

-   **列出所有包括已停止的容器**

    ```Bash { linenums="0" }
    docker ps -a
    ```

-   **停止运行容器**

    ```Bash { linenums="0" }
    docker stop con1"(1)!" 
    ```

    1. 容器名、容器ID 都可以

-   **删除容器**

    ```Bash { linenums="0" }
    docker rm con1"(1)!" 
    ```

    1. 容器名、容器ID都可以

-   **进入容器的交互式终端**

    ```Bash { linenums="0" }
    docker exec -it con1 bash"(1)!"
    ```

    1. 容器名、容器ID都可以, 但是后面要接一个命令

///

## 数据卷 { id="volume" }

数据卷相当于**共享目录**，可以允许多个容器同时读写。并且当**容器销毁时，数据卷数据不受影响**。

当数据卷过多时可以创建**数据卷容器**集中管理数据卷，但它**不是中间层跳板**。其他容器只是通过**继承**数据卷容器的挂载点从而指向宿主机目录，所以数据卷容器删除后，**其他容器依旧可正常访问数据卷**。

///html | div.grid.cards

-   列出所有数据卷

    ```Bash { linenums="0" }
    docker volume ls
    ```

-   创建运行容器并将数据卷挂载到容器目录

    ```Bash { linenums="0" }
    docker run -id --name con3 -v ~/date:/root/dateCon3 ubuntu:22.04
    ```

-   创建运行**数据卷容器**

    ```Bash { linenums="0" }
    docker run -id --name=vo1 -v /volume ubuntu:22.04
    ```

-   将数据卷容器**挂载到当前容器**

    ```Bash { linenums="0" }
    docker run -id --name=con4 --volume-from vo1 ubuntu:22.04
    ```

///

