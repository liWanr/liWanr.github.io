---
icon: lucide/external-link
title: 删掉默认 win+v 快捷键
tags:
  - Windows
---

<small>
created: 2026-02-18
</small>

Win+V 这个快捷键是剪贴板用户服务注册的, 要强制禁用每用户服务:

:   首先去 **注册表** 定位到这个目录, 将对应的服务 **Start** 键调至 **4**, **UserServiceFlags** 键调至 **0**

    ```Text
    计算机\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services
    ```

    |服务功能|服务名|
    |-|-|
    |GameDVR 和广播用户服务|BcastDVRUserService|
    |剪贴板用户服务|cbdhsvc|
    |连接设备平台用户服务|CDPUserSvc|
    |同步主机|OneSyncSvc|
    |联系人数据|PimIndexMaintenanceSvc|
    |Windows Push Notifications User Service|WpnUserService|

或者关闭云剪贴板：

:   -   组策略-计算机配置-管理模板-系统-OS 策略-允许使用剪贴板历史记录：已禁用

    -   组策略-计算机配置-管理模板-系统-OS 策略-允许剪贴板在设备间同步：已禁用