# 电控组速查表

> 复习 / 建模时快速翻。详细解释见对应讲次。软件以 **MATLAB R2021b+（Simulink / Stateflow）** 为基准，不同版本菜单可能有差异，**以你机器上为准**。

---

## 一、Simulink 常用模块速查（模块知识骨架）

| 库 | 模块（中英） | 用途 |
|---|---|---|
| `Sources` | `Constant` 常量、`Step` 阶跃、`Sine Wave` 正弦、`Clock` 时钟 | 造输入信号 |
| `Sinks` | `Scope` 示波器、`Display` 数值、`To Workspace` 存工作区 | 看结果 |
| `Continuous` | `Integrator` 积分、`Derivative` 微分、`Transfer Fcn` 传递函数 | 动态系统 |
| `Math Operations` | `Gain` 增益、`Sum` 求和、`Product` 乘、`Abs` 绝对值 | 运算 |
| `Logic and Bit` | `Logical Operator`、`Relational Operator` 比较 | 条件判断 |
| `Signal Routing` | `Mux` 合成、`Demux` 分解、`Bus Creator` | 信号打包 |
| `Discontinuities` | `Saturation` 饱和限幅、`Rate Limiter` 变化率限幅、`Dead Zone` 死区 | **车上必备限幅** |
| `Discrete` | `Unit Delay` 单位延时、`Zero-Order Hold` | 离散控制 |
| `Stateflow` | `Chart` 状态机 | 逻辑切换 |

**常用五件套**：`Constant` / `Gain` / `Sum` / `Integrator` / `Scope`（给输入 → 运算 → 积分 → 看波形）。
**车上必备**：`Saturation` + `Rate Limiter`（没有限幅的控制器不敢上车）。

---

## 二、Simulink 操作与求解器

| 项 | 要点 |
|---|---|
| 建模四步 | 新建 → 拖模块 → 连线 → 双击设参数 → `Run` |
| 求解器 | `Fixed-step` 定步长（车上常用，步长常取 `0.001s`）/ 变步长（`ode45` 等）；配置在 `Model Settings → Solver` |
| 波形不对的三个原因 | 步长太大（丢细节）、参数单位错、反馈没接成闭环 |
| 文件类型 | `.slx` 模型；Stateflow 在模型里是 `Chart` 模块，双击进入编辑器 |

---

## 三、MBD 流程与烧录链路

```
                          ┌── 需求与系统设计
            V 模型左侧 →──┤   模型开发 + MIL（模型在环）
                          └   代码生成 → SIL（软件在环）
                                        → PIL / HIL（处理器/硬件在环）
            V 模型右侧 →──────────────── 实车标定
```

**一条铁律**：先仿真后上车 —— 先在 MIL 里跑通逻辑，再生成代码。

**烧录四步**：

| 步 | 做什么 | 关键点 |
|---|---|---|
| ① | 固定接口与数据类型 | 用 `Inport`/`Outport`，车上不用 `double`，限幅写进模型 |
| ② | 配置 `Model Configuration Parameters` | 定步长求解器 + 目标文件 `ert.tlc` + 目标硬件 |
| ③ | `Embedded Coder` 生成代码 | 生成 `.c/.h` → 用目标板工具链（TI CCS / Keil / GNU）编译成 `.hex`/`.bin` |
| ④ | 刷写与标定 | JTAG/SWD 或 CAN bootloader 刷写 → 台架验证 → 上车在线标定 |

> ⚠️ 每次烧录记录**模型版本与固件版本**，否则现场分不清车上跑的是哪一版。

---

## 四、VCU 速查

**定义**：VCU = Vehicle Control Unit，整车控制器 —— 车辆的**中央控制与协调单元**（车上的"总调度员"）。

