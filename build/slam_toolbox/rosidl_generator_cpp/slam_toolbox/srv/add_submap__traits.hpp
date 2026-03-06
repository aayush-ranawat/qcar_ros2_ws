// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from slam_toolbox:srv/AddSubmap.idl
// generated code does not contain a copyright notice

#ifndef SLAM_TOOLBOX__SRV__ADD_SUBMAP__TRAITS_HPP_
#define SLAM_TOOLBOX__SRV__ADD_SUBMAP__TRAITS_HPP_

#include "slam_toolbox/srv/add_submap__struct.hpp"
#include <rosidl_generator_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::AddSubmap_Request>()
{
  return "slam_toolbox::srv::AddSubmap_Request";
}

template<>
struct has_fixed_size<slam_toolbox::srv::AddSubmap_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<slam_toolbox::srv::AddSubmap_Request>
  : std::integral_constant<bool, false> {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::AddSubmap_Response>()
{
  return "slam_toolbox::srv::AddSubmap_Response";
}

template<>
struct has_fixed_size<slam_toolbox::srv::AddSubmap_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<slam_toolbox::srv::AddSubmap_Response>
  : std::integral_constant<bool, true> {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::AddSubmap>()
{
  return "slam_toolbox::srv::AddSubmap";
}

template<>
struct has_fixed_size<slam_toolbox::srv::AddSubmap>
  : std::integral_constant<
    bool,
    has_fixed_size<slam_toolbox::srv::AddSubmap_Request>::value &&
    has_fixed_size<slam_toolbox::srv::AddSubmap_Response>::value
  >
{
};

template<>
struct has_bounded_size<slam_toolbox::srv::AddSubmap>
  : std::integral_constant<
    bool,
    has_bounded_size<slam_toolbox::srv::AddSubmap_Request>::value &&
    has_bounded_size<slam_toolbox::srv::AddSubmap_Response>::value
  >
{
};

}  // namespace rosidl_generator_traits

#endif  // SLAM_TOOLBOX__SRV__ADD_SUBMAP__TRAITS_HPP_
