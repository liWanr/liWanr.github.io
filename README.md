# 部署方式

## 启动方式

### 激活方式

`source ../.env/zensical/bin/activate`

### 退出激活

`deactivate`

### 启动命令

1. 边写边预览 `zensical serve`

2. 编译 `zensical build`

    - 清除缓存并编译 `zensical build -c`
    - 指定编译目录 `zensical build -f`

### 版本控制

1. 升级 `pip install --upgrade --force-reinstall zensical`

2. 显示当前版本 `pip show zensical`

### 杀掉被占用的进程

`sudo lsof -i :8000`

`sudo kill -9` PID