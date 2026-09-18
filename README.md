# WHUT-study

武汉理工大学学习笔记仓库 — 课程笔记 + 车队技能学习笔记。快速复习、考前突击、知识点索引。

四大学习板块：Linux 入门 → 智能巴哈感知组 → 机械组 → 电控组。统一结构、统一体量（每讲约 10 分钟），可直接跳着看某一讲。

## 仓库结构

```
WHUT-study/
├── README.md                 # 本文件
├── courses/                  # 课程笔记（按学期/课程分类）
│   ├── semester-1/
│   │   ├── advanced-math/    # 高等数学
│   │   ├── linear-algebra/   # 线性代数
│   │   ├── c-programming/    # C语言程序设计
│   │   └── physics/          # 大学物理
│   ├── semester-2/
│   │   ├── data-structures/  # 数据结构
│   │   ├── discrete-math/    # 离散数学
│   │   └── oop/              # 面向对象程序设计
│   └── ...
├── quick-ref/                # 快速参考卡片（单页速查）
│   ├── formulas/             # 公式速查
│   ├── algorithms/           # 算法复杂度/模板
│   └── commands/             # 常用命令/工具
├── exams/                    # 往年真题/模拟题/重点整理
│   ├── midterm/
│   └── final/
├── projects/                 # 课程设计/实验/大作业代码
├── resources/                # 参考资料/教材PDF/链接索引
└── interest-learning/        # 兴趣/社团技能学习（非课程）
    ├── linux/                # Linux 入门（10 讲 + 速查表）
    ├── perception/           # 智能巴哈·感知组学习笔记（6 大类 27 讲 + 速查表）
    ├── mechanical/           # 智能巴哈·机械组 CATIA/ANSYS 学习笔记（4 模块 16 讲 + 速查表）
    ├── electronic-control/   # 智能巴哈·电控组 Simulink/Stateflow 学习笔记（5 模块 16 讲 + 速查表）
    ├── programming/          # 编程进阶/框架/语言
    ├── design/               # UI/平面/视频剪辑
    ├── hardware/             # 单片机/嵌入式/电路
    ├── soft-skills/          # 沟通/演讲/项目管理
    └── competitions/         # 竞赛备战/方案
```

## 已完成的笔记

`interest-learning/` 下的笔记统一结构：`00-大纲.md`（路线图 + 讲次索引 + 环境准备）+ 编号讲稿 + `<主题>-速查表.md`。

| 板块 | 学什么 | 规模 | 入口 |
|---|---|---|---|
| 📘 Linux 入门 | 命令行、文件、权限、进程、网络、Shell | 10 讲 | [00-大纲.md](interest-learning/linux/00-大纲.md) |
| 🤖 智能巴哈·感知组 | ROS 2、Python/OpenCV、视觉感知、Git、工程思维 | 6 大类 27 讲 | [00-大纲.md](interest-learning/perception/00-大纲.md) |
| 🔧 智能巴哈·机械组 | CATIA 建模、ANSYS 有限元、赛车结构、线控底盘 | 4 模块 16 讲 | [00-大纲.md](interest-learning/mechanical/00-大纲.md) |
| ⚡ 智能巴哈·电控组 | Simulink、MBD、VCU、Stateflow 状态机 | 5 模块 16 讲 | [00-大纲.md](interest-learning/electronic-control/00-大纲.md) |

### 📘 Linux 入门　`interest-learning/linux/`

[00-大纲.md](interest-learning/linux/00-大纲.md) · 10 讲 · 每讲约 10 分钟（正文 5 + 练习 5）· [速查表](interest-learning/linux/linux-速查表.md)

| 讲 | 主题 | 讲 | 主题 |
|---|---|---|---|
| 01 | [Linux 是什么](interest-learning/linux/01-linux是什么.md) | 06 | [用户与权限](interest-learning/linux/06-用户与权限.md) |
| 02 | [终端与基本概念](interest-learning/linux/02-终端与基本概念.md) | 07 | [软件包管理](interest-learning/linux/07-软件包管理.md) |
| 03 | [文件系统与导航](interest-learning/linux/03-文件系统与导航.md) | 08 | [进程管理](interest-learning/linux/08-进程管理.md) |
| 04 | [文件操作](interest-learning/linux/04-文件操作.md) | 09 | [网络基础](interest-learning/linux/09-网络基础.md) |
| 05 | [文件查看与编辑](interest-learning/linux/05-文件查看与编辑.md) | 10 | [Shell 脚本入门](interest-learning/linux/10-shell脚本入门.md) |

### 🤖 智能巴哈·感知组　`interest-learning/perception/`

