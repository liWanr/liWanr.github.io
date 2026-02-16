---
icon: lucide/git-merge
title: Git 基本知识
tags:
    - Knowledge
    - Git
---

<small>
created: 2025-01-20
updated: 2025-02-22
</small>

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

## 常用的命令 {id="common-commands"}

|命令|主要作用|常用参数|使用场景|
|:-|:-|:-|:-|
|`gitinit`|初始化仓库|`--bare`创建裸仓库|在新项目目录创建Git仓库|
|`gitclone`|拷贝一份远程仓库|`-b<branch>`克隆指定分支<br>`--depth1`浅克隆|下载远程项目到本地|
|`gitadd`|添加文件到暂存区|`.`添加所有文件<br>`-A`添加所有变更<br>`-p`交互式添加|准备提交前暂存修改|
|`gitstatus`|查看仓库当前状态|`-s`简洁模式<br>`-b`显示分支信息|查看哪些文件被修改/暂存|
|`gitcommit`|提交暂存区到本地仓库|`-m"message"`添加提交信息<br>`-a`自动暂存已跟踪文件<br>`--amend`修改上次提交|保存代码变更到本地历史|
|`gitreset`|回退版本|`--soft`保留工作区和暂存区<br>`--mixed`保留工作区<br>`--hard`全部丢弃|撤销提交或取消暂存|
|`gitrm`|删除文件|`-r`递归删除目录<br>`--cached`仅从暂存区删除|从版本控制中移除文件|
|`gitmv`|移动或重命名文件|无特殊参数|重命名文件并保留历史|
|`gitcheckout`|切换分支/恢复文件|`-b<branch>`创建并切换分支<br>`--<file>`恢复文件|切换工作分支或丢弃文件修改|
|`gitswitch`|切换分支（新命令）|`-c<branch>`创建并切换分支|更清晰的分支切换操作|
|`gitrestore`|恢复文件（新命令）|`--staged`取消暂存<br>`--source`指定来源|恢复工作区或暂存区文件|
|`gitshow`|显示对象详细信息|`<commit>`查看指定提交<br>`<tag>`查看标签|查看提交内容或标签信息|
|`gitlog`|查看提交历史|`--oneline`单行显示<br>`--graph`图形化<br>`-n<num>`限制数量|浏览项目历史记录|
|`gitremote`|管理远程仓库|`add<name><url>`添加远程库<br>`-v`查看详细信息|配置远程仓库地址|
|`gitfetch`|获取远程更新|`--all`获取所有远程库<br>`--prune`清理远程已删除分支|下载远程更新但不合并|
|`gitpull`|拉取并合并远程代码|`--rebase`使用变基方式<br>`origin<branch>`指定分支|同步远程分支到本地|
|`gitpush`|推送到远程仓库|`-uorigin<branch>`设置上游<br>`--force`强制推送<br>`--tags`推送标签|上传本地提交到远程|
|`gitbranch`|分支管理|`-a`查看所有分支<br>`-d`删除分支<br>`-m`重命名|创建/查看/删除分支|
|`gitmerge`|合并分支|`--no-ff`禁用快进<br>`--squash`压缩提交|将其他分支合并到当前分支|
|`gitrebase`|变基整理历史|`-i`交互式变基<br>`--continue`继续变基|整理提交历史或同步主分支|
|`gitstash`|临时保存工作区|`save"message"`添加说明<br>`pop`恢复并删除<br>`list`查看列表|暂存当前修改切换任务|
|`gittag`|标签管理|`-a<tag>`创建附注标签<br>`-d<tag>`删除标签|标记重要版本节点|
|`gitdiff`|查看差异|`--cached`查看暂存区差异<br>`<commit1><commit2>`对比提交|对比文件或提交的变更|
|`gitconfig`|配置Git|`--globaluser.name`设置用户名<br>`--list`查看配置|初始配置或修改Git设置|
|`gitcherry-pick`|挑选提交|`<commit>`应用指定提交|将特定提交应用到当前分支|

## Git 项目常见配置文件说明 {id="git-project-files"}

