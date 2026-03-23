#include <memory>
#include <string>
#include <vector>

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/compressed_image.hpp"
#include "cv_bridge/cv_bridge.h"
#include <opencv2/opencv.hpp>

class LaneDetect : public rclcpp::Node {
public:
    LaneDetect() : Node("lane_detect") {
        // Define QoS Profile: Best Effort, Keep Last 10, Volatile
        auto qos = rclcpp::QoS(rclcpp::KeepLast(10));
        qos.best_effort();
        qos.durability_volatile();

        // Initialize OpenCV Windows
        cv::namedWindow("frame", cv::WINDOW_AUTOSIZE);
        cv::namedWindow("warped_frame", cv::WINDOW_AUTOSIZE);

        // Set Mouse Callback
        // In C++, we pass 'this' as the userdata pointer to access class members
        cv::setMouseCallback("frame", &LaneDetect::onMouseStatic, this);

        std::string topic_name = "/qcar/csi_front";

        subscription_ = this->create_subscription<sensor_msgs::msg::CompressedImage>(
            topic_name, qos,
            std::bind(&LaneDetect::compressedImageCallback, this, std::placeholders::_1));

        RCLCPP_INFO(this->get_logger(), "Lane detector C++ node started");
    }

private:
    // Static wrapper for OpenCV mouse callback
    static void onMouseStatic(int event, int x, int y, int flags, void* userdata) {
        auto* instance = static_cast<LaneDetect*>(userdata);
        instance->getClickCoordinates(event, x, y);
    }

    void getClickCoordinates(int event, int x, int y) {
        if (event == cv::EVENT_LBUTTONDOWN && !current_frame_.empty()) {
            int orig_x = static_cast<int>(x / factor_);
            int orig_y = static_cast<int>(y / factor_);

            RCLCPP_INFO(this->get_logger(), "Clicked Window: (x=%d, y=%d) | Original Frame: (x=%d, y=%d)", 
                        x, y, orig_x, orig_y);
        }
    }

    void compressedImageCallback(const sensor_msgs::msg::CompressedImage::SharedPtr msg) {
        try {
            // Decode compressed image to BGR
            cv_bridge::CvImagePtr cv_ptr = cv_bridge::toCvCopy(msg, "bgr8");
            current_frame_ = cv_ptr->image;

            processAndDisplay();
        } catch (cv_bridge::Exception& e) {
            RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
        }
    }

    void processAndDisplay() {
        if (current_frame_.empty()) return;

        // Define Points for Homography
        std::vector<cv::Point2f> srcPoints = {{32 , 331}, {673, 321}, {177,279}, {499,276} , {240 ,259} , {439,254}};
        std::vector<cv::Point2f> dstPoints = {{220,470}, {420, 470}, {220,350}, {420 , 350 }, {220 , 230 } , {420 , 230}};

        // Compute Homography
        cv::Mat H = cv::findHomography(srcPoints, dstPoints, cv::RANSAC, 5.0);

        // Warp Perspective
        cv::Mat warped_frame;
        cv::warpPerspective(current_frame_, warped_frame, H, current_frame_.size());

        // Resize for display
        cv::Mat small, warped_resized;
        cv::resize(current_frame_, small, cv::Size(640 * factor_, 480 * factor_), 0, 0, cv::INTER_AREA);
        cv::resize(warped_frame, warped_resized, cv::Size(640 * factor_, 480 * factor_), 0, 0, cv::INTER_AREA);

        cv::imshow("frame", small);
        cv::imshow("warped_frame", warped_resized);
        cv::waitKey(1);
    }

    // Member variables
    rclcpp::Subscription<sensor_msgs::msg::CompressedImage>::SharedPtr subscription_;
    cv::Mat current_frame_;
    double factor_ = 1.0;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LaneDetect>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}