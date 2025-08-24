"""
This launch file serves as the main entry point for launching the core components of the Eagle Bot.

It brings up the following main components:
1. Robot State Publisher (rsp.launch.py): Publishes the robot's state (TF tree) based on its URDF.
2. RPLIDAR (rplidar.launch.py): Launches the driver for the RPLIDAR sensor.
3. Twist Mux: Multiplexes different velocity command topics into one.
4. ROS2 Control (controller.launch.py): Launches the hardware controllers for the differential drive base.
   This is launched after a short delay to ensure hardware is ready.
"""

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription,
                            SetEnvironmentVariable, TimerAction)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
import launch_ros.substitutions

def generate_launch_description():
    """Generates the launch description for the Eagle Bot."""

    package_name = "eagle_bot"
    pkg_share = launch_ros.substitutions.FindPackageShare(package=package_name).find(package_name)

    # --- General Arguments and Configurations ---

    # Set environment variable for unbuffered console output
    SetEnvironmentVariable("RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED", "1")

    # Declare launch arguments
    default_rviz_config_path = os.path.join(pkg_share, "config/nav2_default_view.rviz")
    use_sim_time = LaunchConfiguration("use_sim_time", default="false")

    # --- Node and Launch File Definitions ---

    # 1. Robot State Publisher
    # Publishes the TF transformations for the robot based on the URDF model.
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory(package_name), "launch", "rsp.launch.py")
        ),
        launch_arguments={"use_sim_time": use_sim_time, "use_ros2_control": "true"}.items(),
    )

    # 2. RPLIDAR Driver
    # Launches the node for the RPLIDAR laser scanner.
    rplidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory(package_name), "launch", "rplidar.launch.py")
        )
    )

    # 3. Twist Mux (Velocity Command Multiplexer)
    # This node takes velocity commands from multiple sources (e.g., teleop, nav2)
    # and arbitrates between them, sending a single command to the robot controller.
    twist_mux_params = os.path.join(pkg_share, "config", "twist_mux.yaml")
    twist_mux = Node(
        package="twist_mux",
        executable="twist_mux",
        parameters=[twist_mux_params],
        remappings=[("/cmd_vel_out", "/diff_controller/cmd_vel_unstamped")],
    )

    # 4. ROS2 Control for Hardware
    # Launches the differential drive controller and joint state broadcaster.
    ros2control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("eagle_bot"), "launch", "controller.launch.py")
        )
    )

    # --- Delayed Launch ---
    # The TimerAction introduces a delay before launching certain nodes.
    # This is often necessary to give hardware interfaces time to initialize properly.
    delay_action = TimerAction(
        period=3.5,
        actions=[
            ros2control_launch,
        ],
    )

    # --- LaunchDescription Assembly ---
    # Assemble all the components into the final launch description.
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "rvizconfig",
                default_value=default_rviz_config_path,
                description="Absolute path to RViz config file",
            ),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Flag to enable use_sim_time",
            ),

            # Launch core components
            rsp,
            rplidar_launch,
            twist_mux,

            # Launch delayed components
            delay_action,
        ]
    )
