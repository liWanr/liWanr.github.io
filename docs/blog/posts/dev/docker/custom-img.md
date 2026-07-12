---
icon: lucide/file-terminal
title: 自制镜像
comments: true
# date:
#     craeted: 2026-03-04
tags:
    - Tech
---

## 前言

先说本质，Docker 镜像本质上是一个「**只读的、分层**」的文件系统模板，包含应用程序及其依赖的运行环境（如 rootfs），通过联合文件系统（如 UnionFS）堆叠多层实现高效共享和复用。

1. **docker 的 ubuntu 镜像只要几百 MB，为什么 ubuntu 操作系统的 IOS 却要几个GB？**

    因为 Docker 镜像中仅包含用户空间文件系统（rootfs），剔除了内核（bootfs）、引导程序、GUI 和大量不必要工具，这些容器直接使用宿主机内核。相比之下，Ubuntu ISO 达几个GB，是完整可引导的安装介质，包括内核、安装程序、多种架构支持和完整软件包。

2. **那为什么 tomcat 镜像要几百兆，实际的 tomcat 只需要几十兆呢？**

    官方 Tomcat 镜像几百MB，主要基于基础镜像 + JDK 和 Tomcat 文件，以及安装过程中的缓存、文档等冗余层。大概就是这个逻辑：

    ```mermaid
    ---
    config:
        packet:
            bitsPerRow: 24
            showBits: false
    ---
    packet
        +1: "2️⃣"
        +23: "Tomcat 镜像"
        +1: "1️⃣"
        +23: "JDK 镜像"
        +1: "0️⃣"
        +23: "rootfs 基础镜像(root 系统文件, 不同发行版的这个部分不同)"
    ```

    纯 Tomcat tar.gz 只需几十 MB，但镜像需完整运行环境，无法仅打包二进制文件。优化如使用 Alpine 基础镜像或多阶段构建可将 Tomcat 镜像缩小至100MB 以内。

## Dockerfile

| 关键字 | 作用 |
| ----- | --- |
| FROM | 指定 dokcer 基于哪个镜像构建 |
| LABEL | 使用键值对的形式添加镜像的元数据，还可以指定 Dockerfile 的作者/维护者。 |
| RUN | 在 building 时执行的命令，默认是 `bin/sh`。<br>格式：`RUN command` 或者 `RUN ["command", "param1", "paran2]` |
| CMD | 在 building 后写的启动命令，和 `ENTERPOINT` 配合使用。（可以被覆盖）<br>格式：`CMD command param1 param2` 或者 `CMD ["command", "param1", "paran2]` |
| ENTERYPOINT | 设置容器创建时的主要命令，一般在制作一些执行就关闭的容器中使用。（不可被覆盖） |
| COPY | 在 building 时将文件或目录复制本地文件到镜像中。 |
| ADD | 在 building 时将文件、目录或远程 URL 添加到镜像中。当目标文件为压缩包时会自动复制并强制解压到目标路径。 |
| ENV | 指定 building 时的环境变量，可以在启动容器的时候痛过 `-e` 覆盖。<br>格式：`ENV name=value` |
| ARG | 在构建的时候传递给构建器的变量，可使用 "docker build" 命令设置。<br>如果有 `ENV`，那么 `ENV` 的环境会覆盖 `ARG` 的参数 |
| VOLUME | 指定 building 的镜像哪些可挂载到文件系统中。启动容器的时候通过 `-v` 绑定。<br>格式：`VOLUME ["dir"]` |
| EXPOSE | 容器运行时的监听端口，也可以在启动时使用 `-p` 绑定暴露的端口。<br>格式：`EXPOSE 8080` 或者 `EXPOSE 8080/udp` |
| WORKDIR | 指定容器内部的工作目录，如果没有创建则自动创建，其实就是进入容器的路径。 |
| USER | 用于指定执行后续命令的用户和用户组（用户和用户组必须提前已经存在）。 |
| HEALTHCHECK | 指定周期性检查容器健康状态的命令。基本用不着，因为很多应用本身有这个机制。 |
| ONBUILD | 当前镜像被用作另一个构建过程的基础时执行的命令，不影响当前镜像。 |
| STOPSIGNAL | 设置发送给容器用于退出的系统调用信号。 |
| SHELL | 覆盖 Docker 中默认的 shell，在 `RUN | CMD | ENTERPOINT` 执行命令的时候使用。 |

## 服务编排 `dockercompose`

简单说，就是「**让一堆服务像团队一样协作工作**」的规则和工具。

单体应用时代，一个程序启动就完事。但微服务/容器时代，一套系统往往包含网关、多个后端、数据库、缓存、消息队列等多个组件，需要一起启动、按依赖顺序运行、统一升级回滚。

1. 利用 dockerfile 定义运行环境镜像

2. 使用 docker-compose.yml 定义构成应用程序的服务，让这些服务在隔离环境中一起运行。

3. 执行 docker-compose up 命令来启动并运行整个应用程序。

### 安装

///html | div.step

1. 在 Linux 上可以从 [GitHub](https://github.com/docker/compose/releases) 中下载二进制文件包进行安装:

    ```Bash { linenums="0" }
    sudo curl -SL https://github.com/docker/compose/releases/download/v5.0.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
    ```

2. 将可执行权限给这个二进制文件

    ```Bash { linenums="0" }
    sudo chmod +x /usr/local/bin/docker-compose
    ```

3. 可以查看一下版本信息

    ```Bash { linenums="0" }
    docker-compose -v "(1)!"
    ```

    1. `--version` 也可以

///

### 卸载

卸载二进制文件即可

```Bash { linenums="0" }
sudo rm /usr/local/bin/docker-compose
```

### 使用

先留空等着写 `vue` + `springboot` + `mysql` 的 `docker-compose.yml` 示例，后续再写一些 `docker-compose` 的使用细节。

## 私有仓库