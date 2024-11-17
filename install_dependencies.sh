#!/bin/bash
#execute this script by running:
    # chmod +x install_dependencies.sh
    #./install_dependencies.sh

# Install ROS 2 Galactic dependencies
sudo apt update
sudo apt install -y \
    ros-galactic-joint-state-publisher-gui \
    ros-galactic-xacro \
    ros-galactic-gazebo-ros-pkgs \
    ros-galactic-robot-localization \
    ros-galactic-slam-toolbox \
    ros-galactic-navigation2 \
    ros-galactic-nav2-bringup \
    ros-galactic-ros2-control \
    ros-galactic-ros2-controllers \
    libserial-dev

# Add any additional dependencies here
# sudo apt install -y <additional-dependency>

echo "All dependencies installed successfully."