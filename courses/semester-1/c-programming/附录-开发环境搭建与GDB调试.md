# 附录：Linux GCC 环境搭建与 Makefile 入门

## 你将学到
- 为什么选 VS Code + GCC（而非 Dev-C++/VC6.0）
- 三种主流环境的装法（WSL2 / MSYS2 / Linux 原生）
- 编写、编译、运行第一个 C 程序
- 看懂编译器警告、用调试器单步执行
- Makefile 基础：自动化编译多文件项目

---

## 1. 为什么这套工具链？

| 工具 | 角色 | 为什么选它 |
|------|------|-----------|
| **GCC (GNU Compiler Collection)** | 编译器 | 标准支持最好（C17/C23）、跨平台、生产环境标配 |
| **GDB (GNU Debugger)** | 调试器 | 功能最强、脚本化、VS Code 原生支持 |
| **VS Code** | 编辑器/IDE | 轻量、插件生态强、远程开发（WSL/SSH）一流 |
| **Make / CMake** | 构建系统 | 多文件项目自动化编译、增量构建 |
| **Valgrind / ASan** | 内存检测 | 发现泄漏、越界、用后释放等隐形 Bug |

> ⚠️ **禁用清单**：Dev-C++（自带 GCC 4.9 太老）、VC++ 6.0（1998 年产物）、Turbo C（博物馆展品）、**Code::Blocks 自带编译器**。这些工具会让你养成不标准的代码习惯，调试器也难用。

---

## 2. 环境搭建三选一（按推荐度）

### 方案 A：Windows + WSL2 + VS Code（⭐ 最推荐，最接近真实开发）

**优点**：真 Linux 环境、原生 GCC/GDB/Valgrind、VS Code 远程开发体验极佳、后续学 Linux/ROS/嵌入式零切换成本。

```powershell
# 1. 管理员 PowerShell 执行（约 2-5 分钟）
wsl --install
# 重启电脑，按提示设置 Ubuntu 用户名/密码

# 2. 进入 Ubuntu，更新并装工具链
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential gdb valgrind clang-format cmake

# 3. 验证
gcc --version    # 应 ≥ 11
gdb --version
valgrind --version

# 4. Windows 侧装 VS Code + 插件
# 必装：C/C++ (Microsoft)、C/C++ Extension Pack、WSL、Code Runner
# 推荐：CMake Tools、Git Graph、Error Lens
```

**VS Code 连接 WSL**：
- `Ctrl+Shift+P` → `WSL: Connect to WSL` → 选中 Ubuntu
- 左下角显示 `WSL: Ubuntu` 即成功
- 终端自动是 Linux bash，直接 `code .` 在当前目录打开编辑器

---

### 方案 B：Windows 原生 MSYS2/MinGW-w64 + VS Code（无法用 WSL 时备选）

**优点**：无需虚拟化、启动快、原生 Windows 路径。

```powershell
# 1. 下载安装 MSYS2：https://www.msys2.org/
#    默认安装到 C:\msys64

# 2. 打开 "MSYS2 MinGW 64-bit" 终端（不是 MSYS2 MSYS）
pacman -Syu              # 可能需重复 2 次直到无更新
pacman -S mingw-w64-x86_64-toolchain mingw-w64-x86_64-gdb mingw-w64-x86_64-valgrind mingw-w64-x86_64-cmake

# 3. 把 C:\msys64\mingw64\bin 加入系统 PATH（环境变量）
#    验证：新开 PowerShell 输入 gcc --version

# 4. VS Code 配置（settings.json）
{
  "terminal.integrated.defaultProfile.windows": "Command Prompt",
  "C_Cpp.default.compilerPath": "C:/msys64/mingw64/bin/gcc.exe",
  "C_Cpp.default.debuggerPath": "C:/msys64/mingw64/bin/gdb.exe"
}
```

> ⚠️ MSYS2 下 **Valgrind 功能受限**（Windows 内存模型不同），推荐用 **ASan (AddressSanitizer)**：编译加 `-fsanitize=address -fno-omit-frame-pointer`。

---

