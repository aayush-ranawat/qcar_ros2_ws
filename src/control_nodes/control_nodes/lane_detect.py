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


from sensor_msgs.msg import Image,CompressedImage
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
                history 	  = QoSHistoryPolicy.KEEP_LAST,
                durability    = QoSDurabilityPolicy.VOLATILE,
                depth 		  = 10)
        


        cv2.namedWindow("frame")

        # # Register mouse callback ONCE
        # cv2.setMouseCallback("frame", self.get_hsv_value)

        self.c=0
        

        topicName="/qcar/csi_front"
        # topicName="/qcar/rgbd_color"


         # start counter for time delta
        self.startTime = time.perf_counter()
        self.bridge    = CvBridge()
        


        self.subscription = self.create_subscription(CompressedImage,
                                                        str(topicName),
                                                        self.Compressed_Image_callback,
                                                        self.qcar_qos_profile)
        


    def Compressed_Image_callback(self,data):

        # Convert compressed image msg to cv2 format
        currentImage = self.bridge.compressed_imgmsg_to_cv2(data)

        #Display image using cv2
        self.Image_display(currentImage)



    def Image_display(self, currentFrame):
        # print(currentFrame.shape)
        self.frame=currentFrame

        if self.c==0:
            cv2.imwrite("lane_homography.png",currentFrame)
            self.c+=1

        
        # lane=Colour_based_lane_detection(currentFrame,resolution=(480,640))

        # left,right,tot,hsv=lane.masked_affine()
        # lane.extract_lane_parameters()
    
        # # print(lane.parameter_l,lane.parameter_r)

        # mark=lane.visulaise()
        # # print(resized.shape)
        factor=0.2
        small = cv2.resize(currentFrame, (int(640*factor), int(480*factor)), interpolation=cv2.INTER_AREA)
        # mark = cv2.resize(mark, (int(640*factor), int(480*factor)), interpolation=cv2.INTER_AREA)

        cv2.imshow("frame", small)
       



        cv2.waitKey(1)


    # def get_hsv_value(self, event, x, y, flags, param):

    #     if event == cv2.EVENT_LBUTTONDOWN and self.frame is not None:

    #         bgr = self.frame[y, x]
    #         hsv = cv2.cvtColor(
    #             np.uint8([[bgr]]),
    #             cv2.COLOR_BGR2HSV
    #         )[0][0]

    #         self.get_logger().info(f"Clicked HSV: {hsv}")








def main(args=None):
    rclpy.init(args=args)
    print("lane detector started")
    lane_detect_node = lane_detect()
    rclpy.spin(lane_detect_node)

    lane_detect_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
