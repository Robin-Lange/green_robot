"""
This script contains a ROS 2 node for calculating and printing wheel velocities.

It subscribes to `dynamic_joint_states` and `/diff_controller/cmd_vel_unstamped` topics
to compute the linear velocities of the left and right wheels of a differential
drive robot. The calculated velocities are then printed to the console.
"""
import rclpy
from rclpy.node import Node
from control_msgs.msg import DynamicJointState
from geometry_msgs.msg import Twist
from math import sin, cos, isnan
import math

class WheelVelocitiesCalculator(Node):
    """
    A ROS 2 node to calculate and display wheel velocities.

    This class subscribes to joint state and command velocity topics to calculate
    the linear velocities of the wheels. It is primarily used for debugging and
    data analysis.

    Attributes:
        subscription_dynamic_joint_states: Subscription to the dynamic joint states.
        subscription_cmd_vel: Subscription to the command velocity topic.
        left_wheel_radius (float): The radius of the left wheel in meters.
        right_wheel_radius (float): The radius of the right wheel in meters.
        wheelbase (float): The distance between the wheels in meters.
    """

    def __init__(self):
        """Initializes the WheelVelocitiesCalculator node."""
        super().__init__('your_node_name')
        self.subscription_dynamic_joint_states = self.create_subscription(
            DynamicJointState,
            'dynamic_joint_states',
            self.dynamic_joint_states_callback,
            10)
        self.subscription_cmd_vel = self.create_subscription(
            Twist,
            '/diff_controller/cmd_vel_unstamped',
            self.cmd_vel_callback,
            10)

        self.left_wheel_radius = 0.05  # Replace with your left wheel radius (in meters)
        self.right_wheel_radius = 0.05  # Replace with your right wheel radius (in meters)
        self.wheelbase = 0.2  # Replace with your robot's wheelbase (distance between the wheels, in meters)

    def dynamic_joint_states_callback(self, msg):
        """
        Callback for the dynamic_joint_states topic.

        This method calculates the linear velocity of each wheel based on the
        received joint state messages.

        Args:
            msg (control_msgs.msg.DynamicJointState): The incoming joint state message.
        """
        left_wheel_velocity = 0.0
        right_wheel_velocity = 0.0

        left_wheel_index = -1
        right_wheel_index = -1

        for i, joint_name in enumerate(msg.joint_names):
            if joint_name == 'left_wheel_joint':
                left_wheel_index = i
            elif joint_name == 'right_wheel_joint':
                right_wheel_index = i

        if left_wheel_index != -1:
            left_wheel_velocity = msg.interface_values[left_wheel_index].values[1] * self.left_wheel_radius
        if right_wheel_index != -1:
            right_wheel_velocity = msg.interface_values[right_wheel_index].values[1] * self.right_wheel_radius

        print(f'|{left_wheel_velocity:.3f}|{left_wheel_velocity:.3f}|{right_wheel_velocity:.3f}|{right_wheel_velocity:.3f}|')

    def cmd_vel_callback(self, msg):
        """
        Callback for the cmd_vel topic.

        This method calculates the expected wheel velocities based on the inverse
        kinematics of a differential drive robot.

        Args:
            msg (geometry_msgs.msg.Twist): The incoming command velocity message.
        """
        if math.isnan(msg.linear.x) or math.isnan(msg.angular.z):
            left_wheel_velocity = 0.0
            right_wheel_velocity = 0.0
        else:
            linear_x = msg.linear.x
            angular_z = msg.angular.z

            left_wheel_velocity = (linear_x - angular_z * self.wheelbase / 2.0) / self.left_wheel_radius
            right_wheel_velocity = (linear_x + angular_z * self.wheelbase / 2.0) / self.right_wheel_radius

        print(f'|{left_wheel_velocity:.3f}|0|{right_wheel_velocity:.3f}|0|')

def main(args=None):
    """
    The main function to run the WheelVelocitiesCalculator node.

    Initializes rclpy, creates an instance of WheelVelocitiesCalculator, and spins
    the node until it's shut down.

    Args:
        args: Command-line arguments.
    """
    rclpy.init(args=args)
    wheel_velocities_calculator = WheelVelocitiesCalculator()
    rclpy.spin(wheel_velocities_calculator)
    wheel_velocities_calculator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
