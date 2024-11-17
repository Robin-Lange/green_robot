import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
from datetime import datetime

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber')
        self.subscription = self.create_subscription(
            Image,
            '/camera/color/image_raw',
            self.image_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.cv_bridge = CvBridge()
        self.video_writer = None
        self.is_recording = False
        self.frame_width = 0
        self.frame_height = 0

    def image_callback(self, msg):
        try:
            # Convert ROS Image message to OpenCV image
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, 'bgr8')
            
            # Check if the video writer is initialized
            if self.video_writer is None:
                self.frame_width = cv_image.shape[1]
                self.frame_height = cv_image.shape[0]
                self.initialize_video_writer()

            # Write the frame to the video
            self.video_writer.write(cv_image)

            # Display the frame (optional)
            cv2.imshow("ROS2 Video Stream", cv_image)
            cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error(f"Error processing image: {e}")

    def initialize_video_writer(self):
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            video_filename = f"videos/ros2_video_{timestamp}.mp4"
            video_path = os.path.join(os.getcwd(), 'videos')
            os.makedirs(video_path, exist_ok=True)

            # Define the codec and create VideoWriter object
            codec = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_writer = cv2.VideoWriter(video_filename, codec, 10.0, (self.frame_width, self.frame_height))

            self.get_logger().info(f"Video recording started: {video_filename}")

        except Exception as e:
            self.get_logger().error(f"Error initializing video writer: {e}")
            self.video_writer = None

    def destroy_node(self):
        if self.is_recording:
            self.stop_recording()

        if self.video_writer is not None:
            self.video_writer.release()
            self.get_logger().info("Video recording stopped.")

        super().destroy_node()

    def start_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.get_logger().info("Recording started")

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.get_logger().info("Recording stopped")

def main(args=None):
    rclpy.init(args=args)

    image_subscriber = ImageSubscriber()

    try:
        rclpy.spin(image_subscriber)
    except KeyboardInterrupt:
        image_subscriber.get_logger().info("Shutting down")

    image_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
