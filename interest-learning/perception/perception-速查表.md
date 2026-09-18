# 感知组速查表

> 一页纸版本，考前/现场快速翻。详细解释见对应讲次。

---

## 一、ROS 2 常用命令

```bash
# ── 环境 ──
source /opt/ros/humble/setup.bash     # 每次新开终端都要做（或写进 ~/.bashrc）
ros2 --version                        # 检查是否装好

# ── 节点 ──
ros2 node list                        # 有哪些节点在跑
ros2 node info /节点名                 # 该节点的发布/订阅/服务

# ── 话题 ──
ros2 topic list                       # 有哪些话题
ros2 topic list -t                    # 带消息类型
ros2 topic info /话题名                # 谁在发、谁在收、消息类型、QoS
ros2 topic echo /话题名                # 打印话题内容（看数据对不对）
ros2 topic hz /话题名                  # ★ 实时发布频率 FPS（掉帧靠它定位）
ros2 topic bw /话题名                  # 带宽占用
ros2 topic pub /话题名 std_msgs/msg/String "{data: 'hi'}" -r 10   # 手动按 10Hz 发消息

# ── 图形化诊断 ──
rqt_graph                             # 画出节点与话题的连接图
rqt_console                           # 日志查看器

# ── 包与构建 ──
ros2 pkg list                         # 已安装的包
ros2 pkg create --build-type ament_python my_pkg   # 新建包
colcon build --symlink-install        # 在工作空间根目录构建
source install/setup.bash             # 构建后 source 才能找到自己的包
ros2 run 包名 可执行名                 # 跑一个节点
ros2 launch 包名 xxx.launch.py         # 一次启动多个节点
```

**诊断四步法**（话题没数据时按顺序查）：

| 顺序 | 检查 | 命令 | 没问题的话 |
|---|---|---|---|
| 1 | 节点在不在 | `ros2 node list` | 能看到发布者节点 |
| 2 | 话题有没有 | `ros2 topic list` | 话题名拼写一致 |
| 3 | 频率对不对 | `ros2 topic hz /xxx` | 有稳定的 Hz 输出 |
| 4 | 内容对不对 | `ros2 topic echo /xxx` | 数据是期望的数值 |

> ⚠️ 话题名区分大小写、区分 `/` 前缀；QoS 不匹配时也能 list 到但 echo 不到数据。

---

## 二、OpenCV + NumPy 常用片段

```python
import cv2, numpy as np

# ── 读写与显示 ──
img = cv2.imread("a.jpg")                  # 默认 BGR，失败返回 None（路径错/不支持格式）
cv2.imwrite("out.png", img)                # 保存
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
rgb  = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# ── 尺寸与通道 ──
h, w = img.shape[:2]                       # 高度、宽度
print(img.shape)                           # (480, 640, 3) → 高, 宽, 通道数
print(img.dtype)                           # uint8，取值 0~255

# ── 切片 / ROI ──
upper = img[0:240, :]                      # ★ 上半部分（前 240 行）—— 切片最常用的一招
left  = img[:, 0:320]                      # 左半部分
roi   = img[y:y+h2, x:x+w2]                # 任意矩形区域
img[0:50, 0:50] = 0                        # 直接改像素（抹掉左上角）

# ── 几何变换 ──
resized = cv2.resize(img, (640, 480))      # 注意：(宽, 高)
flipped = cv2.flip(img, 1)                 # 1=水平翻转 0=垂直 -1=双向
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)   # 画框（BGR 绿）
cv2.circle(img, (cx, cy), r, (0, 0, 255), 2)
cv2.putText(img, "text", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

# ── 阈值分割 ──
_, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
_, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
adapt = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                              cv2.THRESH_BINARY, 11, 2)
mask = cv2.inRange(hsv, np.array([11,43,46]), np.array([25,255,255]))   # 按颜色抠
out  = cv2.bitwise_and(img, img, mask=mask)                            # 抠出来

# ── 滤波 ──
blur = cv2.GaussianBlur(img, (5, 5), 0)    # 高斯模糊，去高频噪声
med  = cv2.medianBlur(img, 5)              # 中值滤波，去椒盐噪声

# ── 边缘 ──
edges = cv2.Canny(gray, 50, 150)

# ── 轮廓 ──
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
c = max(contours, key=cv2.contourArea)     # 最大连通域
area = cv2.contourArea(c)
x, y, w, h = cv2.boundingRect(c)

# ── 摄像头 ──
cap = cv2.VideoCapture(0)                                  # 0=默认摄像头
# Windows 打不开时改用：cv2.VideoCapture(0, cv2.CAP_DSHOW)
if not cap.isOpened():
    print("摄像头打不开：换索引 1/2 试试，或检查是否被其他程序占用")
ret, frame = cap.read()                    # ret 为 True 才算读到
cv2.imwrite("photo.jpg", frame)            # ★ 保存照片 —— 拍照三步走的第二步
cap.release()                              # 用完必须释放
cv2.destroyAllWindows()
```

