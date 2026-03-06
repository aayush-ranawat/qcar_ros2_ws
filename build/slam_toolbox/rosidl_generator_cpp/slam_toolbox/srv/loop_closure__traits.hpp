// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from slam_toolbox:srv/LoopClosure.idl
// generated code does not contain a copyright notice

#ifndef SLAM_TOOLBOX__SRV__LOOP_CLOSURE__TRAITS_HPP_
#define SLAM_TOOLBOX__SRV__LOOP_CLOSURE__TRAITS_HPP_

#include "slam_toolbox/srv/loop_closure__struct.hpp"
#include <rosidl_generator_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::LoopClosure_Request>()
{
  return "slam_toolbox::srv::LoopClosure_Request";
}

template<>
struct has_fixed_size<slam_toolbox::srv::LoopClosure_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<slam_toolbox::srv::LoopClosure_Request>
  : std::integral_constant<bool, true> {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::LoopClosure_Response>()
{
  return "slam_toolbox::srv::LoopClosure_Response";
}

template<>
struct has_fixed_size<slam_toolbox::srv::LoopClosure_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<slam_toolbox::srv::LoopClosure_Response>
  : std::integral_constant<bool, true> {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<slam_toolbox::srv::LoopClosure>()
{
  return "slam_toolbox::srv::LoopClosure";
}

template<>
struct has_fixed_size<slam_toolbox::srv::LoopClosure>
  : std::integral_constant<
    bool,
    has_fixed_size<slam_toolbox::srv::LoopClosure_Request>::value &&
    has_fixed_size<slam_toolbox::srv::LoopClosure_Response>::value
  >
{
};

template<>
struct has_bounded_size<slam_toolbox::srv::LoopClosure>
  : std::integral_constant<
    bool,
    has_bounded_size<slam_toolbox::srv::LoopClosure_Request>::value &&
    has_bounded_size<slam_toolbox::srv::LoopClosure_Response>::value
  >
{
};

}  // namespace rosidl_generator_traits

#endif  // SLAM_TOOLBOX__SRV__LOOP_CLOSURE__TRAITS_HPP_
