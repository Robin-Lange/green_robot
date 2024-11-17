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


def generate_launch_description():
    package_name='eagle_bot'
    arg = SetEnvironmentVariable('RCUTILS_CONSOLE_STDOUT_LINE_BUFFERED', '1')
    pkg_share = launch_ros.substitutions.FindPackageShare(package=package_name).find(package_name)


    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'false'}.items()
    )

    
    robot_localization_node = launch_ros.actions.Node(
       package='robot_localization',
       executable='ekf_node',
       name='ekf_filter_node',
       output='screen',
       parameters=[os.path.join(pkg_share, 'config/ekf.yaml'), {'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    parameters_file_path = Path(get_package_share_directory('bluespace_ai_xsens_mti_driver'), 'param', 'xsens_mti_node.yaml')
    xsens_mti_node = Node(
            package='bluespace_ai_xsens_mti_driver',
            executable='xsens_mti_node',
            name='xsens_mti_node',
            output='screen',
            parameters=[parameters_file_path],
            arguments=[]
            )
    ros2control_launch = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory("diff_controller"),'launch','diffbot_system.launch.py'
                )]),
    )
    # Launch them all!
    return LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='false',
                                            description='Flag to enable use_sim_time'),
        rsp,
        robot_localization_node,
        xsens_mti_node,





    ])
