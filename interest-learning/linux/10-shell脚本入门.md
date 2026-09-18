# 第10讲：Shell 脚本入门（正文约5分钟 + 练习约5分钟）

## 你将学到
- 什么是 Shell 脚本
- 写第一个脚本
- 变量、条件、循环
- 实用脚本示例

---

## 1. 什么是 Shell 脚本

Shell 脚本就是把一堆命令写到文件里，然后一次性执行。

> 💡 类比：命令行是"一个一个敲菜谱"，Shell 脚本是"把菜谱写在纸上，照着做"。

## 2. 第一个脚本

```bash
# 创建脚本文件
nano ~/hello.sh
```

输入以下内容：

```bash
#!/bin/bash
echo "Hello, Linux!"
echo "Today is $(date)"
echo "Current user: $(whoami)"
```

保存退出后：

```bash
# 添加执行权限
chmod +x ~/hello.sh

# 运行脚本
~/hello.sh
```

> ⚠️ 第一行 `#!/bin/bash` 叫 shebang，告诉系统用 bash 来执行这个脚本。
> 想让脚本在更多系统上通用，可以写 `#!/usr/bin/env bash`（它会在 PATH 里查找 bash；macOS / BSD 自带的 bash 版本较老，写死路径容易踩坑）。

> 💡 加不加 `.sh` 后缀只是习惯约定，执行靠的是 `chmod +x` 和路径，跟扩展名无关（但示例里为了可读性都加上了）。

## 3. 变量

```bash
#!/bin/bash

# 定义变量（等号两边不能有空格！）
name="Bit"
age=25

# 使用变量（加 $ 符号）
echo "My name is $name, age is $age"
echo "My name is ${name}, age is ${age}"

# 命令结果赋值给变量
current_date=$(date +%Y-%m-%d)
file_count=$(find . -maxdepth 1 -type f | wc -l)

echo "Today: $current_date"
echo "Files in current dir: $file_count"
```

> ⚠️ 赋值时 `name="Bit"` 正确，`name = "Bit"` 错误（等号两边不能有空格）。

## 4. 条件判断

```bash
#!/bin/bash

age=20

if [ "$age" -ge 18 ]; then
    echo "You are an adult"
elif [ "$age" -ge 12 ]; then
    echo "You are a teenager"
else
    echo "You are a child"
fi
```

> 💡 变量可能是空的时，用 `${var:-默认值}` 兜底：`if [ "${age:-0}" -ge 18 ]; then`
> 否则空变量会让 `[` 报 `[: -ge: unary operator expected`，而且还会静默走 else 分支。

**常用比较运算符**：

| 运算符 | 含义 |
|--------|------|
| `-eq` | 等于 |
| `-ne` | 不等于 |
| `-gt` | 大于 |
| `-ge` | 大于等于 |
| `-lt` | 小于 |
| `-le` | 小于等于 |
| `=` | 字符串相等 |
| `==` | 字符串相等（只在 bash 的 `[[ ]]` 里安全，`[ ]` 里请用 `=`） |
| `!=` | 字符串不等 |
| `-z` | 字符串为空 |
| `-n` | 字符串非空 |
| `-e` | 路径存在 |
| `-f` | 存在且是普通文件 |
| `-d` | 存在且是目录 |
| `-r` / `-w` / `-x` | 有读 / 写 / 执行权限 |

**文件判断示例**：

```bash
#!/bin/bash

if [ -f "/etc/passwd" ]; then
    echo "Password file exists"
fi

if [ ! -d "/tmp/mydir" ]; then
    echo "Directory does not exist, creating..."
    mkdir -p /tmp/mydir
fi
```

## 5. 循环

### for 循环

```bash
#!/bin/bash

# 遍历列表
for name in Alice Bob Charlie; do
    echo "Hello, $name"
done

# 遍历文件
for file in *.txt; do
    echo "Processing: $file"
done

# C 风格 for 循环
for ((i=1; i<=5; i++)); do
    echo "Number: $i"
done
```

> ⚠️ 目录里一个 `.txt` 都没有时，`*.txt` 会**原样**留下 "*.txt" 这个词，循环会拿着这个不存在的文件名跑一次（典型现象：`echo` 出 `*.txt`，或 `mv: cannot stat`）。
> 在脚本开头加 `shopt -s nullglob`，没有匹配时循环次数就是 0，配合 `if [ -e "$file" ]` 判断更稳。

### while 循环

