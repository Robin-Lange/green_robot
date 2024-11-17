import os

from ament_index_python.packages import get_package_share_directory

from launch.actions import DeclareLaunchArgument
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from nav2_common.launch import HasNodeParams
from launch_ros.actions import Node
import launch_ros
import launch
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import LifecycleNode
from launch_ros.actions import Node
from launch.actions import SetEnvironmentVariable
from pathlib import Path
from launch.actions import TimerAction

def generate_launch_description():
    package_name='eagle_bot'
    arg = SetEnvironmentVariable('RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1')
    pkg_share = launch_ros.substitutions.FindPackageShare(package=package_name).find(package_name)
    default_rviz_config_path = os.path.join(pkg_share, 'config/nav2_default_view.rviz')


    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    rplidar_launch = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rplidar.launch.py'
                )]),
    )

    rs_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py'
        )]),
        launch_arguments={'pointcloud.enable': 'true', 'align_depth' : 'true'}.items()
    )

    robot_localization_node = launch_ros.actions.Node(
       package='robot_localization',
       executable='ekf_node',
       name='ekf_filter_node',
       output='screen',
       parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )


    launch_nav = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','nav_launch.py'
                )]),
    )


    twist_mux_params = os.path.join(get_package_share_directory(package_name),'config','twist_mux.yaml')
    twist_mux = Node(
            package="twist_mux",
            executable="twist_mux",
            parameters=[twist_mux_params],
            remappings=[('/cmd_vel_out','/diff_controller/cmd_vel_unstamped')]
        )

    ros2control_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory("eagle_bot"),'launch','controller.launch.py'
                )]),
    )
    
    delay_action = TimerAction(
        period= 3.5,  # Adjust the delay time as needed (e.g., 5 seconds)
        actions=[
        #robot_localization_node,
        #launch_nav,
        #params_declare,
        ros2control_launch,
        #driver_node,
        #xsens_mti_node,
        ]  # Specify the action(s) to execute after the delay
    )
    # Launch them all!
    return LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='false',
                                            description='Flag to enable use_sim_time'),
        rsp,
        rplidar_launch,
        #rs_launch,
        twist_mux,
        delay_action,





    ])