| 功能 | 说明 |
|---|---|
| 信号采集与解析 | 把开关/传感器/CAN 报文翻译成有物理意义的量 |
| 驾驶模式管理 | 待机 / 遥控 / 自主 / 紧急 —— 即模块三的状态机 |
| 指令仲裁与限幅 | 多来源指令谁生效、限幅、平滑 |
| 指令输出 | 驱动扭矩、转向、制动指令下发到执行机构 |
| 故障诊断与安全保护 | 看门狗、故障分级、进安全状态 |
| 通信与上下电管理 | CAN 与遥控、自主系统、电机控制器、BMS 交互 |

**核心价值**：把**安全逻辑集中在一处**（急停最高优先级、故障必进安全态）。
**信号流**：输入（遥控/自主目标值/急停/车速转角 IMU）→ VCU → 执行机构（电机控制器 / 线控转向 / EHB）→ 反馈回 VCU。

---

## 五、Stateflow 语法速查

| 语法 | 含义 |
|---|---|
| `entry: ...` | **进入**该状态时执行一次 |
| `during: ...` | **停留**在该状态期间每个步长都执行 |
| `exit: ...` | **离开**该状态时执行一次 |
| `[条件]` | 转移标签的条件，方括号必填 |
| `[条件]{动作}` | 条件成立并转移时执行动作 |
| 默认转移 | 从空白处画出的转移 = **上电入口**，一般指向 `Standby` |
| 超状态（superstate） | 把若干状态框起来当父状态；**排他（OR）分解下同时只有一个子状态激活** |
| 执行顺序 | 同一状态多条出边同时为真时按它裁决；在状态上右键可查改 |

> 💡 **状态机设计里最关键的一条规则**：**超状态的出边优先级高于其内部子状态的出边** —— 所以把急停转移挂在父状态上，"任何情况下急停都赢"就是**画出来的，不是排出来的**。

---

## 六、车辆运行模式状态机完整设计（★建模用）

### 6.1 层次结构

```text
                       ┌────────── Operational ──────────┐
   上电默认转移 ───────→│  Standby  ·  Manual  ·  Auto     │
                       └──────────────────────────────────┘
                                     │ [Emergency_Stop || Vehicle_Fault]   ★最高优先级
                                     ▼
                                 Emergency
                                     │ [Emergency_Reset && !Emergency_Stop]
                                     ▼
                                  Standby
```

### 6.2 状态与输出

| 状态 | 名称 | 输出动作 |
|---|---|---|
| `Standby` | 待机 | `entry: VCU_Mode = 0; Target_Torque = 0;`（不输出驱动力）|
| `Manual` | 遥控驾驶 | `entry: VCU_Mode = 1;` |
| `Auto` | 自主驾驶 | `entry: VCU_Mode = 2;` |
| `Emergency` | 紧急模式 | `entry: VCU_Mode = 3; Target_Torque = 0; Brake_Request = 1;`<br>`during: Target_Torque = 0; Brake_Request = 1;`<br>`exit: Brake_Request = 0;` ← **必须清零** |

> ⚠️ `Brake_Request` 不在 `exit` 里清零，退出紧急后制动请求会一直挂着，车动不了。

### 6.3 转移条件表

| # | 源 | 目标 | 条件 |
|---|---|---|---|
| 0 | 默认转移 | `Standby` | 无（Default transition）|
| 1 | `Standby` | `Manual` | `[Manual_Enable && RC_Online]` |
| 2 | `Standby` | `Auto` | `[Auto_Enable && Auto_System_OK]` |
| 3 | `Manual` | `Standby` | `[!Manual_Enable \|\| !RC_Online]` |
| 4 | `Auto` | `Standby` | `[!Auto_Enable \|\| !Auto_System_OK]` |
| 5 | **`Operational`（父）** | `Emergency` | `[Emergency_Stop \|\| Vehicle_Fault]` ★最高优先级 |
| 6 | `Emergency` | `Standby` | `[Emergency_Reset && !Emergency_Stop]` |

### 6.4 三条设计要求的落地

