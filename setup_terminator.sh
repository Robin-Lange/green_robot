
#This script is used to setup Terminator with multiple tabs and commands for ROS 2.
#It will start the following in separate tabs:
#    1. Eagle Launch
#    2. Navigation Launch
#    3. RPLidar Launch
#    4. Keyboard Control
#    5. ROS Bag Record
#
#To run this script, you need to make it executable first:
#    chmod +x setup_terminator.sh
#Then, you can run it in the green_robot folder:
#    ./setup_terminator.sh

# Source ROS 2 setup
source /opt/ros/galactic/setup.bash

# Build the workspace
colcon build --symlink-install

# Source the workspaces
source install/setup.bash

# Start Terminator with multiple tabs and commands
ros2 launch  eagle_bot eagle.launch.py


#Manual control
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_controller/cmd_vel_unstamped



#Autonomous with existing map
ros2 launch eagle_bot localization_nav.launch.py



#Unknown area
ros2 launch eagle_bot nav_launch.py

ros2 run nav2_map_server map_saver_cli -f ~/map

