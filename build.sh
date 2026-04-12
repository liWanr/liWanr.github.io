#!/bin/bash

# ================= 配置区 =================
PASSWORD="admin"                            # sudo 密码，如果为""则手动输入

NGINX_FLAG=true                             # 是否启用 Nginx，true/false
# if true ⬇
NGINX_DIR="../nginx1.26.3/sbin/nginx"       # Nginx 可执行文件路径
NGINX_HTML_DIR="../nginx1.26.3/html/zensical" # Nginx 站点目录
NGINX_CONF_DIR="../nginx1.26.3/conf"        # Nginx 配置目录
# 83 行有一个将本地 nginx.config 复制到 Nginx 配置目录的命令，不需要就删掉

PY_ENV="../.env/zensical/bin/activate"      # Python 虚拟环境激活脚本路径
CACHE_DIR="./.cache"                        # 构建缓存目录
SITE_DIR="./site"                           # 构建输出目录

PORT=8000                                   # 本地预览的端口
DEPLOY_URL="https://liwanr.com"             # 部署后的访问 URL
# ==========================================

# ====== 执行 sudo 命令 ======
run_sudo() {
    if [ -n "$PASSWORD" ]; then
        echo "$PASSWORD" | sudo -S "$@"
    else
        sudo "$@"
    fi
}

# ====== 清除缓存 ======
clean() {
    run_sudo rm -rf "$CACHE_DIR" "$SITE_DIR" "$NGINX_HTML_DIR"/* > /dev/null 2>&1
    echo -ne "清理缓存完成... \r"
}

# ====== 激活 Python 虚拟环境 ======
activate_env() {
    source "$PY_ENV"
}

# ====== 检查 Nginx 配置并重载 ======
check_nginx() {
    if [ "$NGINX_FLAG" = true ]; then
        echo -ne "检查 Nginx 配置... \r"
        CHECK_RESULT=$(run_sudo "$NGINX_DIR" -t 2>&1)

        echo "$CHECK_RESULT" | grep -q "test is successful"
        if [ $? -eq 0 ]; then
            echo -ne "Nginx 正常 \r"
            run_sudo "$NGINX_DIR" -s reload
        else
            echo
            echo "------------------------------------------------"
            echo "错误：Nginx 配置检查失败！"
            echo "$CHECK_RESULT"
            echo "------------------------------------------------"
            exit 1
        fi
    fi
}

# ====== 终止占用端口进程 ======
kill_port() {
    pid=$(lsof -ti:$PORT 2>/dev/null)
    if [ -n "$pid" ]; then
        echo "Port $PORT 被占用，PID: $pid，正在终止..."
        kill -9 "$pid"
    fi
}

# ====== 构建与部署 ======
deploy() {
    clean
    activate_env

    zensical build -c > /dev/null 2>&1
    echo -ne "构建完成... \r"

    python3 custom_fixes.py

    if [ "$NGINX_FLAG" = true ]; then
        echo -ne "部署到 Nginx... \r"
        run_sudo cp -r "$SITE_DIR"/* "$NGINX_HTML_DIR" > /dev/null 2>&1
        run_sudo cp ./nginx.conf "$NGINX_CONF_DIR" > /dev/null 2>&1
        check_nginx
        rm -rf "$CACHE_DIR" "$SITE_DIR" > /dev/null 2>&1
    fi

    echo "部署完成：$DEPLOY_URL"
}

# ====== 本地预览 ======
local_serve() {
    kill_port
    rm -rf "$CACHE_DIR" "$SITE_DIR" > /dev/null 2>&1

    echo "========== Local Mode =========="
    activate_env
    zensical serve
}

# ====== 更新框架 ======
update() {
    clean
    activate_env

    pip install --upgrade --force-reinstall zensical > /dev/null 2>&1
    echo "========== Zensical 已更新 =========="

    pip freeze > requirements.txt
    echo "======== 依赖文件更新完成 ========"

    pip show zensical
}

# ====== 全局中断清理 ======
cleanup_on_exit() {
    if [ -d "$CACHE_DIR" ] || [ -d "$SITE_DIR" ]; then
        echo
        echo "检测到中断或退出，正在清理缓存和构建目录..."
        rm -rf "$CACHE_DIR" "$SITE_DIR"
    fi
}

# 捕获常见信号：Ctrl+C、kill
trap cleanup_on_exit SIGINT SIGTERM

# ====== 默认提示 ======
confirm_deploy() {
    echo "请选择操作："
    echo "  ./build.sh        → 确认后构建并部署"
    echo "  ./build.sh -y     → 自定构建并部署"
    echo "  ./build.sh local  → 本地预览"
    echo "  ./build.sh update → 更新框架后构建并部署"
    echo

    read -p "是否构建并部署？(y/N): " choice

    if [[ "$choice" == "y" || "$choice" == "Y" ]]; then
        deploy
    else
        echo "已取消。"
        exit 0
    fi
}

# ====== 参数处理 ======
case "$1" in
    -y)
        deploy
        ;;
    local)
        local_serve
        ;;
    update)
        update
        ;;
    "")
        confirm_deploy
        ;;
    *)
        echo -n "未知参数: $1, "
        confirm_deploy
        ;;
esac