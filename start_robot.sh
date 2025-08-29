#!/bin/bash

# This script provides a user-friendly menu to launch the ROS2-based robot,
# automating the process of opening multiple terminals and running commands.

echo "Sourcing the workspace and launching core systems..."

# Open a new terminal with the workspace sourced. This is for user convenience for manual commands.
# The 'exec bash' command at the end keeps the terminal window open after the initial command completes.
gnome-terminal --title="Workspace Sourced" -- bash -c "source install/setup.bash; echo 'This terminal has the workspace sourced. You can use it for manual commands.'; exec bash"

# Launch the main robot communication stack in a new terminal.
# Each terminal that runs ROS2 commands must source the workspace first.
gnome-terminal --title="Eagle Bot Launch" -- bash -c "source install/setup.bash; ros2 launch eagle_bot eagle.launch.py; read"

echo "Waiting for 3 seconds for core systems to initialize..."
sleep 3

# --- User Menu ---
# Prompt the user to select one of the three main operational modes.
echo "-------------------------------------"
echo "Please choose an operational mode:"
echo "1) Manual Control"
echo "2) Autonomous Navigation (with a pre-existing map)"
echo "3) Mapping (for exploring unknown areas)"
echo "-------------------------------------"
echo -n "Enter your choice [1-3]: "
read choice

# --- Execute Choice ---
# Use a case statement to execute the commands for the selected mode.
case $choice in
    1)
        echo "Starting Manual Control..."
        # Launch the teleop node for keyboard control.
        # The command remaps the /cmd_vel topic to the one expected by the differential drive controller.
        gnome-terminal --title="Manual Control" -- bash -c "source install/setup.bash; ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_controller/cmd_vel_unstamped; read"
        ;;
    2)
        echo "Starting Autonomous Navigation..."
        # Launch the autonomous navigation system, which includes localization (AMCL) and Nav2.
        gnome-terminal --title="Autonomous Navigation" -- bash -c "source install/setup.bash; ros2 launch eagle_bot localization_nav.launch.py; read"
        ;;
    3)
        echo "Starting Mapping mode..."
        # Launch all nodes required for creating a new map.

        # Terminal 1: Manual control for driving the robot around the new area.
        gnome-terminal --title="Manual Control (Mapping)" -- bash -c "source install/setup.bash; ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_controller/cmd_vel_unstamped; read"

        # Terminal 2: The mapping process itself (SLAM).
        gnome-terminal --title="Create Map (SLAM)" -- bash -c "source install/setup.bash; ros2 launch eagle_bot nav_launch.py; read"

        # Terminal 3: A dedicated terminal for saving the map once exploration is complete.
        # The 'read' command pauses the script, waiting for the user to press Enter in this terminal.
        gnome-terminal --title="Save Map" -- bash -c "source install/setup.bash; echo 'Drive the robot around to build the map.'; echo 'When you are ready, press Enter in THIS terminal to save the map.'; read; ros2 run nav2_map_server map_saver_cli -f ~/map; echo 'Map saved to ~/map.pgm and ~/map.yaml'; exec bash"
        ;;
    *)
        echo "Invalid choice. Please run the script again and select a valid option."
        ;;
esac

echo "Startup script finished."
