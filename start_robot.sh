#!/bin/bash

# This script launches the robot's core systems and provides an interactive
# menu for selecting the operational mode.

echo "Sourcing the workspace and launching core systems..."

# Source the workspace in a new terminal. Note: This is just for user convenience.
# Each terminal needs to source the workspace independently.
gnome-terminal --title="Workspace Sourced" -- bash -c "echo 'This terminal has the workspace sourced. You can use it for manual commands.'; exec bash"

# Launch the main robot communication
gnome-terminal --title="Eagle Bot Launch" -- bash -c "source install/setup.bash; ros2 launch eagle_bot eagle.launch.py; exec bash"

echo "Waiting for 3 seconds before showing options..."
sleep 3

# --- User Menu ---
echo "Please choose an operational mode:"
echo "1) Manual Control"
echo "2) Autonomous Navigation (with saved map)"
echo "3) Mapping (in an unknown area)"
echo -n "Enter your choice [1-3]: "
read choice

# --- Execute Choice ---
case $choice in
    1)
        echo "Starting Manual Control..."
        gnome-terminal --title="Manual Control" -- bash -c "source install/setup.bash; ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_controller/cmd_vel_unstamped; exec bash"
        ;;
    2)
        echo "Starting Autonomous Navigation..."
        gnome-terminal --title="Autonomous Navigation" -- bash -c "source install/setup.bash; ros2 launch eagle_bot localization_nav.launch.py; exec bash"
        ;;
    3)
        echo "Starting Mapping mode..."
        # Terminal 1: Manual Control for mapping
        gnome-terminal --title="Manual Control (Mapping)" -- bash -c "source install/setup.bash; ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_controller/cmd_vel_unstamped; exec bash"

        # Terminal 2: Create Map
        gnome-terminal --title="Create Map" -- bash -c "source install/setup.bash; ros2 launch eagle_bot nav_launch.py; exec bash"

        # Terminal 3: Save Map (waits for Enter)
        gnome-terminal --title="Save Map" -- bash -c "source install/setup.bash; echo 'Drive the robot around to build the map.'; echo 'When you are ready, press Enter in THIS terminal to save the map.'; read; ros2 run nav2_map_server map_saver_cli -f ~/map; echo 'Map saved to ~/map.pgm and ~/map.yaml'; exec bash"
        ;;
    *)
        echo "Invalid choice. Please run the script again and select a valid option."
        ;;
esac

echo "Startup script finished."
