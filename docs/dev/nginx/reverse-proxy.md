---
icon: lucide/square-arrow-out-up-right
title: 反向代理
comments: true
# date:
#     created: 2026-03-11
tags:
    - Tech
---

最基础的反向代理配置

```Bash
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://liwanr.com;

        proxy_set_header Host liwanr.com;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_ssl_server_name on;
    }
}
```