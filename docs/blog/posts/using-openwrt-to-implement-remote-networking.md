---
icon: lucide/workflow
title: OpenWrt 异地组网
tags:
  - Network
---

<small>
全称：使用 OpenWrt 配置 IPv6 + DDNS + OpenVPN 实现远程访问及异地组网
</small>

<small>
:octicons-light-bulb-16:
灵感来自 YouTube 上的 UP 主：[**24K钢丝**](https://www.youtube.com/watch?v=yb-g4ZaNm9Y){target="_blank"}，
也要感谢 [**世界上最好的奶龙**](https://dxlcq.cn/){target="_blank"} 提供帮助

</small>

首先说明本次用到的装备：

|设备名称|详情|
|:-|:-|
|公网的IPv6或IPv4地址|至少一个，可以是固定的也可以是弹性公网，如果没有的就做内网穿透|
|域名|可以在阿里云、腾讯云、华为云等厂家购买域名，我用的是阿里云的|
|软路由设备|我用的是 R4S，买成￥571，记得选带 TF 卡和 TF 读写器，或者自己单独买也行。<br>也可以用其他的 RS 设备、x86_64 机子或小米、树莓派、Raspberry Pi等路由设备|
|Open Wrt| 我用的是 BleachWrt ，版本是 bleachwrt plus 20250117，[同版本固件下载地址](https://openwrt.mpdn.fun:8443/?dir=lede)，找自己对应版本的固件下载，并且要注意不熟悉Wrt的人尽量不要用 `.mini-daily` ，这个是精简版，**推荐使用高大全版本下载 `plus-daily`**|
|rufus|刷固件的软件，也可以用其他的软件，我用的是rufus-v4.6，[下载地址](https://github.com/pbatard/rufus/releases/download/v4.6/rufus-4.6.exe)|

## 下载并安装固件 {id="download-and-install-the-firmware"}

**路由结构**

:   光猫接 R4S 的 WAN 口，R4S 的 LAN 口出去接路由器/交换机的 LAN 口

    ``` mermaid
    graph LR
    A[**光猫**<br>桥接模式] -->|2.5G - WAN| B[**R4S**<br>PPPoE拨号];
    B -->|LAN - WAN| C[**路由器/交换机**<br>路由器为桥接模式]
    C --> D[手机]
    C --> E[电脑]
    C --> F[其他设备]
    ```

    <small>
    :octicons-light-bulb-16:
    **光猫改桥接模式：** 我本来想自己找光猫的超级管理员账户和密码，结果找了半天没找到，就给宽带师傅打电话，让他远程给我改的。其实直接找宽带师傅更快，几分钟就搞好了，都不用自己在网上慢慢找慢慢测试
    </small>

**将固件刷到软路由中**

:   R4S 是用 TF 卡的，所以只需要将固件刷进 TF 卡就行了，**设备选择 U 盘**，**引导类型选择下好的 Wrt 固件** ，然后点击开始，等待 **准备就绪** 那一条变成绿色就可以将 TF 直接插到 R4S 的卡槽中了。

    ![1.png](../../../images/knowledge/openwrt/1.png)

## 系统基本设置 {id="system-basic-settings"}

**登录页面**

:   给 R4S 接上电后，等待 system 的绿灯亮起来后就可以进入了。打开浏览器，在地址栏输入 [`192.168.1.1`](http://192.168.1.1/){target="_blank"}，默认用户名：`root`，密码：`password`

    <small>
    :octicons-light-bulb-16:
    如果你发现你没有网络存储、VPN 这些内容的话，你下的就是mini的精简版，请重新找一下 plus 的高大全版。
    </small>

**设置软路由 PPPoE 拨号**

:   1. 在 **网络-接口** 中将全局网络选项中的 IPv6 前缀删掉。

        ![2.png](../../images/knowledge/openwrt/2.png)

    2. 然后找到顶部的 WAN 口，如果是 IPv6 的话就设置 WAN6 ，将传输协议设置为 PPPoE，用户名和密码就是宽带账号和密码，如果不知道就在改光猫桥接的时候问一下，设置完成后点击 **保存&应用**

        ![3.png](../../images/knowledge/openwrt/3.png)

## 配置 Lucky {id="config-Lucky"}

**插件检查**

:   首先看一下在 VPN 下面有没有 OpenVPN，没有的话就是版本不对。然后在`iStore`中搜索并下载`Lucky`插件，下载的时候会有终端弹窗，当弹窗边缘是绿色的时候就可以关闭终端弹窗了。

    ![4.png](../../images/knowledge/openwrt/4.png)

**打开 Lucky 插件**

:   在`服务 - Lucky`中找到插件基本设置，然后启动服务，进入 Lucky 后台管理页面，**初始用户名和密码都是`666`** 。进入之后设置一下两个东西，第一个是安全入口，第二个是用户名和密码，否则不能设置 DDNS 动态域名

    ![5.png](../../images/knowledge/openwrt/5.png)

**设置 DDNS 动态域名**

:   1. 点击 **动态域名** :octicons-arrow-right-24: **添加 DDNS 任务**，以下内容没写的都是默认，不用改

        |项目|设置详情|
        |:-|:-|
        |操作模式|简易模式|
        |DNS 服务商设置|这个得根据你域名的 DNS 托管商，如果你域名的 DNS 是阿里的，这里就选阿里，我这里用的阿里|
        |AccessKey ID和Secret|点击上面的创建 AccessKey 一步一步来就行了|
        |类型|根据你的公网 IP 进行更改，我没有公网 IPv4 ，就选的 IPv6 |
        |获取公网 IP 方式|通过网卡获取|
        |网卡列表|br-lan|
        |IP选择匹配规则|测试一下，如果测试结果是 240e、2409、2408开头的都是公网 IP（分别代表电信、移动、联通）<br>如果实在不知道就把测试得到的 IP 拿去 ITDOG ping 一下，如果全绿就是公网 IP，否则就不是|
        |域名列表|就是你买的那个域名，可以设置成三级域名，比如我的就是 `ovpn.leeyearn.com`|

        ![6.png](../../images/knowledge/openwrt/6.png)

    2. 看同步情况

        如果同步情况是 **公网 IP 未改变** / **托管商记录一致** 都表示通过了

        ![7.png](../../images/knowledge/openwrt/7.png)

## 配置 OpenVPN {id="config-OpenVPN"}

**启用 OpenVPN**

:   在 Wrt 中 **VPN** :octicons-arrow-right-24: **OpenVPN** 中按照如下表格进行配置，完成后保存并应用。

    |设置名|设置详情|
    |:-|:-|
    |启用|勾选|
    |协议|看你选的是 v4 还是 v6 ，但是 UDP 和 TCP 中 **建议选 UDP**|
    |端口|默认|
    |WAN 口...IP|就填刚刚 DDNS 的那个域名，比如 ovpn.leeyearn.com|
    |客户端网段|默认|
    |客户端推送配置1|根据你的 Wrt 的 IP 环境来定，这里是写 Wrt 所在的整个网段，后面的子网掩码不变<br>比如 Wrt 的地址是 192.168.1.1，那这里就填 192.168.1.0，但是如果是 192.168.3.1，那这里就填 192.168.3.0|
    |客户端推送配置2|默认|
    |客户端推送配置3|默认|
    |客户端推送配置4|建议把 DNS 后面的 IP 改成域名商的 DNS IP，比如阿里的就是 223.5.5.5|

    ![8.png](../../images/knowledge/openwrt/8.png)

**添加 OpenVPN-Server 的参数**

:   为了保障同一时间可以有多台设备连接到服务器，就要在 OpenVPN 的 Server 端修改配置参数允许所有 Client 端用同一个证书进行验证

    1. 通过 SSH 远程连接 Wrt 设备并修改 `/etc/config/openvpn` 文件

        ![9.png](../../images/knowledge/openwrt/9.png)

        <small>
        :octicons-light-bulb-16:
        **提示:** 登录的用户名为`root`，密码为`password`
        </small>

    2. 按 ++i++ 进入编辑模式，然后在最后面粘贴参数 `option duplicate_cn "1"` ，然后按键盘左上角的 ++esc++ 退出编辑模式，再按 ++colon++ 进入命令模式后输入人 `wq` 保存并退出。退出后使用 `/etc/init.d/openvpn restart` 命令重启 OpenVPN 服务即可

        ![10.png](../../images/knowledge/openwrt/10.png)


## 在手机上测试 {id="test-on-mobile-phone"}

1. 在 Wrt 中的 **VPN** :octicons-arrow-right-24: **OpenVPN** 上面导出自己的 `*.ovpn` 文件。

    ![11.png](../../images/knowledge/openwrt/11.png)

2. 然后在手机上下载 [OpenVPN Connect](https://openvpn.net/client/){target="_blank"} 的软件并导入到手机。一般文件可以选择打开方式，打开方式就选择 **OpenVPN Connect** 打开。然后在非 Wrt 路由下打开 [192.168.1.1](http://192.168.1.1/) 地址，如果是 Wrt 登录页说明没问题了。

    <small>
    :octicons-light-bulb-16:
    **提示:** <u>*非 Wrt 路由下*</u> 表示不要连接 Wrt 以及它下级的所有设备。
    </small>

## 防火墙地址伪装 {id="firewall-address-spoofing"}

但是现在只能访问 OpenWrt，无法访问内网的其他设备，可以用 **Windows App** 软件简单地测试，一定是连不上内网的 Windows 主机的。因为 Wrt 没有给你的地址进行内网转换，这时候就需要对防火墙的 NAT 进行设置，将来自内网且经过防火墙的流量进行地址转换，使其能够正确地通过外网进行通信。


**实现方式**

:   在 Wrt 中的 **网络** :octicons-arrow-right-24: **防火墙** :octicons-arrow-right-24: **自定义规则** 输入框末尾添加 `iptables -t nat -A POSTROUTING -o br-lan -j MASQUERADE` 参数，然后重启防火墙即可。

    <small>
    :octicons-light-bulb-16:
    **提示:** 参数的含义就是对于从 br-lan 接口发出的所有数据包，将它们的源 IP 地址修改为 br-lan 接口的 IP 地址，使内网主机能够通过 NAT 访问外部网络。
    </small>

    ![12.png](../../images/knowledge/openwrt/12.png)


**远程访问内网设备测试**

:   这里通过手机使用流量在 **Windows App** 软件远程连接内网 PC 进行测试。但是首先打开电脑的远程连接功能。

    ![13.png](../../images/knowledge/openwrt/13.png)

    然后在 **Windows App** 中点击 ++plus++ 号添加设备，输入电脑的。

    ![14.png](../../images/knowledge/openwrt/14.png)


*[TF]: microSD
*[Windows App]: 微软官网的远程 Windows 工具