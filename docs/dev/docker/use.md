---
icon: lucide/terminal
title: 使用
# date:
#     craeted: 2026-03-05
---

## 前情提要 { id="context" }

由于一般都是用 `sudo` 安装的 docker，所以使用 docker 的时候也需要用管理员权限运行命令，一般开发 / 测试 / 个人服务器环境下推荐将非 root 用户添加进 docker 组里面，这样就不用重复输入 `sudo` 提升权限了。

??? note "将非 root 用户添加进 docker 组"

    1. 把用户加入 docker 组

        ```Bash
        sudo usermod -aG docker $USER
        ```

    2. 重新登录

        ```Bash
        exit
        ```

    3. 重启 Docker

        ```Bash
        sudo systemctl restart docker
        ```

    4. 再试一下命令
        
        ```Bash
        docker images
        ```

**但是在生产环境中不建议这样使用**，因为 docker 组的权限几乎等价于“能以 root 权限运行容器”。攻击者只要拿到这个用户的 shell，就可以通过 `docker run -v /:/host ...` 等方式逃逸到宿主机，读写任意文件，甚至提权为 root。



## 服务 { id="servers" }

<div class="grid cards" markdown>

-   **启动服务**

    ```Bash
    systemctl start docker
    ```

-   **停止服务**

    ```Bash
    systemctl stop docker
    ```

-   **查看状态**

    ```Bash
    systemctl status docker
    ```

-   **重启服务**

    ```Bash
    systemctl restart docker
    ```

-   **开启自启服务**

    ```Bash
    systemctl enable docker
    ```

</div>

## 镜像 { id="images" }

<div class="grid cards" markdown>

-   **查看本地镜像**

    ```Bash
    docker images
    ```

-   **在 docker hub 上搜索镜像**

    ```Bash
    docker search ubuntu
    ```

-   **拉取镜像**

    ```Bash
    docker pull ubuntu
    ```

-   **拉取指定版本的镜像**

    ```Bash
    docker pull ubuntu:22.04
    ```

-   **删除镜像**

    ```Bash
    docker rmi ubuntu:22.04
    ```

</div>

## 容器 { id="container" }

<div class="grid cards" markdown>

-   创建并**持续在后台**运行的**名为 con1** 的<br> **ubuntu22.04** 容器

    ```Bash
    docker run -id --name=con1 ubuntu:22.04
    ```

-   创建并**持续**运行**名为 con2** 的<br> **ubuntu22.04** 容器并**进入终端**

    ```Bash
    docker run -it --name=con2 ubuntu:22.04
    ```

-   **列出所有包括已停止的容器**

    ```Bash
    docker ps -a
    ```

-   **停止运行容器**

    ```Bash
    docker stop con1"(1)!" 
    ```

    1. 容器名、容器ID 都可以

-   **删除容器**

    ```Bash
    docker rm con1"(1)!" 
    ```

    1. 容器名、容器ID都可以

-   **进入容器的交互式终端**

    ```Bash
    docker exec -it con1 bash"(1)!"
    ```

    1. 容器名、容器ID都可以, 但是后面要接一个命令

</div>

## 数据卷 { id="volume" }

数据卷相当于**共享目录**，可以允许多个容器同时读写。并且当**容器销毁时，数据卷数据不受影响**。

当数据卷过多时可以创建**数据卷容器**集中管理数据卷，但它**不是中间层跳板**。其他容器只是通过**继承**数据卷容器的挂载点从而指向宿主机目录，所以数据卷容器删除后，**其他容器依旧可正常访问数据卷**。

<div class="grid cards" markdown>

-   列出所有数据卷

    ```Bash
    docker volume ls
    ```

-   创建运行容器并将数据卷挂载到容器目录

    ```Bash
    docker run -id --name con3 -v ~/date:/root/dateCon3 ubuntu:22.04
    ```

-   创建运行**数据卷容器**

    ```Bash
    docker run -id --name=vo1 -v /volume ubuntu:22.04
    ```

-   将数据卷容器**挂载到当前容器**

    ```Bash
    docker run -id --name=con4 --volume-from vo1 ubuntu:22.04
    ```

</div>


| 命令 | 功能 | 示例 |
|-|-|-|
| docker run | 启动一个新的容器并运行命令 | docker run -d ubuntu |
| docker ps | 列出当前正在运行的容器 | docker ps |
| docker ps -a | 列出所有容器（包括已停止的容器） | docker ps -a |
| docker build | 使用 Dockerfile 构建镜像 | docker build -t my-image . |
| docker images | 列出本地存储的所有镜像 | docker images |
| docker pull | 从 Docker 仓库拉取镜像 | docker pull ubuntu |
| docker push | 将镜像推送到 Docker 仓库 | docker push my-image |
| docker exec | 在运行的容器中执行命令 | docker exec -it container_name bash |
| docker stop | 停止一个或多个容器 | docker stop container_name |
| docker start | 启动已停止的容器 | docker start container_name |
| docker restart | 重启一个容器 | docker restart container_name |
| docker rm | 删除一个或多个容器 | docker rm container_name |
| docker rmi | 删除一个或多个镜像 | docker rmi my-image |
| docker logs | 查看容器的日志 | docker logs container_name |
| docker inspect | 获取容器或镜像的详细信息 | docker inspect container_name |
| docker exec -it | 进入容器的交互式终端 | docker exec -it container_name /bin/bash |
| docker network ls | 列出所有 Docker 网络 | docker network ls |
| docker volume ls | 列出所有 Docker 卷 | docker volume ls |
| docker-compose up | 启动多容器应用（从 docker-compose.yml 文件） | docker-compose up |
| docker-compose down | 停止并删除由 docker-compose 启动的容器、网络等 | docker-compose down |
| docker info | 显示 Docker 系统的详细信息 | docker info |
| docker version | 显示 Docker 客户端和守护进程的版本信息 | docker version |
| docker stats | 显示容器的实时资源使用情况 | docker stats |
| docker login | 登录 Docker 仓库 | docker login |
| docker logout | 登出 Docker 仓库 | docker logout |