| 要求 | 怎么实现 |
|---|---|
| 急停最高优先级 | 急停转移挂在**父状态 `Operational`** 上 —— 超状态出边优先于子状态出边，任何模式下急停都赢 |
| 遥控与自主不能同时生效 | ①**结构层**：Manual 与 Auto 是排他（OR）兄弟状态，同时只能有一个激活 ②**仲裁层**：两条件同时为真时按执行顺序裁决，把 `→ Manual` 排在 `→ Auto` 前面（遥控优先）③**加固**：条件互锁 `&& !Auto_Enable` / `&& !Manual_Enable` |
| 故障下进安全状态 | `Emergency_Stop \|\| Vehicle_Fault` 从任何模式都能进 Emergency；空档（进安全态）比冒险好 |

### 6.5 验证激励时序

```
t=0.0s 上电                                    → Standby（VCU_Mode=0）
t=1.0s Manual_Enable=1, RC_Online=1            → Manual（VCU_Mode=1）
t=2.0s RC_Online=0                             → Standby（VCU_Mode=0）
t=3.0s Auto_Enable=1, Auto_System_OK=1         → Auto（VCU_Mode=2）
t=4.0s Emergency_Stop=1                        → Emergency（Torque=0, Brake_Request=1）★
t=5.0s Emergency_Stop=0, Emergency_Reset=1     → Standby，且 Brake_Request 必须已归零
```

### 6.6 产出检查清单

```
□ Stateflow 状态机框图截图（能看清：全部状态名 / 每条转移的条件 / 状态内的动作）
□ 状态转移条件表（7 条：6 条转移 + 默认转移）
□ 各状态输出表（VCU_Mode / Target_Torque / Brake_Request）
```

---

## 七、线控底盘速查

**定义**：线控 = **X-by-Wire**，用**电信号 + 电控执行器**替代机械 / 液压 / 气动的力传递路径。

| | 线控转向 | 线控制动 |
|---|---|---|
| 方案 | **SBW**：方向盘与转向轮**解耦**（转角传感器 → ECU → 转向电机）| **EHB** 电控液压（踏板传感器 → ECU → 电磁阀块/泵建压）；**EMB** 电控机械（电机直驱卡钳）|
| 与传统的区别 | **EPS 只"助力"**，机械连接仍保留；**SBW 可取消机械杆** | 传统靠踏板力经液压放大；线控由电信号触发建压 |

**自己的理解（两面都要写）**：
- 好处：布置自由（不迁就机械路径）、响应快、手感可软件标定、天生适配自动驾驶（接口就是信号）、便于集中安全逻辑
- 代价：失去机械备份 → 必须做**冗余与失效降级**；强依赖供电与通信 → **EMC 与看门狗**；成本与开发复杂度上升；涉及**功能安全（ISO 26262 / ASIL）**

**冗余三招**：双路供电/双绕组电机、双 CAN 通道、机械限位作最终兜底。

---

## 八、自主驾驶下的转向与制动

```
感知 → 规划 → 控制 → [ VCU ] → 执行机构 → 车辆 → 反馈（转角 / 车速 / IMU）
                       │
        ┌──────────────┼──────────────┐
   目标转向角 → 线控转向执行器   目标扭矩 → 电机控制器   制动 → EHB 建缸压
```

**VCU 做三件事**：指令转换、多源仲裁、安全限幅。
**安全三条**：角度限幅 / 扭矩斜率限制 / **制动优先于驱动**。
**必须提**：自主模式下**仍受急停最高优先级约束**；任一路信号丢失要能**降级**（回待机 / 切遥控 / 进紧急）。

---

## 九、表述结构（通用）

```
① 一句话结论    ← 先给判断，别铺垫
② 两三个要点    ← 每个要点 = 判断 + 理由，不能只扔名词
③ 一句落地      ← 提到巴哈 / 我们的 VCU / 遥控与自主，立刻脱离套话
```

**❌ 套话特征（出现就删）**："随着……的发展"、"众所周知"、"具有重要意义"，以及任何**换到别的问题也成立**的句子。每个问题 150~300 字足够。
