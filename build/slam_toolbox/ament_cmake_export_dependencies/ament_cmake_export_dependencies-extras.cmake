# generated from ament_cmake_export_dependencies/cmake/ament_cmake_export_dependencies-extras.cmake.in

set(_exported_dependencies "builtin_interfaces;geometry_msgs;std_msgs;action_msgs;nav_msgs;rclcpp;message_filters;nav_msgs;sensor_msgs;tf2;tf2_ros;visualization_msgs;pluginlib;nav2_map_server;tf2_geometry_msgs;tf2_sensor_msgs;std_msgs;std_srvs;builtin_interfaces")

find_package(ament_cmake_libraries QUIET REQUIRED)

# find_package() all dependencies
# and append their DEFINITIONS INCLUDE_DIRS, LIBRARIES, and LINK_FLAGS
# variables to slam_toolbox_DEFINITIONS, slam_toolbox_INCLUDE_DIRS,
# slam_toolbox_LIBRARIES, and slam_toolbox_LINK_FLAGS.
# Additionally collect the direct dependency names in
# slam_toolbox_DEPENDENCIES as well as the recursive dependency names
# in slam_toolbox_RECURSIVE_DEPENDENCIES.
if(NOT _exported_dependencies STREQUAL "")
  find_package(ament_cmake_core QUIET REQUIRED)
  set(slam_toolbox_DEPENDENCIES ${_exported_dependencies})
  set(slam_toolbox_RECURSIVE_DEPENDENCIES ${_exported_dependencies})
  set(_libraries)
  foreach(_dep ${_exported_dependencies})
    if(NOT ${_dep}_FOUND)
      find_package("${_dep}" QUIET REQUIRED)
    endif()
    if(${_dep}_DEFINITIONS)
      list_append_unique(slam_toolbox_DEFINITIONS "${${_dep}_DEFINITIONS}")
    endif()
    if(${_dep}_INCLUDE_DIRS)
      list_append_unique(slam_toolbox_INCLUDE_DIRS "${${_dep}_INCLUDE_DIRS}")
    endif()
    if(${_dep}_LIBRARIES)
      list(APPEND _libraries "${${_dep}_LIBRARIES}")
    endif()
    if(${_dep}_LINK_FLAGS)
      list_append_unique(slam_toolbox_LINK_FLAGS "${${_dep}_LINK_FLAGS}")
    endif()
    if(${_dep}_RECURSIVE_DEPENDENCIES)
      list_append_unique(slam_toolbox_RECURSIVE_DEPENDENCIES "${${_dep}_RECURSIVE_DEPENDENCIES}")
    endif()
    if(_libraries)
      ament_libraries_deduplicate(_libraries "${_libraries}")
      list(APPEND slam_toolbox_LIBRARIES "${_libraries}")
    endif()
  endforeach()
endif()
