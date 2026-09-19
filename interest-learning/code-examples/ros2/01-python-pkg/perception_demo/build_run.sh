#!/bin/bash
# 完整构建运行流程

# 1. 创建工作空间和功能包
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python perception_demo

# 2. 把 talker.py / listener.py 写进
#    ~/ros2_ws/src/perception_demo/perception_demo/
#    (本文件已包含完整代码，可直接复制)

# 3. 修改 setup.py (加 entry_points 和 launch 目录)
# 4. 修改 package.xml (补 <depend>rclpy</depend> <depend>std_msgs</depend>)

# 5. 编译并 source
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash

# 6. 方式 A：两个终端分别跑
# 终端 1:
ros2 run perception_demo talker
# 终端 2:
ros2 run perception_demo listener

# 7. 验证
ros2 node list                      # 应看到 /minimal_publisher 和 /minimal_subscriber
ros2 topic list -t                  # 应看到 /perception_hello [std_msgs/msg/String]
ros2 topic info /perception_hello -v
ros2 topic hz perception_hello      # 应约 2.000 Hz (对应 0.5s 定时器)
ros2 topic echo /perception_hello --once

# 8. 方式 B：一键启动
ros2 launch perception_demo demo.launch.py
# Ctrl+C 一次全关
