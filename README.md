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


For autonomous driving, use 2D Pose estimate where the robot is approximately to get started then it will navigate to the set waypoint. In order to do so, use the command '2D Pose Estimate' in the top bar in the RVIZ interface. The robot will locate itself in the existing map. Then use 'NAV2 Goal' to let it drive to the dedicated spot. Make sure you use the correct map



# Eagle2

## Simulation in gazebo
change the used lidar
### Needed Folders
APRN_ws (launch files under src->v2->launch) [check for the slam parameter] and APRN_sim (all the data for the simulation)
### World Map
Either:
- 'APRN_basic_2.sdf'
- worldwpods.sdf

### Launch files (simultaneously launch)
launch_sn.launch.py
nav_launch.py

### get ros2 rosbags in another terminal (that are not called rosbag)
use ros2 topics list auch in kombi mit echo um die topics zu sehen
get rosbag for position and lidar data
lidardata should be something like laser_scan


Get manual drive and lidar data and encoder data ros bag

### Real drive


Use Existing SLAM and add the positioning system to it

https://pdf.sciencedirectassets.com/313346/1-s2.0-S2405896322X00311/1-s2.0-S2405896322027495/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQC80ltVXrccoFrO18M23Fhqq3qPVo1Q1i9rHA2Q1R8GTAIgGhvuWc0c%2F4836lfMEio9GNSqwyV8KRSTUOGUarOdTtcqswUIHxAFGgwwNTkwMDM1NDY4NjUiDPrgrFaPTNf8DwFshCqQBUBd3zdRKEOz9YIlJpIRT1IF%2Bm9bKSGoBhCCwqJfpP1XZvmiC%2F6D3DcNg3vpzGSwu%2F5WNm2QM%2BbPW7GBFIgumTzN7VlyTyF0NkyOObINUfPUoIHFHlDMUvK98AIlfZnGkYJ7JCFTQ3gWloYBZ%2BaOTayzuj6EFswuVoBhRIMXZkwvyLD85zoKG2OJdb0T%2FnuKOVCQ28hS0yK1%2BrptlYu3lsE9D9axtWEDV6P2OkynxgLPsxVUqf9IFH9LFQegl8MKDISea1gMd%2F5%2Fh3GFb64kT5ufR8PosEfAcZc88HhAzrd9jgmVKCrbWhaLENorb4f2DxeT14T79EDzUOLVFDPh44HPnLHuf4DGT1nGzPC%2B5K9pTvmMoCcajoVD3wTmef43cgLWnc6wK%2FmmSxr7ya4paIzjDj%2F88gd5pbGNFQLeVin8YTHdeBuAQ4NXo8GCoylG%2FGGNk184LRgNBlRA9YyorZY5RV0uAmKfc3Y4ElnQEISz6rTlS5UYGMNyBTth0pTIXKakpRtgxRbOvm6ZNt9H0gVOUgYj74vmkVABF0prgFOMo2jZoXyaHNyBy47FEXNnR31mY7jsaeKtcjYwL6K6l5%2FWBgTrQ0d4u8uZ2vrHbPK8%2BOu7SUMqMuQnJgVFIeiEjbsIvgX4fLv0FZ805YaY8rarfH3%2B3M2G73CFif9hBxZZ%2BVEu7Ptzyy9%2B2i296BdSiNmtJefudd%2BV3DnFUSE8coGO7rWLuLz0pS%2BxCsPIHWg84jWXhoa2f9g7BoChycbjvbD6LAEb3YE4hdwlFE7HEY0U6kJ7Xd7tLrfy%2BzxpJjUv5M%2BWhOklTxu0VmdYY%2BrnrbOlpCH8ZXJGmtYQMByX4LoR5El%2BdLXWHx3JJw9Zl0P1MKmuqrkGOrEBFzAvzREDP06gP6QWAutKB9l%2FkOtEzlO5kOF7VN1Co3xkvabuwRga1ntjsmt%2FEZr2Y47YabLJaOsYNEqE6sqZ2NNKzrPJj8AJX2ylT5Iqf57JQTRlrQiT%2Fwmcsczw7IS5khJ%2BX8QOnTzrqXw88ma99wIuS3howofU%2BbdoC3aUFf%2BMbtwKIC%2FMnKThGsk9dJui9TJJxNEALhuPI6vVE39t2AzgOub%2FO66giKz1VRZq0bDK&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20241105T225422Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYUITMIFWM%2F20241105%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=94116b8b302956538133410e67df2cd93647cbdd600378ddea1e0dceb72d406c&hash=a0b5491fa25798f47a176be772c642d4ed5ce5af8fd6f8baf9da84d1d5eab194&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S2405896322027495&tid=spdf-715f823d-82f1-4abb-b6df-626c7379dcb8&sid=01dbadf11380a54ac7798c789008eacd25fcgxrqa&type=client&tsoh=d3d3LnNjaWVuY2VkaXJlY3QuY29t&ua=0f165f0b045052060a0258&rr=8de06cdb99f1b099&cc=us
https://www.sciencedirect.com/science/article/pii/S2772941924000565
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10058595

https://dev.intelrealsense.com/docs/compiling-librealsense-for-linux-ubuntu-guide?_ga=2.27613044.973360539.1731886892-166595236.1731886892
https://docs.ros.org/en/galactic/Installation/Ubuntu-Install-Debians.html
Ros manual robot control:



https://index.ros.org/p/teleop_twist_keyboard/github-ros2-teleop_twist_keyboard/

