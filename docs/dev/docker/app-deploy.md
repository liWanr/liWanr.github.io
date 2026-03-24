---
icon: octicons/terminal-16
title: 应用部署
# date:
#     craeted: 2026-03-10
#     updated: 2026-03-24
comments: true
---

## 部署 Nginx

1. 搜索并拉取 Nginx 镜像

    ```Bash { linenums="0" }
    docker search nginx
    ```

    ```Bash { linenums="0" }
    docker pull nginx:1.26.3
    ```

2. 创建容器，设置端口映射、目录映射

    ??? info "默认 nginx.config"

        ```Bash {linenums="0"}
        user  nginx;
        worker_processes  1;

        error_log  /var/log/nginx/error.log warn;
        pid        /var/run/nginx.pid;

        events {
            worker_connections  1024;
        }

        http {
            include       /etc/nginx/mime.types;
            default_type  application/octet-stream;

            log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                            '$status $body_bytes_sent "$http_referer" '
                            '"$http_user_agent" "$http_x_forwarded_for"';

            access_log  /var/log/nginx/access.log  main;

            sendfile        on;
            #tcp_nopush     on;

            keepalive_timeout  65;

            #gzip  on;

            server {
                listen       80 default_server;
                listen       [::]:80 default_server;
                server_name  _;
                root         /usr/share/nginx/html;

                location / {
                    index  index.html index.htm;
                }

                error_page  404              /404.html;
                location = /404.html {
                }

                error_page   500 502 503 504  /50x.html;
                location = /50x.html {
                }
            }

            # server {
            #     listen       80;
            #     server_name  example.com;
            #     root         /var/www/example.com;
            #     location / {
            #         try_files $uri $uri/ =404;
            #     }
            # }
        }
        ```

    ```Bash
    docker run -id --name=docker_nginx \ 
    -p 80:80 "(1)!"
    -v $PWD/conf/nginx.conf:/etc/nginx/nginx.conf \ "(2)!"
    -v $PWD/logs/var/log/nginx \ "(3)!"
    -v $PWD/html:/usr/share/nginx/html \
    nginx "(4)!"
    ```

    1. 端口映射，让本机的 80 端口映射到 nginx 容器的 80 端口
    2. 数据卷，让本地当前目录(`$PWD`)下的 `/conf/nginx.conf` Nginx 配置文件映挂载到容器中，其余的数据卷是同样的道理，「**配置文件要提前准备好**」