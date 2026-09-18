# 第01讲：Git 是什么 & 四个区域（正文约8分钟 + 练习约7分钟）

## 你将学到
- 为什么写代码一定要用版本控制
- Git 的四个区域：工作区 / 暂存区 / 本地仓库 / 远程仓库
- `git add`、`git commit`、`git push`、`git pull` 各自把代码搬到了哪里
- 怎么看懂 `git status` 和 `git log`

---

## 1. 为什么要版本控制

不用 Git 的人，最后都会变成这样：

```
项目.py
项目_final.py
项目_final_真的final.py
项目_final_20260918_改之前.py
```

三个致命问题：**改坏了回不去**、**不知道谁改的为什么改**、**多人同时改会互相覆盖**。

版本控制（Version Control）就是解决这三件事的工具，`git` 是目前最主流的那个。

> 💡 类比：Git 就是游戏的**存档系统**。你打完一个关卡就存一次档（commit），以后不管把角色练废成什么样，都能读档回到那个时间点。
> 💡 Git 存的不是"最终样子"，而是一串**快照（snapshot）**——每次提交都是当时整个项目的一张完整存档。

## 2. 四个区域（本讲最重要的一张图）

| 区域 | 英文 | 实际在哪 | 一句话理解 |
|------|------|---------|-----------|
| 工作区 | Working Directory | 你能看到的那个项目文件夹 | 正在敲代码的地方 |
| 暂存区 | Staging Area（又叫 Index） | `.git/index` | "待提交清单"，还没进历史 |
| 本地仓库 | Local Repository | `.git/` 里的提交历史 | 你自己电脑上的存档点集合 |
| 远程仓库 | Remote Repository | GitHub / Gitee 服务器 | 云端备份 + 团队共享 |

```text
  【工作区】                【暂存区】                  【本地仓库】              【远程仓库】
  Working Directory         Staging Area (Index)        Local Repository          Remote Repository
  你正在编辑的文件          add 后的"待提交清单"        .git 里的提交历史         GitHub / Gitee 上的仓库
        │                        │                          │                          │
        │  ① git add <文件>      │                          │                          │
        ├───────────────────────►│                          │                          │
        │                        │  ② git commit -m "说明"  │                          │
        │                        ├─────────────────────────►│                          │
        │                        │                          │  ③ git push              │
        │                        │                          ├─────────────────────────►│
        │                        │                          │                          │
        │◄───────────────────────┴──────────────────────────┤  ④ git pull              │
        │      把版本读回来覆盖工作区（= fetch + merge）      │◄─────────────────────────┤
        │                        │                          │                          │
        │  git restore / 手动改回头                          │  ← 反向操作：撤销           │
```

> 💡 类比：**工作区**是案板上的菜，**暂存区**是"已装盘、马上要下锅"的那部分，**本地仓库**是已经做好的菜封进了冰箱存档，**远程仓库**是你把存档上传到云端，队友也能拿到。

## 3. 四条命令各自动了哪个区

| 命令 | 方向 | 干了什么 |
|------|------|---------|
| `git add <文件>` | 工作区 → 暂存区 | 把改动放上"待提交清单"，**还没进历史** |
| `git commit -m "说明"` | 暂存区 → 本地仓库 | 生成一条提交记录（快照），从此可追溯 |
| `git push` | 本地仓库 → 远程仓库 | 把本地提交上传到 GitHub / Gitee |
| `git pull` | 远程仓库 → 本地仓库 + 工作区 | 先 `fetch`（下载）再 `merge`（合并），把队友的提交同步下来 |

> 🎯 **试题 4(1)（5 分）标准答案，一眼可查：**
> - `git add` —— 把**工作区**的修改放入**暂存区（Staging Area / Index）**；
> - `git commit` —— 把**暂存区**的内容提交到**本地仓库（Local Repository）**，生成一条提交记录；
> - `git push` —— 把**本地仓库**的提交推送到**远程仓库（Remote Repository）**。
>
> 一句话记忆链：**工作区 --add--> 暂存区 --commit--> 本地仓库 --push--> 远程仓库**。

> ⚠️ 常见坑：只 `commit` 不 `push`，队友是看不到你代码的，换个电脑也拿不到。**commit 是存档到本机，push 才是发布到云端。**

