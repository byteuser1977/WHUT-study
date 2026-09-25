# Stanley 横向控制算法

## 你将学到
- Stanley 算法的核心思想和几何直觉
- 带阻尼 Stanley 的完整数学公式
- 代码逐行解析与公式对应
- 低速软化和转角限幅的工程意义

---

## 1. Stanley 是什么

Stanley 是一种**几何类横向路径跟踪算法**，由斯坦福大学团队提出，用于前轮转向车辆。核心思想：让车辆前轴同时修正**航向偏差**和**横向偏差**，既对齐路径方向，又贴合路径位置。

> 💡 类比：想象你在走一条直道，但走歪了。Stanley 做两件事——①把身体转回和路平行（航向修正），②往路中间走（横向修正）。两件事同时做，很快就能回到路中央。

---

## 2. 基础 Stanley 公式

### 航向误差

车辆当前航向与路径切线方向的夹角：

```
θ_e = θ_path - θ_vehicle
```

> 角度需归一化到 [-π, π]，否则 ±360° 会导致错误。

### 横向误差

前轴中心到路径的垂直距离（左正右负）：

```
e = -(x_idx - x) × sin(θ_vehicle) + (y_idx - y) × cos(θ_vehicle)
```

### Stanley 转向角

```
δ = θ_e + arctan(k_e × e / v)
```

其中：
- `k_e`：横向误差增益（越大纠偏越激进）
- `v`：当前车速（分母，高速时横向修正减弱）
- `arctan`：保证输出有界

> ⚠️ 常见坑：当 v=0 时分母为零，会报错。工程上需要加低速软化。

---

## 3. 带阻尼的 Stanley（完整版）

基础 Stanley 在高速或大曲率时容易振荡。加入**阻尼项**抑制横摆振荡。

### 完整公式

**Step 1：低速软化**
```
v_eff = |v| + k_s
```
`k_s` 是软化系数（如 1.0 m/s），防止低速除零。

**Step 2：Stanley 主项**
```
δ_st = θ_e + arctan2(k_e × e, v_eff)
```

**Step 3：阻尼修正**
```
r_ref = v × κ_idx          # 路径曲率对应的期望横摆率
δ = δ_st - k_d × (r - r_ref)  # r 为实际横摆角速度
```

**Step 4：转角限幅**
```
δ_final = clip(δ, -δ_max, δ_max)
```

### 参数含义

| 参数 | 含义 | 典型值 | 调参方向 |
|------|------|--------|----------|
| k_e | 横向误差增益 | 0.6 | 增大→纠偏更激进，可能振荡 |
| k_s | 低速软化系数 | 1.0 m/s | 增大→低速更平滑 |
| k_d | 阻尼增益 | 0.10 s | 增大→抑制振荡更强，响应变慢 |
| δ_max | 最大转角 | 40° | 取决于机械结构 |

---

## 4. 代码逐行对照

```python
import numpy as np

class StanleyDamped:
    def __init__(self, k_e=0.6, k_s=1.0, k_d=0.10,
                 delta_max=np.deg2rad(40.0)):
        self.k_e = k_e          # 横向误差增益
        self.k_s = k_s          # 低速软化系数 (m/s)
        self.k_d = k_d          # 阻尼增益 (s)
        self.delta_max = delta_max

    def _wrap(self, angle):
        # 角度归一化到 [-π, π]
        return (angle + np.pi) % (2 * np.pi) - np.pi

    def steer(self, x, y, yaw, v, r, path):
        # 1) 搜索最近路径点（最近邻）
        dx = np.asarray(path['x']) - x
        dy = np.asarray(path['y']) - y
        idx = int(np.argmin(dx**2 + dy**2))

        # 2) 航向误差 = 路径切向角 - 车辆航向角
        theta_e = self._wrap(path['yaw'][idx] - yaw)

        # 3) 横向误差: 前轴到路径的垂距（左为正）
        e = -dx[idx] * np.sin(yaw) + dy[idx] * np.cos(yaw)

        # 4) Stanley 主项（含低速软化）
        v_eff = abs(v) + self.k_s
        delta_st = theta_e + np.arctan2(self.k_e * e, v_eff)

        # 5) 阻尼项: 基于横摆角速度偏差
        r_ref = v * path['kappa'][idx]
        delta = delta_st - self.k_d * (r - r_ref)

        # 6) 转角限幅
        return float(np.clip(delta, -self.delta_max, self.delta_max))
```

### 代码 → 公式 对照表

| 代码行 | 对应公式 |
|--------|----------|
| `idx = argmin(dx²+dy²)` | 最近路径点搜索 |
| `theta_e = _wrap(path['yaw'][idx] - yaw)` | θ_e = Wrap(θ_path - θ_vehicle) |
| `e = -dx*sin(yaw) + dy*cos(yaw)` | 横向误差投影 |
| `v_eff = abs(v) + k_s` | v_eff = |v| + k_s |
| `delta_st = theta_e + arctan2(k_e*e, v_eff)` | δ_st = θ_e + arctan(k_e·e / v_eff) |
| `r_ref = v * kappa[idx]` | r_ref = v × κ |
| `delta = delta_st - k_d*(r - r_ref)` | δ = δ_st - k_d·(r - r_ref) |
| `clip(delta, -δ_max, δ_max)` | 转角限幅 |

---

## 5. Stanley 的优劣势

| 维度 | 评价 |
|------|------|
| 优点 | 结构直观、计算量小、适合嵌入式实时控制 |
| 优点 | 低速到中速场景表现良好 |
| 局限 | 忽略车辆动力学（轮胎侧偏角），高速/大曲率时跟踪误差大 |
| 局限 | 纯几何方法，无法处理动态障碍物避让 |
| 改进方向 | 结合 MPC（模型预测控制）处理约束和预测 |

---

## 🎯 课后练习

1. 手算：给定 θ_e=5°, e=0.3m, v=2m/s, k_e=0.6, k_s=1.0，求 δ_st。
2. 思考：如果 k_e 设得非常大（如 10），车辆行为会怎样？为什么？
3. 对比：PID 横向控制 vs Stanley，各有什么优劣？

---

## 本讲小结

| 概念 | 要点 |
|------|------|
| 航向误差 | 路径切线角 - 车辆航向角，需归一化 |
| 横向误差 | 前轴到路径的垂直距离，左正右负 |
| Stanley 主项 | 航向修正 + arctan 横向修正 |
| 低速软化 | 加 k_s 防止 v=0 除零 |
| 阻尼项 | 用横摆角速度偏差抑制振荡 |
| 转角限幅 | clip 到机械允许范围 |
