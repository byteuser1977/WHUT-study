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
