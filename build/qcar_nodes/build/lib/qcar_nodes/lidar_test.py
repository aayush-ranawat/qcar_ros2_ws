import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import numpy as np

class LidarTester(Node):
    def __init__(self):
        super().__init__('lidar_tester')
        
        # Subscribe to the topic defined in your previous code
        self.subscription = self.create_subscription(
            LaserScan,
            '/qcar/scan',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        print("LIDAR Tester Running...")
        print("Stand on the LEFT or RIGHT of the car to test.")

    def listener_callback(self, msg):
        # Convert ranges to a numpy array for easier slicing
        ranges = np.array(msg.ranges)
        
        # Filter out "inf" (infinity) or 0.0 values which mean "no echo"
        # We replace them with a large number so they don't interfere with min() calculation
        ranges[ranges == 0] = 999.0
        ranges[np.isinf(ranges)] = 999.0
        angle_min=msg.angle_min
        angle_max=msg.angle_max
        increment=msg.angle_increment
        
        # --- define sectors based on array indices ---
        # Based on 360 measurements:
        # Index 0   = Front
        # Index 90  = Left
        # Index 180 = Back
        # Index 270 = Right
        
        # We look at a 60-degree cone on each side to be forgiving
        # Left Sector: Indices 60 to 120 (Centered on 90)
        sector = ranges[260-280]
        
        # Right Sector: Indices 240 to 300 (Centered on 270)
        

        # --- detection logic ---
        # Find the closest object in each sector
        min_left = np.min(sector)
       

        # Threshold distance (in meters)
        detection_threshold = 1.5 

        output = "Scanning... "

        if min_left < detection_threshold:
            output += f" [Object Detected: min dist is {min_left}] "
            output+=f"angle min is {angle_min} , angle_max is {angle_max} increments is {increment}"
        
        # if min_right < detection_threshold:
        #     output += " [Object Detected: RIGHT angle is 240-300] "

        # Only print if something is detected to keep console clean
        if "Detected" in output:
            self.get_logger().info(output)

def main(args=None):
    rclpy.init(args=args)
    node = LidarTester()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()