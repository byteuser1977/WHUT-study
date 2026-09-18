# Linux 常用命令速查表

> 括号里的「第0X讲」表示它讲自哪一讲。
> ⚠️ 标记的行属于危险操作，先在安全目录里练手。

## 目录

1. 文件操作（第03/04讲）
2. 编辑器与文件查看（第05讲）
3. 系统信息（第01讲）
4. 用户与权限（第06讲）
5. 软件管理（第07讲）
6. 进程管理（第08讲）
7. 网络（第09讲）
8. 管道与重定向（第05讲）
9. 常用快捷键
10. Shell 脚本速查（第10讲）
11. ⚠️ 危险命令

## 1. 文件操作（第03/04讲）
| 命令 | 用途 | 示例 |
|------|------|------|
| `pwd` | 显示当前路径 | `pwd` |
| `cd` | 切换目录 | `cd /var/log` |
| `cd -` | 回到上一次的目录 | `cd -` |
| `ls -la` | 列出所有文件（含隐藏） | `ls -la /etc` |
| `ls -lh` | 大小用 KB/MB 显示 | `ls -lh /var/log` |
| `mkdir -p` | 创建目录（含多级） | `mkdir -p a/b/c` |
| `touch` | 创建空文件 | `touch file.txt` |
| `cp` | 复制 | `cp -r dir1 dir2` |
| `mv` | 移动/重命名 | `mv old.txt new.txt` |
| `rm` | 删除（⚠️ 不可恢复，先 ls 确认目标） | `rm -r dir/` |
| `find` | 查找文件 | `find ~ -name "*.log"` |
| `ln -s` | 创建软链接 | `ln -s /path/to/target link` |
| `*` / `?` | 通配符：匹配任意多个 / 任意一个字符 | `ls *.log`；`ls file?.txt` |

## 2. 编辑器与文件查看（第05讲）
| 命令 | 用途 | 示例 |
|------|------|------|
| `cat` | 显示全部内容 | `cat file.txt` |
| `less` | 分页查看（`Space` 翻页 / `b` 上翻 / `q` 退出） | `less /var/log/syslog` |
| `head -n 20` | 前 20 行 | `head -n 20 file.txt` |
| `tail -n 20` | 后 20 行 | `tail -n 20 file.txt` |
| `tail -f` | 实时跟踪 | `tail -f app.log` |
| `wc -l` | 统计行数 | `find . -maxdepth 1 -type f \| wc -l` |
| `grep "关键词"` | 搜索内容 | `grep "error" app.log` |
| `diff a.txt b.txt` | 比较文件 | `diff a.txt b.txt` |
| `nano` | 新手编辑器（`Ctrl+O` 保存 / `Ctrl+X` 退出） | `nano file.txt` |
| `vim` | 进阶编辑器 | `vim file.txt` |
| vim 三步走 | `i` 插入 → `Esc` 返回 → `:wq` 保存退出（`:q!` 不保存退出） | 在 vim 里按 `i` |
| vim 移动 | 普通模式下 `h j k l` = 左 下 上 右 | 在 vim 里按 `hjkl` |
| vim 编辑 | `dd` 删行 / `yy` 复制行 / `p` 粘贴 / `/关键词` 搜索 | 在 vim 里按 `dd` |

## 3. 系统信息（第01讲）
| 命令 | 用途 | 示例 |
|------|------|------|
| `uname -a` | 系统信息 | `uname -a` |
| `hostname` | 主机名 | `hostname` |
| `whoami` | 当前用户 | `whoami` |
| `date` | 当前时间 | `date` |
| `uptime` | 运行时间 | `uptime` |
| `df -h` | 磁盘空间 | `df -h` |
| `du -sh *` | 目录大小 | `du -sh *` |
| `free -h` | 内存使用 | `free -h` |
| `man 命令` / `命令 --help` | 自助查手册（速查表永远不全，这才是终极答案） | `man ls`；`ls --help` |

