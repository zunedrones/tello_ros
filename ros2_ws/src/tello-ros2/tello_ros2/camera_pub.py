import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from tello_zune.tello_zune import TelloZune


class TelloCameraPublisher(Node):
    def __init__(self):
        super().__init__('tello_camera_publisher')
        self.declare_parameter('resolution', (960, 720))
        resolution = self.get_parameter('resolution').value
        self.declare_parameter('topic', '/tello/camera')
        topic = self.get_parameter('topic').value
        self.declare_parameter('publish_rate', 30.0)
        rate = self.get_parameter('publish_rate').value

        self.publisher = self.create_publisher(Image, topic, 10)
        self.bridge = CvBridge()

        self.tello = TelloZune()
        self.tello.start_tello()

        self.timer = self.create_timer(1.0 / rate, self.publish_frame)
        self.get_logger().info(
            f'Publishing Tello camera at {resolution[0]}x{resolution[1]} '
            f'on {topic}'
        )

    def publish_frame(self):
        img = self.tello.get_frame()
        if img is None:
            self.get_logger().warn('No frame received from Tello', throttle_duration_sec=5.0)
            return
        img = cv2.resize(img, (960, 720), interpolation=cv2.INTER_LINEAR)

        self.publisher.publish(
            self.bridge.cv2_to_imgmsg(img, encoding='bgr8')
        )

    def destroy_node(self):
        self.tello.end_tello()
        cv2.destroyAllWindows()
        return super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = TelloCameraPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
