---
icon: simple/nginx
title: Ubuntu 编译安装 Nginx 
tags:
  - Server
  - Network
---

<small>
created: 2026-02-17
</small>

## 准备环境与依赖库 {id="prep-env-deps"}

在编译之前先要明白自己的需求, 比如我现在需要 https / http2 和挂多个 HTTPS 域名, 那在编译 Nginx 之前首先就要安装构建工具和 Nginx 依赖的库

```Bash
sudo apt update
sudo apt install build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev openssl libssl-dev curl -y
```

<small>
:octicons-light-bulb-16:
注意：安装 `libssl-dev` 是确保 TLS SNI support enabled 的关键，因为它提供了编译所需的 OpenSSL 开发头文件。
</small>

## 下载 Nginx 源码 {id="download-nginx-src"}

我选定的版本是 1.26.3, 前往自己喜欢的目录去拉取对应版本的源码包。比如我这里去 `~/website/nginx1.26.3` 这个目录

```Bash
wget https://nginx.org/download/nginx-1.26.3.tar.gz
tar -zxvf nginx-1.26.3.tar.gz
cd nginx-1.26.3
```


## 配置编译参数 {id="config-build-opts"}

接下来将所有的安装路径都指向刚才的目标目录, 并且当前用户拥有目录的所有权。

```Bash
./configure \
--prefix=$HOME/website/nginx1.26.3 \
--with-http_ssl_module \
--with-http_v2_module \
--with-cc-opt="-I/usr/include" \
--with-ld-opt="-L/usr/lib"
```

<small>
关于 TLS SNI Support: 只要你的系统 openssl 版本不低于 0.9.8f（Ubuntu 20.04+ 通常是 1.1.1 或 3.0+），在 configure 阶段会自动检测并显示 TLS SNI support enabled。
</small>

如果没有目录的所有权，就执行这个


```Bash
sudo chown -R ubuntu:ubuntu ~/website/env/nginx-1.26.3
sudo chmod -R 755 ~/website/env/nginx-1.26.3
```

<div class="result" markdown>

第一个 ubuntu 是**用户名**, 第二个 ubuntu 是**用户组名**

</div>

## 编译/安装/验证 {id="build-install-verify"}

首先编译和安装

```Bash
make && make install
```

进入安装后的目录并检查

```Bash
cd ~/website/nginx1.26.3
./sbin/nginx -V
```

<div class="result" mardown>

输出内容

```Text { .yaml .no-copy}
nginx version: nginx/1.26.3
built by gcc 11.4.0 (Ubuntu 11.4.0-1ubuntu1~22.04.2) 
built with OpenSSL 3.0.2 15 Mar 2022
TLS SNI support enabled
configure arguments: --prefix=/home/ubuntu/website/nginx1.26.3 --with-http_ssl_module --with-http_v2_module
```

</div>

## 基本命令

=== "测试配置"

    ```Bash
    .sbin/nginx -t
    ```

    正常输出：

    ```Text { .yaml .no-copy }
    nginx: the configuration file */conf/nginx.conf syntax is ok
    nginx: configuration file */conf/nginx.conf test is successful
    ```

=== "启动服务"

    ```Bash
    .sbin/nginx
    ```

    常规没输出

=== "热重载配置"

    ```Bash
    .sbin/nginx -s reload
    ```

    常规没输出

=== "终止服务"

    ```Bash
    .sbin/nginx -s stop
    ```

    常规没输出