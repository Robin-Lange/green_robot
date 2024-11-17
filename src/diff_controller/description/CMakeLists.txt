cmake_minimum_required(VERSION 3.5)
project(diff_controller)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config gazebo launch ros2_control urdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
