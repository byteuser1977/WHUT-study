#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROS 2 C++ 包：最小发布者 + CMakeLists.txt 详解
对应教程：interest-learning/autonomous-driving/ros-build/01-功能包与构建系统.md
          interest-learning/autonomous-driving/ros-build/02-cmakelists逐段解读.md
          interest-learning/autonomous-driving/ros-build/03-动手编译一个包.md
"""

import os

# ============================================================
# 1. talker.cpp - 最小 C++ 发布者
# 放在: ~/ros2_ws/src/cpp_demo/src/talker.cpp
# ============================================================
TALKER_CPP = '''
#include <chrono>
#include <memory>
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

using namespace std::chrono_literals;

int main(int argc, char ** argv) {
  // 1. 初始化 ROS 2
  rclcpp::init(argc, argv);
  
  // 2. 创建节点
  auto node = std::make_shared<rclcpp::Node>("talker");
  
  // 3. 创建发布者：话题 "hello"，队列长度 10
  auto pub = node->create_publisher<std_msgs::msg::String>("hello", 10);
  
  // 4. 创建定时器：每 500ms 触发一次 (2 Hz)
  auto timer = node->create_wall_timer(500ms, [&]{
    auto msg = std_msgs::msg::String();
    msg.data = "hello from cpp";
    pub->publish(msg);
  });
  
  // 5. 进入事件循环
  rclcpp::spin(node);
  
  // 6. 清理
  rclcpp::shutdown();
  return 0;
}
'''

# ============================================================
# 2. CMakeLists.txt - 逐行详解版
# 放在: ~/ros2_ws/src/cpp_demo/CMakeLists.txt
# ============================================================
CMAKELISTS_TXT = '''cmake_minimum_required(VERSION 3.8)
project(cpp_demo)

# 只有 GCC/Clang 下开启严格警告，不影响功能
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ===== 必备件 1：引入 ROS 2 构建宏 =====
find_package(ament_cmake REQUIRED)

# ===== 必备件 2：找到依赖的包（头文件+链接库）=====
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# ===== 必备件 3：声明可执行目标 + 源文件 =====
add_executable(talker src/talker.cpp)

# ===== 必备件 4：把依赖挂到目标上 =====
ament_target_dependencies(talker rclcpp std_msgs)

# ===== 必备件 5：安装产物到 lib/${PROJECT_NAME}/ =====
install(TARGETS talker DESTINATION lib/${PROJECT_NAME})

# ===== 铁律：ament_package() 必须是最后一行！=====
# 写在中间会导致后面的 install() 不生效，包不被识别
ament_package()
'''

# ============================================================
# 3. package.xml - 依赖声明（必须与 CMakeLists.txt 对齐！）
# 放在: ~/ros2_ws/src/cpp_demo/package.xml
# ============================================================
PACKAGE_XML = '''<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>cpp_demo</name>
  <version>0.1.0</version>
  <description>C++ 最小发布者示例</description>
  <maintainer email="you@example.com">you</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>

  <!-- 运行时依赖：必须与 CMakeLists.txt 里的 find_package 对齐 -->
  <depend>rclcpp</depend>
  <depend>std_msgs</depend>

  <test_depend>ament_lint_auto</test_depend>
  <test_depend>ament_lint_common</test_depend>

  <export>
    <build_type>ament_cmake</build_type>
  </export>
</package>
'''

# ============================================================
# 4. 完整构建运行流程
# ============================================================
BUILD_RUN_SH = '''#!/bin/bash
# ROS 2 C++ 包完整构建运行流程

# 1. 创建包骨架
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake cpp_demo

# 2. 写入 talker.cpp 到 src/talker.cpp
# 3. 修改 CMakeLists.txt (加上 find_package, add_executable, ament_target_dependencies, install)
# 4. 修改 package.xml (补 <depend>rclcpp</depend> <depend>std_msgs</depend>)

# 5. 在工作空间根目录编译
cd ~/ros2_ws
colcon build --packages-select cpp_demo    # 只编这个包

# 关键：只有出现 "Summary: 1 package finished" 才算成功
# 看到 Failed 就往上翻报错

# 6. 每个新终端都要 source
source install/setup.bash

# 7. 运行
ros2 run cpp_demo talker

# 8. 另开终端验证
# source install/setup.bash
# ros2 topic hz hello    # 应约 2.000 Hz

# 9. 改代码后必须重新编译 (Python 包加 --symlink-install 可免编译)
# 把 500ms 改成 100ms 重新编译，再看 ros2 topic hz hello 变 10 Hz
'''

# ============================================================
# 5. CMakeLists.txt 六个必备件 + 三种常见翻车
# ============================================================
CMAKE_EXPLANATION = '''
=== CMakeLists.txt 六个必备件 ===

1. cmake_minimum_required(VERSION 3.8)
   - 声明最低 CMake 版本，老版本会报语法错

2. project(cpp_demo)
   - 定包名，生成变量 ${PROJECT_NAME}

3. find_package(ament_cmake REQUIRED)
   - 引入 ROS 的构建宏 (ament_* 命令)

4. find_package(rclcpp REQUIRED) / find_package(std_msgs REQUIRED)
   - 找到依赖的头文件与链接库

5. add_executable(talker src/talker.cpp)
   - 声明 talker 目标和源码

6. ament_target_dependencies(talker rclcpp std_msgs)
   - 把依赖挂到 talker 上 (包含头文件路径、链接库、编译选项)

7. install(TARGETS talker DESTINATION lib/${PROJECT_NAME})
   - 把产物装进 lib/cpp_demo/，供 ros2 run 找到

8. ament_package()  ← 必须是最后一行！
   - 注册进 ament 索引并生成 CMake 配置

=== 三种最常见的翻车 ===

❌ 1. 忘了 ament_package()
   现象：编译不报错，但 ros2 pkg list 里看不到包
   原因：没登记进 ament 索引

❌ 2. install 目标漏了
   现象：产物只躺在 build/ 里，运行时 "找不到可执行文件"
   原因：没装到 install/ 空间

❌ 3. package.xml 没声明依赖却 find_package 了
   现象：本机编译能过，装到别的机器就失败
   原因：rosdep 无法自动安装缺失依赖

=== 验证 ament_package() 的作用 ===
ls /opt/ros/humble/share/ament_index/resource_index/packages/
# 能看到的包名列表，正是 ament_package() 登记的
'''

# ============================================================
# 6. 对比：Python 包 vs C++ 包
# ============================================================
COMPARISON = '''
=== Python 包 vs C++ 包 对比 ===

| 维度           | Python 包 (ament_python)        | C++ 包 (ament_cmake)           |
|----------------|----------------------------------|--------------------------------|
| 构建类型       | ament_python                     | ament_cmake                    |
| 必需文件       | setup.py                         | CMakeLists.txt                 |
| 不需要的文件   | CMakeLists.txt                   | setup.py                       |
| 可执行文件登记 | setup.py 的 entry_points         | CMakeLists.txt 的 add_executable + install |
| 依赖声明       | package.xml + setup.py install_requires | package.xml + find_package |
| 修改代码后     | --symlink-install 直接生效       | 必须重新 colcon build          |
| 编译产物       | Python 字节码 (.pyc)             | 机器码 (.so / 可执行文件)       |
| 适用场景       | 原型开发、非实时、调用 Python 库  | 实时控制、高性能、嵌入式部署    |

=== 目录结构对比 ===

Python 包:
perception_demo/
├── package.xml
├── setup.py
├── resource/perception_demo
├── launch/demo.launch.py
└── perception_demo/
    ├── __init__.py
    ├── talker.py
    └── listener.py

C++ 包:
cpp_demo/
├── package.xml
├── CMakeLists.txt
└── src/
    └── talker.cpp
'''


def write_files():
    """将文件写入对应目录"""
    base = "/mnt/d/workspace/git/WHUT-study/interest-learning/code-examples/ros2/02-cpp-pkg/cpp_demo"
    
    dirs = [
        f"{base}/src",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    files = {
        f"{base}/src/talker.cpp": TALKER_CPP,
        f"{base}/CMakeLists.txt": CMAKELISTS_TXT,
        f"{base}/package.xml": PACKAGE_XML,
        f"{base}/build_run.sh": BUILD_RUN_SH,
    }
    
    for path, content in files.items():
        with open(path, 'w') as f:
            f.write(content.strip() + '\n')
    
    print(f"已写入 {len(files)} 个文件到 {base}")


if __name__ == "__main__":
    write_files()
    
    print(CMAKE_EXPLANATION)
    print(COMPARISON)