### 方案 C：Linux 原生 / macOS（已是主力系统直接用）

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y build-essential gdb valgrind clang-format cmake

# Fedora/RHEL
sudo dnf install -y gcc gcc-c++ gdb valgrind clang cmake

# macOS (自带 clang/lldb)
xcode-select --install
# 借用 Homebrew 装 valgrind 替代品
brew install gcc  # 装真 GCC，gcc-14 等
# macOS 用 leaks / ASan 替代 valgrind
```

---

## 3. 第一个程序：Hello World

### 3.1 创建项目目录

```bash
# 在 WSL/Linux 家目录下
mkdir -p ~/c-learning/01-hello
cd ~/c-learning/01-hello
code .   # 用 VS Code 打开（WSL 模式下直接在 Linux 侧打开）
```

### 3.2 编写 `hello.c`

```c
// hello.c — 第一个 C 程序
#include <stdio.h>   // 预处理：引入标准输入输出库，提供 printf

// 主函数：程序入口，返回 int 给操作系统
int main(void) {
    // printf 格式字符串：%s 占位符，\n 换行
    printf("Hello, World!\n");

    // 返回 0 表示成功；非 0 表示失败（脚本可捕获 $?）
    return 0;
}
```

> 💡 **关键点**：
> - `#include <stdio.h>` —— 尖括号找系统头文件；双引号找当前目录
> - `int main(void)` —— C99 标准写法，`void` 明确无参；`main()` 老写法隐式无参
> - `return 0;` —— 显式返回，**养成习惯**；C99 允许省略（隐式 return 0），但显式更清晰

### 3.3 编译运行（终端手动，理解过程）

```bash
# 1. 编译：源文件 → 可执行文件
gcc -Wall -Wextra -std=c17 -o hello hello.c

# 参数解释：
# -Wall -Wextra     开启常见/额外警告（把警告当错改）
# -std=c17          指定 C17 标准（也可 c11/c99）
# -o hello          输出文件名（Windows 下会是 hello.exe）
# hello.c           源文件

# 2. 运行
./hello
# 输出：Hello, World!

# 3. 查看返回值
echo $?   # 输出 0
```

> ✅ **成功标准**：终端打印 `Hello, World!`，`echo $?` 显示 `0`。

---

## 4. VS Code 一键编译调试（launch.json）

在 `.vscode/launch.json`（`Ctrl+Shift+P` → `C/C++: Add Debug Configuration` → `GCC`）：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "C Debug (gcc)",
      "type": "cppdbg",
      "request": "launch",
      "program": "${fileDirname}/${fileBasenameNoExtension}",
      "args": [],
      "stopAtEntry": false,
      "cwd": "${fileDirname}",
      "environment": [],
      "externalConsole": false,
      "MIMode": "gdb",
      "miDebuggerPath": "/usr/bin/gdb",    // WSL/Linux 路径
      "setupCommands": [
        { "description": "启用美观打印", "text": "-enable-pretty-printing", "ignoreFailures": true }
      ],
      "preLaunchTask": "C Build"    // 先执行 tasks.json 的构建任务
    }
  ]
}
```

配合 `.vscode/tasks.json`（`Ctrl+Shift+P` → `Tasks: Configure Task` → `Others`）：

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "C Build",
      "type": "shell",
      "command": "gcc",
      "args": [
        "-Wall", "-Wextra", "-Werror",   // 警告当错
        "-std=c17", "-g",                // 调试信息
        "-o", "${fileDirname}/${fileBasenameNoExtension}",
        "${file}"
      ],
      "group": { "kind": "build", "isDefault": true },
      "problemMatcher": "$gcc",
      "detail": "编译当前 C 文件为同名可执行文件"
    }
  ]
}
```

**使用**：
- `Ctrl+Shift+B` → 编译当前文件
- `F5` → 编译 + 启动调试（断点生效、变量监视、调用栈、单步执行）

---

## 5. 看懂警告：把警告当错误

```c
// warn_demo.c
#include <stdio.h>

int main(void) {
    int a;           // 未初始化
    printf("%d\n", a);  // 使用未初始化变量
    return 0;
}
```

