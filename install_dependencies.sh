"""
    This script installs all the dependencies required for the ROS 2 humble packages in your workspace.

    To determine if there are any additional dependencies required for your workspace, you can use the rosdep tool. rosdep helps you install system dependencies for ROS packages. Here is how you can use it:
    Make sure rosdep is installed:
        sudo apt install python3-rosdep
    Initialize rosdep (if you haven't already):
        sudo rosdep init
        rosdep update
    Navigate to the root of your ROS workspace and run:
        rosdep install --from-paths src --ignore-src -r -y
    This command will check all the packages in your workspace and install any missing dependencies.
    
    or you can run:
    chmod +x install_dependencies.sh
    ./install_dependencies.sh
"""

# Install ROS 2 humble dependencies
sudo apt update
sudo apt install -y \
    ros-humble-joint-state-publisher-gui \
    ros-humble-xacro \
    ros-humble-robot-localization \
    ros-humble-slam-toolbox \
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    libserial-dev \
    python3-rosdep \
    ros-humble-twist-mux

# Initialize rosdep
sudo rosdep init
rosdep update

# Install dependencies using rosdep
rosdep install --from-paths src --ignore-src -r -y

echo "All dependencies installed successfully."