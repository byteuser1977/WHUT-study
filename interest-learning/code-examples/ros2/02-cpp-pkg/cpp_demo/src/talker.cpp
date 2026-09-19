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
