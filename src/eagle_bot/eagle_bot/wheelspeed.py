import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class MotorController(Node):

    def __init__(self):
        super().__init__('motor_controller')
        self.publisher_ = self.create_publisher(String, 'wheelspeed', 10)
        self.subscription = self.create_subscription(Twist, '/diff_controller/cmd_vel_unstamped', self.cmd_vel_callback, 10)
        self.left_wheel_speed = 0.0
        self.right_wheel_speed = 0.0

    def cmd_vel_callback(self, msg):
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        # Assuming some conversion logic to get left and right wheel speeds
        # Replace this with your actual conversion code
        self.left_wheel_speed = linear_x - angular_z
        self.right_wheel_speed = linear_x + angular_z

        # Publish the wheel speeds
        self.publish_wheel_speed()

    def publish_wheel_speed(self):
        msg = String()
        msg.data = f"{self.left_wheel_speed} {self.right_wheel_speed}"
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    motor_controller = MotorController()
    rclpy.spin(motor_controller)
    motor_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
