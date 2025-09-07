"""
This script contains a ROS 2 node for subscribing to an image topic and saving the feed as a video.

It uses OpenCV to handle image processing and video writing. The node subscribes to a
specified image topic, converts the ROS Image messages to OpenCV format, and writes them
to an MP4 video file. The video files are saved with a timestamp in the 'videos' directory.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os
from datetime import datetime

class ImageSubscriber(Node):
    """
    A ROS 2 node that subscribes to a raw image topic and saves the video stream.

    This class sets up a subscription to an image topic, converts the incoming ROS Image
    messages to OpenCV images, and writes them to a video file. It also provides
    functionality to start and stop recording.

    Attributes:
        subscription: The subscription to the image topic.
        cv_bridge (CvBridge): A bridge to convert between ROS and OpenCV images.
        video_writer: The OpenCV VideoWriter object.
        is_recording (bool): A flag to indicate if recording is active.
        frame_width (int): The width of the video frames.
        frame_height (int): The height of the video frames.
    """
    def __init__(self):
        """Initializes the ImageSubscriber node."""
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
        """
        Callback function for the image subscription.

        This method is called for each new image message. It converts the message to an
        OpenCV image, initializes the video writer if it's not already, and writes the
        frame to the video file.

        Args:
            msg (sensor_msgs.msg.Image): The incoming ROS Image message.
        """
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
        """
        Initializes the OpenCV VideoWriter.

        This method sets up the video writer with the correct codec, filename, and
        frame dimensions. The video files are saved in a 'videos' directory, which is
        created if it doesn't exist.
        """
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
        """
        Cleans up resources when the node is destroyed.

        This method releases the video writer, ensuring that the video file is
        properly closed.
        """
        if self.is_recording:
            self.stop_recording()

        if self.video_writer is not None:
            self.video_writer.release()
            self.get_logger().info("Video recording stopped.")

        super().destroy_node()

    def start_recording(self):
        """Starts the video recording."""
        if not self.is_recording:
            self.is_recording = True
            self.get_logger().info("Recording started")

    def stop_recording(self):
        """Stops the video recording."""
        if self.is_recording:
            self.is_recording = False
            self.get_logger().info("Recording stopped")

def main(args=None):
    """
    The main function to run the ImageSubscriber node.

    Initializes rclpy, creates an instance of ImageSubscriber, and spins the node
    until it's shut down.

    Args:
        args: Command-line arguments.
    """
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
