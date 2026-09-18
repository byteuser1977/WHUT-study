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
    ├── programming/          # 编程进阶/框架/语言
    ├── design/               # UI/平面/视频剪辑
    ├── hardware/             # 单片机/嵌入式/电路
    ├── soft-skills/          # 沟通/演讲/项目管理
    └── competitions/         # 竞赛备战/历年题/方案
```

## 已完成的教程

| 教程 | 入口 | 规模 |
|---|---|---|
| Linux 入门快速教程 | [interest-learning/linux/00-大纲.md](interest-learning/linux/00-大纲.md) | 10 讲，每讲约 10 分钟 |
| 智能巴哈·感知组学习教程 | [interest-learning/perception/00-大纲.md](interest-learning/perception/00-大纲.md) | 6 大类 27 讲，含题库对照表 |

## 使用方式

### 本地克隆
```bash
git clone https://github.com/byteuser1977/WHUT-study.git
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