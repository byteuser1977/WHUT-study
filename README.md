# WHUT-study

武汉理工大学课程学习笔记仓库 — 快速复习、考前突击、知识点索引。

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
└── interest-learning/        # 兴趣/社团学习（非课程）
    ├── linux/                # Linux 入门快速教程（10 讲 + 速查表）
    ├── perception/           # 智能巴哈·感知组学习教程（6 大类 27 讲 + 速查表）
    ├── mechanical/           # 智能巴哈·机械组招新笔试备考（4 模块 16 讲 + 速查表）
    ├── programming/          # 编程进阶/框架/语言
    ├── design/               # UI/平面/视频剪辑
    ├── hardware/             # 单片机/嵌入式/电路
    ├── soft-skills/          # 沟通/演讲/项目管理
    └── competitions/         # 竞赛备战/历年题/方案
```

## 已完成的教程

`interest-learning/` 下的教程统一结构：`00-大纲.md`（路线图 + 讲次索引 + 环境准备）+ 编号讲稿 + `<主题>-速查表.md`。

### 📘 Linux 入门快速教程　`interest-learning/linux/`

[00-大纲.md](interest-learning/linux/00-大纲.md) · 10 讲 · 每讲约 10 分钟（正文 5 + 练习 5）· [速查表](interest-learning/linux/linux-速查表.md)

| 讲 | 主题 | 讲 | 主题 |
|---|---|---|---|
| 01 | [Linux 是什么](interest-learning/linux/01-linux是什么.md) | 06 | [用户与权限](interest-learning/linux/06-用户与权限.md) |
| 02 | [终端与基本概念](interest-learning/linux/02-终端与基本概念.md) | 07 | [软件包管理](interest-learning/linux/07-软件包管理.md) |
| 03 | [文件系统与导航](interest-learning/linux/03-文件系统与导航.md) | 08 | [进程管理](interest-learning/linux/08-进程管理.md) |
| 04 | [文件操作](interest-learning/linux/04-文件操作.md) | 09 | [网络基础](interest-learning/linux/09-网络基础.md) |
| 05 | [文件查看与编辑](interest-learning/linux/05-文件查看与编辑.md) | 10 | [Shell 脚本入门](interest-learning/linux/10-shell脚本入门.md) |

### 🤖 智能巴哈·感知组学习教程　`interest-learning/perception/`

[00-大纲.md](interest-learning/perception/00-大纲.md) · 6 大类 27 讲 · 约 17.4 万字 · [速查表](interest-learning/perception/perception-速查表.md)

面向车队感知组招新试题，从科普到进阶（环境 → 工具 → 框架 → 核心能力 → 工程实战）：

| 大类 | 目录 | 讲次 | 内容 | 对应试题 |
|---|---|---|---|---|
| 一 | [ros2/](interest-learning/perception/ros2/) | 5 | ROS 2 通信与诊断：节点、发布订阅、话题命令行、服务参数动作、写第一个节点 | 技术 1(1)(2) |
| 二 | [python-vision-basics/](interest-learning/perception/python-vision-basics/) | 4 | 图像与 NumPy、切片 ROI、摄像头拍照、形态学操作 | 技术 2(1)~(4) |
| 三 | [ai-perception/](interest-learning/perception/ai-perception/) | 5 | 视觉任务全景、颜色空间与阈值、**可行驶区域识别实战**、深度学习入门、工程集成 | 技术 3(1) |
| 四 | [git/](interest-learning/perception/git/) | 4 | 四个区域、撤销与恢复、分支合并、团队协作规范 | 技术 4(1)(2) |
| 五 | [engineering-thinking/](interest-learning/perception/engineering-thinking/) | 5 | 报错方法论、协作与求助模板、算力优化、Prompt 工程、工程清单 | 思维 1/2/3/5 |
| 六 | [baja-track-perception/](interest-learning/perception/baja-track-perception/) | 4 | 赛道难点、**颜色特征失效后的方案**、障碍物识别与轻量化、方案设计 | 思维 4(1)(2) |

> 15 条招新试题（技术类 9 小问 + 思维类 6 题）全部有对应讲次，对照表见 [00-大纲.md 第四节](interest-learning/perception/00-大纲.md)。

### 🔧 WUTIB 智能巴哈·机械组招新笔试备考　`interest-learning/mechanical/`

[00-大纲.md](interest-learning/mechanical/00-大纲.md) · 4 模块 16 讲 · 每讲约 10 分钟 · [速查表](interest-learning/mechanical/mechanical-速查表.md)

面向机械组招新笔试（建模实操 50 分 + 书面简答 50 分 + 选做加分 15 分），软件基准 CATIA 2023 / ANSYS 2024 R2：

| 模块 | 目录 | 讲次 | 内容 | 对应分值 |
|---|---|---|---|---|
| 一 | [catia/](interest-learning/mechanical/catia/) | 7 | 草图完全约束、基础特征与参考平面、**斜面草图定位**、孔与圆角、必做题完整拆解、肋与加强筋 | 必做题 50 + 加分 15 |
| 二 | [ansys/](interest-learning/mechanical/ansys/) | 5 | 有限元是什么、Workbench 全流程、网格与求解、**车架弯曲与扭转工况**、结果解读 | 简答 1、3 |
| 三 | [racecar-engineering/](interest-learning/mechanical/racecar-engineering/) | 3 | 开发流程与 CATIA/ANSYS 定位、EPS 与 EHB 部件、**支架与安装座设计** | 简答 2、4、5 |
| 四 | [written-answers/](interest-learning/mechanical/written-answers/) | 1 | 五道简答题的答题框架、得分要点、丢分点、提交规范 | 简答 50 |

> 13 项评分点（必做题 5 + 加分题 3 + 简答 5）全部有对应讲次，对照表见 [00-大纲.md 第四节](interest-learning/mechanical/00-大纲.md)。简答部分只给思考框架不给套话——试题明确禁止 AI 套话答案。

## 教程编写规范

新建教程（或续写已有教程）必须遵循同一套骨架，保证不同主题的教程读起来是同一种东西：

```markdown
# 第NN讲：标题（正文约X分钟 + 练习约Y分钟）

