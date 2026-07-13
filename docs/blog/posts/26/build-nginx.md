---
icon: simple/nginx
title: Nginx 编译安装
date:
   created: 2026-02-17
   updated: 2026-07-09
categories:
    - Nginx
---

## 准备环境与依赖库

在编译之前先要明白自己的需求, 比如我现在需要 https / http2 和挂多个 HTTPS 域名, 那在编译 Nginx 之前首先就要安装构建工具和 Nginx 依赖的库。

```Bash
sudo apt update

sudo apt install -y build-essential \
libssl-dev libpcre3-dev \
zlib1g-dev \
wget
```

<!-- more -->

///html | small
:octicons-light-bulb-16:
注意：安装 `libssl-dev` 是确保 TLS SNI support enabled 的关键，因为它提供了编译所需的 OpenSSL 开发头文件。
///

## 下载 Nginx 源码

我选定的版本是 1.26.3, 前往自己喜欢的目录去拉取对应版本的源码包。

```Bash
wget https://nginx.org/download/nginx-1.26.3.tar.gz
tar -zxvf nginx-1.26.3.tar.gz
cd nginx-1.26.3
```

## 配置编译参数

接下来将安装路径指向自定义目录, 比如我这里指定的是 `/usr/local/nginx` 目录。

```Bash
./configure --prefix=/usr/local/nginx \
--pid-path=/usr/local/nginx/logs/nginx.pid \
--with-http_ssl_module \
--with-http_v2_module \
--with-cc-opt="-I/usr/include" \
--with-ld-opt="-L/usr/lib"
```

///html | small
关于 TLS SNI Support: 只要你的系统 openssl 版本不低于 0.9.8f（Ubuntu 20.04+ 通常是 1.1.1 或 3.0+），在 configure 阶段会自动检测并显示 TLS SNI support enabled。
///

## 编译/安装/验证

编译和安装。

```Bash
make -j$(nproc)

sudo make install
```

检查 Nginx 是否安装成功。

```Bash
/usr/local/nginx/sbin/nginx -V
```

///html | div.result
```Bash { linenums="0" .yaml .no-copy }
nginx version: nginx/1.26.3
built by gcc 11.4.0 (Ubuntu 11.4.0-1ubuntu1~22.04.3)
built with OpenSSL 3.0.2 15 Mar 2022
TLS SNI support enabled
configure arguments: --prefix=/usr/local/nginx --with-http_ssl_module --with-http_v2_module --with-cc-opt=-I/usr/include --with-ld-opt=-L/usr/lib
```
///

## 允许免密登录

修改 ssh 配置文件, 允许公钥登录。

```Bash
vim /etc/ssh/sshd_config
```

///html | div.result
`PubkeyAuthentication no` --> `PubkeyAuthentication yes`
///

重启 ssh 服务

```Bash
systemctl restart ssh
```

## 开机自启 nginx 服务

创建 Nginx 的 systemd 服务配置文件。

```Bash
sudo vim /etc/systemd/system/nginx.service
```

输入以下内容：

```Ini { linenums="0" }
[Unit]
Description=The NGINX HTTP and reverse proxy server
After=network.target

[Service]
Type=forking
PIDFile=/usr/local/nginx/logs/nginx.pid

ExecStartPre=/usr/local/nginx/sbin/nginx -t
ExecStart=/usr/local/nginx/sbin/nginx
ExecReload=/usr/local/nginx/sbin/nginx -s reload
ExecStop=/usr/local/nginx/sbin/nginx -s quit

PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

重新加载 systemd 配置并启动 Nginx 服务。

```Bash
sudo systemctl daemon-reload

sudo systemctl start nginx
```

查看 Nginx 服务当前的运行状态。

```Bash
sudo systemctl status nginx
```

///html | div.result
```Bash { linenums="0" .yaml .no-copy }
● nginx.service - The NGINX HTTP and reverse proxy server
     Loaded: loaded (/etc/systemd/system/nginx.service; disabled; vendor preset: enabled)
     Active: active (running) since Thu 2026-07-09 05:39:11 UTC; 5s ago
    Process: 20504 ExecStartPre=/usr/local/nginx/sbin/nginx -t (code=exited, status=0/SUCCESS)
    Process: 20505 ExecStart=/usr/local/nginx/sbin/nginx (code=exited, status=0/SUCCESS)
   Main PID: 20506 (nginx)
      Tasks: 2 (limit: 1090)
     Memory: 2.5M
        CPU: 32ms
     CGroup: /system.slice/nginx.service
             ├─20506 "nginx: master process /usr/local/nginx/sbin/nginx"
             └─20507 "nginx: worker process" "" "" "" "" "" ""

Jul 09 05:39:10 hostname systemd[1]: Starting The NGINX HTTP and reverse proxy server...
Jul 09 05:39:10 hostname nginx[PID]: nginx: the configuration file /usr/local/nginx/conf/nginx.conf syntax is ok
Jul 09 05:39:10 hostname nginx[PID]: nginx: configuration file /usr/local/nginx/conf/nginx.conf test is successful
```
///

设置开机自启

```Bash
sudo systemctl enable nginx
```

///html | div.result
成功提示：

```Bash { linenums="0" .yaml .no-copy }
Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /etc/systemd/system/nginx.service.
```
///