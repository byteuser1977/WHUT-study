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
