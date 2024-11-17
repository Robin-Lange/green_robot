import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import serial

class WheelSpeedSubscriber(Node):

    def __init__(self):
        super().__init__('wheel_speed_subscriber')
        self.subscription = self.create_subscription(String, 'wheelspeed', self.wheelspeed_callback, 10)
        
        try:
            self.serial_port = serial.Serial('/dev/ttyUSB0', baudrate=9600)  # Adjust port and baudrate accordingly
            self.get_logger().info("Serial connection established")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to open serial port: {e}")

    def wheelspeed_callback(self, msg):
        data = msg.data.split()
        left_speed = float(data[0])
        right_speed = float(data[1])

        # Send left and right speeds to Arduino
        try:
            self.send_to_arduino(left_speed, right_speed)
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to send data to Arduino: {e}")

    def send_to_arduino(self, left_speed, right_speed):
        message = f"{left_speed} {right_speed}\n"
        try:
            self.serial_port.write(message.encode('utf-8'))
            self.get_logger().info(f"Sent message to Arduino: {message.strip()}")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to send data to Arduino: {e}")

def main(args=None):
    rclpy.init(args=args)
    wheel_speed_subscriber = WheelSpeedSubscriber()
    rclpy.spin(wheel_speed_subscriber)
    wheel_speed_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
