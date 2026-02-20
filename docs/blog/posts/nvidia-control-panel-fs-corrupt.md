---
icon: simple/nvidia
title: N卡面板文件损坏
# date:
#   created: 2023-02-18
tags:
    - Factoid
---
 
##  前言

问题描述：

```Bash { .yaml .no-copy}
C:\Program Files\WindowsApps\NVIDIACorp.NVIDIAControlPanel_8.1.959.0_x64_5...\nvcplui.exe

参数错误
```

## 怀疑

我发现这个问题的时候是重装电脑后，安装完驱动后发现右键的N卡控制面板打不开。

我就很疑惑，官方下载的镜像文件为什么会有这种问题，网上试了很多办法，删掉n卡控制面板、卸载显卡驱动再重装、清理注册表都没用（至少我电脑没用）。

我发现好像很多的文件损坏都可以用这个方法进行恢复，我的照片打不开也用的这个方法

## 解决方法

右键以**管理员身份打开命令提示符**, 在命令栏中输入以下指令后回车等待完成即可

```Bash
sfc /SCANNOW
```

然后等待这段内容显示出来就好了

```Bash { .yaml .no-copy }
开始系统扫描。此过程将需要一些时间。
开始系统扫描的验证阶段。
验证3%已完成。
```