## 4. 看懂 git status 和 git log

`git status` 回答"我现在在哪一步"，它会用颜色和分区告诉你：

```bash
git status
```

> ✅ 你应该看到（类似）：
> ```
> On branch main
> Changes to be committed:            ← 已在暂存区，等 commit
>   modified:   detect.py
> Changes not staged for commit:      ← 改了但还没 add
>   modified:   camera.py
> Untracked files:                    ← 新文件，Git 还不认识它
>   test.jpg
> ```

`git log` 回答"历史上都发生了什么"，按时间**从新到旧**排列：

```bash
git log --oneline --graph
```

> ✅ 你应该看到（类似）：
> ```
> * 3f2a1b0 (HEAD -> main, origin/main) feat: 增加可行驶区域识别
> * 9c8d7e6 fix: 修正摄像头索引写死的问题
> * 1a2b3c4 docs: 补充 README 运行说明
> ```
> 每行开头是提交哈希（唯一编号），括号里的 `HEAD -> main` 表示"你现在站在 main 分支的最新提交上"。

再补两把常用小工具：

| 命令 | 看什么 |
|------|--------|
| `git diff` | **工作区 vs 暂存区**的差异（还没 add 的改动） |
| `git diff --staged` | **暂存区 vs 本地仓库**的差异（马上要提交的改动） |
| `git add .` / `git add -A` | 把当前目录下所有改动（含新增、删除）加入暂存区 |

> 💡 提交前的好习惯：先 `git status` 看清单，再 `git diff --staged` 看内容，确认没把密码、临时文件或调试代码一起提交上去。

## 5. 三个常见疑问

| 疑问 | 回答 |
|------|------|
| 为什么要有暂存区，`add` 完直接 `commit` 不行吗？ | 可行，但你失去了"这一批改动只提交一半"的能力。暂存区就是让你**挑选**这次要打包哪些改动，好处是提交历史干净、`revert` 时能精确回滚。 |
| 提交之后文件被改坏，能靠 Git 恢复吗？ | 能。只要提交过，就能 `git show <哈希>:<文件名>` 取出当时那份，或在 IDE / VS Code 的 Git 面板里看到历史版本。 |
| `git push` 报错 "rejected / fetch first"？ | 说明远程有别人新推的提交，你本地落后了。先 `git pull`（必要时按提示解决冲突），再 `git push`。 |

---

## 🎯 课后练习（约7分钟）

```bash
# 0. 装 Git（已装过会提示已是最新）
sudo apt update && sudo apt install -y git
git --version

# 1. 配置身份（只需一次，提交记录里会用到）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"

# 2. 建一个练习仓库
mkdir -p ~/git-practice && cd ~/git-practice
git init

# 3. 建文件，然后用 status 观察"四个区域"在怎么变
echo "print('hello')" > demo.py
git status                 # demo.py 此时是 Untracked

# 4. 进暂存区
git add demo.py
git status                 # 变成 Changes to be committed

# 5. 进本地仓库
git commit -m "feat: 添加 demo 脚本"
git status                 # 工作区干净了：nothing to commit, working tree clean
git log --oneline          # 能看到刚才那条提交
```

> ✅ 你应该看到（关键几行）：
> ```
> Initialized empty Git repository in /home/xxx/git-practice/.git/
> Untracked files:   demo.py
> Changes to be committed:   new file:   demo.py
> [main (root-commit) 3f2a1b0] feat: 添加 demo 脚本
> nothing to commit, working tree clean
> ```

---

## 本讲小结

| 概念 | 要点 |
|------|------|
| 版本控制 | 给代码存档 + 追溯历史 + 多人协作，Git 是主流工具 |
| 工作区 | 正在编辑的项目文件 |
| 暂存区 | `git add` 之后的"待提交清单"，尚未成为历史 |
| 本地仓库 | `git commit` 之后的提交历史，存在 `.git/` |
| 远程仓库 | GitHub / Gitee，`git push` 上传、`git pull` 下载 |
| 记忆链 | 工作区 --add--> 暂存区 --commit--> 本地仓库 --push--> 远程仓库 |
| `git status` | 看每处改动现在待在哪个区 |
| `git log --oneline` | 从新到旧看提交历史 |