## 4. 用户与权限（第06讲）
| 命令 | 用途 | 示例 |
|------|------|------|
| `sudo` | 以管理员（默认 root）身份执行 | `sudo apt update` |
| `sudo -i` | 获取 root shell | `sudo -i` |
| `su - user` | 切换用户 | `su - "$USER"` |
| `chmod 755` | 修改权限（数字法） | `chmod 755 script.sh` |
| `chmod u+x` | 修改权限（符号法） | `chmod u+x script.sh` |
| `chmod g+w` | 给用户组加写权限 | `chmod g+w shared.txt` |
| `chmod o-r` | 去掉其他人的读权限 | `chmod o-r file.txt` |
| `chown user:group` | 修改所有者（必须加 sudo） | `sudo chown "$USER:$USER" file.txt` |
| `passwd` | 修改密码 | `passwd` |

## 5. 软件管理（第07讲）
| 命令 | 用途 | 示例 |
|------|------|------|
| `apt update` | 更新列表 | `sudo apt update` |
| `apt upgrade` | 升级所有已装软件 | `sudo apt upgrade` |
| `apt install` | 安装 | `sudo apt install tree -y` |
| `apt remove` | 卸载 | `sudo apt remove nginx` |
| `apt purge` | 卸载 + 删配置文件 | `sudo apt purge nginx` |
| `apt search` | 搜索 | `apt search nginx` |
| `apt install -f` | 修复依赖 | `sudo apt install -f` |
| `dpkg -l` | 查看已安装 | `dpkg -l \| grep nginx` |
| `dpkg -i` | 安装本地 .deb | `sudo dpkg -i pkg.deb` |
| `yum` / `dnf` | CentOS/RHEL 对应命令（dnf 是新版） | `sudo dnf install nginx` |

## 6. 进程管理（第08讲）
| 命令 | 用途 | 示例 |
|------|------|------|
| `ps aux` | 查看所有进程 | `ps aux \| head` |
| `ps -u "$USER"` | 查看某用户的进程 | `ps -u "$USER"` |
| `pgrep -a` | 按关键词找进程 | `pgrep -a nginx` |
| `top` / `htop` | 实时监控（`P`/`M` 排序，`q` 退出） | `htop` |
| `kill PID` | 终止进程（优先用） | `kill 5678` |
| `kill -9 PID` | ⚠️ 强制终止（先试 `kill PID`） | `kill -9 5678` |
| `killall` | 按名称终止 | `killall nginx` |
| `pkill` | 模糊匹配终止 | `pkill python3` |
| `nohup cmd > app.log 2>&1 &` | 后台不挂断运行并留日志 | `nohup python3 app.py > app.log 2>&1 &` |
| `jobs` | 查看后台任务 | `jobs` |
| `fg %1` | 把后台任务调回前台 | `fg %1` |
| `bg %1` | 把挂起的任务放回后台运行 | `bg %1` |

## 7. 网络（第09讲）
| 命令 | 用途 | 示例 |
|------|------|------|
| `ip addr` | 查看 IP | `ip addr` |
| `ip route` | 查看路由表 | `ip route` |
| `ss -tlnp` | 查看端口占用（看进程名要 sudo） | `sudo ss -tlnp` |
| `ping` | 测试连通 | `ping -c 4 baidu.com` |
| `nc -zv` | 测试端口是否开放 | `nc -zv localhost 8080` |
| `dig` / `nslookup` | 查 DNS（来自 dnsutils） | `dig baidu.com` |
| `ssh user@host` | 远程登录 | `ssh -p 2222 root@192.168.1.100` |
| `ssh-keygen -t ed25519` | 生成密钥对 | `ssh-keygen -t ed25519` |
| `ssh-copy-id` | 把公钥传到服务器 | `ssh-copy-id user@server` |
| `scp` / `scp -r` | 远程复制文件/目录（端口用大写 `-P`） | `scp -P 2222 file.txt user@server:/tmp/` |
| `rsync -avz` | 增量同步 | `rsync -avz mydir/ user@server:/tmp/mydir/` |
| `wget URL` | 下载 | `wget -c https://example.com/f.iso` |
| `curl URL` | 请求 URL / 下载 | `curl -O https://example.com/f.zip` |
| `ufw status` / `allow` / `enable` | 防火墙：状态 / 放行 / 开启 | `sudo ufw allow 22/tcp && sudo ufw enable` |
| `ufw delete` / `deny` | 删除规则 / 拒绝端口 | `sudo ufw delete allow 80` |
| `firewall-cmd` | CentOS 防火墙 | `sudo firewall-cmd --add-port=80/tcp --permanent` |

