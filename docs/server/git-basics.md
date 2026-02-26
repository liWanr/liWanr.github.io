---
icon: lucide/git-merge
title: Git 基本知识
# date:
#     created: 2025-01-20
#     updated: 2025-02-26
tags:
    - Git
---

## 安装 Git {id="install-git"}

若要在命令行上使用 Git, 需要在计算机上安装、安装和设置 Git。 [下载并安装最新版本的 Git](https://git-scm.com/install/windows)

!!! warning "在 Chrome OS 上启用和安装 Git"

    从 2020 年开始大部分 Chrome OS 设备都内置 Git。 如果需要启用可以去 Launcher 搜索 Linux 并打开。

    如果你使用较早版本的 Chrome OS 设备, 则需要使用 **其他方法** ：

    1. 在 Chrome OS 设备上安装终端模拟器, 例如 Google Play 商店中的 Termux。

    2. 从您安装的终端模拟器安装 Git。 例如, 在 Termux 中, 输入 `pkg install git` 并在出现提示时键入 ++y++。

## 速查表 {id="git-cheat-sheet"}

=== "**Git 文件**"

    <div class="grid cards" markdown>

    - 本地 Git 配置文件

        ```Bash
        .git/config
        ```

    - 全局 Git 配置文件

        ```Bash
        ~/.gitconfig
        ```

    - 忽略文件规则

        ```Bash
        .gitignore
        ```

    </div>

=== "**配置**"

    <div class="grid cards" markdown>

    - 设置用户信息

        ```Bash
        git config user.name "(1)"
        git config user.email "(2)"
        ```

        1. 用户名
        2. 电子邮箱

    - 全局配置

        ```Bash
        git config --global ...
        ```

    - 添加别名

        ```Bash
        git config alias.st status
        ```

    - 查看所有配置选项

        ```Bash
        man git-config
        ```
    
    </div>

=== "**仓库**"

    <div class="grid cards" markdown>

    - 初始化一个新的仓库

        ```Bash
        git init
        ```

    - 克隆现有仓库

        ```Bash
        git clone <url>
        ```

    - 查看远程仓库

        ```Bash
        git remote -v
        ```

    - 添加远程仓库

        ```Bash
        git remote add origin <url>
        ```

    - 修改远程仓库地址

        ```Bash
        git remote set-url origin <url>
        ```

    - 删除远程仓库

        ```Bash
        git remote remove origin
        ```

    </div>

=== "**暂存**"

    <div class="grid cards" markdown>

    - 添加未跟踪文件或修改到暂存区

        ```Bash
        git add <file>
        ```

    - 添加所有未跟踪文件和修改

        ```Bash
        git add .
        ```

    - 交互式选择要暂存的部分内容

        ```Bash
        git add -p
        ```

    - 移动或重命名文件

        ```Bash
        git mv <old> <new>
        ```

    - 删除文件

        ```Bash
        git rm <file>
        ```

    - 从版本控制中移除但保留本地文件

        ```Bash
        git rm --cached <file>
        ```

    - 取消暂存某个文件

        ```Bash
        git reset <file>
        ```

    - 取消暂存所有文件

        ```Bash
        git reset
        ```

    - 查看当前状态

        ```Bash
        git status
        ```

    </div>

=== "**提交**"

    <div class="grid cards" markdown>

    - 提交更改

        ```Bash
        git commit
        ```

    - 提交并附带说明信息

        ```Bash
        git commit -m "message"
        ```

    - 提交所有已跟踪文件的修改

        ```Bash
        git commit -am "message"
        ```

    - 修改上一次提交

        ```Bash
        git commit --amend
        ```

    </div>

=== "**推送**"

    <div class="grid cards" markdown>

    - 将 `main` 分支推送到远程仓库 `origin`

        ```Bash
        git push origin main
        ```

    - 推送当前分支到其远程跟踪分支

        ```Bash
        git push
        ```

    - 首次推送新分支并建立跟踪关系

        ```Bash
        git push -u origin <name>
        ```

    - 强制推送（更安全方式）

        ```Bash
        git push --force-with-lease
        ```

    - 推送所有标签

        ```Bash
        git push --tags
        ```

    </div>

=== "**拉取**"

    <div class="grid cards" markdown>

    - 获取远程更新但不修改本地分支

        ```Bash
        git fetch origin main
        ```

    - 拉取并变基

        ```Bash
        git pull --rebase
        ```

    - 拉取并合并

        ```Bash
        git pull origin main
        ```

        ```Bash
        git pull
        ```

    </div>

=== "**差异**"

    <div class="grid cards" markdown>

    - 查看未暂存修改

        ```Bash
        git diff
        ```

    - 查看已暂存修改

        ```Bash
        git diff --staged
        ```

    - 比较两个分支

        ```Bash
        git diff branch1..branch2
        ```

    - 比较两个提交

        ```Bash
        git diff <commit1> <commit2>
        ```

    </div>

=== "**分支**"

    <div class="grid cards" markdown>

    - 切换分支

        ```Bash
        git checkout <name>
        ```

        ```Bash
        git switch <name>
        ```

    - 创建并切换到新分支

        ```Bash
        git checkout -b <name>
        ```

        ```Bash
        git switch -c <name>
        ```

    - 列出分支

        ```Bash
        git branch
        ```

    - 按最近提交时间排序列出分支

        ```Bash
        git branch --sort=-committerdate
        ```

    - 删除分支

        ```Bash
        git branch -d <name>
        ```

    - 强制删除分支

        ```Bash
        git branch -D <name>
        ```

    </div>

    <small>
    :octicons-light-bulb-16:
    Git `v2.23` 后新增了 `switch` 和`restore` 命令, 用于拆解原来多功能命令 `checkout`。以前的 `checkout` 同时在做切换分支、创建分支、恢复文件三件事, 现在 `switch` 用于切换分支、创建分支, `restore` 用于恢复文件 
    </small>

=== "**合并分叉分支**"

    <div class="grid cards" markdown>

    - 合并分支

        ```Bash
        git switch main
        git merge <branch>
        ```

        ```mermaid
        ---
        config:
            themeVariables:
                'git0': '#FFCB5E'
                'git1': '#77A3FF'
        ---
        gitGraph
            commit id: "A"
            commit id: "B"
            branch banana
            commit id: "D"
            commit id: "E"
            checkout main
            commit id: "C"
            merge banana
        ```

    - 与 `rebase` 结合使用

        ```Bash
        git switch <branch>
        git rebase main
        ```

        ```mermaid
        ---
        config:
            themeVariables:
                    'git0': '#FFCB5E'
                    'git1': '#ffb2b2ff'
                    'git2': '#77A3FF'
        ---
        gitGraph
            commit id: "A"
            commit id: "B"

            branch lost
            commit id: "D" type: REVERSE
            commit id: "E" type: REVERSE

            checkout main
            commit id: "C"

            branch banana
            checkout banana
            commit id: "D'"
            commit id: "E'"
        ```

    - 与 `squash` merge 合并

        ```Bash
        git merge --squash <branch>
        ```

        ```mermaid
        ---
        config:
            themeVariables:
                'git0': '#FFCB5E'
                'git1': '#77A3FF'
        ---
        gitGraph
            commit id: "A"
            commit id: "B"
            branch banana
            commit id: "D"
            commit id: "E"
            checkout main
            commit id: "D E"
        ```

    - 将一个提交复制到当前分支

        ```Bash
        git cherry-pick <commit>
        ```

        ```mermaid
        ---
        config:
            themeVariables:
                'git0': '#FFCB5E'
                'git1': '#77A3FF'
        ---
        gitGraph
            commit id: "A"
            commit id: "B"
            branch banana
            commit id: "D"
            commit id: "E"
            checkout main
            commit id: "C"
            commit id: "D'"
        ```

    - 交互式变基

        ```Bash
        git rebase -i HEAD~3
        ```

        ```mermaid
        ---
        config:
            themeVariables:
                'git0': '#FFCB5E'
                'git1': '#77A3FF'
        ---
        gitGraph
            commit id: "A"
            commit id: "B"
            commit id: "C" type: REVERSE
            commit id: "D" type: REVERSE
            commit id: "E" type: REVERSE
            commit id: "C'"
            commit id: "DE'"
        ```

    </div>

=== "**回退**"

    <div class="grid cards" markdown>

    - 回退到上一个提交（保留修改）

        ```Bash
        git reset --soft HEAD~1
        ```

    - 回退到上一个提交（丢弃修改）

        ```Bash
        git reset --hard HEAD~1
        ```

    - 生成新的回滚提交

        ```Bash
        git revert <commit>
        ```

    </div>

=== "**放弃更改**"

    <div class="grid cards" markdown>

    - 丢弃某个文件的未暂存修改

        ```Bash
        git restore <file>
        ```

        ```Bash
        git checkout <file>
        ```

    - 丢弃单个文件的所有修改

        ```Bash
        git restore --staged --worktree <file>
        ```

        ```Bash
        git checkout HEAD <file>
        ```

    - 丢弃所有已暂存和未暂存的修改

        ```Bash
        git reset --hard
        ```

    - 删除未跟踪文件

        ```Bash
        git clean -f
        ```

    </div>

=== "**标签**"

    <div class="grid cards" markdown>

    - 创建标签

        ```Bash
        git tag v1.0
        ```

    - 创建带说明的标签

        ```Bash
        git tag -a v1.0 -m "release"
        ```

    - 查看标签

        ```Bash
        git tag
        ```

    - 删除标签

        ```Bash
        git tag -d v1.0
        ```

    </div>

=== "**日志**"

    <div class="grid cards" markdown>

    - 查看提交历史

        ```Bash
        git log
        ```

    - 单行简洁显示

        ```Bash
        git log --oneline
        ```

    - 图形化显示分支结构

        ```Bash
        git log --oneline --graph --decorate --all
        ```

    - 查看某个文件的提交历史

        ```Bash
        git log <file>
        ```

    - 查看文件每一行的修改者

        ```Bash
        git blame <file>
        ```

    - 查看引用记录（找回误删提交）

        ```Bash
        git reflog
        ```

    </div>

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

5. 当密钥添加到 GitHub 且本地已经配置用户名和电子邮箱的完成后，就可以检测本地和 GitHub 的连接状态了

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

6. 这期间可能存在会有问题, 特别是用了代理的玩家, 可能会出现 **远程主机已关闭连接** 的报错

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