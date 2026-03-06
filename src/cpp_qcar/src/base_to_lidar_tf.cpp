#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "tf2_ros/static_transform_broadcaster.h"

class BaseToLidarTF : public rclcpp::Node
{
public:
  BaseToLidarTF() : Node("base_to_lidar_tf")
  {
    static_broadcaster_ =
      std::make_shared<tf2_ros::StaticTransformBroadcaster>(this);

    geometry_msgs::msg::TransformStamped transform;

    transform.header.stamp = this->get_clock()->now();
    transform.header.frame_id = "base_link";
    transform.child_frame_id = "lidar";

    // 🔧 Translation (meters)
    transform.transform.translation.x = 0.20;
    transform.transform.translation.y = 0.0;
    transform.transform.translation.z = 0.15;

    // 🔄 Rotation (Quaternion: no rotation)
    transform.transform.rotation.x = 0.0;
    transform.transform.rotation.y = 0.0;
    transform.transform.rotation.z = 0.0;
    transform.transform.rotation.w = 1.0;

    static_broadcaster_->sendTransform(transform);

    RCLCPP_INFO(this->get_logger(),
                "Published static TF: base_link -> lidar");
  }

private:
  std::shared_ptr<tf2_ros::StaticTransformBroadcaster> static_broadcaster_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<BaseToLidarTF>());
  rclcpp::shutdown();
  return 0;
}

