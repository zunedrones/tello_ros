# Tello ROS 2 Camera Capture

A small ROS 2 package that receives video from a DJI Tello drone and publishes
the frames as `sensor_msgs/msg/Image`. You can inspect the live stream or record
it to a ROS 2 bag for later playback and processing.

## Requirements

- Ubuntu with ROS 2 Humble installed and sourced.
- Python 3, OpenCV, and `cv_bridge` (install the ROS package
  `ros-humble-cv-bridge` if needed).
- The `tello-zune` Python package used by this project (`tello_zune` module).
- A DJI Tello and a computer with Wi-Fi. Connect the computer to the Tello's
  Wi-Fi network before starting the camera node.

## Build

Clone this repository and build the ROS 2 workspace:

```bash
git clone https://github.com/zunedrones/tello_ros.git
cd tello_ros/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

Source ROS 2 in each new terminal before sourcing the workspace:

```bash
source /opt/ros/humble/setup.bash
source /path/to/tello_ros/ros2_ws/install/setup.bash
```

If `rosdep` does not resolve `tello-zune` on your system, install the Python
package that provides the `tello_zune` module in the same Python environment
used by ROS 2.

## Capture and view the Tello image

Connect to the drone's Wi-Fi, then start the publisher:

```bash
ros2 run tello-ros2 camera_pub
```

The default image topic is **`/tello/camera`**, with message type
`sensor_msgs/msg/Image`. The node publishes BGR images at a target rate of
30 Hz, resizing frames to 960 × 720 pixels.

Check that the topic is available and receiving images:

```bash
ros2 topic list
ros2 topic info /tello/camera
ros2 topic hz /tello/camera
```

To display the stream in another terminal:

```bash
ros2 run rqt_image_view rqt_image_view /tello/camera
```

Stop the camera node with `Ctrl+C` when finished.

## Record and replay a bag

With the camera publisher running, open another sourced ROS 2 terminal and
record the image topic:

```bash
ros2 bag record /tello/camera
```

To choose the output directory name:

```bash
ros2 bag record -o tello_flight_01 /tello/camera
```

Stop recording with `Ctrl+C`. The bag will be saved in the current directory.
To replay it later, with the Tello disconnected if desired, run:

```bash
ros2 bag play tello_flight_01
```

The recorded images will again be published on `/tello/camera`. Inspect a bag
before playback with:

```bash
ros2 bag info tello_flight_01
```

Bag files can grow quickly, so ensure you have enough disk space. Bags are
ignored by Git in this repository; keep recordings locally or store them in a
dedicated data repository.

## ROS interface

| Name | Type | Description |
| --- | --- | --- |
| `/tello/camera` | `sensor_msgs/msg/Image` | Tello video frames (BGR, 960 × 720 by default) |

The node also declares `topic`, `publish_rate`, and `resolution` parameters.

## License

This project is licensed under the Apache-2.0 License; see [LICENSE](ros2_ws/src/tello-ros2/LICENSE).