|文件名|主要作用|备注/常见内容示例|
|:-|:-|:-|
|`.gitignore`|指定文件/目录不被Git跟踪|**最常用的配置文件**<br>- 忽略临时文件、构建产物、依赖包、敏感信息<br>- 使用glob模式，如`*.log`、`node_modules/`、`.env`<br>- 可用[gitignore.io](https://gitignore.io)生成模板|
|`.gitattributes`|定义文件属性和处理规则|- 统一换行符：`*text=auto`或`*.shtexteol=lf`<br>- 标记二进制文件：`*.pngbinary`<br>- GitLFS配置：`*.psdfilter=lfs`<br>- 自定义diff驱动|
|`.gitkeep`|跟踪空目录的占位文件|- Git默认不跟踪空目录，此文件可让目录进入版本控制<br>- 文件内容通常为空或一行注释<br>- 常用于`logs/`、`tmp/`、`uploads/`等目录|
|`.gitmodules`|子模块(submodule)配置|- 执行`gitsubmoduleadd<url>`时自动生成<br>- 记录子模块路径、URL、分支信息<br>- 格式：`[submodule"name"]`<br>`path=xxx`<br>`url=xxx`|
|`README.md`|项目说明文档|**必备文件**<br>- 包含：项目介绍、功能特性、安装步骤、使用示例、贡献方式<br>- GitHub/GitLab自动渲染为仓库首页<br>- 支持Markdown格式（标题、代码块、图片、徽章等）|
|`LICENSE`<br>`LICENSE.md`|开源许可协议|- 常见协议：MIT（宽松）、Apache2.0、GPL（传染性）、BSD<br>- GitHub创建仓库时可自动添加<br>- 会显示在仓库侧边栏和文件列表顶部<br>- **没有LICENSE意味着默认版权保留**|
|`CONTRIBUTING.md`|贡献者指南|- 包含：如何提交Issue/PR、代码规范、分支策略、测试要求<br>- GitHub在创建Issue/PR时会自动提示此文件|
|`CHANGELOG.md`<br>`HISTORY.md`|版本变更日志|- 记录每个版本的新增功能、bug修复、破坏性变更<br>- 推荐格式：[KeepaChangelog](https://keepachangelog.com/)<br>- 分类：`Added`、`Changed`、`Deprecated`、`Removed`、`Fixed`、`Security`|
|`SECURITY.md`|安全政策和漏洞报告指南|- 说明如何报告安全漏洞（通常是私密渠道）<br>- 列出支持的版本、修复时间表<br>- GitHub会在仓库安全标签页显示此文件|
|`CODE_OF_CONDUCT.md`|社区行为准则|- 定义社区规范、期望行为、不可接受行为、执行措施<br>- 常用模板：[ContributorCovenant](https://www.contributor-covenant.org/)<br>- GitHub会在社区健康文件中显示|
|`.editorconfig`|统一编辑器配置|- 跨编辑器统一代码风格（缩进、换行符、字符集等）<br>- 示例：`indent_style=space`、`indent_size=2`<br>- 主流编辑器（VSCode、IDEA）都支持|
|`.env.example`<br>`.env.sample`|环境变量配置模板|- 提供环境变量示例（实际`.env`在`.gitignore`中）<br>- 包含：数据库连接、API密钥（占位符）、功能开关<br>- 开发者复制为`.env`后填入真实配置|
|`package.json`|Node.js项目配置文件|- 定义依赖、脚本、版本、入口文件等<br>- npm/yarn/pnpm的核心配置<br>- 包含`dependencies`、`devDependencies`、`scripts`|
|`requirements.txt`<br>`Pipfile`|Python项目依赖文件|- `requirements.txt`：pip依赖列表<br>- `Pipfile`：Pipenv依赖管理<br>- 用于`pipinstall-rrequirements.txt`安装依赖|
|`Makefile`|自动化任务脚本|- 定义常用命令快捷方式（构建、测试、部署等）<br>- 使用`makebuild`、`maketest`等执行<br>- 跨平台兼容性需注意|
|`Dockerfile`<br>`docker-compose.yml`|Docker容器化配置|- `Dockerfile`：镜像构建指令<br>- `docker-compose.yml`：多容器编排配置<br>- 用于统一开发、测试、生产环境|