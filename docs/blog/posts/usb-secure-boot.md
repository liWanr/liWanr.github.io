---
icon: material/usb
title: U 盘安全启动
# date:
#     created: 2025-01-20
#     updated: 2026-01-12
tags:
    - Factoid
---

## 解决方案 {id="solution"}

:   拔掉所有 U 盘, 进入 Bios 设置, 关闭 security boot 即可。

    *[security boot]: 安全启动

## 情况说明 {id="condition"}

:   今天用 U 盘给笔记本重新刷 Ubuntu 系统的时候, 死活进不去, 一直显示这个内容

    !!! bug "错误内容"
        
        **Verifiying shim SBAT data failed: Security Policy Violation
        Something has gone seriously wrong: SBAT self-check failed: Security Policy Violation**

    然后去网上找方法, 就是进入 Bios 之后, 关闭 security boot 就好了, 一般在高级设置中。
    我是 ROG 的电脑, 进入 Bios 之后按 `F7` 进入高级设置后有一栏 `security`, 进去之后有一个 `security boot`, 将选项设置为 `Disabled` 即关闭状态然后按 `F10` 保存重启就好了。

    再插入 U 盘就能开心的折电脑了

## 成因解释 {id="reason"}

:   首先虽然我的系统镜像是从官网下载的 `ubuntu-20.04.6-desktop-amd64` , 但是在刷到 U 盘中时, 软件提到一句***引导加载器被吊销了***, 起初我没太在意。

    然后就发生了这个问题, 因为安全启动（security boot）是为了***防止未经授权的操作系统或恶意软件加载的功能***, 要求操作系统的引导加载程序（比如 GRUB 或 shim）必须经过数字签名验证, 以确保它们没有被篡改。

    错误信息 `Verifying shim SBAT data failed: Security Policy Violation` 就是表示系统无法验证启动加载程序, 如 shim等的签名, 所以导致 U 盘刷机的时候一直启动失败。