## 你将学到          ← 3~4 条口语化收获
## 分节正文          ← 至少 1 个 💡 生活类比；可含 ⚠️ 常见坑；对比信息用表格
## 🎯 课后练习        ← 可直接复制运行，附「✅ 你应该看到」的预期输出
## 本讲小结          ← Markdown 表格
```

硬性要求：

- **篇幅：每讲 1800~2600 字，约 10 分钟**（正文 6 + 练习 4），基准体量看 `interest-learning/linux/`。超过 3000 字即算过度展开 —— 砍铺垫、砍举例堆砌、砍重复解释；每句话都该是"删了就丢分"的
- 单讲**科普 → 进阶**，术语首次出现必须解释
- 所有命令/代码必须**实际跑通**过；`cv2.imread` 一类读文件的操作必须带失败保护，否则新手看到的是 `(-215:Assertion failed)` 这种鬼报错
- **图形软件（CATIA/ANSYS 等）的教程**：操作写成编号步骤，标清在哪个工作台、点哪个图标；凡是随版本变化的菜单名/按钮位置必须注明"以你机器上为准"，**禁止编造菜单名**
- 相同技术事实跨讲必须口径一致（例：OpenCV 的 HSV 里 H 是 0~179，橙 = 11~25，红色跨两端 = 0~10 与 170~179；ANSYS 默认单位制 mm-t-N 下密度填 `7.85×10⁻⁹ t/mm³` 而不是 `7850 kg/m³`）
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
| 教程讲稿 | `NN-主题.md` | `04-形态学操作.md` |
| 教程速查表 | `<主题>-速查表.md` | `perception-速查表.md` |
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