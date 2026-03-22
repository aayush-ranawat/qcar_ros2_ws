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
from rclpy.duration import Duration


from lane_detection.python.lane_detect import *

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge

from geometry_msgs.msg import Vector3Stamped

import math
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar ImageViewer Node
class lane_detect(Node):
    def __init__(self):
        super().__init__('lane_detect')


        self.cmdPublisher = self.create_publisher(Vector3Stamped,
												'/qcar/user_command', 10)


        self.prev_delta = 0.0

        self.max_steering_rate = 2.0   # Maximum allowed change in radians per second
        self.dt = 0.1                  # Loop time in seconds (e.g., 10Hz timer)
        self.max_change_per_tick = self.max_steering_rate * self.dt



      



                # Define source and destination points
        srcPoints = np.array([[32 , 331], [673, 321], [177,279], [499,276] , [240 ,259] , [439,254]], dtype=np.float32)
        dstPoints = np.array([[220,470], [420, 470], [220,350], [420 , 350 ], [220 , 230 ] , [420 , 230]], dtype=np.float32)
                 # Compute homography matrix
        self.H, mask = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)

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

        height, width = self.frame.shape[:2]


        

        lane=Colour_based_lane_detection(currentFrame,resolution=(480,640))

        left,right,tot,hsv=lane.masked_affine()
        left_am,right_am=lane.extract_lane_parameters()

        wrap_left=cv2.warpPerspective(left_am,self.H,(width,height))

        wrap_right=cv2.warpPerspective(right_am,self.H,(width,height))

        left=np.where(wrap_left>0)
        right=np.where(wrap_right>0)
    
        # print(lane.parameter_l,lane.parameter_r)

        # mark=lane.visulaise()

        

        


        warped_frame = cv2.warpPerspective(self.frame,self.H, (width, height))


        left_points = np.column_stack((left[1], left[0]))

        right_points= np.column_stack((left[1], left[0]))


        

        

                # 2. Fit the line
        # Note: OpenCV returns these as 1D arrays, so we unpack them like this:
        [vx], [vy], [x], [y] = cv2.fitLine(left_points, cv2.DIST_L2, 0, 0.01, 0.01)


        [vx_r], [vy_r], [x_r], [y_r] = cv2.fitLine(right_points, cv2.DIST_L2, 0, 0.01, 0.01)

        vx , vy , x , y = (vx+vx_r)/2 , (vy+vy_r)/2 , (x+x_r)/2 , (y+y_r)/2

        




        # 3. Calculate start and end points to draw the line
        # We use a large multiplier (like 1000) for 't' to ensure the line stretches off the screen


        # try: 
        #     lefty = int((-x * vy / vx) + y)
        #     righty = int(((warped_frame.shape[1] - x) * vy / vx) + y)

        #     point1 = (0, lefty)
        #     point2 = (warped_frame.shape[1] - 1, righty)

        # except:

        #     return




        point= (320, 465)

        line_coff= ( vy , -vx , vx * y - vy * x)

        # print(line_coff)

        


        d = self.distance_standard_form(point , line_coff)

        if math.isnan(vy):
            d= 0

        # self.get_logger().info(f"the distance is {d/4}")

        angle = np.rad2deg(np.arctan2(vy,vx))



        


        


        if angle>=0:
            theta_e= 90 - angle
        
        else:
            theta_e= -(90 + angle)

        theta_e = np.deg2rad(theta_e)
            

        # self.get_logger().info(f"theta_e is in degree is {(theta_e)}")


      
        # self.get_logger().info(f"theta_e is in degree is {np.rad2deg(theta_e)}")
        # self.get_logger().info(f"lateral error is  in degree is {lateral_e}")



        k_stanley=0.001
        lateral_e = d/4 - 25

        f=0.1

        if abs(lateral_e) > 7 and abs(theta_e)< np.pi/12:
            k_stanley=0.04

            f=0.01



        

        

        


        # # 2. Apply Slew Rate Limiter
        # delta_change = delta - self.prev_delta
        
        # # Clamp the change to our maximum allowed physical limit
        # delta_change = np.clip(delta_change, -self.max_change_per_tick, self.max_change_per_tick)
        
        # # Calculate the final smoothed angle
        # smoothed_delta = self.prev_delta + delta_change
        
        # # 3. Save current angle for the next loop iteration
        # self.prev_delta = smoothed_delta

        delta = f*theta_e + np.arctan( k_stanley * lateral_e /(1))


      
        # delta = np.arctan( k_stanley * lateral_e /(velocity))


        # print(f"theta_e is {np.rad2deg(theta_e)} and arc term is {np.rad2deg(np.arctan( k_stanley * lateral_e /(1)))}")

    


        



        

        



         




        

        velocity=0.06
     
        self.throttleCommand, self.steeringCommand=     velocity ,   delta
        
        self.userCommand  = [self.throttleCommand, self.steeringCommand]

        commandPublisher = Vector3Stamped()
        commandPublisher.header.stamp = self.get_clock().now().to_msg()
        commandPublisher.header.frame_id = 'my_command_input'
        commandPublisher.vector.x = float(self.userCommand[0])
        commandPublisher.vector.y = float(self.userCommand[1])


        self.cmdPublisher.publish(commandPublisher)









        # 4. Draw the fitted line
        # cv2.line(warped_frame, point1, point2, (0, 255, 0), 2)



        # cv2.line(warped_frame, (220,470), (220,230), (0, 255, 0) , 3)
        # cv2.line(warped_frame, (420,470), (420,230), (0,0, 255) , 3)



        # warped_frame= cv2.resize(right_am,(int(640 * self.factor), int(480 * self.factor)), interpolation=cv2.INTER_AREA)

        




        

        

        

        # # # Use the class attribute self.factor for resizing
        # # small = cv2.resize(currentFrame, (int(640 * self.factor), int(480 * self.factor)), interpolation=cv2.INTER_AREA)

        

        # # cv2.imshow("frame", small)
        # cv2.imshow("wraped_frame",warped_frame)
        # cv2.waitKey(1)



    def distance_standard_form(self,point, line_coeffs):
        """
        point: a tuple (x0, y0)
        line_coeffs: a tuple (A, B, C) representing Ax + By + C = 0
        """
        x0, y0 = point
        A, B, C = line_coeffs
        
        numerator = (A * x0 + B * y0 + C)
        denominator = np.sqrt(A**2 + B**2)
        
        return numerator / denominator





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