#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROS 2 Python 包：最小发布者 + 订阅者 + launch 文件
对应教程：interest-learning/perception/ros2/05-写第一个节点.md
"""

import os

# ============================================================
# 1. talker.py - 最小发布者
# 放在: ~/ros2_ws/src/perception_demo/perception_demo/talker.py
# ============================================================
TALKER_PY = '''
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalPublisher(Node):
    """最小发布者：每 0.5 秒往话题 /perception_hello 发一条字符串"""

    def __init__(self):
        super().__init__('minimal_publisher')          # ① 节点名，全局唯一
        self.publisher_ = self.create_publisher(
            String,            # ② 消息类型
            'perception_hello',  # ③ 话题名（不带 / 会自动补成 /perception_hello）
            10)                # ④ 发送队列长度
        self.timer = self.create_timer(0.5, self.timer_callback)  # 每 0.5s 触发一次 ≈ 2 Hz
        self.count = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'第 {self.count} 帧 / hello from perception'
        self.publisher_.publish(msg)                     # 发出去
        self.get_logger().info(f'发布: "{msg.data}"')     # 打印，方便肉眼确认
        self.count += 1


def main(args=None):
    rclpy.init(args=args)          # 初始化（搭好 DDS 环境）
    node = MinimalPublisher()      # 创建节点
    try:
        rclpy.spin(node)           # 一直"转"，处理回调，直到 Ctrl+C
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()        # 销毁节点
        rclpy.shutdown()           # 清理


if __name__ == '__main__':
    main()
'''

# ============================================================
# 2. listener.py - 最小订阅者
# 放在: ~/ros2_ws/src/perception_demo/perception_demo/listener.py
# ============================================================
LISTENER_PY = '''
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MinimalSubscriber(Node):
    """最小订阅者：每收到一条 /perception_hello 就打印一次"""

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,                 # 类型必须和发布者一致
            'perception_hello',     # 话题名必须完全一致
            self.listener_callback,  # 收到消息时调用的函数
            10)
        self.count = 0

    def listener_callback(self, msg):
        self.count += 1
        self.get_logger().info(f'收到第 {self.count} 条: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
'''

# ============================================================
# 3. setup.py - 注册可执行文件（Python 包必须）
# 放在: ~/ros2_ws/src/perception_demo/setup.py
# ============================================================
SETUP_PY = '''
from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'perception_demo'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='you',
    maintainer_email='you@example.com',
    description='感知组入门示例：最小发布者与订阅者',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'talker = perception_demo.talker:main',
            'listener = perception_demo.listener:main',
        ],
    },
)
'''

# ============================================================
# 4. package.xml - 依赖声明
# 放在: ~/ros2_ws/src/perception_demo/package.xml
# ============================================================
PACKAGE_XML = '''<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>perception_demo</name>
  <version>0.1.0</version>
  <description>感知组入门示例：最小发布者与订阅者</description>
  <maintainer email="you@example.com">you</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_python</buildtool_depend>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
'''

# ============================================================
# 5. launch/demo.launch.py - 一键启动多节点
# 放在: ~/ros2_ws/src/perception_demo/launch/demo.launch.py
# ============================================================
LAUNCH_PY = '''
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='perception_demo',
            executable='talker',      # 对应 setup.py 里 entry_points 的名字
            name='talker_node',       # 重命名节点（可选）
            output='screen',          # 日志打在屏幕上
        ),
        Node(
            package='perception_demo',
            executable='listener',
            name='listener_node',
            output='screen',
        ),
    ])
'''

# ============================================================
# 6. 完整构建运行脚本
# ============================================================
BUILD_RUN_SH = '''#!/bin/bash
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
'''

# ============================================================
# 7. 进阶挑战：模拟 30 FPS 相机
# ============================================================
ADVANCED_TALKER = '''
# 进阶挑战：把定时器改成 30 FPS
# self.create_timer(1/30, self.timer_callback)  # 模拟 30 FPS 相机

# 重新启动节点，再用 ros2 topic hz perception_hello 验证是不是约 30 Hz
# 你会亲眼看到"算法帧率"和"实测帧率"的关系——这正是感知组每天要盯的数字
'''


def write_files():
    """将所有文件写入对应目录"""
    base = "/mnt/d/workspace/git/WHUT-study/interest-learning/code-examples/ros2/01-python-pkg/perception_demo"
    
    dirs = [
        f"{base}/perception_demo",
        f"{base}/launch",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    files = {
        f"{base}/perception_demo/talker.py": TALKER_PY,
        f"{base}/perception_demo/listener.py": LISTENER_PY,
        f"{base}/setup.py": SETUP_PY,
        f"{base}/package.xml": PACKAGE_XML,
        f"{base}/launch/demo.launch.py": LAUNCH_PY,
        f"{base}/build_run.sh": BUILD_RUN_SH,
    }
    
    for path, content in files.items():
        with open(path, 'w') as f:
            f.write(content.strip() + '\n')
    
    print(f"已写入 {len(files)} 个文件到 {base}")


if __name__ == "__main__":
    write_files()
    
    print("""
=== ROS 2 Python 包完整示例 ===

目录结构：
perception_demo/
├── package.xml
├── setup.py
├── launch/
│   └── demo.launch.py
└── perception_demo/
    ├── __init__.py
    ├── talker.py
    └── listener.py

快速开始：
1. cd ~/ros2_ws/src
2. 复制上述文件到对应位置
3. cd ~/ros2_ws && colcon build --symlink-install && source install/setup.bash
4. 终端1: ros2 run perception_demo talker
   终端2: ros2 run perception_demo listener
5. 或一键: ros2 launch perception_demo demo.launch.py

关键点：
- Python 包用 ament_python，必须有 setup.py（C++ 包用 CMakeLists.txt）
- entry_points 里登记 "名字 = 包.文件:main"
- 发布者/订阅者的 "话题名 + 消息类型" 必须完全一致
- rclpy.spin() 是让节点活着的关键，没有它节点瞬间退出
- --symlink-install 让改 Python 代码后直接重启节点生效，不用重编译
- 每个新终端都要 source install/setup.bash
""")