> ⚠️ `cv2.imshow` 在纯 WSL（无图形界面）下会报错，需用 `cv2.imwrite` 存文件再在 Windows 里看；或用 WSLg / VcXsrv。

---

## 三、HSV 颜色阈值参考表（OpenCV 里 H 为 0~179）

| 颜色 | H | S | V |
|---|---|---|---|
| 红（段1） | 0~10 | 43~255 | 46~255 |
| 红（段2） | 170~179 | 43~255 | 46~255 |
| 橙（锥桶） | 11~25 | 43~255 | 46~255 |
| 黄 | 26~34 | 43~255 | 46~255 |
| 绿 | 35~77 | 43~255 | 46~255 |
| 蓝 | 100~124 | 43~255 | 46~255 |

> ⚠️ 红色跨 H 轴两端，必须两段 `inRange` 后 `bitwise_or`。

---

## 四、形态学操作对照表

| 操作 | 常量 | 计算 | 效果 | 用途 |
|---|---|---|---|---|
| 腐蚀 | `cv2.erode` | — | 白块变小 | 去噪、断开粘连 |
| 膨胀 | `cv2.dilate` | — | 白块变大 | 补洞、连接 |
| **开运算** | `MORPH_OPEN` | 先腐蚀后膨胀 | 形状不变，**去掉小白点** | **去噪** |
| **闭运算** | `MORPH_CLOSE` | 先膨胀后腐蚀 | 形状不变，**填掉小黑洞** | **补孔洞、连断缝** |
| 梯度 | `MORPH_GRADIENT` | 膨胀−腐蚀 | 只剩边缘线 | 提轮廓 |
| 顶帽 | `MORPH_TOPHAT` | 原图−开运算 | 突出亮的小细节 | 光照补偿 |
| 黑帽 | `MORPH_BLACKHAT` | 闭运算−原图 | 突出暗的小细节 | 光照补偿 |

```python
kernel = np.ones((5,5), np.uint8)
out = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)   # 一句话调用
```

**记法**：开运算 = **开**掉噪点；闭运算 = **闭**上孔洞。

---

## 五、Git 撤销场景对照表

| 你的处境 | 命令 | 后果 |
|---|---|---|
| 改乱了，**还没 add** | `git restore .`（旧：`git checkout -- .`） | 工作区回到上次提交，**改动丢失** |
| 已 `add`，**没 commit** | `git restore --staged .` 再 `git restore .` | 先撤销暂存，再还原文件 |
| 已 `commit`，**没 push**，想改提交内容 | `git reset --soft HEAD~1` | 提交撤销，改动**留在暂存区** |
| 已 `commit`，**没 push**，想彻底回到上一版 | `git reset --hard HEAD~1` | ⚠️ 改动**永久丢失** |
| 已 **push** 到远程，想撤 | `git revert <commit>` | 生成一个"反向提交"，**历史保留**，最安全 |
| 想临时存一下去干别的 | `git stash` / `git stash pop` | 改动存起来，工作区变干净 |
| 误删了提交/分支 | `git reflog` 找回 | 能看到所有 HEAD 移动记录 |

### 四个区域与数据流向

```
工作区                暂存区                本地仓库              远程仓库
Working Dir    ──add──▶  Staging   ──commit──▶  Local Repo  ──push──▶  Remote
（你改的文件）           （Index）              （.git 里的历史）        （GitHub）

     ◀────────────────────  pull / fetch + merge  ────────────────────
     ◀──── restore（丢弃工作区改动）  ◀──── reset（回退提交）
```

```bash
git status            # 看当前在哪个区、哪些文件变了
git log --oneline -10 # 看最近 10 条提交
git diff              # 工作区 vs 暂存区
git diff --staged     # 暂存区 vs 本地仓库
```

---

## 六、算力优化清单（不换硬件）

