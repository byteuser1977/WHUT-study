cmake_minimum_required(VERSION 3.8)
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
