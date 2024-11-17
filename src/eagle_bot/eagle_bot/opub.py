import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped, Quaternion, Twist
from tf2_ros import TransformBroadcaster
from math import sin, cos


class OdometryPublisher(Node):
    def __init__(self):
        super().__init__('odometry_publisher')

        self.odom_pub = self.create_publisher(Odometry, 'odom', 50)
        self.odom_broadcaster = TransformBroadcaster(self)
        self.cmd_vel_pub = self.create_publisher(Twist, 'command', 10)

        self.x = 0.0
        self.y = 0.0
        self.th = 0.0

        self.vx = 0.0
        self.vy = 0.0
        self.vth = 0.0

        self.current_time = self.get_clock().now()
        self.last_time = self.get_clock().now()

        self.cmd_vel_sub = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10
        )

        self.timer = self.create_timer(0.01, self.timer_callback)  # Update at a faster rate (e.g., 100 Hz)
        self.odom_publish_timer = self.create_timer(0.5, self.odom_publish_callback)  # Publish commands every 0.05 seconds

    def cmd_vel_callback(self, msg):
        self.vx = msg.linear.x
        self.vy = msg.linear.y
        self.vth = msg.angular.z

    def timer_callback(self):
        self.current_time = self.get_clock().now()

        dt = (self.current_time - self.last_time).nanoseconds / 1e9

        # Calculate delta values based on elapsed time
        delta_x = (self.vx * cos(self.th) - self.vy * sin(self.th)) * dt
        delta_y = (self.vx * sin(self.th) + self.vy * cos(self.th)) * dt
        delta_th = self.vth * dt

        self.x += delta_x
        self.y += delta_y
        self.th += delta_th

        self.last_time = self.current_time

    def odom_publish_callback(self):
        # Publish odometry message
        odom = Odometry()
        odom.header.stamp = self.current_time.to_msg()
        odom.header.frame_id = 'odom'

        # Set the child frame ID to 'base_link'
        odom.child_frame_id = 'base_link'

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0

        odom_quat = Quaternion()
        odom_quat.z = sin(self.th / 2)
        odom_quat.w = cos(self.th / 2)
        odom.pose.pose.orientation = odom_quat

        odom.twist.twist.linear.x = self.vx
        odom.twist.twist.linear.y = self.vy
        odom.twist.twist.angular.z = self.vth

        self.odom_pub.publish(odom)

        # Publish transform from 'odom' to 'base_link'
        transform = TransformStamped()
        transform.header.stamp = self.current_time.to_msg()
        transform.header.frame_id = 'odom'
        transform.child_frame_id = 'base_link'
        transform.transform.translation.x = self.x
        transform.transform.translation.y = self.y
        transform.transform.translation.z = 0.0
        transform.transform.rotation = odom_quat

        self.odom_broadcaster.sendTransform(transform)

        # Print velocities in the terminal
        """ self.get_logger().info(
            f"Linear Velocities: vx={self.vx:.2f}, vy={self.vy:.2f}"
        )
        self.get_logger().info(f"Angular Velocity: vth={self.vth:.2f}") """

        # Publish velocity commands to robot_cmds topic
        cmd_vel_msg = Twist()
        cmd_vel_msg.linear.x = self.vx
        cmd_vel_msg.linear.y = self.vy
        cmd_vel_msg.angular.z = self.vth

        self.cmd_vel_pub.publish(cmd_vel_msg)


def main(args=None):
    rclpy.init(args=args)
    odom_publisher = OdometryPublisher()
    rclpy.spin(odom_publisher)
    odom_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
