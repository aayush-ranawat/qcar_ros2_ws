cmake_minimum_required(VERSION 3.8)
project(control_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(OpenCV REQUIRED)

# Add the executable
add_executable(lane_detect_node src/lane_detect_node.cpp)

# Include directories
target_include_directories(lane_detect_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
  ${OpenCV_INCLUDE_DIRS}
)

# Link dependencies
target_link_libraries(lane_detect_node
  ${OpenCV_LIBS}
)
ament_target_dependencies(lane_detect_node
  rclcpp
  sensor_msgs
  cv_bridge
)

# Install the executable
install(TARGETS
  lane_detect_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()