[00-大纲.md](interest-learning/perception/00-大纲.md) · 6 大类 27 讲 · 约 17.4 万字 · [速查表](interest-learning/perception/perception-速查表.md)

从科普到进阶：环境 → 工具 → 框架 → 核心能力 → 工程实战。

| 大类 | 目录 | 讲次 | 内容 |
|---|---|---|---|
| 一 | [ros2/](interest-learning/perception/ros2/) | 5 | ROS 2 通信与诊断：节点、发布订阅、话题命令行、服务参数动作、写第一个节点 |
| 二 | [python-vision-basics/](interest-learning/perception/python-vision-basics/) | 4 | 图像与 NumPy、切片 ROI、摄像头拍照、形态学操作 |
| 三 | [ai-perception/](interest-learning/perception/ai-perception/) | 5 | 视觉任务全景、颜色空间与阈值、**可行驶区域识别实战**、深度学习入门、工程集成 |
| 四 | [git/](interest-learning/perception/git/) | 4 | 四个区域、撤销与恢复、分支合并、团队协作规范 |
| 五 | [engineering-thinking/](interest-learning/perception/engineering-thinking/) | 5 | 报错方法论、协作与求助模板、算力优化、Prompt 工程、工程清单 |
| 六 | [baja-track-perception/](interest-learning/perception/baja-track-perception/) | 4 | 赛道难点、**颜色特征失效后的方案**、障碍物识别与轻量化、方案设计 |

> 每个知识点都有对应讲次，对照表见 [00-大纲.md 第四节](interest-learning/perception/00-大纲.md)。

### 🔧 智能巴哈·机械组　`interest-learning/mechanical/`

[00-大纲.md](interest-learning/mechanical/00-大纲.md) · 4 模块 16 讲 · 每讲约 10 分钟 · [速查表](interest-learning/mechanical/mechanical-速查表.md)

软件基准 CATIA 2023 / ANSYS 2024 R2：

| 模块 | 目录 | 讲次 | 内容 |
|---|---|---|---|
| 一 | [catia/](interest-learning/mechanical/catia/) | 7 | 草图完全约束、基础特征与参考平面、**斜面草图定位**、孔与圆角、综合零件完整拆解、加强筋与肋 |
| 二 | [ansys/](interest-learning/mechanical/ansys/) | 5 | 有限元是什么、Workbench 全流程、网格与求解、**车架弯曲与扭转工况**、结果解读 |
| 三 | [racecar-engineering/](interest-learning/mechanical/racecar-engineering/) | 3 | 开发流程与 CATIA/ANSYS 定位、EPS 与 EHB 部件、**支架与安装座设计** |
| 四 | [self-check/](interest-learning/mechanical/self-check/) | 1 | 五个重点问题自测与易错点 |

> 每个知识点都有对应讲次，对照表见 [00-大纲.md 第四节](interest-learning/mechanical/00-大纲.md)。

### ⚡ 智能巴哈·电控组　`interest-learning/electronic-control/`

[00-大纲.md](interest-learning/electronic-control/00-大纲.md) · 5 模块 16 讲 · 每讲约 10 分钟 · [速查表](interest-learning/electronic-control/electronic-control-速查表.md)

软件基准 MATLAB R2021b+（Simulink / Stateflow）：

| 模块 | 目录 | 讲次 | 内容 |
|---|---|---|---|
| 一 | [simulink/](interest-learning/electronic-control/simulink/) | 5 | Simulink 界面与建模、**常用模块库清单**、第一个模型、**MBD 开发流程**、代码生成与烧录到 VCU |
| 二 | [vcu/](interest-learning/electronic-control/vcu/) | 3 | **VCU 是什么与主要功能**、输入输出与执行机构、自主驾驶下的转向与制动实现 |
| 三 | [stateflow/](interest-learning/electronic-control/stateflow/) | 5 | 状态机思想与界面、转移条件与动作语法、**优先级与层次结构**、**车辆运行模式状态机设计**、建模仿真与验证 |
| 四 | [chassis-control/](interest-learning/electronic-control/chassis-control/) | 2 | **线控转向与线控制动**、线控执行器与安全冗余 |
| 五 | [self-check/](interest-learning/electronic-control/self-check/) | 1 | 五个重点问题自测与易错点 |

> 每个知识点都有对应讲次，对照表见 [00-大纲.md 第四节](interest-learning/electronic-control/00-大纲.md)。状态机设计用**父状态 `Operational` 的出边**实现"急停最高优先级"——结构保证，不靠人工排序。

## 笔记编写规范

新建笔记（或续写已有笔记）必须遵循同一套骨架，保证不同主题的笔记读起来是同一种东西：

