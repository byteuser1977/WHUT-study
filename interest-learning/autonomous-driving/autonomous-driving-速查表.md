# 无人组速查表

> 一页速查。想细看每一行背后的道理，点对应的讲次。

## 一、排序算法速查

| 算法 | 平均 | 最坏 | 额外空间 | 稳定 | 一句话 |
|---|---|---|---|---|---|
| 冒泡 | O(n²) | O(n²) | O(1) | ✅ 稳定 | 相邻两两比，大的往后冒 |
| 选择 | O(n²) | O(n²) | O(1) | ❌ 不稳定 | 每轮选最小放到前面 |
| 插入 | O(n²) | O(n²) | O(1) | ✅ 稳定 | 像理牌，把新牌插进已排好的部分 |
| 快速排序 | O(n log n) | **O(n²)** | O(log n) 递归栈 | ❌ 不稳定 | 按基准分区，两边各自递归 |
| 归并排序 | O(n log n) | O(n log n) | **O(n)** | ✅ 稳定 | 折半递归，再线性合并两个有序段 |

**不稳定指的是**：相等元素在排序后相对次序可能被打乱。
**快排最坏 O(n²) 的触发**：输入已有序 + 基准取首元素 → 每次分区都歪向一边，递归退化成链（实测 n=1000 已有序时甚至会 `RecursionError`）。用随机基准或三数取中可避开。

## 二、五个算法的代码骨架

```python
def bubble(a):
    for i in range(len(a) - 1):
        for j in range(len(a) - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def selection(a):
    for i in range(len(a)):
        k = i
        for j in range(i + 1, len(a)):
            if a[j] < a[k]:
                k = j
        a[i], a[k] = a[k], a[i]
    return a

def insertion(a):
    for i in range(1, len(a)):
        cur, j = a[i], i - 1
        while j >= 0 and a[j] > cur:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = cur
    return a
```

```python
def quick(a):
    if len(a) <= 1:
        return a
    pivot = a[0]                      # 已有序输入时这里最坏
    left  = [x for x in a[1:] if x <= pivot]
    right = [x for x in a[1:] if x > pivot]
    return quick(left) + [pivot] + quick(right)

def merge_sort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left, right = merge_sort(a[:mid]), merge_sort(a[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:       # <= 保证稳定
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    return out + left[i:] + right[j:]
```

## 三、实战怎么选

| 场景 | 用什么 | 为什么 |
|---|---|---|
| Python 里排序 | `sorted(a)` / `a.sort()` | 底层 **Timsort**（归并 + 插入混合，稳定）；对部分有序数据接近 O(n) |
| C++ 里排序 | `std::sort` | 底层**内省排序 introsort**（快排 + 堆排 + 插入），**不稳定** |
| C++ 且要求稳定 | `std::stable_sort` | 代价是额外空间 |
| 内存很紧 | `std::sort` 或堆排 | 原地排序，额外空间 O(1)~O(log n) |
| 数据量很小（几十个） | 插入排序 | 常数小，比快排还快 |

**结论：实战优先用语言自带排序。** 手写算法是为了理解原理、应对特殊约束（比如要自定义比较、要可复现的最坏情况保证）。

## 四、ROS 2 功能包长什么样

```
my_pkg/
├── package.xml            ← 包的"身份证"：包名、版本、依赖声明
├── CMakeLists.txt         ← C++ 包才有；Python 包换成 setup.py
├── src/                   ← C++ 源码（本教程用这个）
│   └── talker.cpp
├── include/my_pkg/        ← 对外暴露的头文件
├── launch/                ← 启动文件
└── config/                ← 参数文件
```

| 包类型 | 构建类型 | 需要哪些文件 |
|---|---|---|
| C++ 包 | `ament_cmake` | `CMakeLists.txt` + `package.xml`，**不需要 setup.py** |
| Python 包 | `ament_python` | `setup.py` + `package.xml`，**不需要 CMakeLists.txt** |

> 感知组的 ROS 2 五讲讲的是 Python 包（`setup.py`），本教程模块二补 C++ 包这一半。见 [../perception/ros2/05-写第一个节点.md](../perception/ros2/05-写第一个节点.md)。

## 五、最小可用 CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(talker src/talker.cpp)
ament_target_dependencies(talker rclcpp std_msgs)
# 或用原生 CMake 写法：target_link_libraries(talker ${rclcpp_TARGETS} ...)

install(TARGETS talker DESTINATION lib/${PROJECT_NAME})

