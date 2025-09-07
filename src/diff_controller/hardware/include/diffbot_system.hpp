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
/**
 * @class DiffBotSystemHardware
 * @brief A ros2_control SystemInterface for a differential drive robot.
 *
 * This class provides the hardware abstraction for a differential drive robot,
 * allowing the ros2_control framework to interface with the robot's hardware.
 * It handles communication with the low-level hardware (e.g., an Arduino) and
 * exposes state and command interfaces for the wheels.
 */
class DiffBotSystemHardware : public hardware_interface::SystemInterface
{
  /**
   * @struct Config
   * @brief Configuration parameters for the hardware interface.
   */
  struct Config
  {
    std::string left_wheel_name = "";       ///< Name of the left wheel joint.
    std::string right_wheel_name = "";      ///< Name of the right wheel joint.
    float loop_rate = 0.0;                  ///< The loop rate for the control loop.
    std::string device = "";                ///< The serial device for communication.
    int baud_rate = 0;                      ///< The baud rate for serial communication.
    int timeout_ms = 0;                     ///< The timeout in milliseconds for serial communication.
    int enc_counts_per_rev = 0;             ///< The number of encoder counts per revolution.
    int pid_p = 0;                          ///< Proportional gain for the PID controller.
    int pid_d = 0;                          ///< Derivative gain for the PID controller.
    int pid_i = 0;                          ///< Integral gain for the PID controller.
    int pid_o = 0;                          ///< Output gain for the PID controller.
  };

public:
  RCLCPP_SHARED_PTR_DEFINITIONS(DiffBotSystemHardware);

  /**
   * @brief Initializes the hardware interface.
   * @param info The hardware info structure.
   * @return CallbackReturn::SUCCESS on success, CallbackReturn::ERROR on failure.
   */
  DIFF_CONTROLLER_PUBLIC
  CallbackReturn on_init(const hardware_interface::HardwareInfo & info) override;

  /**
   * @brief Exports the state interfaces.
   * @return A vector of state interfaces.
   */
  DIFF_CONTROLLER_PUBLIC
  std::vector<hardware_interface::StateInterface> export_state_interfaces() override;

  /**
   * @brief Exports the command interfaces.
   * @return A vector of command interfaces.
   */
  DIFF_CONTROLLER_PUBLIC
  std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;

  /**
   * @brief Called when the hardware interface is activated.
   * @param previous_state The previous state of the lifecycle node.
   * @return CallbackReturn::SUCCESS on success, CallbackReturn::ERROR on failure.
   */
  DIFF_CONTROLLER_PUBLIC
  CallbackReturn on_activate(const rclcpp_lifecycle::State & previous_state) override;

  /**
   * @brief Called when the hardware interface is deactivated.
   * @param previous_state The previous state of the lifecycle node.
   * @return CallbackReturn::SUCCESS on success, CallbackReturn::ERROR on failure.
   */
  DIFF_CONTROLLER_PUBLIC
  CallbackReturn on_deactivate(const rclcpp_lifecycle::State & previous_state) override;

  /**
   * @brief Reads the current state from the hardware.
   * @param time The current time.
   * @param period The time since the last read.
   * @return hardware_interface::return_type::OK on success, hardware_interface::return_type::ERROR on failure.
   */
  DIFF_CONTROLLER_PUBLIC
  hardware_interface::return_type read(const rclcpp::Time & time,
    const rclcpp::Duration & period) override;

  /**
   * @brief Writes the current command to the hardware.
   * @param time The current time.
   * @param period The time since the last write.
   * @return hardware_interface::return_type::OK on success, hardware_interface::return_type::ERROR on failure.
   */
  DIFF_CONTROLLER_PUBLIC
  hardware_interface::return_type write(const rclcpp::Time & time,
    const rclcpp::Duration & period) override;

private:
  rclcpp::Time last_read_time_ = rclcpp::Time(0); ///< The time of the last read operation.
  ArduinoComms comms_;                           ///< The communication interface to the Arduino.
  Config cfg_;                                   ///< The configuration for the hardware interface.
  Wheel wheel_l_;                                ///< The left wheel.
  Wheel wheel_r_;                                ///< The right wheel.
  std::chrono::time_point<std::chrono::system_clock> time_; ///< The current time.
};

}  // namespace diff_controller

#endif  // DIFF_CONTROLLER__DIFFBOT_SYSTEM_HPP_
