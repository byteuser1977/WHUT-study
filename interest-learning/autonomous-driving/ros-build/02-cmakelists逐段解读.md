# 第02讲：CMakeLists.txt 逐段解读（正文约6分钟 + 练习约4分钟）

> 上一讲说了 C++ 包必须有 [CMakeLists.txt](01-功能包与构建系统.md)。这一讲逐行看它。

## 你将学到
- 一个最小可用 CMakeLists.txt 的完整样子
- 每一行管什么、少一行会怎样
- 六个必备件，和必须待在最后一行的话

---

## 1. 先看全貌

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

install(TARGETS talker DESTINATION lib/${PROJECT_NAME})

ament_package()
```

## 2. 逐行在干什么

| 这一行 | 作用 | 漏了会怎样 |
|---|---|---|
| `cmake_minimum_required(VERSION 3.8)` | 声明最低 CMake 版本 | 老版本报语法错 |
| `project(my_pkg)` | 定包名，生成变量 `${PROJECT_NAME}` | 用到它的地方全是空 |
| `if(...) add_compile_options(...)` | 只在 GCC/Clang 下开严格警告 | 不影响功能，只是少提醒 |
| `find_package(ament_cmake REQUIRED)` | 引入 ROS 的构建宏 | `ament_*` 命令全成「未知命令」 |
| `find_package(rclcpp/std_msgs REQUIRED)` | 找到依赖的头文件与链接库 | 报「找不到头文件」 |
| `add_executable(talker src/talker.cpp)` | 声明 `talker` 目标和源码 | 没有目标可编译、可安装 |
| `ament_target_dependencies(...)` | 把依赖挂到 `talker` 上 | 链接期报 `undefined reference` |
| `install(TARGETS ... DESTINATION lib/${PROJECT_NAME})` | 把产物装进 `lib/my_pkg/` | `ros2 run` 找不到可执行文件 |
| `ament_package()` | 注册进 ament 索引并生成 CMake 配置 | `ros2 pkg list` 里看不到它 |

## 3. 六个必备件 + 一条铁律

缺一不可的六个：`cmake_minimum_required`、`project`、`find_package(ament_cmake REQUIRED)`、`add_executable`（或 `add_library`）、`ament_target_dependencies`（或 `target_link_libraries`）、`install(... DESTINATION lib/${PROJECT_NAME})`。

**铁律：`ament_package()` 必须写在最后一行。** 写在中间，排在它后面的 `install()` 就不生效了。

> 💡 类比：CMakeLists.txt 像一张装修施工单——先定标准，再写户主是谁，然后订货、干活、验收，最后**盖章备案**。章盖在半截，房子就住不进去：`ros2` 不认这个包。

## 4. 三种最常见的翻车

> ⚠️ 常见坑：**忘了 `ament_package()`** → 编译不报错，但包从 `ros2 pkg list` 消失；**`install` 目标漏了** → 产物只躺在 `build/` 里，运行时提示「找不到可执行文件」；**`package.xml` 没声明依赖却 `find_package` 了** → 本机编译能过，装到别的机器就失败。

---

## 🎯 课后练习（约4分钟）

那句「忘了 `ament_package()` 包就不被识别」，能在系统里看到证据：

```bash
# 被 ROS 认出来的包，都在这份名册里有登记
ls /opt/ros/humble/share/ament_index/resource_index/packages/ | head -n 5
```

> ✅ 你应该看到：一串包名，和 `ros2 pkg list` 出来的基本对应——这名册正是 `ament_package()` 登记的。

---

## 本讲小结

| 要点 | 说明 |
|---|---|
| 三件事 | `find_package` 找依赖 → `add_executable` 声明目标 → `install` 装产物 |
| 六个必备件 | 见第 3 节；后两项也可写成 `add_library` / `target_link_libraries` |
| 铁律 | `ament_package()` 必须是最后一行，否则包不被识别 |
| 两份清单对齐 | `find_package` 的包，`package.xml` 里也要有对应声明 |
