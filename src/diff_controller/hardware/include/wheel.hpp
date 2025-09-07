#ifndef DIFF_CONTROLLER_WHEEL_HPP
#define DIFF_CONTROLLER_WHEEL_HPP

#include <string>
#include <cmath>

/**
 * @class Wheel
 * @brief Represents a single wheel of the robot.
 *
 * This class encapsulates the properties of a wheel, including its name,
 * encoder state, command, position, and velocity. It also provides a helper
 * function to calculate the angle from encoder counts.
 */
class Wheel
{
public:
    std::string name = "";      ///< The name of the wheel joint.
    int enc = 0;                ///< The latest encoder reading.
    double cmd = 0;             ///< The latest velocity command.
    double pos = 0;             ///< The position of the wheel in radians.
    double vel = 0;             ///< The velocity of the wheel in radians per second.
    double rads_per_count = 0;  ///< The conversion factor from encoder counts to radians.

    /**
     * @brief Default constructor.
     */
    Wheel() = default;

    /**
     * @brief Constructs a Wheel object.
     * @param wheel_name The name of the wheel.
     * @param counts_per_rev The number of encoder counts per revolution.
     */
    Wheel(const std::string &wheel_name, int counts_per_rev)
    {
      setup(wheel_name, counts_per_rev);
    }

    
    /**
     * @brief Sets up the wheel's parameters.
     * @param wheel_name The name of the wheel.
     * @param counts_per_rev The number of encoder counts per revolution.
     */
    void setup(const std::string &wheel_name, int counts_per_rev)
    {
      name = wheel_name;
      rads_per_count = (2*M_PI)/counts_per_rev;
    }

    /**
     * @brief Calculates the angle of the wheel in radians from the encoder count.
     * @return The angle in radians.
     */
    double calc_enc_angle()
    {
      return enc * rads_per_count;
    }
};

#endif // DIFF_CONTROLLER_WHEEL_HPP
