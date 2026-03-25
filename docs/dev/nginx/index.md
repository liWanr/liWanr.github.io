---
icon: simple/nginx
title: Nginx
# date:
#     created: 2026-02-17
tags:
    - Net
comments: true
---

## 准备环境与依赖库 {id="prep-env-deps"}

在编译之前先要明白自己的需求, 比如我现在需要 https / http2 和挂多个 HTTPS 域名, 那在编译 Nginx 之前首先就要安装构建工具和 Nginx 依赖的库

```Bash
sudo apt update
sudo apt install build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev openssl libssl-dev curl -y
```

///html | small
:octicons-light-bulb-16:
注意：安装 `libssl-dev` 是确保 TLS SNI support enabled 的关键，因为它提供了编译所需的 OpenSSL 开发头文件。
///

## 下载 Nginx 源码 {id="download-nginx-src"}

我选定的版本是 1.26.3, 前往自己喜欢的目录去拉取对应版本的源码包。比如我这里去 `/usr/local/nginx` 这个目录

```Bash
wget https://nginx.org/download/nginx-1.26.3.tar.gz
tar -zxvf nginx-1.26.3.tar.gz
cd nginx-1.26.3
```

## 配置编译参数 {id="config-build-opts"}

接下来将所有的安装路径都指向刚才的目标目录, 并且当前用户拥有目录的所有权。

```Bash
./configure --prefix=/usr/local/nginx \
--with-http_ssl_module \
--with-http_v2_module \
--with-cc-opt="-I/usr/include" \
--with-ld-opt="-L/usr/lib"
```

///html | small
关于 TLS SNI Support: 只要你的系统 openssl 版本不低于 0.9.8f（Ubuntu 20.04+ 通常是 1.1.1 或 3.0+），在 configure 阶段会自动检测并显示 TLS SNI support enabled。
///

## 编译/安装/验证 {id="build-install-verify"}

///html | div.step

1. 首先编译和安装

    ```Bash { linenums="0" }
    make && make install
    ```

2. **进入安装目录**并检查

    ```Bash { linenums="0" }
    ./sbin/nginx -V
    ```

    ///html | div.result

    nginx version: nginx/1.26.3<br>
    built by gcc 11.4.0 (Ubuntu 11.4.0-1ubuntu1~22.04.3)<br>
    built with OpenSSL 3.0.2 15 Mar 2022<br>
    TLS SNI support enabled<br>
    configure arguments: --prefix=/usr/local/nginx --with-http_ssl_module --with-http_v2_module --with-cc-opt=-I/usr/include --with-ld-opt=-L/usr/lib

    ///


## 基本命令

///tab | 测试配置

```Bash { linenums="0" }
.sbin/nginx -t
```

///

///tab | 启动服务

```Bash { linenums="0" }
.sbin/nginx
```

///

///tab | 热重载配置

```Bash { linenums="0" }
.sbin/nginx -s reload
```

///

///tab | 终止服务

```Bash { linenums="0" }
.sbin/nginx -s stop
```

///