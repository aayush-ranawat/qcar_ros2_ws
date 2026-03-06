# CMake generated Testfile for 
# Source directory: /home/nvidia/ros2_ws/src/slam_toolbox
# Build directory: /home/nvidia/ros2_ws/build/slam_toolbox
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(lifelong_metrics_test "/usr/bin/python3" "-u" "/opt/ros/dashing/share/ament_cmake_test/cmake/run_test.py" "/home/nvidia/ros2_ws/build/slam_toolbox/test_results/slam_toolbox/lifelong_metrics_test.gtest.xml" "--package-name" "slam_toolbox" "--output-file" "/home/nvidia/ros2_ws/build/slam_toolbox/ament_cmake_gtest/lifelong_metrics_test.txt" "--command" "/home/nvidia/ros2_ws/build/slam_toolbox/lifelong_metrics_test" "--gtest_output=xml:/home/nvidia/ros2_ws/build/slam_toolbox/test_results/slam_toolbox/lifelong_metrics_test.gtest.xml")
set_tests_properties(lifelong_metrics_test PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/nvidia/ros2_ws/build/slam_toolbox/lifelong_metrics_test" TIMEOUT "60" WORKING_DIRECTORY "/home/nvidia/ros2_ws/src/slam_toolbox" _BACKTRACE_TRIPLES "/opt/ros/dashing/share/ament_cmake_test/cmake/ament_add_test.cmake;118;add_test;/opt/ros/dashing/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;81;ament_add_test;/opt/ros/dashing/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;88;ament_add_gtest_test;/home/nvidia/ros2_ws/src/slam_toolbox/CMakeLists.txt;175;ament_add_gtest;/home/nvidia/ros2_ws/src/slam_toolbox/CMakeLists.txt;0;")
subdirs("lib/karto_sdk")
subdirs("slam_toolbox__py")
subdirs("gtest")
