---
icon: lucide/shield-check
title: 激活 Ubuntu 网卡
tags:
  - Network
  - GitHub
---

## 检查网络接口状态 {id="check-network-interface-status"}

在终端输入 `ip a` , 如果网卡信息是这样, 表示网卡状态是 `DOWN` , 说明网卡没有启用, 需要以下方法激活它。

!!! quote "终端输出"

    ```shell-session { .yaml .no-copy .no-select title="" }
    ubuntu@ubuntu:~/Desktop$ ip a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
            valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host 
            valid_lft forever preferred_lft forever
    2: ens33: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
        link/ether 00:0c:29:21:c6:8c brd ff:ff:ff:ff:ff:ff
        altname enp2s1
    ```

<small>
:octicons-light-bulb-16:
这里有两张网卡, 第一张网卡是 `lo`, 表示的是本机, 并不是连接互联网的网卡。第二张 `ens33` 才是实际连接互联网的, 这个可能会根据网卡设备而有不同名称, 但一般是第二个。
</small>

## 激活网卡 {id="activate-network-card"}

1. 启用网卡： 再次运行 `ip a` 检查网卡是否变为 UP 状态。

    ```bash title=""
    sudo ip link set ens33 up
    ```

2. 获取 IP： 一般到这个时候只是将网卡启用了, 但是不会给网卡分配 IP, 所以要手动获取 IP 地址

    ```bash title=""
    sudo dhclient ens33
    ```

3. 检查： 此时就能够使用网络了, 输入 `ip a` 查看是否有 IPv4 地址, 如果还是没有可以尝试重启网络服务就有了

    ```bash title=""
    sudo systemctl restart NetworkManager
    ```
