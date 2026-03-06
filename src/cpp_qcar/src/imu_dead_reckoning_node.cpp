#include <memory>
#include <chrono>
#include <cmath>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "geometry_msgs/msg/vector3_stamped.hpp"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_ros/transform_broadcaster.h"
#include "geometry_msgs/msg/transform_stamped.hpp"

using std::placeholders::_1;

class QCarDeadReckoning : public rclcpp::Node
{
public:
  QCarDeadReckoning() : Node("qcar_dead_reckoning_node")
  {
    // Subscribers
    imu_sub_ = this->create_subscription<sensor_msgs::msg::Imu>(
      "/qcar/imu", 10, std::bind(&QCarDeadReckoning::imu_callback, this, _1));
    
    cmd_sub_ = this->create_subscription<geometry_msgs::msg::Vector3Stamped>(
      "/qcar/user_command", 10, std::bind(&QCarDeadReckoning::cmd_callback, this, _1));

    // Publishers
    odom_pub_ = this->create_publisher<nav_msgs::msg::Odometry>("/imu_filtered", 10);
    tf_broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(this);

    // Initialize State
    x_ = 0.0; y_ = 0.0; theta_ = 0.0;
    vx_ = 0.0; vy_ = 0.0;
    cmd_velocity_ = 0.0;
    
    last_timestamp_ = this->now();
    RCLCPP_INFO(this->get_logger(), "QCar Dead Reckoning with ZUPT Started");
  }

private:
  void cmd_callback(const geometry_msgs::msg::Vector3Stamped::SharedPtr msg)
  {
    cmd_velocity_ = msg->vector.x;
  }

  void imu_callback(const sensor_msgs::msg::Imu::SharedPtr msg)
  {
    rclcpp::Time current_time = msg->header.stamp;
    double dt = (current_time - last_timestamp_).seconds();
    
    if (dt <= 0 || dt > 0.5) {
      last_timestamp_ = current_time;
      return;
    }

    // 1. Heading Integration
    double wz = msg->angular_velocity.z;
    theta_ += wz * dt;

    // 2. Zero Velocity Update (ZUPT) Logic
    if (std::abs(cmd_velocity_) < 0.001) {
      // Car is commanded to stop: Reset integrated velocities to kill drift
      vx_ = 0.0;
      vy_ = 0.0;
    } else {
      // Car is moving: Integrate acceleration
      double ax = msg->linear_acceleration.x;
      double ay = msg->linear_acceleration.y;

      // Transform local acceleration to global frame
      double ax_global = ax * cos(theta_) - ay * sin(theta_);
      double ay_global = ax * sin(theta_) + ay * cos(theta_);

      vx_ += ax_global * dt;
      vy_ += ay_global * dt;

      // Optional: Velocity Blending/Clamping
      // If the integrated velocity differs too much from cmd_velocity, 
      // we can nudge it back to keep it realistic.
      double current_speed = std::sqrt(vx_*vx_ + vy_*vy_);
      if (current_speed > 0.001) {
          double scale = std::abs(cmd_velocity_) / current_speed;
          // Apply a gentle correction factor (Alpha) to blend measurements
          double alpha = 0.1; 
          vx_ = vx_ * (1.0 - alpha) + (vx_ * scale) * alpha;
          vy_ = vy_ * (1.0 - alpha) + (vy_ * scale) * alpha;
      }
    }

    // 3. Position Integration
    x_ += vx_ * dt;
    y_ += vy_ * dt;

    last_timestamp_ = current_time;
    publish_data(msg->header.stamp);
  }

  void publish_data(const rclcpp::Time & stamp)
  {
    tf2::Quaternion q;
    q.setRPY(0, 0, theta_);

    auto odom_msg = nav_msgs::msg::Odometry();
    odom_msg.header.stamp = stamp;
    odom_msg.header.frame_id = "odom";
    odom_msg.child_frame_id = "base_link";
    odom_msg.pose.pose.position.x = x_;
    odom_msg.pose.pose.position.y = y_;
    odom_msg.pose.pose.orientation.x = q.x();
    odom_msg.pose.pose.orientation.y = q.y();
    odom_msg.pose.pose.orientation.z = q.z();
    odom_msg.pose.pose.orientation.w = q.w();
    odom_msg.twist.twist.linear.x = vx_;
    odom_msg.twist.twist.linear.y = vy_;
    odom_pub_->publish(odom_msg);

    geometry_msgs::msg::TransformStamped t;
    t.header.stamp = stamp;
    t.header.frame_id = "odom";
    t.child_frame_id = "base_link";
    t.transform.translation.x = x_;
    t.transform.translation.y = y_;
    t.transform.rotation.x = q.x();
    t.transform.rotation.y = q.y();
    t.transform.rotation.z = q.z();
    t.transform.rotation.w = q.w();
    tf_broadcaster_->sendTransform(t);
  }

  double x_, y_, theta_, vx_, vy_, cmd_velocity_;
  rclcpp::Time last_timestamp_;
  rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr imu_sub_;
  rclcpp::Subscription<geometry_msgs::msg::Vector3Stamped>::SharedPtr cmd_sub_;
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_pub_;
  std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<QCarDeadReckoning>());
  rclcpp::shutdown();
  return 0;
}
