# Eagle Bot ROS2 Workspace

This repository contains the ROS2 workspace for the Eagle Bot, a differential drive robot designed for indoor warehouse environments.

## Overview

The goal of this project is to provide a fully autonomous mobile robot platform. It uses a differential drive base, is controlled via ROS2, and uses a LIDAR for SLAM (Simultaneous Localization and Mapping) and navigation.

### Key Features
- **ROS2-based:** Utilizes the modern ROS2 framework.
- **Interactive Startup:** A single script (`start_robot.sh`) to launch all necessary nodes with a user-friendly menu.
- **Navigation Ready:** Comes with configurations for the Nav2 stack, including modes for mapping, localization, and autonomous navigation.
- **Tunable:** Key parameters for motor control and navigation are exposed in YAML files for easy tuning.

---

## Repository Structure

A brief overview of the most important directories:
- **/src/eagle_bot:** The main package for the robot.
  - **/launch:** Contains all the ROS2 launch files.
  - **/config:** Holds all the configuration files (Nav2, controllers, etc.).
- **/src/diff_controller:** The `ros2_control` hardware interface for the differential drive base.
- **/start_robot.sh:** The main script to run the robot.

---

## 💻 Installation & Setup

### 1. Dependencies
This project requires ROS2 (Humble recommended) and a few other system packages. An installation script is provided to simplify this process.

```bash
# Run the dependency installer
./install_dependencies.sh
```

<details>
<summary><strong>Manual Dependency Installation</strong></summary>

If you prefer to install dependencies manually, you will need `ros-humble-navigation2`, `ros-humble-slam-toolbox`, `ros-humble-ros2-control`, `ros-humble-ros2-controllers`, and `gnome-terminal`.
</details>

### 2. Configure udev Rules (for Hardware)
To ensure your user has permission to access the robot's hardware (like the RPLIDAR and motor controller), you may need to add udev rules. These rules create a consistent device name (e.g., `/dev/rplidar`) and set the correct permissions.

Refer to the documentation for your specific hardware (e.g., RPLIDAR, Arduino/microcontroller) to get the correct `idVendor` and `idProduct`.

<details>
<summary><strong>Example: RPLIDAR udev Rule</strong></summary>

1.  Create a new rules file: `sudo nano /etc/udev/rules.d/99-rplidar.rules`
2.  Add the following line (replace `2c42` if your vendor ID is different):
    ```
    SUBSYSTEM=="tty", ATTRS{idVendor}=="2c42", MODE="0666", SYMLINK+="rplidar"
    ```
3.  Reload the rules: `sudo udevadm control --reload-rules`
4.  Unplug and replug the device.
</details>

### 3. Build the Workspace
Compile the ROS2 packages using `colcon`.

```bash
# From the root of the repository (the 'green_robot' folder)
colcon build --symlink-install
```

---

## 🚀 Execution

The primary way to run the robot is with the interactive startup script.

### Using the Interactive Startup Script
This script handles sourcing the workspace and launching the correct nodes based on your selection.

```bash
# Make sure you are in the root of the repository
./start_robot.sh
```
The script will present a menu with three options:
1.  **Manual Control:** For driving the robot with the keyboard.
2.  **Autonomous Navigation:** For navigating in a known, pre-mapped area.
3.  **Mapping:** For creating a new map of an unknown area using SLAM.

---

## 🔧 Tuning & Troubleshooting

<details>
<summary><strong>Problem: The robot drifts to one side when trying to drive straight.</strong></summary>

- **Cause:** Minor physical imperfections in the motors or wheels cause them to spin at slightly different rates.
- **Solution:** Adjust the `wheel_radius_multiplier` parameters in `src/eagle_bot/config/my_controllers.yaml`.
  - If the robot drifts **right**, the left wheel is spinning too fast. **Decrease** `left_wheel_radius_multiplier` by a small amount (e.g., to `0.99`).
  - If the robot drifts **left**, the right wheel is spinning too fast. **Decrease** `right_wheel_radius_multiplier` by a small amount.
  - **File to edit:** `src/eagle_bot/config/my_controllers.yaml`
    ```yaml
    left_wheel_radius_multiplier: 1.0
    right_wheel_radius_multiplier: 1.0
    ```
</details>

<details>
<summary><strong>Problem: The robot "dances" or oscillates around the navigation goal without stopping.</strong></summary>

- **Cause:** The goal tolerances for the navigation system are too strict. The robot gets very close to the goal but overshoots slightly and then tries to correct itself in a loop.
- **Solution:** Increase the goal tolerances to give the robot a larger "success" radius.
  - **File to edit:** `src/eagle_bot/config/nav2_params.yaml`
  - **Parameters to change:**
    ```yaml
    # In the 'general_goal_checker' section
    xy_goal_tolerance: 0.5  # meters
    yaw_goal_tolerance: 0.5 # radians

    # In the 'FollowPath' (DWB) section
    xy_goal_tolerance: 0.5  # meters
    ```
</details>

---

## 📚 Useful Resources
- [ROS2 Documentation](https://docs.ros.org/en/humble/index.html)
- [Nav2 (Navigation2) Documentation](https://navigation.ros.org/)
- [ros2_control Documentation](https://control.ros.org/master/index.html)
- [Community Tutorials for `teleop_twist_keyboard`](https://index.ros.org/p/teleop_twist_keyboard/)
