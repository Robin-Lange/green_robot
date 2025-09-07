"""
This launch file is used to launch both the localization and navigation stacks.

It serves as a top-level launch file to bring up the entire navigation system,
including localization (AMCL and map server), the Nav2 planner and controller
servers, and RViz for visualization.
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
import launch
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from nav2_common.launch import HasNodeParams
import launch_ros


def generate_launch_description():
    """
    Generates the launch description for the combined localization and navigation system.

    This function includes the individual launch files for localization and navigation,
    and also starts RViz with a default configuration.

    Returns:
        LaunchDescription: The launch description object.
    """
    package_name = "eagle_bot"
    pkg_share = launch_ros.substitutions.FindPackageShare(package=package_name).find(
        package_name
    )
    nav2_dir = get_package_share_directory("nav2_bringup")
    params_file = os.path.join(
        pkg_share, "config/mapper_params_online_async_localization.yaml"
    )
    default_params_file = os.path.join(
        get_package_share_directory(package_name),
        "config",
        "mapper_params_online_async_localization.yaml",
    )
    default_rviz_config_path = os.path.join(pkg_share, "config/nav2_default_view.rviz")
    declare_params_file_cmd = DeclareLaunchArgument(
        "params_file",
        default_value=default_params_file,
        description="src/mapper_params_online_async_localization.yaml",
    )

    has_node_params = HasNodeParams(source_file=params_file, node_name="slam_toolbox")

    actual_params_file = PythonExpression(
        [
            '"',
            params_file,
            '" if ',
            has_node_params,
            ' else "',
            default_params_file,
            '"',
        ]
    )

    start_async_slam_toolbox_node = Node(
        parameters=[
            actual_params_file,
            {"use_sim_time": False},  # Set use_sim_time parameter
        ],
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="slam_toolbox",
        output="screen",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", LaunchConfiguration("rvizconfig")],
    )

    launch_localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory(package_name),
                    "launch",
                    "localization.launch.py",
                )
            ]
        ),
    )

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_dir, "launch", "navigation_launch.py")
        ),
        launch_arguments={
            "use_sim_time": "false",
            "map_subscribe_transient_local": "true",
        }.items(),  # Pass use_sim_time as an argument
    )

    return LaunchDescription(
        [
            # start_async_slam_toolbox_node,
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use sim time if true",
            ),
            launch.actions.DeclareLaunchArgument(
                name="rvizconfig",
                default_value=default_rviz_config_path,
                description="Absolute path to rviz config file",
            ),
            launch_localization,
            nav2_launch,
            declare_params_file_cmd,
            rviz_node,
        ]
    )
