#!/bin/bash
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