| 手段 | 省什么 | 代价 |
|---|---|---|
| 降低输入分辨率（640→320） | 计算量按面积平方下降（约省 75%） | 远处小目标丢细节 |
| ROI 裁剪（只处理下半幅/路面区域） | 直接砍掉无关像素 | 上方目标漏检 |
| 抽帧 / 跳帧（30fps 检测 10fps） | 检测耗时降到 1/3 | 高速运动时漏帧，需跟踪补偿 |
| 算法简化与降级 | 大幅降低单帧耗时 | 精度下降、边界变糙 |
| 模型量化 INT8 / FP16 | 推理速度 2~4 倍，内存减半 | 少量精度损失，需校准 |
| 剪枝 / 知识蒸馏 | 参数量与计算量下降 | 需重新训练调优 |
| TensorRT / ONNX Runtime / GPU | 推理吞吐大幅提升 | 部署复杂度、功耗上升 |
| 多线程 / C++ 重写 OpenCV 环节 | 消除 Python GIL 瓶颈 | 开发成本高 |
| 缓存与查表、减少颜色空间转换次数 | 省重复计算与内存拷贝 | 代码可读性下降 |
| 降采样后再精算（金字塔） | 先粗定位再细算 | 实现变复杂 |

**优先级建议**：先 ROI 裁剪 → 再降分辨率 → 再抽帧+跟踪 → 最后才上量化/剪枝。

---

## 七、报错自查清单

```
1. 读报错：看【最后一行】的异常类型（ModuleNotFoundError / ImportError /
   AttributeError / TypeError / ValueError / Segmentation fault ...）
2. 定位：向上找【第一处出现你自己文件名】的 File "xxx.py", line N
3. 提取关键词：去掉绝对路径、版本号、内存地址，只留 异常名 + 动作词
4. 搜：用英文原文搜、把整句异常加引号搜、加上版本号与技术栈
5. 改之前存档三件套：git commit / 复制一份文件 / 记下当前参数
6. 一次只改一处，改完立刻验证
7. 实在不行：把新加的代码注释掉，确认是不是它引入的
```

**求助时的六件套**：

| 项 | 例子 |
|---|---|
| 环境版本 | Ubuntu 22.04 / Python 3.10 / opencv 4.9.0 / ROS 2 Humble |
| 复现步骤 | 依次执行了哪几条命令 |
| 期望结果 | 应该弹出摄像头窗口显示画面 |
| 实际结果 | 窗口一闪而过，终端输出下面这段报错 |
| 已尝试 | 换过摄像头索引、重装过 opencv-python |
| 完整报错 | （整段粘贴，不要只贴一行） |

---

## 八、提示词模板（与 AI 高效对话）

```
【角色】你是有 5 年 ROS 2 开发经验的机器人工程师
【目标】写一个 ROS 2 节点，订阅摄像头图像并在终端打印分辨率
【环境】Ubuntu 22.04 + ROS 2 Humble + Python 3.10 + opencv-python 4.9
【输入】无（直接用笔记本自带摄像头，索引 0）
【约束】只用 rclpy + cv2；不要用 cv_bridge；单文件；加中文注释
【输出格式】完整可运行代码 + 逐行解释 + colcon 构建与运行命令
【验收标准】ros2 run 后能持续打印 "分辨率 640x480"，Ctrl+C 能正常退出
【示例】（可选，给一份你希望的输出样式）
```

**迭代追问四步**：

| 轮次 | 问什么 | 为什么这么问 |
|---|---|---|
| 1 | 先要整体方案与依赖 | 先确认路线对不对，别急着要代码 |
| 2 | 要完整代码 + 构建运行步骤 | 环境信息已给全，一次拿到能跑的东西 |
| 3 | 贴报错要针对性修改 | 带上下文纠错，比重新描述高效十倍 |
| 4 | 要自检清单与参数说明 | 让它自查边界情况，暴露它没说的假设 |

**别信 AI 的场合**：比赛规则与赛制细节、最新版本 API 变更、安全相关代码、具体硬件接线。

---

## 九、可行驶区域识别流水线（一步不落）

```
原图(BGR)
  → 转灰度 / 转 HSV
  → 高斯模糊（去高频噪点）
  → 阈值分割（颜色 inRange 或灰度阈值/Otsu）→ 得到二值掩膜
  → 形态学闭运算（补小孔洞）+ 开运算（去小白点）
  → 找轮廓 → 取最大连通域（假设可行驶区域是最大的一块）
  → 填充 + 生成掩膜 → 与原图叠加可视化
  → 输出：区域掩膜 / 检出框 / 占比百分比
```

**答辩要点（每步都要能说出为什么）**：
- 为什么先模糊：抑制噪点，避免阈值后出现碎斑
- 为什么用颜色/灰度双路：单一路径在泥水下不稳定
- 为什么形态学：修补分割错误，让区域连续
- 为什么取最大连通域：可行驶区域在图像中通常是最大的一块连通区域
- 失败场景：泥水完全遮盖、强逆光、区域被障碍物切断 → 需要多特征融合（见大类六第 02 讲）
