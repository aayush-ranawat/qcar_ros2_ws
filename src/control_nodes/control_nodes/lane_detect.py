#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from rclpy.qos import QoSHistoryPolicy, QoSDurabilityPolicy
import numpy as np
import cv2
import time

from lane_detection.python.lane_detect import *

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar ImageViewer Node
class lane_detect(Node):
    def __init__(self):
        super().__init__('lane_detect')

        # test out making custom QoS profile:
        self.qcar_qos_profile = QoSProfile(
                reliability   = QoSReliabilityPolicy.BEST_EFFORT,
                history       = QoSHistoryPolicy.KEEP_LAST,
                durability    = QoSDurabilityPolicy.VOLATILE,
                depth         = 10)
        
        # 1. Create the window first
        cv2.namedWindow("frame")

        # 2. Register mouse callback ONCE pointing to our new function
        cv2.setMouseCallback("frame", self.get_click_coordinates)

       
        
        # 3. Make the resize factor a class attribute so the callback can use it
        self.factor = 1
        
        topicName = "/qcar/csi_front"

         # start counter for time delta
        self.startTime = time.perf_counter()
        self.bridge    = CvBridge()
        
        self.subscription = self.create_subscription(CompressedImage,
                                                        str(topicName),
                                                        self.Compressed_Image_callback,
                                                        self.qcar_qos_profile)
        
    def Compressed_Image_callback(self, data):
        # Convert compressed image msg to cv2 format
        currentImage = self.bridge.compressed_imgmsg_to_cv2(data)

        # Display image using cv2
        self.Image_display(currentImage)

    def Image_display(self, currentFrame):
        self.frame = currentFrame


                # Define source and destination points
        srcPoints = np.array([[100, 100], [150, 100], [150, 150], [100, 150]], dtype=np.float32)
        dstPoints = np.array([[200, 200], [250, 200], [250, 250], [200, 250]], dtype=np.float32)

        # Compute homography matrix
        H, mask = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)

        height, width = self.frame.shape[:2]


        warped_frame = cv2.warpPerspective(self.frame, H, (width, height))

        warped_frame= cv2.resize(currentFrame,(int(640 * self.factor), int(480 * self.factor)), interpolation=cv2.INTER_AREA)

        




        

        

        

        # Use the class attribute self.factor for resizing
        small = cv2.resize(currentFrame, (int(640 * self.factor), int(480 * self.factor)), interpolation=cv2.INTER_AREA)

        

        cv2.imshow("frame", small)
        cv2.imshow("wraped_frame",warped_frame)
        cv2.waitKey(1)

    # 4. Define the active callback function for mouse events
    def get_click_coordinates(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and hasattr(self, 'frame') and self.frame is not None:
            
            # Scale coordinates back up to match the original image size
            orig_x = int(x / self.factor)
            orig_y = int(y / self.factor)

            # Log both the window coordinates and the true image coordinates
            self.get_logger().info(f"Clicked Window: (x={x}, y={y}) | Original Frame: (x={orig_x}, y={orig_y})")

            # Optional: Keep the HSV/BGR extraction if you still need it
            # bgr = self.frame[orig_y, orig_x]
            # hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
            # self.get_logger().info(f"HSV at this point: {hsv}")

def main(args=None):
    rclpy.init(args=args)
    print("lane detector started")
    lane_detect_node = lane_detect()
    rclpy.spin(lane_detect_node)

    lane_detect_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()