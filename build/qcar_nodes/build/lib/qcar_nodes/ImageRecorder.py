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
import os
from datetime import datetime

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar ImageRecorder Node

class ImageRecorder(Node):
    def __init__(self, topicName, imageType):
        super().__init__('image_recorder',
        allow_undeclared_parameters=True,
        automatically_declare_parameters_from_overrides=True
        )

        # Create QoS profile
        self.qcar_qos_profile = QoSProfile(
                reliability   = QoSReliabilityPolicy.BEST_EFFORT,
                history      = QoSHistoryPolicy.KEEP_LAST,
                durability   = QoSDurabilityPolicy.VOLATILE,
                depth        = 10)

        print("Subscribing to: {}".format(topicName))

        # Initialize variables
        self.startTime = time.perf_counter()
        self.bridge = CvBridge()
        self.recording = False
        self.video_writer = None
        
        # Create recordings directory if it doesn't exist
        self.recordings_dir = "recordings"
        if not os.path.exists(self.recordings_dir):
            os.makedirs(self.recordings_dir)

        # Subscribe to image topic
        if imageType == "CompressedImage":
            self.subscription = self.create_subscription(CompressedImage,
                                                        str(topicName),
                                                        self.Compressed_Image_callback,
                                                        self.qcar_qos_profile)
        elif imageType == "Image":
            self.subscription = self.create_subscription(Image,
                                                        str(topicName),
                                                        self.Image_callback,
                                                        self.qcar_qos_profile)
        else:
            print("Incorrect topic type!")

    def start_recording(self, frame_size):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.recordings_dir, f"recording_{timestamp}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = 30.0
        self.video_writer = cv2.VideoWriter(filename, fourcc, fps, frame_size)
        self.recording = True
        print(f"Started recording to {filename}")

    def stop_recording(self):
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
            self.recording = False
            print("Stopped recording")

    def Compressed_Image_callback(self, data):
        currentImage = self.bridge.compressed_imgmsg_to_cv2(data)
        self.process_frame(currentImage)

    def Image_callback(self, data):
        currentImage = self.bridge.imgmsg_to_cv2(data)
        self.process_frame(currentImage)

    def process_frame(self, currentFrame):
        time2 = time.perf_counter()
        timeDelta = time2 - self.startTime
        framesPerSecond = str(1/timeDelta)

        # Image information
        imageInfo = str(np.shape(currentFrame))

        # Text settings for open cv
        fpsCoordinate = (50, 50)
        font = cv2.FONT_HERSHEY_PLAIN
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2

        # Add recording status to display
        status = "REC" if self.recording else "STOP"
        status_color = (0, 0, 255) if self.recording else (0, 255, 0)
        cv2.putText(currentFrame, status, (50, 80), font, fontScale, status_color, thickness, cv2.LINE_AA)

        text = framesPerSecond + str(" ") + imageInfo
        image = cv2.putText(currentFrame, text, fpsCoordinate, font, fontScale, color, thickness, cv2.LINE_AA)

        # Save frame if recording
        if self.recording and self.video_writer is not None:
            self.video_writer.write(currentFrame)

        cv2.imshow("Camera Video Stream", image)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):  # Press 'r' to start/stop recording
            if not self.recording:
                self.start_recording((currentFrame.shape[1], currentFrame.shape[0]))
            else:
                self.stop_recording()
        elif key == ord('q'):  # Press 'q' to quit
            if self.recording:
                self.stop_recording()
            cv2.destroyAllWindows()
            rclpy.shutdown()

        self.startTime = time2

#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Main

def main(args=None):
    rclpy.init(args=args)

    # Prompt the user for camera topic and type
    topic_name = input("Please input the name of the image node you will like to subscribe to (example: /qcar/csi_left): ")
    print("Please input image message type.\nFor compressed image topic use: CompressedImage, for regular Image topic use: Image")
    Image_type = input("Image message type: ")
    
    image_recorder = ImageRecorder(topic_name, Image_type)
    
    print("\nControls:")
    print("Press 'r' to start/stop recording")
    print("Press 'q' to quit")

    while rclpy.ok():
        try:
            rclpy.spin_once(image_recorder)
        except KeyboardInterrupt:
            print("\nDone")
            break
    
    image_recorder.destroy_node()
    rclpy.shutdown()

#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run

if __name__ == '__main__':
    main()
#endregion 