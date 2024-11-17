// Copyright 2021 ros2_control Development Team
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef DIFF_CONTROLLER__DIFFBOT_SYSTEM_HPP_
#define DIFF_CONTROLLER__DIFFBOT_SYSTEM_HPP_

#include <memory>
#include <string>
#include <vector>

#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "rclcpp/macros.hpp"
#include "rclcpp_lifecycle/node_interfaces/lifecycle_node_interface.hpp"
#include "rclcpp_lifecycle/state.hpp"
#include "visibility_control.h"
#include "rclcpp/time.hpp"
#include "rclcpp/clock.hpp"
#include "rclcpp/duration.hpp"
#include "arduino_comms.hpp"
#include "wheel.hpp"

using CallbackReturn = rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;
using rclcpp::Time;
namespace diff_controller
{
class DiffBotSystemHardware : public hardware_interface::SystemInterface
{

  struct Config
  {
    std::string left_wheel_name = "";
    std::string right_wheel_name = "";
    float loop_rate = 0.0;
    std::string device = "";
    int baud_rate = 0;
    int timeout_ms = 0;
    int enc_counts_per_rev = 0;
    int pid_p = 0;
    int pid_d = 0;
    int pid_i = 0;
    int pid_o = 0;
  };

public:
  RCLCPP_SHARED_PTR_DEFINITIONS(DiffBotSystemHardware);

  DIFF_CONTROLLER_PUBLIC
  CallbackReturn on_init(const hardware_interface::HardwareInfo & info) override;

  DIFF_CONTROLLER_PUBLIC
  std::vector<hardware_interface::StateInterface> export_state_interfaces() override;

  DIFF_CONTROLLER_PUBLIC
  std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;

  DIFF_CONTROLLER_PUBLIC
  CallbackReturn on_activate(const rclcpp_lifecycle::State & previous_state) override;

  DIFF_CONTROLLER_PUBLIC
  CallbackReturn on_deactivate(const rclcpp_lifecycle::State & previous_state) override;

  DIFF_CONTROLLER_PUBLIC
  hardware_interface::return_type read() override;

  DIFF_CONTROLLER_PUBLIC
  hardware_interface::return_type write() override;

private:
  rclcpp::Time last_read_time_ = rclcpp::Time(0); 
  ArduinoComms comms_;
  Config cfg_;
  Wheel wheel_l_;
  Wheel wheel_r_;
  std::chrono::time_point<std::chrono::system_clock> time_;
};

}  // namespace diff_controller

#endif  // DIFF_CONTROLLER__DIFFBOT_SYSTEM_HPP_
