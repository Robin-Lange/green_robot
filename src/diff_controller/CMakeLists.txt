cmake_minimum_required(VERSION 3.16)
project(diff_controller LANGUAGES CXX)

if(CMAKE_CXX_COMPILER_ID MATCHES "(GNU|Clang)")
  add_compile_options(-Wall -Wextra)
endif()

# find dependencies
set(THIS_PACKAGE_INCLUDE_DEPENDS
  hardware_interface
  pluginlib
  rclcpp
  rclcpp_lifecycle
)

# find dependencies
find_package(ament_cmake REQUIRED)
foreach(Dependency IN ITEMS ${THIS_PACKAGE_INCLUDE_DEPENDS})
  find_package(${Dependency} REQUIRED)
endforeach()


## COMPILE
add_library(
  diff_controller
  SHARED
  hardware/src/diffbot_system.cpp
)
target_compile_features(diff_controller PUBLIC cxx_std_17)
target_include_directories(diff_controller PUBLIC
$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/hardware/include>
$<INSTALL_INTERFACE:include/diff_controller>
)
ament_target_dependencies(
  diff_controller PUBLIC
  ${THIS_PACKAGE_INCLUDE_DEPENDS}
)

target_link_libraries(diff_controller PUBLIC serial)

# Causes the visibility macros to use dllexport rather than dllimport,
# which is appropriate when building the dll but not consuming it.
target_compile_definitions(${PROJECT_NAME} PRIVATE "diff_controller_BUILDING_DLL")


# Export hardware plugins
pluginlib_export_plugin_description_file(hardware_interface diff_controller.xml)

# INSTALL
install(
  DIRECTORY hardware/include/
  DESTINATION include/diff_controller
)
install(
  DIRECTORY description/config description/ros2_control description/urdf description/gazebo
  DESTINATION share/diff_controller
)
install(
  DIRECTORY bringup/launch bringup/config
  DESTINATION share/diff_controller
)
install(TARGETS diff_controller
  EXPORT export_diff_controller
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)
endif()

## EXPORTS
ament_export_targets(export_diff_controller HAS_LIBRARY_TARGET)
ament_export_dependencies(${THIS_PACKAGE_INCLUDE_DEPENDS})
ament_package()
