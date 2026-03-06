// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from slam_toolbox:srv/Pause.idl
// generated code does not contain a copyright notice

#ifndef SLAM_TOOLBOX__SRV__PAUSE__TRAITS_HPP_
#define SLAM_TOOLBOX__SRV__PAUSE__TRAITS_HPP_

#include "slam_toolbox/srv/pause__struct.hpp"
#include <rosidl_generator_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::Pause_Request>()
{
  return "slam_toolbox::srv::Pause_Request";
}

template<>
struct has_fixed_size<slam_toolbox::srv::Pause_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<slam_toolbox::srv::Pause_Request>
  : std::integral_constant<bool, true> {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::Pause_Response>()
{
  return "slam_toolbox::srv::Pause_Response";
}

template<>
struct has_fixed_size<slam_toolbox::srv::Pause_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<slam_toolbox::srv::Pause_Response>
  : std::integral_constant<bool, true> {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::Pause>()
{
  return "slam_toolbox::srv::Pause";
}

template<>
struct has_fixed_size<slam_toolbox::srv::Pause>
  : std::integral_constant<
    bool,
    has_fixed_size<slam_toolbox::srv::Pause_Request>::value &&
    has_fixed_size<slam_toolbox::srv::Pause_Response>::value
  >
{
};

template<>
struct has_bounded_size<slam_toolbox::srv::Pause>
  : std::integral_constant<
    bool,
    has_bounded_size<slam_toolbox::srv::Pause_Request>::value &&
    has_bounded_size<slam_toolbox::srv::Pause_Response>::value
  >
{
};

}  // namespace rosidl_generator_traits

#endif  // SLAM_TOOLBOX__SRV__PAUSE__TRAITS_HPP_
