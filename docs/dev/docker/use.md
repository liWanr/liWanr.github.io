---
icon: lucide/terminal
title: 使用
# date:
#     craeted: 2026-03-05
---

## 前情提要 { id="context" }

由于一般都是用 `sudo` 安装的 docker，所以使用 docker 的时候也需要用管理员权限运行命令，一般开发 / 测试 / 个人服务器环境下推荐将非 root 用户添加进 docker 组里面，这样就不用重复输入 `sudo` 提升权限了。

但是在生产环境中不建议这样使用，因为 docker 组的权限几乎等价于“能以 root 权限运行容器”。攻击者只要拿到这个用户的 shell，就可以通过 `docker run -v /:/host ...` 等方式逃逸到宿主机，读写任意文件，甚至提权为 root。

=== "把用户加入 docker 组"

    ```Bash
    sudo usermod -aG docker $USER
    ```

=== "重新登录"

    ```Bash
    exit
    ```

=== "重启 Docker"

    ```Bash
    sudo systemctl restart docker
    ```

=== "再试一下命令"
    
    ```Bash
    docker images
    ```

## 服务 { id="servers" }

=== "启动服务"

    ```Bash
    systemctl start docker
    ```

=== "停止服务"

    ```Bash
    systemctl stop docker
    ```

=== "查看状态"

    ```Bash
    systemctl status docker
    ```

=== "重启服务"

    ```Bash
    systemctl restart docker
    ```

=== "开启自启服务"

    ```Bash
    systemctl enable docker
    ```

## 镜像 { id="images" }

=== "查看本地镜像"

    ```Bash
    docker images
    ```