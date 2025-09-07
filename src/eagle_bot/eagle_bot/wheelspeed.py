"""
This script contains a ROS 2 node for converting Twist messages to wheel speeds.

It subscribes to a `cmd_vel` topic (specifically `/diff_controller/cmd_vel_unstamped`),
calculates the required left and right wheel speeds to achieve the desired motion,
and then publishes these speeds as a string on the 'wheelspeed' topic.
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class MotorController(Node):
    """
    A ROS 2 node to convert Twist messages to individual wheel speeds.

    This class implements the inverse kinematics for a differential drive robot,
    converting a Twist message (linear and angular velocities) into speeds for the
    left and right wheels.

    Attributes:
        publisher_: Publisher for the 'wheelspeed' topic.
        subscription: Subscription to the command velocity topic.
        left_wheel_speed (float): The calculated speed for the left wheel.
        right_wheel_speed (float): The calculated speed for the right wheel.
    """

    def __init__(self):
        """Initializes the MotorController node."""
        super().__init__('motor_controller')
        self.publisher_ = self.create_publisher(String, 'wheelspeed', 10)
        self.subscription = self.create_subscription(Twist, '/diff_controller/cmd_vel_unstamped', self.cmd_vel_callback, 10)
        self.left_wheel_speed = 0.0
        self.right_wheel_speed = 0.0

    def cmd_vel_callback(self, msg):
        """
        Callback for the command velocity topic.

        This method takes a Twist message and calculates the corresponding wheel
        speeds using a simplified differential drive model.

        Args:
            msg (geometry_msgs.msg.Twist): The incoming command velocity message.
        """
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        # Assuming some conversion logic to get left and right wheel speeds
        # Replace this with your actual conversion code
        self.left_wheel_speed = linear_x - angular_z
        self.right_wheel_speed = linear_x + angular_z

        # Publish the wheel speeds
        self.publish_wheel_speed()

    def publish_wheel_speed(self):
        """
        Publishes the calculated wheel speeds.

        The speeds are formatted into a string and published on the 'wheelspeed' topic.
        """
        msg = String()
        msg.data = f"{self.left_wheel_speed} {self.right_wheel_speed}"
        self.publisher_.publish(msg)


def main(args=None):
    """
    The main function to run the MotorController node.

    Initializes rclpy, creates an instance of MotorController, and spins the
    node until it's shut down.

    Args:
        args: Command-line arguments.
    """
    rclpy.init(args=args)
    motor_controller = MotorController()
    rclpy.spin(motor_controller)
    motor_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
