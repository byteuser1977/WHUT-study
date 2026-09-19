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
