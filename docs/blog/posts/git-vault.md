---
icon: lucide/github
title: Git 宝库
tags:
    - Knowledge
    - Git
---

## Git 基本知识 {id="git-basics"}


### 使用 Git {id="using-git"}

1. 若要在命令行上使用 Git，需要在计算机上安装、安装和设置 Git。 [下载并安装最新版本的 Git](https://git-scm.com/downloads)

    ??? warning "在 Chrome OS 上启用和安装 Git"

        从 2020 年开始大部分 Chrome OS 设备都内置 Git。 如果需要启用可以去 Launcher 搜索 Linux 并打开。

        如果你使用较早版本的 Chrome OS 设备，则需要使用 **其他方法** ：

        1. 在 Chrome OS 设备上安装终端模拟器，例如 Google Play 商店中的 Termux。

        2. 从您安装的终端模拟器安装 Git。 例如，在 Termux 中，输入 `pkg install git` 并在出现提示时键入 `y`。

2. 在 Git 中设置用户名与电子邮件地址。 [设置命令 :octicons-arrow-right-16:](#setting-your-username-and-commit-email-address)

### 通过 Git 向 GitHub 进行身份验证 {id="authenticating-with-GitHub-via-Git"}

从 Git 连接到 GitHub 仓库时需要通过 HTTP 或 SSH 进行身份验证。

#### 通过 SSH 连接 {id="connecting-over-ssh"}

检查是否已有 SSH 密钥，如果有 `.pub` ，则说明已有 SSH 密钥。

```Bash
ls -al ~/.ssh
```

如果没有就要 **生成 SSH 密钥** ，按照提示完成密钥的生成，生成的密钥默认会保存在 `~/.ssh/` 目录下，文件名为 `id_ed25519` 或其他默认名称，取决于密钥类型。

```Bash
ssh-keygen -t ed25519 -C "(1)"
```

1. Git 的邮箱，比如 **`"iseastonlee@outlook.com"`**

??? tip "`ssh-keygen`命令参数 `-t` 的含义"

    代表生成的 SSH 密钥的类型，它定义了密钥对的加密算法。目前有如下几种：

    1. `ed25519`: 一种现代、较为安全的算法，生成的密钥较短，但安全性较高（推荐）。

    2. `rsa`: 传统的 RSA 算法，长度通常为 2048 位或 4096 位，其安全性会随着密钥长度的增加而提高。

    3. `ecdsa`: 基于椭圆曲线的加密算法，提供比 RSA 更好的安全性和性能，但在使用时也有一些限制。

**将 SSH 密钥添加到 GitHub**

首先登录到 GitHub，进入 `Settings -> SSH and GPG keys -> New SSH key`，然后将 `~/.ssh/id_ed25519.pub` 文件中的内容粘贴到 GitHub 上。完成后通过以下命令测试 SSH 连接状态

```Bash
ssh -T git@github.com
```

<div class="result" markdown>

!!! quote "成功提示"
    
    Hi ***! You've successfully authenticated, but GitHub does not provide shell access.

</div>

#### 通过 HTTPS 连接 {id="connecting-over-https"}

`https://` 克隆 URL 在所有存储库上都可用，无论可见性如何。 即使你在防火墙或代理后面，`https://` 克隆 URL 也有效。

在命令行上使用 HTTPS URL 将 `git clone`、`git fetch`、`git pull` 或 `git push` 执行到专用远程仓库时，Git 将要求你提供 GitHub 用户名和密码。 当 Git 提示你输入密码时，请输入你的personal access token。 或者，可以使用 [Git 凭据管理器](https://github.com/GitCredentialManager/git-credential-manager/blob/main/README.md)等凭据帮助程序。 Git 的基于密码的身份验证已被删除，取而代之的是更安全的身份验证方法。 

如果要访问使用 SAML SSO 的组织，并且使用的是 personal access token (classic)，则在进行身份验证之前，还必须授权 personal access token 访问该组织。 

!!! tip "提示"

    您可以使用凭据小助手，让 Git 在每次与 GitHub 通信时记住您的 GitHub 凭据。 
    
    要克隆仓库而不在命令行中对 GitHub 进行身份验证，你可以使用 GitHub Desktop 进行克隆。

    如果希望使用 SSH，但不能通过端口 22 进行连接，则可通过 HTTPS 端口使用 SSH。

#### 可能存在的问题 {id="potential-problems"}

!!! failure "**问题内容** ssh_exchange_identification: Connection closed by remote host"

**防火墙可能会阻止 SSH 连接。** 确保远程主机的防火墙设置正确，允许 SSH 端口（默认是 22）通过：

1. 检查防火墙规则：

    ```Bash
    sudo ufw status
    ```

2. 如果防火墙阻止了 SSH 端口（22），可以使用以下命令允许：

    ```Bash
    sudo ufw allow 22
    ```

**如果未开启防火墙或开放端口之后仍然无效** 

如果仍然无效，则可能是设置代理后，22端口的 SSH 连接被代理阻塞，可以尝试通过更改 SSH 设置文件，将 GitHub 的 SSH 连接端口从 22 改为 443。

1. 首先打开 config 文件：

    ```Bash
    user@host:~$ vim ~/.ssh/config
    ```

2. 在文件中添加以下内容：

    ```Bash title=""
    Host github.com
        Hostname ssh.github.com
        Port 443
        User git
    ```

## 设置用户名与电子邮箱 {id="setting-your-username-and-commit-email-address"}

### 设置信息 {id="setting-information"}

**设置用户名**

```Bash title=""
git config --global user.name "(1)"
```

1. 里面填 git 账户名，比如 **`"iseastonlee"`**

**设置电子邮件**

```Bash
git config --global user.email "(1)"
```

1. 里面填 git 账号绑定的邮箱，比如 **`"iseastonlee@outlook.com"`**

!!! note ""

    如果想查看 **特定目录的 Git 设置** 就进入仓库目录后删掉 **`--global`** 参数即可

### 查看 {id="view-information"}

通过此命令可以查看 Git 的全局设置项，如用户名、邮箱地址等，帮助确保 Git 设置正确无误。

```Bash
git config --global --list
```

<div class="result" markdown>

!!! quote "示例输出"

    user.name=Your Name<br>
    user.email=your.email@example.com<br>

如果想查看 **特定目录的 Git 设置** 就进入仓库后去掉以下命令的 **`--global`** 即可
</div>

## 创建和管理仓库 {id="creating-and-managing-repositories"}

### 命令 {id="commands"}

| 命令 | 主要作用 |
| :- | :- |
| `git init` | 初始化仓库|
| `git clone` | 拷贝一份远程仓库，也就是下载一个项目|
| `git add` | 添加文件到暂存区|
| `git status` | 查看仓库当前的状态，显示有变更的文件  |
| `git commit` | 提交暂存区到本地仓库  |
| `git reset` | 回退版本 |
| `git rm` | 将文件从暂存区和工作区中删除 |
| `git mv` | 移动或重命名工作区文件 |
| `git checkout` | 分支切换 |
| `git show` | 显示 Git 对象的详细信息 |
| `git log` | 查看历史提交记录 |
| `git remote` | 远程仓库操作 |
| `git fetch` | 从远程获取代码库 |
| `git pull` | 下载远程代码并合并 |
| `git push` | 上传远程代码并合并 |
| `git branch` | 查看/创建/删除分支 |
| `git merge` | 合并分支 |
| `git rebase` | 变基（重新整理提交历史） |
| `git stash` | 临时保存当前工作区变更 |
| `git tag` | 创建/查看/删除标签 |
| `git diff` | 查看工作区/暂存区/提交间的差异 |
| `git config` | 查看/设置 Git 配置（如用户名、邮箱） |

### 文件 {id="file"}

|文件名|主要作用|备注 / 常见内容示例|
|:-|:-|:-|
|`.gitignore`|指定哪些文件/目录不被 Git 跟踪（忽略临时文件、构建产物、敏感信息等）|最经典的“特殊文件”，内容是 glob 模式|
|`.gitattributes`|定义文件属性（如哪些文件用 LF/CRLF、哪些用 diff、哪些二进制不 diff 等）|常用于跨平台换行符处理、LFS 文件标记|
|`.gitkeep`|占位文件（让 Git 跟踪空目录）|内容通常为空或写注释|
|`.gitmodules`|子模块（submodule）配置文件|用 `git submodule ad`d 时自动生成|
|`README.md`|项目说明文档（首页介绍、安装步骤、使用方法、贡献指南等）|GitHub/GitLab 等会自动渲染成仓库首页|
|`LICENSE` / `LICENSE.md`|项目开源许可协议（MIT、Apache 2.0、GPL 等）|GitHub 会自动识别并显示在侧边栏|
|`CONTRIBUTING.md`|贡献指南（如何提交 PR、代码规范、开发流程等）|GitHub 会自动链接到 PR 页面|
|`CHANGELOG.md` / `HISTORY.md`|版本变更记录（每个版本加了什么、修复了什么 bug）|常和 release 一起用|
|`SECURITY.md`|安全政策和漏洞报告指南|GitHub 会显示在仓库安全页面|
|`CODE_OF_CONDUCT.md`|行为准则（社区规范）|GitHub 会显示在社区部分|