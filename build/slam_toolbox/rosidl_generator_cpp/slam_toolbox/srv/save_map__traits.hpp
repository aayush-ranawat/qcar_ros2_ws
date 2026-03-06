// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from slam_toolbox:srv/SaveMap.idl
// generated code does not contain a copyright notice

#ifndef SLAM_TOOLBOX__SRV__SAVE_MAP__TRAITS_HPP_
#define SLAM_TOOLBOX__SRV__SAVE_MAP__TRAITS_HPP_

#include "slam_toolbox/srv/save_map__struct.hpp"
#include <rosidl_generator_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

// Include directives for member types
// Member 'name'
#include "std_msgs/msg/string__traits.hpp"

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::SaveMap_Request>()
{
  return "slam_toolbox::srv::SaveMap_Request";
}

template<>
struct has_fixed_size<slam_toolbox::srv::SaveMap_Request>
  : std::integral_constant<bool, has_fixed_size<std_msgs::msg::String>::value> {};

template<>
struct has_bounded_size<slam_toolbox::srv::SaveMap_Request>
  : std::integral_constant<bool, has_bounded_size<std_msgs::msg::String>::value> {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::SaveMap_Response>()
{
  return "slam_toolbox::srv::SaveMap_Response";
}

template<>
struct has_fixed_size<slam_toolbox::srv::SaveMap_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<slam_toolbox::srv::SaveMap_Response>
  : std::integral_constant<bool, true> {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::SaveMap>()
{
  return "slam_toolbox::srv::SaveMap";
}

template<>
struct has_fixed_size<slam_toolbox::srv::SaveMap>
  : std::integral_constant<
    bool,
    has_fixed_size<slam_toolbox::srv::SaveMap_Request>::value &&
    has_fixed_size<slam_toolbox::srv::SaveMap_Response>::value
  >
{
};

template<>
struct has_bounded_size<slam_toolbox::srv::SaveMap>
  : std::integral_constant<
    bool,
    has_bounded_size<slam_toolbox::srv::SaveMap_Request>::value &&
    has_bounded_size<slam_toolbox::srv::SaveMap_Response>::value
  >
{
};

}  // namespace rosidl_generator_traits

#endif  // SLAM_TOOLBOX__SRV__SAVE_MAP__TRAITS_HPP_