## 8. 管道与重定向（第05讲）
| 符号 | 功能 | 示例 |
|------|------|------|
| `\|` | 管道：把上个命令的输出交给下个命令 | `ls \| grep txt` |
| `>` | 覆盖写入 | `echo "hi" > f.txt` |
| `>>` | 追加写入 | `echo "hi" >> f.txt` |
| `<` | 输入重定向：把文件当命令的输入 | `sort < file.txt` |
| `2>` | 只保存错误输出 | `cmd 2> err.log` |
| `2>&1` | 合并错误输出 | `cmd > out 2>&1` |
| `2>/dev/null` | 丢弃错误输出 | `find / -name x 2>/dev/null` |

## 9. 常用快捷键
| 快捷键 | 功能 | 示例/说明 |
|--------|------|-----------|
| `Tab` | 自动补全 | 输入 `ls /et` 按 Tab → `ls /etc/` |
| `↑` / `↓` | 翻阅历史命令 | 找回上一条命令 |
| `Ctrl + C` | 终止当前命令 | 命令卡住不动时的第一反应（SIGINT） |
| `Ctrl + L` | 清屏 | 等价于 `clear` |
| `Ctrl + R` | 搜索历史命令 | 输入关键词后回车执行 |
| `Ctrl + A` / `Ctrl + E` | 光标移到行首 / 行尾 | 长命令改开头时好用 |
| `Ctrl + W` | 删除前一个单词 | 改命令时好用 |
| `Ctrl + Z` | 挂起当前进程 | 之后 `fg` 恢复前台、`bg` 继续后台 |
| `!!` | 重复上一条命令（进阶） | `sudo !!` |
| `!$` | 上一条命令的最后一个参数（进阶） | `mkdir /tmp/x && cd !$` |

## 10. Shell 脚本速查（第10讲）

```bash
#!/bin/bash                  # 脚本第一行（shebang）
name="value"                 # 变量：等号两边不能有空格
echo "$name"                 # 引用变量
echo "${name:-默认值}"        # 变量可能为空时兜底
count=$((count + 1))         # 整数运算
if [ "$age" -ge 18 ]; then echo adult; else echo child; fi
for x in list; do echo "$x"; done
while [ "$n" -le 5 ]; do n=$((n + 1)); done
shopt -s nullglob            # 通配符无匹配时循环 0 次
bash -x script.sh            # 逐行调试
echo $?                      # 上条命令的退出码（0=成功）
chmod +x script.sh && ./script.sh   # 执行脚本
```

## 11. ⚠️ 危险命令

| 命令 | 风险 | 安全做法 |
|------|------|---------|
| `rm -rf 目录/` | 不可恢复地删除整棵目录树 | 先 `ls` 确认目标；`alias rm='rm -i'` |
| `chmod -R 777 /` | 系统性权限灾难 | 只对需要的文件改权限 |
| `kill -9 PID` | 程序没机会清理，可能丢数据 | 先 `kill PID`（SIGTERM） |
| `> 文件` | 覆盖写入会清空原内容 | 用 `>>` 追加，或先备份 |
| `dd` | 写错设备会直接毁掉磁盘 | 反复确认 `of=` 的设备路径 |