```bash
gcc -Wall -Wextra -std=c17 warn_demo.c
# 输出：
# warn_demo.c: In function 'main':
# warn_demo.c:5:9: warning: 'a' is used uninitialized [-Wuninitialized]
#      printf("%d\n", a);
```

加上 `-Werror` 会直接**报错停止编译**：

```bash
gcc -Wall -Wextra -Werror -std=c17 warn_demo.c
# error: 'a' is used uninitialized [-Werror=uninitialized]
```

> 🎯 **铁律**：**开发全程 `-Wall -Wextra -Werror`**。警告就是隐性 Bug，不修警告 = 埋雷。

---

## 6. 调试器初体验：GDB 基础三板斧

```bash
# 1. 编译带调试信息
gcc -g -o hello hello.c

# 2. 启动 GDB
gdb ./hello
```

GDB 内常用命令：

| 命令 | 简写 | 作用 |
|------|------|------|
| `break main` / `b 10` | `b` | 在 main / 第 10 行设断点 |
| `run` / `r [args]` | `r` | 运行程序（可带参数） |
| `next` / `n` | `n` | 单步**跳过**函数调用 |
| `step` / `s` | `s` | 单步**进入**函数内部 |
| `print a` / `p a` | `p` | 打印变量 `a` 值 |
| `continue` / `c` | `c` | 继续运行到下一断点 |
| `backtrace` / `bt` | `bt` | 打印调用栈 |
| `quit` / `q` | `q` | 退出 GDB |

**实操演练**：

```bash
(gdb) break main
Breakpoint 1 at 0x1155: file hello.c, line 5.
(gdb) run
Starting program: /home/user/c-learning/01-hello/hello

Breakpoint 1, main () at hello.c:5
5           printf("Hello, World!\n");
(gdb) next
Hello, World!
6           return 0;
(gdb) print 42
$1 = 42
(gdb) continue
[Inferior 1 (pid 12345) exited normally]
(gdb) quit
```

> 💡 VS Code 调试面板就是这些命令的图形化封装：**断点红点、F5 运行、F10 单步跳过、F11 单步进入、左侧变量监视、调用栈面板**。先会命令行，再用图形界面更得心应手。

---

## 7. 编译四步拆解（第 02 讲详讲，这里先见名知意）

```bash
# 1. 预处理：展开宏、包含头文件、去注释 → .i 文件
gcc -E hello.c -o hello.i

# 2. 编译：.i → 汇编 .s
gcc -S hello.i -o hello.s

# 3. 汇编：.s → 目标文件 .o（二进制机器码，未链接）
gcc -c hello.s -o hello.o

# 4. 链接：.o + 库 → 可执行文件
gcc hello.o -o hello
```

```bash
# 一步到位（内部自动跑完四步）
gcc hello.c -o hello
```

> 💡 理解四步是为了：**排查头文件重复包含、宏定义冲突、链接报错 undefined reference、看汇编优化结果**。

---

## 8. Makefile 基础：自动化编译

当项目有多个源文件时，手动编译很麻烦。Makefile 可以**自动化编译**，只重新编译修改过的文件。

### 8.1 为什么需要 Makefile？

```bash
# 手动编译多文件项目
gcc -c main.c -o main.o
gcc -c utils.c -o utils.o
gcc main.o utils.o -o app

# 修改了 utils.c 后，需要重新编译所有文件（浪费时间）
```

### 8.2 Makefile 基本结构

```makefile
# 规则格式：
# 目标：依赖
# 	命令（必须用 Tab 缩进，不能用空格）

# 示例：最简单的 Makefile
app: main.o utils.o
	gcc main.o utils.o -o app

main.o: main.c utils.h
	gcc -c main.c -o main.o

utils.o: utils.c utils.h
	gcc -c utils.c -o utils.o

# 清理生成的文件
clean:
	rm -f *.o app
```

### 8.3 使用 Makefile

```bash
# 编译项目
make

# 清理
make clean

# 指定目标
make app
```

### 8.4 Makefile 变量

