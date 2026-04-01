---
icon: local/apple-ai
title: Mac 强开 Apple AI
# date:
#   created: 2026-03-26
comments: true
---

<h1>
在 MacOS 上强制开启 Apple Intelligence
</h1>

## 基础要求

1. 机型：必须是 M1 及以上的 Mac 电脑。

2. 系统版本：需要安装 macOS 15.4 或更高版本

3. 必须拥有一个非国区的 iCloud 账号

## 安装流程

///html | div.step
1. 创建一个新管理员用户
2. 暂时关闭Mac的SIP系统完整性保护，完成所有操作后还会重新打开，不用担心。

    将 Mac 关机后，长按电源键不放，根据提示选择刚才的账户进行登录，然后打开终端，输入这个命令并根据提示一路确认并输入密码之后 `reboot` 重启电脑。

    ```Bash { linenums="0" }
    csrutil disable
    ``` 

3. 进入系统后登陆美区账户，然后将 Siri 的语言改为美国，并且在「通用 --> 语言与地区」中将地区改为美国，然后将「首选语言」改为英语（美国）但不要重启电脑，然后删掉简体中文。此时再重启电脑。

4. 然后下载这个[脚本](/public/Tec/enable_ai.sh)，然后打开终端 terminal，将刚才这个脚本设置为可执行文件

    ```Bash { linenums="0" }
    chmod +x ~/Downloads/enable_ai.sh
    ```

5. 运行这个脚本

    ```Bash { linenums="0" }
    ~/Downloads/enable_ai.sh
    ```

    根据步骤一步一步来就行了。方法的话优先使用方法一，如果不行就使用方法二。

6. 重新开启SIP，让Mac恢复到比较安全的状态，方法和一开始关闭SIP差不多，将Mac关机，按住电源键不放开机，进入启动选项，打开终端，输入开启命令并重启电脑即可。

    ```Bash { linenums="0" }
    csrutil enable
    ```
///
