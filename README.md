# green_robot
Project for the green warehouse robot

Before running, make sure all dependencies are installed, see install_dependencies.sh

Tims emails:

These are the ones I can think of off the top of my head. Ill email you more as I think of them.

sudo apt install ros-<ros2-distro>-joint-state-publisher-gui
sudo apt install ros-<ros2-distro>-xacro
sudo apt install ros-<ros2-distro>-gazebo-ros-pkgs
sudo apt install ros-<ros2-distro>-robot-localization
sudo apt install ros-<ros2-distro>-slam-toolbox
sudo apt install ros-<ros2-distro>-navigation2
sudo apt install ros-<ros2-distro>-nav2-bringup
sudo apt install   ros-galactic-ros2-control
sudo apt install   ros- galactic  -ros2-controllers
sudo apt install libserial-dev

Step 2: Write the udev Rule
Open or create a new udev rules file in /etc/udev/rules.d/. For Arduino, the file is often named 99-arduino.rules:


use lsusb to find the values for the Arduino 
The idVendor (VID) and idProduct (PID) are identifiers used to recognize USB devices. To find the VID and PID for your Arduino Mega, follow these steps:

Connect your Arduino Mega: Plug your Arduino Mega into your computer.

List USB devices: Use the lsusb command to list all connected USB devices:

Identify your Arduino Mega: Look for an entry that corresponds to your Arduino Mega. It will look something like this:

Extract VID and PID: The numbers before the device name are the VID and PID. In the example above, 2341 is the idVendor and 0042 is the idProduct.
bash
Copy code
sudo nano /etc/udev/rules.d/99-arduino.rules
Add the following rule (adjust VID and PID as necessary):

plaintext
Copy code
SUBSYSTEM=="tty", ATTRS{idVendor}=="2341", ATTRS{idProduct}=="0042", MODE="0666", SYMLINK+="arduino_mega"

SUBSYSTEM=="tty": Matches USB serial devices.
ATTRS{idVendor} and ATTRS{idProduct}: Match the VID and PID of your Arduino Mega.
MODE="0666": Grants read/write access to all users.
SYMLINK+="arduino_mega": Creates a user-friendly symlink (/dev/arduino_mega).
Step 3: Apply the udev Rule
Reload udev rules:

bash
Copy code
sudo udevadm control --reload-rules
Unplug and replug your Arduino Mega to apply the new rule."

To save SLAM map after running slam toolbox and nav with odom:

ros2 run nav2_map_server map_saver_cli -f ~/map

Run just navigation:

ros2 launch nav2_bringup navigation_launch.py

Run slam toolbox:

ros2 launch slam_toolbox online_async_launch.py

Run navigation with a defined parameter file
ros2 launch nav2_bringup navigation_launch.pyparams_file:=<full/path/to/config/nav2_params.yaml>

Run tools to see transform coordinate frames and connections

ros2 run tf2_tools view_frames.py

Node graph command
rqt_graph

Keyboard control of robot without topic remapping (should work for simulation environment)
ros2 run teleop_twist_keyboard teleop_twist_keyboard

Keyboard control to drive physical robot:
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_controller/cmd_vel_unstamped


For autonomous driving, use 2D Pose estimate where the robot is approximately to get started then it will navigate to the set waypoint