```makefile
# 定义变量
CC = gcc
CFLAGS = -Wall -Wextra -std=c17
TARGET = app

# 使用变量
$(TARGET): main.o utils.o
	$(CC) $(CFLAGS) main.o utils.o -o $(TARGET)

main.o: main.c utils.h
	$(CC) $(CFLAGS) -c main.c -o main.o

utils.o: utils.c utils.h
	$(CC) $(CFLAGS) -c utils.c -o utils.o

clean:
	rm -f *.o $(TARGET)
```

### 8.5 自动变量

```makefile
# $@ - 当前目标
# $< - 第一个依赖
# $^ - 所有依赖

app: main.o utils.o
	gcc $^ -o $@  # 等价于 gcc main.o utils.o -o app

%.o: %.c
	gcc -c $< -o $@  # 通用规则：任何 .c 编译为 .o
```

### 8.6 实用 Makefile 模板

```makefile
# 通用 C 项目 Makefile
CC = gcc
CFLAGS = -Wall -Wextra -Werror -std=c17 -g
LDFLAGS =

# 源文件和目标文件
SRC = $(wildcard *.c)
OBJ = $(SRC:.c=.o)
TARGET = app

# 默认目标
all: $(TARGET)

# 链接
$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET) $(LDFLAGS)

# 编译规则（模式匹配）
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# 清理
clean:
	rm -f $(OBJ) $(TARGET)

# 伪目标（避免与文件名冲突）
.PHONY: all clean
```

> 💡 **Makefile 核心思想**：
> 1. **依赖关系**：目标依赖哪些文件
> 2. **增量编译**：只重新编译修改过的文件
> 3. **自动化**：一条 `make` 命令完成整个编译流程

---

## 🎯 课后练习（约 5 分钟）

### 必做（动手敲，不许复制粘贴）

1. **环境验证**：按方案 A/B/C 搭建环境，跑通 `gcc --version`、`gdb --version`、`valgrind --version`（或 ASan）
2. **手动编译运行**：
   ```bash
   mkdir -p ~/c-learning/01-hello && cd $_
   # 用 cat 写文件（或 code hello.c）
   cat > hello.c << 'EOF'
   #include <stdio.h>
   int main(void) {
       printf("Hello, C Language!\n");
       return 0;
   }
   EOF
   gcc -Wall -Wextra -std=c17 -o hello hello.c
   ./hello
   echo $?
   ```
3. **触发警告并修复**：
   ```c
   // warning.c
   #include <stdio.h>
   int main(void) {
       int x;
       printf("x = %d\n", x);  // 未初始化
       return 0;
   }
   ```
   - 用 `-Wall -Wextra` 编译看警告
   - 加 `-Werror` 看报错
   - 初始化 `int x = 0;` 重新编译通过
4. **VS Code 调试**：
   - 对 `hello.c` 第 3 行（`printf`）打断点（行号左侧点一下）
   - `F5` 启动调试，观察变量面板、调用栈、单步执行

### 思考题（写到练习本）

1. `gcc hello.c` 不加 `-o` 时，输出文件叫什么？（Linux/macOS vs Windows）
2. `main` 返回值有什么用？Shell 脚本怎么拿到它？
3. 为什么 `#include <stdio.h>` 用尖括号，而 `#include "my.h"` 用双引号？
4. 什么是"未定义行为"（UB）？`printf("%d", x);` 里 `x` 未初始化属于 UB 吗？

---

## 本讲小结

| 概念 | 要点 |
|------|------|
| 推荐工具链 | GCC + GDB + VS Code (+ WSL2) |
| 禁用工具 | Dev-C++、VC6.0、Turbo C |
| 编译命令 | `gcc -Wall -Wextra -Werror -std=c17 -g -o exe src.c` |
| 运行 | `./exe`（Linux/macOS/WSL） |
| 调试入口 | `gdb ./exe` → `b main` → `r` → `n`/`s` → `p var` |
| 核心习惯 | **警告即错误**，**带 `-g` 编译**，**会用调试器** |
| Makefile | 自动化编译，增量编译，`make` 命令构建项目 |

---

> **返回主目录**：[第 01 讲：C 语言概述与第一个程序](01-C语言概述与第一个程序.md) —— 开始正式学习 C 语言基础。