```markdown
# 第NN讲：标题（正文约X分钟 + 练习约Y分钟）

## 你将学到          ← 3~4 条口语化收获
## 分节正文          ← 恰好 1 个 💡 生活类比；1~2 个 ⚠️ 常见坑；对比信息用表格
## 🎯 课后练习        ← 命令行/代码类笔记用这个（Linux、感知组）
   🎯 动手练习        ← 图形软件类笔记用这个（CATIA/ANSYS/Stateflow，机械组、电控组）
                      两者都要求：3~6 步 + 末尾一行「✅ 你应该看到」的预期结果
## 本讲小结          ← Markdown 表格，4~6 行
```

> 练习标题为什么有两种：命令行笔记的练习**可以复制运行**，叫「课后练习」；图形软件笔记的练习**必须自己操作软件**（没有可复制的东西），叫「动手练习」更准确。按类型二选一，同一套笔记内部必须统一。

硬性要求：

- **篇幅：每讲 1800~2600 字，约 10 分钟**（正文 6 + 练习 4），基准体量看 `interest-learning/linux/`。超过 3000 字即算过度展开 —— 砍铺垫、砍举例堆砌、砍重复解释；每句话都该是"删了就少一个知识点"的
- 单讲**科普 → 进阶**，术语首次出现必须解释；`💡` 恰好 1 个
- **不跨笔记重复**：Git / 报错处理 / 团队协作 / Prompt 已在感知组讲过，其他笔记需要时**一句话指路**（`[../perception/git/]`），不要重写
- 所有命令/代码必须**实际跑通**过；`cv2.imread` 一类读文件的操作必须带失败保护，否则新手看到的是 `(-215:Assertion failed)` 这种鬼报错
- **图形软件（CATIA/ANSYS/Simulink/Stateflow）的笔记**：操作写成编号步骤，标清在哪个工作台、点哪个图标；凡是随版本变化的菜单名/按钮位置必须注明"以你机器上为准"，**禁止编造菜单名**
- 相同技术事实跨笔记必须口径一致（例：OpenCV 的 HSV 里 H 是 0~179，橙 = 11~25，红色跨两端 = 0~10 与 170~179；ANSYS 默认单位制 mm-t-N 下密度填 `7.85×10⁻⁹ t/mm³` 而不是 `7850 kg/m³`）
- 定稿前跑三项脚本校验：① 篇幅在区间内 ② 骨架四件套齐全 ③ 站内链接与表格列数无错
- 目录用 kebab-case；讲稿文件 `NN-主题.md`；速查表 `<主题>-速查表.md`

## 使用方式

### 本地克隆
```bash
git clone https://gitee.com/byteuser1977/WHUT-study.git
cd WHUT-study
```

### 新增课程笔记
```bash
# 例：新增《数据结构》笔记
mkdir -p courses/semester-2/data-structures
# 在对应目录下创建 .md 文件
```

### 快速参考卡片
`quick-ref/` 目录下的文件采用**单页 Markdown** 格式，适合打印或手机离线查看：
- 公式卡片：`quick-ref/formulas/微积分核心公式.md`
- 算法模板：`quick-ref/algorithms/排序算法模板.md`
- 命令速查：`quick-ref/commands/git-常用命令.md`

## 命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 课程目录 | `kebab-case` | `data-structures` |
| 笔记文件 | `章节-主题.md` | `03-树与二叉树.md` |
| 讲稿文件 | `NN-主题.md` | `04-形态学操作.md` |
| 速查表 | `<主题>-速查表.md` | `perception-速查表.md` |
| 速查卡片 | `主题-速查.md` | `微积分核心公式-速查.md` |
| 代码文件 | 语言标准命名 | `sort.cpp`, `main.py` |

## 学习工作流

1. **上课时** → 直接在对应课程目录下记笔记（Markdown）
2. **课后整理** → 提炼核心知识点到 `quick-ref/`
3. **考前复习** → 阅读 `quick-ref/` + `exams/` 真题
4. **定期同步** → `git add . && git commit -m "update: xxx" && git push`

## 标签体系（可选）

在笔记文件顶部添加 front matter 便于检索：
```yaml
---
course: 数据结构
semester: 2
tags: [树, 递归, 遍历, 重点]
difficulty: hard
exam-focus: true
---
```

## 贡献指南

- 仅限个人学习使用，不接受外部 PR
- 如需同步到多设备：`git pull --rebase` 后再推送
- 敏感信息（成绩、个人隐私）请勿提交

## 许可证

MIT License — 仅供个人学习参考。

---

> **Tip**: 建议配合 Obsidian / VS Code + Markdown 插件使用，支持图谱视图、反向链接、LaTeX 公式渲染。
