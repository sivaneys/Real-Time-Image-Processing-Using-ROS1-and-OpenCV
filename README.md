# Real-Time Image Processing Using ROS 1 and OpenCV

TurtleBot3 (waffle_pi) camera feed in Gazebo → `cv_bridge` → OpenCV Haar
cascade face detection → live annotated display + republished ROS topic.

## Prerequisites
- ROS 1 Noetic (Ubuntu 20.04, e.g. via WSL2)
- `turtlebot3`, `turtlebot3_msgs`, `turtlebot3_simulations` packages installed
- `python3-opencv` and `ros-noetic-cv-bridge` installed

## Setup

1. Copy this whole `image_processing_project` folder into your catkin
   workspace's `src/` directory:
   ```
   cp -r image_processing_project ~/catkin_ws/src/
   ```

2. Build the workspace:
   ```
   cd ~/catkin_ws
   catkin_make
   source devel/setup.bash
   ```

3. Make sure the node script is executable (should already be, but just in case):
   ```
   chmod +x ~/catkin_ws/src/image_processing_project/scripts/face_detector_node.py
   ```

## Run

Single command — launches Gazebo with TurtleBot3 **and** starts detection together:
```
export TURTLEBOT3_MODEL=waffle_pi
roslaunch image_processing_project face_detection.launch
```

Or run them separately in two terminals if you want to watch startup logs individually:
```
# Terminal 1
export TURTLEBOT3_MODEL=waffle_pi
roslaunch turtlebot3_gazebo turtlebot3_world.launch

# Terminal 2
rosrun image_processing_project face_detector_node.py
```

## What you should see
- Gazebo opens with TurtleBot3 spawned in the world
- A second window ("TurtleBot3 Camera - Face Detection") shows the live
  camera feed from the robot
- Any face-shaped object the camera sees gets a green bounding box drawn
  around it in real time

## Useful checks
```
rostopic list                     # confirm /camera/rgb/image_raw exists
rostopic hz /camera/rgb/image_raw # confirm frames are actually publishing
rqt_image_view                    # view /detected_image topic separately
```

## Notes
- Default Gazebo worlds have no human-face models in them, so detection
  will show "0 faces" until something face-shaped is in view. Swap the
  cascade file or add a human/person model to the world to test detection.
- `scripts/face_detector_node.py` publishes the annotated frame on
  `/detected_image` so it can be viewed or recorded separately.