```bash
#!/bin/bash

count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    count=$((count + 1))    # $(( )) 里做整数运算：把 count 加 1 再存回 count
done
```

> 💡 `$(( ))` 是算术展开：`$((a + b))`、`$((count + 1))`，只能算整数，结果可以直接赋值给变量。

## 6. 实用脚本示例

### 示例1：批量重命名

```bash
#!/bin/bash
# 把当前目录下所有 .txt 文件加上日期前缀
# 可安全重复执行：已有前缀的文件会被跳过，不会叠加
shopt -s nullglob          # 没有任何 .txt 时循环 0 次，不会进入"假循环"

for file in *.txt; do
    case "$file" in
        [0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]_*)   # 已加过 8 位日期前缀
            echo "跳过（已有前缀）: $file"
            continue
            ;;
    esac

    newname="$(date +%Y%m%d)_$file"
    if mv -- "$file" "$newname"; then
        echo "Renamed: $file -> $newname"
    else
        echo "失败: $file" >&2
    fi
done
```

> ⚠️ 批量改名会在原文件上动手，**先在一份拷贝目录里试跑**，确认输出符合预期再对真实目录执行。

### 示例2：磁盘空间检查

```bash
#!/bin/bash
# 当磁盘使用超过 80% 时告警

usage=$(df / | tail -1 | awk '{print $5}' | tr -d '%')

if [ "$usage" -gt 80 ]; then
    echo "WARNING: Disk usage is at ${usage}%!"
else
    echo "Disk usage is normal: ${usage}%"
fi
```

### 示例3：批量创建用户

```bash
#!/bin/bash

for user in alice bob charlie; do
    if sudo useradd -m "$user" 2>/dev/null; then
        echo "创建成功: $user"
    else
        echo "跳过/失败: $user（可能已存在或权限不足）"
    fi
done
```

> 💡 交互式建号更推荐 `sudo adduser alice`（自动建家目录并提示设密码）。

## 7. 调试与退出码

```bash
# 逐行跟踪执行过程（找出脚本到底跑到哪一步）
bash -x script.sh

# 上一条命令的退出码：0 = 成功，非 0 = 失败
echo $?

# 在脚本里主动退出并返回状态码
exit 1
```

## 8. 让脚本遇错即停（进阶）

```bash
set -euo pipefail    # 出错就停 / 用未定义变量报错 / 管道中任一步失败都算失败
```

> ⚠️ 这会改变脚本行为（未定义变量会直接报错退出），先别给初学者的脚本默认加上，等你摸清楚自己的脚本逻辑再开。

---

## 🎯 课后练习（约5分钟）

```bash
# 1. 创建第一个脚本
# 'EOF' 加引号：里面的 $变量 和 $(命令) 不会被提前展开，原样写进文件
cat > ~/myscript.sh << 'EOF'
#!/bin/bash
echo "=== System Info ==="
echo "User: $(whoami)"
echo "Date: $(date)"
echo "Uptime: $(uptime)"
echo "Disk Usage:"
df -h / | tail -1
EOF

# 2. 赋予权限并运行
chmod +x ~/myscript.sh
~/myscript.sh

# 3. 创建条件判断脚本
cat > ~/check.sh << 'EOF'
#!/bin/bash
if [ -d "/tmp" ]; then
    echo "/tmp exists"
else
    echo "/tmp does not exist"
fi
EOF

chmod +x ~/check.sh
~/check.sh
```

> ✅ 你应该看到（类似）：
> ```
> === System Info ===
> User: bit
> Date: Thu Sep 17 21:50:20 CST 2026
> Uptime:  21:50:20 up 1:30,  1 user,  load average: 0.00, 0.01, 0.05
> Disk Usage:
> /dev/sdb        1007G  9.8G  946G   2% /
> /tmp exists
> ```

---

## 本讲小结

| 概念 | 要点 |
|------|------|
| shebang | `#!/bin/bash`，脚本第一行（可移植写法 `#!/usr/bin/env bash`） |
| 变量 | `name="value"`（等号两边无空格），用 `$name` 引用，空值用 `${name:-默认}` |
| 条件 | `if [ condition ]; then ... fi`；`$(( ))` 做整数运算 |
| for 循环 | `for x in list; do ... done`；通配符建议配 `shopt -s nullglob` |
| while 循环 | `while [ condition ]; do ... done` |
| 调试 | `bash -x script.sh`；`$?` 看退出码，`exit N` 主动返回状态 |
| 执行 | `chmod +x script.sh && ./script.sh` |
