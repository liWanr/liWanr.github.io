---
tags:
  - Network
  - GitHub
---

# U 盘安全启动 {id=" "}

**解决方案**

:   拔掉所有 U 盘, 进入 Bios 设置, 关闭 security boot 即可。

    *[security boot]: 安全启动

**情况说明**

:   今天用 U 盘给笔记本重新刷 Ubuntu 系统的时候, 死活进不去, 一直显示这个内容

    !!! bug "错误内容"
        
        **Verifiying shim SBAT data failed: Security Policy Violation
        Something has gone seriously wrong: SBAT self-check failed: Security Policy Violation**

    然后去网上找方法, 就是进入 Bios 之后, 关闭 security boot 就好了, 一般在高级设置中。
    我是 ROG 的电脑, 进入 Bios 之后按 `F7` 进入高级设置后有一栏 `security`, 进去之后有一个 `security boot`, 将选项设置为 `Disabled` 即关闭状态然后按 `F10` 保存重启就好了。

    再插入 U 盘就能开心的折电脑了

**成因解释**

:   首先虽然我的系统镜像是从官网下载的 `ubuntu-20.04.6-desktop-amd64` , 但是在刷到 U 盘中时, 软件提到一句***引导加载器被吊销了***, 起初我没太在意。

    然后就发生了这个问题, 因为安全启动（security boot）是为了***防止未经授权的操作系统或恶意软件加载的功能***, 要求操作系统的引导加载程序（比如 GRUB 或 shim）必须经过数字签名验证, 以确保它们没有被篡改。

    错误信息 `Verifying shim SBAT data failed: Security Policy Violation` 就是表示系统无法验证启动加载程序, 如 shim等的签名, 所以导致 U 盘刷机的时候一直启动失败。

## 双系统时间同步问题 {id="dual-system-time-synchronization-problem"}

装完 Linux 和 Windows 双系统可能会注意到系统之间存在时间差异, 一般是相差 **当前时区** 的偏移量, 比如中国的时区是 GMT+8 与标准时间相差 +8 个小时。但是不必担心, 这是一个很常见的问题, 可以在 Linux 终端中使用这个命令修复这个问题。

```bash title=""
sudo timedatectl set-local-rtc 1
```

**成因解析**

:   出现这种情况的原因是 Windows 和 Linux 它们在默认情况下看待硬件时间的方式是不一样的。

    计算机有两个主要时间：系统时间[^1] 和硬件时间[^2] (当然时间概念还有格林尼治标准时间[^3]、协调时间[^4]等)。当计算机开机时, 首先会读取硬件时间并用于设置系统时间, 然后系统时间用于跟踪时间, 如果操作系统对系统时间进行任何更改, 例如更改时区等, 它会尝试将此信息同步到硬件时间中。 **但默认情况下, Linux 会认为硬件时间中存储的时间是 UTC 时间, 而不是本地时间, 但 Windows 认为硬件时间上存储的时间是本地时间, 这就是问题所在** 。

    [^1]: SC: 系统时间, 在操作系统中看到的时间。
    [^2]: RTC: 实时时间或 CMOS/BIOS 时间。在计算机领域作为硬件时间的简称。该时间不是位于操作系统, 而是在计算机主板上, 即使系统关闭后它仍会继续运行。
    [^3]: GMT: 格林尼治标准时间, 也就是世界时。GMT 以地球自转为基础的时间计量系统, 但由于地球自转不均匀导致 GMT 不精确, 现在已经不再作为世界标准时间使用。
    [^4]: UTC: 协调世界时间。UTC 是以原子时秒长为基础, 在时刻上尽量接近于 GMT 的一种时间计量系统。为确保 UTC 与 GMT 相差不会超过 0.9 秒, 在有需要的情况下会在 UTC 内加上正或负闰秒。UTC 现在作为世界标准时间使用。

**举个例子**

:   我现在位于东八区, 即 UTC +08:00, 当我登录 Linux 系统后就会自动将这个时间信息同步到硬件时间中, 但东八区的时间偏移量为 08:00 小时, 且 Linux 的硬件时间为 UTC, 于是戏剧性的一幕就这样发生了。

    这时启动 Windows 后, 系统就会将硬件时间为 UTC 时间认为成本地时间, 因此 Windows 将 07:00 显示为比实际时间晚 8:00 小时的时间。所以一般情况下硬件时间存储的就是偏移前的时间。

    <small>
    :octicons-light-bulb-16:
    也就是说假设东八区的当前时间是 15:00, 这意味着 UTC 时间是 07:00。
    </small>

**解决问题**

:   知道了原因, 那解决这个问题的方式就简单了, 一共有三种解决方案：

    1. 让 Linux 和 Windows 通过互联网自动检查日期、时间和时区。

        如果系统皆连接到互联网, 它会自动设置正确的时间。比如要使 Ubuntu 系统自动检查日期和时间, 就可以到 <u>设置(Settings)</u> :octicons-arrow-right-24: <u>系统(System)</u> :octicons-arrow-right-24: <u>日期和时间(Date & Time)</u> 启用 **自动设置日期和时间(Automatic Date & Time)** 和 **自动设置时区(Automatic Time Zone)** 选项, Windows 同理。

    2. 让 Linux 使用本地时间作为硬件时间或者 Windows 反过来

        也就是文章开篇说的方法, 因为在 Linux 中进行更改更容易, Ubuntu 和大多数其他 Linux 发行版现在都使用 systemd, 因此可以使用 `timedatectl` 命令来更改设置。
        
        其实就是告诉 Linux 系统使用本地时间作为硬件时间。可以设置 RTC 的本地时间, 使用 `set-local-rtc` 选项来执行此操作：`sudo timedatectl set-local-rtc 1`