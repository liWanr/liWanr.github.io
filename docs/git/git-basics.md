---
icon: lucide/git-merge
title: Git 基本知识
tags:
    - Knowledge
    - Git
---

## 安装 Git {id="install-git"}

若要在命令行上使用 Git, 需要在计算机上安装、安装和设置 Git。 [下载并安装最新版本的 Git](https://git-scm.com/downloads)

!!! warning "在 Chrome OS 上启用和安装 Git"

    从 2020 年开始大部分 Chrome OS 设备都内置 Git。 如果需要启用可以去 Launcher 搜索 Linux 并打开。

    如果你使用较早版本的 Chrome OS 设备, 则需要使用 **其他方法** ：

    1. 在 Chrome OS 设备上安装终端模拟器, 例如 Google Play 商店中的 Termux。

    2. 从您安装的终端模拟器安装 Git。 例如, 在 Termux 中, 输入 `pkg install git` 并在出现提示时键入 ++y++。

## 在 GitHub 验证身份 {id="authenticating-on-GitHub"}

1. 从 Git 连接到 GitHub 仓库时需要进行身份验证。首先检查是否已有 SSH 密钥, 如果有 `id_*.pub` 的文件, 则说明已有 SSH 密钥。

    ```Bash
    ls -al ~/.ssh
    ```

2. 如果没有就要 **生成 SSH 密钥** , 使用 `ssh-keygen` 命令, 使用参数 `-t` 选择加密算法之后按照提示操作即可。

    ```Bash
    ssh-keygen -t ed25519 -C "(1)"
    ```

    1. Git 的邮箱, 比如 **`"itsWanr@outlook.com"`**

    ??? Quote "推荐的算法类型"

        |算法用途|算法名称|特点|常见应用场景|推荐程度|
        |:-:|-|-|-|-|
        |非对称加密|`RSA`|应用最广、成熟稳定|密钥认证|⭐⭐⭐|
        ||`ECDSA`|密钥短、效率高|密钥认证|⭐⭐⭐⭐|
        ||`Ed25519`|速度快、安全性最高|密钥认证|⭐⭐⭐⭐⭐|
        |数据加密|`AES-128/192/256`|速度快、安全性高|数据传输加密|⭐⭐⭐|
        ||`ChaCha20-Poly1305`|移动设备性能优秀|数据传输加密|⭐⭐⭐⭐⭐|
        |密钥交换|`ECDH`|椭圆曲线 DH|会话密钥协商|⭐⭐⭐|
        ||`Curve25519`|现代高效算法|会话密钥协商|⭐⭐⭐⭐⭐|
        |消息认证|`UMAC`|速度更快|数据完整性验证|⭐⭐|
        ||`Poly1305`|与 ChaCha20 配合|数据完整性验证|⭐⭐⭐|
        ||`HMAC-SHA2-256`|安全性好|数据完整性验证|⭐⭐⭐⭐|
        ||`HMAC-SHA2-512`|更高安全性|数据完整性验证|⭐⭐⭐⭐⭐|
    
3. 查看并复制生成好的 SSH 密钥。

    ```Bash
    cat ~/.ssh/id_ed25519.pub
    ```

4. 将 SSH 密钥添加到 GitHub, 进入 [**Add new SSH Key**](https://github.com/settings/ssh/new) 页面, Title 对应密钥名称, Key type 保持默认的认证加密, Key 就是对应密钥

## 配置用户名与电子邮箱 {id="configure-username-and-commit-email-address"}

1. **配置信息**

    === "配置用户名"

        ```Bash
        git config --global user.name "(1)"
        ```

        1. 里面填 git 账户名, 比如 **`"liWanr"`**

    === "电子邮件"

        ```Bash
        git config --global user.email "(1)"
        ```

        1. 里面填 git 账号绑定的邮箱, 比如 **`"itsWanr@outlook.com"`**

    <small>
    :octicons-light-bulb-16:
    如果想查看 **特定目录的 Git 设置** 就去掉 **`--global`** 参数即可
    </small>

2. **查看信息**

    通过此命令可以查看 Git 的全局设置项, 如用户名、邮箱地址等, 帮助确保 Git 设置正确无误。

    ```Bash
    git config --global --list
    ```

    <div class="result" markdown>

    ```Bash {.yaml .no-copy .no-select title="输出内容"}
    user.name=liWanr
    user.email=itsWanr@ooutlook.com
    ```

    </div>

    <small>
    :octicons-light-bulb-16:
    如果想查看 **特定目录的 Git 设置** 就去掉 **`--global`** 参数即可
    </small>


## 测试连接状态 {id="test-connect-status"}

当密钥添加到 GitHub 且本地已经配置用户名和电子邮箱的完成后，就可以检测本地和 GitHub 的连接状态了

```Bash
ssh -T git@github.com
```

<div class="result" markdown>

=== "成功状态 1"

    ```Bash  {.yaml .no-copy .no-select}
    This key is not known by any other names
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes # (1)!
    Hi ***! You've successfully authenticated, but GitHub does not provide shell access.
    ```

    1. 会让你输入 `yes` 确认

=== "成功状态 2"

    ```Bash  {.yaml .no-copy .no-select}
    Hi ***! You've successfully authenticated, but GitHub does not provide shell access.
    ```
    
</div>

这期间可能存在会有问题, 特别是用了代理的玩家, 可能会出现 **远程主机已关闭连接** 的报错

> **原问题内容 ssh_exchange_identification: Connection closed by remote host**

通常 ssh 的端口是22, 开启代理之后 SSH 的连接被代理阻塞, 但是可以通过更改 SSH 设置文件, 将 GitHub 的 SSH 连接端口从 22 改为 443。

1. 首先打开 config 文件

    === "Linux"

        ```Bash
        vim ~/.ssh/config
        ```

    === "windows"

        ```Text
        C:\Users\{Username}\.ssh\config
        ```

2. 在文件中添加以下内容

    ```Bash
    Host github.com
        Hostname ssh.github.com
        Port 443
        User git
    ```
