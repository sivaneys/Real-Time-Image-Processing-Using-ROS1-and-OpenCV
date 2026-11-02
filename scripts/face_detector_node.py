#!/usr/bin/env python3
"""
Real-Time Face Detection Node using ROS1 + OpenCV + cv_bridge
Subscribes to the TurtleBot3 (waffle_pi) simulated camera in Gazebo,
runs Haar cascade face detection on each frame, displays the result,
and republishes the annotated image on a new topic.
"""

import rospy
import cv2
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image


class FaceDetector:
    def __init__(self):
        rospy.init_node('face_detector_node', anonymous=True)

        self.bridge = CvBridge()

        # Subscribe to the Gazebo-simulated camera topic
        self.image_sub = rospy.Subscriber(
            '/camera/rgb/image_raw', Image, self.image_callback)

        # Publish the annotated (detected) image on a new topic
        self.image_pub = rospy.Publisher(
            '/detected_image', Image, queue_size=1)

        # Load OpenCV's built-in Haar cascade classifier
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        rospy.loginfo("Face detector node started — waiting for camera frames...")

    def image_callback(self, msg):
        # Convert ROS Image message -> OpenCV image (numpy array)
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            rospy.logerr(f"cv_bridge conversion failed: {e}")
            return

        # Detection works best on grayscale images
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )

        # Draw a bounding box around each detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if len(faces) > 0:
            rospy.loginfo(f"Detected {len(faces)} face(s) in current frame")

        # Show the live annotated feed in a window
        cv2.imshow("TurtleBot3 Camera - Face Detection", cv_image)
        cv2.waitKey(1)

        # Convert back to ROS Image message and publish the result
        try:
            out_msg = self.bridge.cv2_to_imgmsg(cv_image, "bgr8")
            self.image_pub.publish(out_msg)
        except CvBridgeError as e:
            rospy.logerr(f"cv_bridge re-conversion failed: {e}")

    def run(self):
        rospy.spin()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        detector = FaceDetector()
        detector.run()
    except rospy.ROSInterruptException:
        pass
