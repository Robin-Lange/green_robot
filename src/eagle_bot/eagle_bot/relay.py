"""
This script contains a ROS 2 node for relaying wheel speed commands to a serial device.

It subscribes to the 'wheelspeed' topic, which is expected to publish a string
containing space-separated left and right wheel speeds. These speeds are then sent
over a serial connection, presumably to a microcontroller like an Arduino.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import serial

class WheelSpeedSubscriber(Node):
    """
    A ROS 2 node that subscribes to wheel speed commands and sends them to a serial device.

    This class sets up a subscription to the 'wheelspeed' topic and establishes a
    serial connection. It is designed to act as a bridge between ROS 2 and a
    microcontroller responsible for motor control.

    Attributes:
        subscription: The subscription to the 'wheelspeed' topic.
        serial_port: The serial port object for communication with the microcontroller.
    """

    def __init__(self):
        """Initializes the WheelSpeedSubscriber node."""
        super().__init__('wheel_speed_subscriber')
        self.subscription = self.create_subscription(String, 'wheelspeed', self.wheelspeed_callback, 10)
        
        try:
            self.serial_port = serial.Serial('/dev/ttyUSB0', baudrate=9600)  # Adjust port and baudrate accordingly
            self.get_logger().info("Serial connection established")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to open serial port: {e}")

    def wheelspeed_callback(self, msg):
        """
        Callback for the 'wheelspeed' topic.

        This method parses the incoming message to extract left and right wheel speeds
        and then sends them to the Arduino.

        Args:
            msg (std_msgs.msg.String): The incoming message containing wheel speeds.
        """
        data = msg.data.split()
        left_speed = float(data[0])
        right_speed = float(data[1])

        # Send left and right speeds to Arduino
        try:
            self.send_to_arduino(left_speed, right_speed)
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to send data to Arduino: {e}")

    def send_to_arduino(self, left_speed, right_speed):
        """
        Sends the wheel speeds to the Arduino over the serial connection.

        Args:
            left_speed (float): The speed of the left wheel.
            right_speed (float): The speed of the right wheel.
        """
        message = f"{left_speed} {right_speed}\n"
        try:
            self.serial_port.write(message.encode('utf-8'))
            self.get_logger().info(f"Sent message to Arduino: {message.strip()}")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to send data to Arduino: {e}")

def main(args=None):
    """
    The main function to run the WheelSpeedSubscriber node.

    Initializes rclpy, creates an instance of WheelSpeedSubscriber, and spins the
    node until it's shut down.

    Args:
        args: Command-line arguments.
    """
    rclpy.init(args=args)
    wheel_speed_subscriber = WheelSpeedSubscriber()
    rclpy.spin(wheel_speed_subscriber)
    wheel_speed_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
