---
icon: lucide/file-sliders
title: 配置文件
comments: true
# date:
#     created: 2026-04-03
tags:
    - Tech
---

Nginx 的配置文件通常位于 `.../nginx/nginx.conf`。

## 基础配置示例

```nginx
# ------------------------------
# 全局配置
# ------------------------------

worker_processes  auto;                # 设置工作进程数，通常建议等于 CPU 核心数

# ------------------------------
# events 块：定义连接处理相关参数
# ------------------------------

events {
    worker_connections  1024;       # 每个 worker 进程允许的最大连接数
}

# ------------------------------
# HTTP 配置块
# ------------------------------
http {
    # 常用 MIME 类型定义
    include       mime.types;
    default_type  application/octet-stream;

    # 文件传输优化
    sendfile        on;     # 高效传输静态文件
    tcp_nopush      on;     # 避免分片发送小包
    tcp_nodelay     on;     # 减少延迟
    keepalive_timeout  65;  # 长连接超时时间（秒）

    # 安全和性能
    server_tokens   off;    # 禁止显示 Nginx 版本号

    gzip            on;     # 启用 Gzip 压缩，提高传输效率
    gzip_min_length 1k;     # 小于 1KB 的文件不压缩
    gzip_comp_level 9;      # 压缩等级 1~9
    gzip_types              # 压缩特定类型的文件
        text/plain
        text/css
        application/javascript
        application/json
        image/svg+xml
        font/woff2;

    # 临时文件路径（可以统一管理缓冲区）
    client_body_temp_path  /temp/client_body;
    proxy_temp_path        /temp/proxy;
    fastcgi_temp_path      /temp/fastcgi;
    uwsgi_temp_path        /temp/uwsgi;
    scgi_temp_path         /temp/scgi;

    # ------------------------------
    # Server 配置
    # ------------------------------
    server {
        # 监听端口
        listen 80;
        listen [::]:80;

        # 域名
        server_name example.com;

        # 默认字符集
        charset utf-8;

        # ==============================
        # 私有文件目录（需鉴权，不缓存）
        # ==============================
        location /private/ {
            alias /var/www/private/;      # 实际存放路径
            autoindex on;                 # 启用目录浏览
            autoindex_exact_size off;     # 文件大小格式化显示
            autoindex_localtime on;       # 显示本地时间

            # HTTP 基本鉴权
            auth_basic "Auth Login";
            auth_basic_user_file /etc/nginx/passwd.dat;

            # 禁用缓存
            add_header Cache-Control "no-store, no-cache, must-revalidate, private";
            add_header Pragma "no-cache";
            expires -1;
        }

        # ==============================
        # 公共文件目录（浏览，不缓存）
        # ==============================
        location /public/ {
            alias /var/www/public/;
            autoindex on;
            autoindex_exact_size off;
            autoindex_localtime on;

            # 禁用缓存
            add_header Cache-Control "no-store, no-cache, must-revalidate";
            add_header Pragma "no-cache";
            expires -1;
        }

        # 网站根目录
        root /var/www/html/website;

        # ==============================
        # 错误页面配置
        # ==============================
        error_page 404 /404.html;   # 当请求不存在页面时返回 404.html
        location = /404.html {
            internal;               # 内部调用，用户无法直接访问
        }

        # ==============================
        # 主站（静态页面）
        # ==============================
        location / {
            index index.html;         # 默认首页
        }

        # ==============================
        # 静态资源缓存（图片/图标/字体/JS/CSS）
        # ==============================
        location ~* \.(jpg|jpeg|png|gif|webp|svg|ico|woff2|js|css)$ {
            root /var/www/html/website;

            # 浏览器缓存 1 周
            expires 7d;
            add_header Cache-Control "public";

            # 关闭访问日志（减轻 IO 压力）
            access_log off;
        }
    }
}
```

## 其他配置

| 配置项 | 作用 |
| ---- | --- |
| `#!nginx worker_processes auto;` | 自动根据 CPU 核心数生成工作进程，充分利用多核 |
| `#!nginx worker_connections` | 增大允许的并发连接数（配合 `#!nginx worker_processes` 使用） |
| `#!nginx sendfile on;` | 零拷贝发送静态文件，提高 I/O 性能 |
| `#!nginx tcp_nopush on;` | 优化大文件传输，减少分片包 |
| `#!nginx tcp_nodelay on;` | 减少小包传输延迟 |
| `#!nginx keepalive_timeout 65;` | HTTP 长连接，减少重复 TCP 握手 |
| `#!nginx gzip on; gzip_types ...;` | 压缩文本资源，减少带宽消耗 |
| `#!nginx open_file_cache` | 缓存文件描述符，减少磁盘 I/O |
| `#!nginx client_body_buffer_size` <br> `#!nginx client_max_body_size` | 调整上传文件缓冲，避免频繁写磁盘 |
| `#!nginx proxy_cache` <br> `#!nginx fastcgi_cache` | 反向代理缓存或动态请求缓存，减轻后端压力 |
| `#!nginx limit_req` <br> `#!nginx limit_conn` | 限制请求频率和连接数，防止刷流量 |
| `#!nginx server_tokens off;` | 禁止显示 Nginx 版本号，减少被针对的风险 |
| `#!nginx client_max_body_size` | 限制上传文件大小，防止大文件攻击 |
| `#!nginx limit_req zone=...` | 防止请求洪水攻击（Rate Limit） |
| `#!nginx limit_conn zone=...` | 限制同一 IP 并发连接数 |
| `#!nginx ssl_protocols TLSv1.2 TLSv1.3;` | 只启用安全的 TLS 协议（HTTPS 时） |
| `#!nginx ssl_ciphers` | 强制安全加密套件 |
| `#!nginx add_header X-Frame-Options SAMEORIGIN;` | 防止点击劫持 |
| `#!nginx add_header X-Content-Type-Options nosniff;` | 防止 MIME 类型混淆攻击 |
| `#!nginx add_header X-XSS-Protection "1; mode=block";` | 启用浏览器 XSS 防护 |
| `#!nginx autoindex off;` | 禁止目录浏览，防止敏感文件泄露 |
| `#!nginx location ~ /\.git` | 禁止访问隐藏文件或目录（如 `.git` / `.env`） |
| `#!nginx auth_basic` / `#!nginx auth_basic_user_file` | 对私有目录启用 HTTP 鉴权 |
| `#!nginx deny all;` / `#!nginx allow 1.2.3.4;` | IP 访问控制 |
