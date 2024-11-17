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

def generate_launch_description():
    package_name='eagle_bot'
    
    pkg_share = launch_ros.substitutions.FindPackageShare(package=package_name).find(package_name)
    world_path=os.path.join(pkg_share, 'worlds/wr1_world.sdf')
    default_rviz_config_path = os.path.join(pkg_share, 'config/nav2_default_view.rviz')

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'eagle_bot'],
                        output='screen')

    # Launch them all!
    return LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='rvizconfig', default_value=default_rviz_config_path,
                                            description='Absolute path to rviz config file'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                            description='Flag to enable use_sim_time'),
        launch.actions.ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_path], output='screen'),
        rsp,
        spawn_entity,


    ])
