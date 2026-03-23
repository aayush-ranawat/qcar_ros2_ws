#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/compressed_image.hpp>
#include <cv_bridge/cv_bridge.h>
#include <opencv2/opencv.hpp>

class LaneDetect : public rclcpp::Node {
public:
    LaneDetect() : Node("lane_detect"), factor(1.0) {
        // 1. Setup QoS Profile
        auto qos_profile = rclcpp::QoS(rclcpp::KeepLast(10));
        qos_profile.best_effort();
        qos_profile.durability_volatile();

        // 2. Initialize OpenCV Windows and Mouse Callback
        cv::namedWindow("frame");
        cv::setMouseCallback("frame", &LaneDetect::onMouseClick, this);

        // 3. Initialize Subscription
        std::string topic_name = "/qcar/csi_front";
        subscription_ = this->create_subscription<sensor_msgs::msg::CompressedImage>(
            topic_name,
            qos_profile,
            std::bind(&LaneDetect::compressedImageCallback, this, std::placeholders::_1)
        );

        RCLCPP_INFO(this->get_logger(), "Lane detector started");
    }

private:
    // Callback for receiving images
    void compressedImageCallback(const sensor_msgs::msg::CompressedImage::SharedPtr msg) {
        try {
            // Convert ROS CompressedImage to cv::Mat
            cv::Mat current_frame = cv_bridge::toCvCopy(msg, "bgr8")->image;
            this->frame_ = current_frame;
            processAndDisplay(current_frame);
        } catch (cv_bridge::Exception& e) {
            RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
        }
    }

    void processAndDisplay(cv::Mat& current_frame) {
        // Define source and destination points
        std::vector<cv::Point2f> srcPoints = {{32 , 331}, {673, 321}, {177,279}, {499,276} , {240 ,259} , {439,254}};
        std::vector<cv::Point2f> dstPoints = {{220,470}, {420, 470}, {220,350}, {420 , 350 }, {220 , 230 } , {420 , 230}};

        // Compute homography matrix
        cv::Mat H = cv::findHomography(srcPoints, dstPoints, cv::RANSAC, 5.0);

        int height = current_frame.rows;
        int width = current_frame.cols;

        // Perspective Warp
        cv::Mat warped_frame;
        cv::warpPerspective(current_frame, warped_frame, H, cv::Size(width, height));

        // Resize for display
        cv::Mat small;
        cv::resize(current_frame, small, cv::Size(), factor, factor, cv::INTER_AREA);

        cv::imshow("frame", small);
        cv::imshow("warped_frame", warped_frame);
        cv::waitKey(1);
    }

    // Static-style callback for OpenCV (must handle the 'this' pointer)
    static void onMouseClick(int event, int x, int y, int flags, void* userdata) {
        if (event == cv::EVENT_LBUTTONDOWN) {
            auto* node = reinterpret_cast<LaneDetect*>(userdata);
            if (!node->frame_.empty()) {
                int orig_x = static_cast<int>(x / node->factor);
                int orig_y = static_cast<int>(y / node->factor);

                RCLCPP_INFO(node->get_logger(), "Clicked Window: (x=%d, y=%d) | Original Frame: (x=%d, y=%d)", 
                            x, y, orig_x, orig_y);
            }
        }
    }

    // Members
    double factor;
    cv::Mat frame_;
    rclcpp::Subscription<sensor_msgs::msg::CompressedImage>::SharedPtr subscription_;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LaneDetect>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}