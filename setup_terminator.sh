"""
This script is used to setup Terminator with multiple tabs and commands for ROS 2.
It will start the following in separate tabs:
    1. Eagle Launch
    2. Navigation Launch
    3. RPLidar Launch
    4. Keyboard Control
    5. ROS Bag Record

To run this script, you need to make it executable first:
    chmod +x setup_terminator.sh
Then, you can run it in the green_robot folder:
    ./setup_terminator.sh
"""

# Source ROS 2 setup
source /opt/ros/galactic/setup.bash

# Build the workspace
colcon build --symlink-install

# Source the workspaces
source ./install/setup.bash

# Start Terminator with multiple tabs and commands
ros2 launch eagle_launch.py