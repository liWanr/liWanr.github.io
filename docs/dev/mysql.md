---
icon: simple/dolphin
title: MySQL
comments: true
# date:
#     created: 2026-03-25
tags:
    - Tech
---

## 安装 / 卸载 / 服务管理

///tab | 安装最新版
///html | div.step
1. 更新软件包并安装 MySQL 服务器，安装过程中会自动启动MySQL服务。

    ```bash
    sudo apt update
    sudo apt install mysql-server
    ```

2. 检查服务状态

    ```bash
    sudo systemctl status mysql
    ```

3. 运行安全安装脚本，设置 root 密码并移除匿名用户等。

    ```bash
    sudo mysql_secure_installation
    ```

4. 登录 MySQL，使用之前设置的 root 密码。

    ```bash
    mysql -u root -p
    ```
///
///

///tab | 安装特定版本
///html | div.step
1. 从服务器获取最新密钥，并将其转换为二进制格式存放在正确的路径

    ```bash
    gpg --keyserver keyserver.ubuntu.com --recv-keys B7B3B788A8D3785C
    gpg --export B7B3B788A8D3785C | sudo gpg --dearmor -o /usr/share/keyrings/mysql-archive-keyring.gpg
    ```

2. 修改软件源配置文件

    ```bash
    echo "deb [signed-by=/usr/share/keyrings/mysql-archive-keyring.gpg] http://repo.mysql.com/apt/ubuntu/ jammy mysql-8.4-lts" | sudo tee /etc/apt/sources.list.d/mysql.list
    ```

3. 同步并安装

    ```bash
    sudo apt update
    ```

4. 正式安装 MySQL 服务

    ```bash 
    sudo apt install mysql-server -y #(1)!
    ```

    1. 安装过程中会弹窗要求设置 root 密码，请务必牢记。

5. 查看 MySQL 服务状态

    ```bash
    sudo systemctl status mysql
    ```

    ///html | div.result
    只要看到 **`Active: active (running)`** 就说明安装成功了。
    ///

6. 检查安装版本

    ```bash
    mysql --version
    ```

    ///html | div.result
    `mysql  Ver 8.4.8 for Linux on x86_64 (MySQL Community Server - GPL)`
    ///

7. 运行安全配置脚本（推荐）

    ```bash
    sudo mysql_secure_installation
    ```

    根据系统提示，你可以进行以下安全加固操作：

    - 开启密码强度校验组件 (VALIDATE PASSWORD component)

    - 更改 root 密码（如果在安装时已经设置且满意，可按 N 跳过）

    - 删除匿名用户 (Remove anonymous users)

    - 禁止 root 用户远程登录 (Disallow root login remotely)

    - 删除测试数据库 (Remove test database)

    - 重新加载权限表 (Reload privilege tables)
///
///

///tab | 卸载
///html | div.step
1. 停止MySQL服务

    ```bash
    sudo systemctl stop mysql
    ```

2. 卸载MySQL相关软件包

    ```bash
    sudo apt-get remove --purge mysql-server mysql-client mysql-common mysql-server-core-* mysql-client-core-*
    sudo apt-get autoremove --purge
    sudo apt-get autoclean
    ```

3. 删除数据和配置目录

    ```bash
    sudo rm -rf /var/lib/mysql /etc/mysql /var/log/mysql
    ```
///
///

///tab | 服务管理

///html | div.grid
```bash { title="启动" linenums="0" }
sudo systemctl start mysql
``` 

```bash { title="停止" linenums="0" }
sudo systemctl stop mysql
```

```bash { title="重启" linenums="0" }
sudo systemctl restart mysql
```

```bash { title="查看状态" linenums="0" }
sudo systemctl status mysql
```
///
///