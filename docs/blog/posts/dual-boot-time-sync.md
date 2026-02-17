---
icon: lucide/hourglass
title: 双系统时间同步
tags:
  - Knowledge
---

<small>
created: 2024-12-25
updated: 2025-02-22
</small>

在装完 Linux 和 Windows 两个系统后大概率会出现时间差异, 但是不必担心, 这是一个很常见的问题, **可以在 Linux 终端中使用这个命令修复这个问题**。

```Bash
sudo timedatectl set-local-rtc 1
```

## 成因解析 {id="cause-analysis"}

出现这种情况的原因是 Windows 和 Linux 它们在默认情况下**看待硬件时间的方式是不一样的**, 计算机有两个主要时间：系统时间[^1] 和硬件时间[^2]。<small>:octicons-light-bulb-16: 除了此之外还有常见的 GMT[^3] 和 UTC[^4] 等时间概念。</small>

当计算机开机时, 首先会读取硬件时间并用于设置系统时间，然后系统时间用于跟踪时间。如果操作系统对系统时间进行任何更改, 例如更改时区等, 它会尝试将此信息同步到硬件时间中。**但默认情况下, Linux 会认为硬件时间中存储的时间是 UTC 时间, 而不是本地时间, 但 Windows 认为硬件时间上存储的时间是本地时间, 这就是问题所在。**

## 举个例子 {id="for-example"}

比如我现在位于东八区 (UTC +08:00), 当我启动 Linux 系统后, 这个时间信息就同步到硬件时间中, 但东八区的时间偏移量为 +8 小时, 且 Linux 的硬件时间采用的是 UTC, 也就是说硬件时间存储的就是偏移前的时间, 于是戏剧性的一幕就发生了。此时启动 Windows 后系统就会认为硬件时间为本地时间, 所以它会更改系统时间并使用 UTC 时间作为本地时间。

假设东八区的当前时间是 15:00, 这意味着 UTC 时间是 07:00, 此时 Linux 的时间是 15:00, 而 Windows 的时间是 07:00。

## 解决问题 {id="problem-solving"}

知道了原因, 那解决这个问题的方式就简单了, 一共有以下解决方案：

1. **让 Linux 和 Windows 通过互联网自动检查日期、时间和时区**

    如果系统都能连网, 就可以自动设置时间，比如要使 Ubuntu 系统自动检查日期和时间, 就可以到 ^^设置(Settings)^^ :octicons-arrow-right-24: ^^系统(System)^^ :octicons-arrow-right-24: ^^日期和时间(Date & Time)^^ 启用 *自动设置日期和时间(Automatic Date & Time)* 和 *自动设置时区(Automatic Time Zone)* 这两个选项, Windows 类似。
   
2. **让 Linux 使用本地时间作为硬件时间** <small>或者 Windows 反过来</small>

    也就是文章开篇说的方法, 因为在 Linux 中进行更改更容易, Ubuntu 和大多数其他 Linux 发行版现在都使用 systemd, 因此可以使用 `timedatectl` 命令来更改设置。
    
    其实就是告诉 Linux 系统使用本地时间作为硬件时间。可以使用 `set-local-rtc`（设置 RTC 的本地时间）选项来执行此操作：`sudo timedatectl set-local-rtc 1`

[^1]: SC: 在操作系统中看到的时间。
[^2]: RC: 实时时间或 CMOS/BIOS 时间。在计算机领域作为硬件时间的简称。该时间不是位于操作系统, 而是在计算机主板上, 即使系统关闭后它仍会继续运行。
[^3]: GMT: 格林尼治标准时间, 也就是世界时。GMT 以地球自转为基础的时间计量系统, 但由于地球自转不均匀导致 GMT 不精确, 现在已经不再作为世界标准时间使用。
[^4]: UTC: 协调世界时。UTC 是以原子时秒长为基础, 在时刻上尽量接近于 GMT 的一种时间计量系统。为确保 UTC 与 GMT 相差不会超过 0.9 秒, 在有需要的情况下会在 UTC 内加上正或负闰秒。UTC 现在作为世界标准时间使用。