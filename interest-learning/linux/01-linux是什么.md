# 第01讲：Linux 是什么 & 为什么学（正文约5分钟 + 练习约5分钟）

## 你将学到
- Linux 到底是什么
- Linux 和 Windows 有什么不同
- 为什么要学 Linux

---

## 1. Linux 是什么

Linux 是一个**操作系统**，和 Windows、macOS 一样，用来管理电脑硬件和软件。

但它有两个关键区别：
- **免费**：不需要花钱买
- **开源**：任何人都能看到和修改它的源代码

> 💡 类比：Windows 是精装商品房（买来就能住，不能改结构），Linux 是毛坯房（免场地费、装修全自由：想怎么改怎么改）。

> 💡 严格说 Linux 只是内核（kernel），但我们平时说的"Linux"指内核 + 一堆工具打包成的发行版（distribution / distro）——下面马上讲。

## 2. 发行版：Linux 的"品牌"

Linux 本身只是一个内核（核心引擎）。各个公司/社区在内核外面加上工具、界面，打包成"发行版（distribution / distro）"：

| 发行版 | 一句话特点 | 包管理命令（第07讲详解） |
|--------|-----------|-----------|
| **Ubuntu** | 新手首选，社区最大 | apt |
| **CentOS** | 企业服务器常用 | dnf（旧版为 yum）① |
| **Debian** | 极其稳定，老手最爱 | apt |
| **Kali** | 网络安全专用 | apt |

① CentOS 7 已于 2024-06-30 EOL；CentOS 已转向 CentOS Stream，生产环境常见替代为 Rocky / AlmaLinux。

**本教程基于 Ubuntu/Debian 系**（命令用 apt），因为：新手友好 + 资料最多 + WSL 默认就是 Ubuntu。

## 3. Linux vs Windows 核心差异

| 维度 | Linux | Windows |
|------|-------|---------|
| 操作方式 | 命令行为主 | 图形界面为主 |
| 软件安装 | 终端一行命令 | 下载安装包双击 |
| 网站服务器系统 | Unix-like 约 92%（其中 Linux 约 62%） | 约 5% |
| 病毒风险 | 极低 | 较高 |
| 价格 | 免费 | 付费 |

> 📊 数据来源：W3Techs，2026-09，口径为"已知操作系统的网站占比"。
> 🎯 Windows 统治桌面，Linux 统治服务器——这才是真实格局。

> 💡 macOS 底层是 Unix，命令和 Linux 高度相通——学完本教程，你在 Mac 的终端里同样能上手。

## 4. 为什么要学 Linux

1. **服务器运维必备**：全世界的网站、云服务都跑在 Linux 上
2. **开发环境标配**：Docker、Git、Python 都在 Linux 下体验最好
3. **提升效率**：一行命令批量处理 1000 个文件，GUI 做不到
4. **高薪岗位敲门砖**：云计算、DevOps、安全工程师都要求会 Linux

## 5. 准备工作：Windows 用户先装 WSL

WSL（Windows Subsystem for Linux）是微软官方提供的"在 Windows 里跑一个真 Linux"，不用装虚拟机。装好后，在开始菜单搜索 "Ubuntu" 打开，就是本教程要用的终端。

安装步骤见微软官方文档（约 5 分钟）：
https://learn.microsoft.com/zh-cn/windows/wsl/install

一句话版：以**管理员**身份打开 PowerShell，执行 `wsl --install`，重启后按提示设置用户名和密码即可。

> 💡 macOS / Linux 用户跳过本节，直接打开系统自带的"终端"（Terminal）。

---

## 🎯 课后练习（约5分钟）

看不懂没关系，这些命令后面会一个个讲到，先感受一下。

打开你的终端（Windows 用户先按第 5 节装好 WSL），输入以下命令：

```bash
# 显示当前用户名
whoami

# 显示主机名
hostname

# 显示系统信息
uname -a

# 显示当前时间
date
```

> ✅ 你应该看到（类似）：
> ```
> bit
> my-pc
> Linux my-pc 5.15.90.1-microsoft-standard-WSL2 #1 SMP ... x86_64 GNU/Linux
> Thu Sep 17 21:50:20 CST 2026
> ```

看到输出了？恭喜，你已经开始用 Linux 了！

---

## 本讲小结

| 概念 | 要点 |
|------|------|
| Linux | 免费开源的操作系统（严格说是内核 + 发行版打包） |
| 发行版 | Ubuntu（新手首选）、CentOS/Rocky（服务器常用） |
| 核心区别 | 命令行交互，不是图形界面 |
| 学习价值 | 服务器/开发/运维/高薪岗位的基础 |