ament_package()          # ★ 必须在最后一行
```

## 六、六个必备件与三个坑

| 必备件 | 作用 | 漏了会怎样 |
|---|---|---|
| `cmake_minimum_required(VERSION 3.8)` | 声明最低 CMake 版本 | 老版本报语法错 |
| `project(my_pkg)` | 定包名，生成 `${PROJECT_NAME}` | 用到它的地方全是空 |
| `find_package(ament_cmake REQUIRED)` | 引入 ROS 构建宏 | `ament_*` 命令全成「未知命令」 |
| `add_executable(目标 源文件)` | 声明目标和源码 | 没有东西可编译、可安装 |
| `ament_target_dependencies(...)` | 把依赖挂到目标上 | 链接期报 `undefined reference` |
| `install(TARGETS ... DESTINATION lib/${PROJECT_NAME})` | 把产物装进 `lib/包名/` | `ros2 run` 找不到可执行文件 |

| 坑 | 现象 |
|---|---|
| 忘了 `ament_package()` | 编译不报错，但包从 `ros2 pkg list` 消失 |
| `install` 目标漏了 | 产物只在 `build/` 里，运行时提示「找不到可执行文件」 |
| `package.xml` 没声明依赖却 `find_package` | 本机编译能过，换台机器就失败 |

**铁律**：`ament_package()` 必须写在最后一行；写在中间，排在它后面的 `install()` 就不生效。

## 七、colcon 命令速查

```bash
colcon build                            # 编工作空间下所有包
colcon build --packages-select my_pkg   # 只编一个包（改了单个包时用）
source install/setup.bash               # 让当前终端认得新编出来的包（每个新终端都要）
ros2 pkg list                           # 看系统认出了哪些包
ros2 pkg executables my_pkg             # 看某个包提供哪些可执行文件
ros2 run my_pkg talker                  # 运行
```

> 环境变量只在当前终端生效。想每个新终端都自动生效，把它加进 `~/.bashrc`。

## 八、自动驾驶数据流速查

```
传感器（相机 / 激光雷达 / 毫米波 / IMU / GNSS / 轮速）
        ↓ 原始数据                              10~30 Hz
感知：检测 + 分割 + 跟踪 + 定位
        ↓ 障碍物列表 + 可行驶区域 + 自车位姿      10~20 Hz
预测：其他交通参与者未来轨迹
        ↓ 预测轨迹                              5~10 Hz
规划：全局路径 → 局部轨迹（避障 + 速度剖面）
        ↓ 轨迹（位姿 + 速度 + 时间戳）            10 Hz
控制：横向（转向）+ 纵向（驱动 / 制动）
        ↓ 转角 / 扭矩 / 制动请求                50~100 Hz
执行器：EPS / EHB / 电机控制器 / VCU
```

| 环节 | 输入 | 输出 |
|---|---|---|
| 感知 | 原始数据 + 标定参数 | 障碍物列表（位置/速度/尺寸/类别/置信度）、可行驶区域、自车位姿 |
| 预测 | 障碍物列表 + 自车位姿 + 地图 | 每个动态目标各自的未来轨迹 |
| 规划 | 预测轨迹 + 地图 + 任务目标 | 局部轨迹（位姿 + 速度 + 时间戳） |
| 控制 | 局部轨迹 + 车辆反馈（车速、转角） | 转角、扭矩、制动请求 |

**一条链路走到底的例子**：感知把 15 m 外锥桶列入障碍物列表 → 预测判定它静止 → 规划抬高该区域代价并降低目标速度 → 控制解算出新的转向角与扭矩指令。

## 九、感知误检应对速查

**先记代价不对称**：误检（假阳性）让车变慢，漏检（假阴性）让车撞上。两者不对称，所以策略整体偏保守。

| 层次 | 策略 |
|---|---|
| 感知端 | 多传感器交叉验证（视觉 + 激光雷达 + 毫米波互证）；连续 N 帧确认；输出置信度与不确定性 |
| 规划端 | 判定不了就按真障碍物保守处理；做代价分级而非 0/1 判断；保留紧急重规划通道与可行驶区域约束 |
| 控制端 | 对规划指令限幅与平滑；留紧急制动兜底 |
| 系统级 | 失效降级（降速/靠边/进安全状态）；遥控接管；黑盒日志与场景回放 |

> ⚠️ 「保守」不等于「不动」。一味保守车会动弹不得；正路是用多帧确认 + 多源校验把误报率压下来，而不是调低灵敏度、放弃检测。

## 十、缩写速查

| 缩写 | 全称 | 中文 |
|---|---|---|
| ROS 2 | Robot Operating System 2 | 机器人操作系统（第二代） |
| CMake | — | 跨平台构建系统 |
| colcon | — | ROS 2 的构建工具 |
| ament | — | ROS 2 的构建系统基础 |
| CAN | Controller Area Network | 控制器局域网 |
| VCU | Vehicle Control Unit | 整车控制器 |
| EPS | Electric Power Steering | 电动助力转向 |
| EHB | Electro-Hydraulic Brake | 电液制动 |
| IMU | Inertial Measurement Unit | 惯性测量单元 |
| GNSS | Global Navigation Satellite System | 全球导航卫星系统 |
| DBC | Database CAN | 描述 CAN 报文与信号的文件格式 |
| Timsort | — | Python 内置排序算法（归并 + 插入混合） |
| introsort | — | C++ `std::sort` 的内省排序（快排 + 堆排 + 插入） |

## 十一、五个算法一句话记忆

| 算法 | 记忆点 |
|---|---|
| 冒泡 | 相邻交换，一轮冒一个最大值到末尾 |
| 选择 | 每轮扫一遍选出最小，放到已排好的末尾 |
| 插入 | 像理牌：左手已排好，右手抽一张插进去 |
| 快速 | 选基准分两堆，两堆各自递归；**平均快、最坏慢** |
| 归并 | 先折半到只剩一个，再两两合并；**稳定但要多一份空间** |
