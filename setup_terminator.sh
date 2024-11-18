"""
# Created: 2021-08-17
This script is used to setup Terminator with multiple tabs and commands for ROS 2.
To run this script, you need to make it executable first:
    chmod +x setup_terminator.sh
Then, you can run it:
    ./setup_terminator.sh
"""
# Source ROS 2 setup
source /opt/ros/galactic/setup.bash

# Build the workspace
colcon build --symlink-install

# Source the workspaces
source ./install/setup.bash

# Start Terminator with multiple tabs and commands
terminator -T "Eagle Launch" -e "bash -c 'ros2 launch eagle_bot eagle_launch.py; exec bash'" \
           -T "Navigation Launch" -e "bash -c 'ros2 launch nav2_bringup nav_launch.py; exec bash'" \
           -T "RPLidar Launch" -e "bash -c 'ros2 launch sllidar_ros2 rplidar.launch.py; exec bash'" \
           -T "Keyboard Control" -e "bash -c 'ros2 run teleop_twist_keyboard teleop_twist_keyboard; exec bash'" \
           -T "ROS Bag Record" -e "bash -c 'ros2 bag record /topic1 /topic2; exec bash'"