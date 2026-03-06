import rclpy
from rclpy.node import Node

import numpy as np
from sensor_msgs.msg import LaserScan
#from ackermann_msgs.msg import AckermannDriveStamped
from geometry_msgs.msg import Vector3Stamped



class WallFollow(Node):
    """ 
    Implement Wall Following on the car
    """
    def __init__(self):
        super().__init__('wall_follow_node')

        lidarscan_topic = 'qcar/scan'
        
        # Create Subscriber and Publisher
        self.scan_sub = self.create_subscription(
            LaserScan, 
            lidarscan_topic, 
            self.scan_callback, 
            10)
            
        self.qcar_command_pub= self.create_publisher(
            Vector3Stamped,
			'/qcar/user_command', 10)


        # PID Gains (Tune these!)
        self.kp = 0.7  # Proportional gain
        self.kd = 0.3  # Derivative gain (dampening)
        self.ki = 0.0  # Integral gain (usually 0 for fast racing)

        # PID History
        self.integral = 0.0
        self.prev_error = 0.0
        self.error = 0.0

        # Wall Following Parameters
        self.desired_distance = 1.0  # Meters from the wall
        self.lookahead_dist = 0.5    # Lookahead for stability (meters)
        
        # Rays to use (Left wall following)
        # 90 degrees (strictly left) and 50 degrees (slightly forward-left)
        self.angle_b = np.radians(315) 
        self.angle_a = np.radians(270) 

    def get_range(self, range_data, angle_data):
        """
        Simple helper to return the corresponding range measurement at a given angle.
        """
        # Convert angle to index
        # angle = angle_min + index * angle_increment
        # index = (angle - angle_min) / angle_increment
        
        angle_min = angle_data['min']
        angle_inc = angle_data['inc']
        print(f"angle min is {np.degrees(angle_min)} and increment is {np.degrees(angle_inc)}")
        
        idx = int((angle_data['target_angle'] - angle_min) / angle_inc)
        
        # Bound check the index
        if idx < 0 or idx >= len(range_data):
            return 0.0

        dist = range_data[idx]

        # Handle NaNs and Infs
        if np.isnan(dist) or np.isinf(dist):
            return 10.0 # Return a large number if no wall is seen
            
        return dist

    def get_error(self, range_data, angle_info):
        """
        Calculates the error to the wall using the Two-Point method.
        """
        
        # 1. Get ranges for our two rays
        # Ray B is usually 90 deg (left), Ray A is roughly 45-50 deg
        angle_info['target_angle'] = self.angle_b
        dist_b = self.get_range(range_data, angle_info)
        
        angle_info['target_angle'] = self.angle_a
        dist_a = self.get_range(range_data, angle_info)

        # theta is the angle between the two rays
        theta = self.angle_b - self.angle_a
        print(f"the angle a is {np.degrees(self.angle_a)}  diatance a is  {dist_a}")
        print(f"the angle b is {np.degrees(self.angle_b)} and diatance b is  {dist_b}")

        # 2. Calculate alpha (orientation of car relative to wall)
        # Formula: alpha = arctan( (a * cos(theta) - b) / (a * sin(theta)) )
        numerator = (dist_a * np.cos(theta)) - dist_b
        denominator = dist_a * np.sin(theta)
        
        # Avoid division by zero
        if abs(denominator) < 0.001:
            return self.prev_error # maintain previous state if data is bad
            
        alpha = np.arctan(numerator / denominator)

        # 3. Calculate current distance to wall (Dt)
        # Dt = b * cos(alpha)
        Dt = dist_b * np.cos(alpha)

        # 4. Project future distance (Lookahead)
        # We control based on where the car WILL be, not where it is.
        # D_t+1 = Dt + L * sin(alpha)
        D_next = Dt + self.lookahead_dist * np.sin(alpha)

        # 5. Calculate Error
        # Error = Desired - Actual
        # If we are too close (D_next < desired), error is positive -> steer right
        # If we are too far (D_next > desired), error is negative -> steer left
        # Note: Sign depends on which wall. For LEFT wall:
        # Error positive = we are far away = turn left (positive steering)
        # Error negative = we are too close = turn right (negative steering)
        
        error = self.desired_distance - D_next
        return error

    def pid_control(self, error, velocity):
        """
        Based on the calculated error, publish vehicle control
        """
        # Calculate Time Step (approximation)
        # Ideally use dt from clock, but standard PID usually assumes fixed rate
        
        # P Term
        p_term = self.kp * error
        
        # D Term
        d_term = self.kd * (error - self.prev_error)
        
        # I Term
        self.integral += error
        i_term = self.ki * self.integral

        # Total Steering Angle
        angle = p_term + d_term + i_term
        
        # Store error for next loop
        self.prev_error = error


        

        # # Create and Publish Message
        # drive_msg = AckermannDriveStamped()
        
        # Convert steering angle (PID output) to actual steering command
        # Note: Depending on your car's coordinate system:
        # Left wall follow: If error > 0 (too far), we need +angle (left).
        # If error < 0 (too close), we need -angle (right).
        # The equation error = desired - actual gives:
        # 1.0 - 0.5 = 0.5 (Too close). We need Right turn (-). 
        # So we likely need to flip the sign or swap terms in get_error.
        # Let's verify: 
        #   Target=1m, Actual=1.5m. Error = -0.5. We are too far. Need Left turn (+).
        #   So Error (-0.5) needs to map to (+0.5).
        #   Therefore: steering_angle = -1 * (P+I+D)
        
        steering_angle = -angle 
        
        # Clamp Steering Angle (e.g., -0.4 to 0.4 radians)
        max_steer = 0.4
        steering_angle = np.clip(steering_angle, -max_steer, max_steer)

        # drive_msg.drive.steering_angle = steering_angle
        # drive_msg.drive.speed = velocity
        
        # self.drive_pub.publish(drive_msg)


        commandPublisher = Vector3Stamped()
        commandPublisher.header.stamp = self.get_clock().now().to_msg()
        commandPublisher.header.frame_id = 'command_input'
        commandPublisher.vector.x = float(velocity)
        commandPublisher.vector.y = float(steering_angle)
        self.qcar_command_pub.publish(commandPublisher)

    def scan_callback(self, msg):
        """
        Callback function for LaserScan messages. 
        """
        # Pack angle data for helper functions
        angle_info = {
            'min': msg.angle_min,
            'inc': msg.angle_increment,
            'target_angle': 0.0 # Placeholder
        }
        
        # 1. Calculate Error
        error = self.get_error(msg.ranges, angle_info)
        
        # 2. Calculate Velocity
        # Simple logic: Go fast on straight (low error), slow on turns (high error)
        if abs(error) < 0.1: # roughly 10cm error
            velocity = 0.1   # Fast
        elif abs(error) < 0.3:
            velocity = 0.1   # Medium
        else:
            velocity = 0.08   # Slow (Cornering)

        # 3. Actuate
        self.pid_control(error, velocity)


def main(args=None):
    rclpy.init(args=args)
    print("WallFollow Initialized")
    wall_follow_node = WallFollow()
    rclpy.spin(wall_follow_node)

    wall_follow_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

