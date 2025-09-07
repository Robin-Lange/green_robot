#ifndef DIFF_CONTROLLER_ARDUINO_COMMS_HPP
#define DIFF_CONTROLLER_ARDUINO_COMMS_HPP

#include <sstream>
#include <libserial/SerialPort.h>
#include <iostream>
#include <thread>
#include <chrono>

/**
 * @brief Converts an integer baud rate to a LibSerial::BaudRate enum.
 * @param baud_rate The baud rate as an integer.
 * @return The corresponding LibSerial::BaudRate enum value.
 */
LibSerial::BaudRate convert_baud_rate(int baud_rate)
{
  // Just handle some common baud rates
  switch (baud_rate)
  {
    case 1200: return LibSerial::BaudRate::BAUD_1200;
    case 1800: return LibSerial::BaudRate::BAUD_1800;
    case 2400: return LibSerial::BaudRate::BAUD_2400;
    case 4800: return LibSerial::BaudRate::BAUD_4800;
    case 9600: return LibSerial::BaudRate::BAUD_9600;
    case 19200: return LibSerial::BaudRate::BAUD_19200;
    case 38400: return LibSerial::BaudRate::BAUD_38400;
    case 57600: return LibSerial::BaudRate::BAUD_57600;
    case 115200: return LibSerial::BaudRate::BAUD_115200;
    case 230400: return LibSerial::BaudRate::BAUD_230400;
    default:
      std::cout << "Error! Baud rate " << baud_rate << " not supported! Default to 57600" << std::endl;
      return LibSerial::BaudRate::BAUD_57600;
  }
}

/**
 * @class ArduinoComms
 * @brief Handles serial communication with an Arduino.
 *
 * This class provides a simple interface for sending and receiving data
 * over a serial connection to an Arduino or similar microcontroller.
 */
class ArduinoComms
{

public:

  /**
   * @brief Default constructor.
   */
  ArduinoComms() = default;

  /**
   * @brief Connects to the serial device.
   * @param serial_device The path to the serial device (e.g., "/dev/ttyUSB0").
   * @param baud_rate The baud rate for the connection.
   * @param timeout_ms The timeout in milliseconds for read operations.
   */
  void connect(const std::string &serial_device, int32_t baud_rate, int32_t timeout_ms)
  {  
    timeout_ms_ = timeout_ms;
    serial_conn_.Open(serial_device);
    serial_conn_.SetBaudRate(convert_baud_rate(baud_rate));
  }

  /**
   * @brief Disconnects from the serial device.
   */
  void disconnect()
  {
    serial_conn_.Close();
    std::cerr << "Disconnected" << std::endl ;
  }

  /**
   * @brief Checks if the serial connection is open.
   * @return True if connected, false otherwise.
   */
  bool connected() const
  {
    return serial_conn_.IsOpen();
  }

  /**
   * @brief Sends a message to the serial device and waits for a response.
   * @param msg_to_send The message to send.
   * @param print_output If true, the sent message and received response are printed to the console.
   * @return The response from the serial device.
   */
  std::string send_msg(const std::string &msg_to_send, bool print_output = false)
  {
    serial_conn_.FlushIOBuffers(); // Just in case
    serial_conn_.Write(msg_to_send);

    std::string response = "";
    try
    {
      // Responses end with \r\n so we will read up to (and including) the \n.
      serial_conn_.ReadLine(response, '\n', timeout_ms_);
    }
    catch (const LibSerial::ReadTimeout&)
    {
        std::cerr << "The ReadByte() call has timed out." << std::endl ;
    }

    if (print_output)
    {
      std::cout << "Sent: " << msg_to_send << " Recv: " << response << std::endl;
    }

    return response;
  }

  /**
   * @brief Sends an empty message to the serial device.
   */
  void send_empty_msg()
  {
    std::string response = send_msg("\r");
  }

  /**
   * @brief Reads the encoder values from the Arduino.
   * @param val_1 A reference to store the first encoder value.
   * @param val_2 A reference to store the second encoder value.
   */
  void read_encoder_values(int &val_1, int &val_2)
  {
    std::string response = send_msg("e\r");

    std::string delimiter = " ";
    size_t del_pos = response.find(delimiter);
    std::string token_1 = response.substr(0, del_pos);
    std::string token_2 = response.substr(del_pos + delimiter.length());

    val_1 = std::atoi(token_1.c_str());
    val_2 = std::atoi(token_2.c_str());
  }

  /**
   * @brief Sets the motor speeds on the Arduino.
   * @param val_1 The speed for the first motor.
   * @param val_2 The speed for the second motor.
   */
  void set_motor_values(int val_1, int val_2)
  {
    std::stringstream ss;
    ss << "m " << val_1 << " " << val_2 << "\r";
    send_msg(ss.str());
  }

  /**
   * @brief Sets the PID values on the Arduino.
   * @param k_p The proportional gain.
   * @param k_d The derivative gain.
   * @param k_i The integral gain.
   * @param k_o The output gain.
   */
  void set_pid_values(int k_p, int k_d, int k_i, int k_o)
  {
    std::stringstream ss;
    ss << "u " << k_p << ":" << k_d << ":" << k_i << ":" << k_o << "\r";
    send_msg(ss.str());
  }

private:
    LibSerial::SerialPort serial_conn_; ///< The serial port object.
    int timeout_ms_;                    ///< The timeout for read operations.
};

#endif // DIFF_CONTROLLER_ARDUINO_COMMS_HPP