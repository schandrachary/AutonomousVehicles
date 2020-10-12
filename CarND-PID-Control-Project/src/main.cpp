#include <math.h>
#include <uWS/uWS.h>
#include <iostream>
#include <string>
#include "json.hpp"
#include "PID.h"

// for convenience
using nlohmann::json;
using std::string;

// For converting back and forth between radians and degrees.
constexpr double pi() { return M_PI; }
double deg2rad(double x) { return x * pi() / 180; }
double rad2deg(double x) { return x * 180 / pi(); }

// Checks if the SocketIO event has JSON data.
// If there is data the JSON object in string format will be returned,
// else the empty string "" will be returned.
string hasData(string s) {
  auto found_null = s.find("null");
  auto b1 = s.find_first_of("[");
  auto b2 = s.find_last_of("]");
  if (found_null != string::npos) {
    return "";
  }
  else if (b1 != string::npos && b2 != string::npos) {
    return s.substr(b1, b2 - b1 + 1);
  }
  return "";
}

int main() {
  uWS::Hub h;

  PID pid_steer;
  PID pid_throttle;
  bool fast_mode = false;
  double target_throttle;

  if(fast_mode)
  {
    target_throttle = 0.85;
    pid_steer.Init(0.085, 0.0001, 3.0);
    pid_throttle.Init(0.2, 0.0001, 0.045);
  }
  else
  {
    target_throttle = 0.35;
    pid_steer.Init(0.085, 0.0001, 3.0);
    pid_throttle.Init(0.0, 0.0, 0.0);
  }
  // double target_throttle = 0.85;

  /**
   * TODO: Initialize the pid variable.
   */
   // pid_steer.Init(0.1, 0.0001, 3.0);
   // pid_throttle.Init(0.3, 0.0001, 0.08);

  h.onMessage([&pid_steer, &pid_throttle, &target_throttle](uWS::WebSocket<uWS::SERVER> ws, char *data, size_t length,
                     uWS::OpCode opCode) {
    // "42" at the start of the message means there's a websocket message event.
    // The 4 signifies a websocket message
    // The 2 signifies a websocket event
    if (length && length > 2 && data[0] == '4' && data[1] == '2') {
      auto s = hasData(string(data).substr(0, length));

      if (s != "") {
        auto j = json::parse(s);

        string event = j[0].get<string>();

        if (event == "telemetry") {
          // j[1] is the data JSON object
          double cte = std::stod(j[1]["cte"].get<string>());
          double speed = std::stod(j[1]["speed"].get<string>());
          double angle = std::stod(j[1]["steering_angle"].get<string>());
          double steer_value;
          /**
           * TODO: Calculate steering value here, remember the steering value is
           *   [-1, 1].
           * NOTE: Feel free to play around with the throttle and speed.
           *   Maybe use another PID controller to control the speed!
           */

           // Calculate steering value
           pid_steer.UpdateError(cte);
           steer_value = pid_steer.TotalError();

           // Calculate throttle value
           pid_throttle.UpdateError(cte);
           double throttle = target_throttle + pid_throttle.TotalError();

           // If the car starts reversing, use the inverted steering value
           if(speed < 5 && throttle < 0)
           {
             steer_value = -steer_value;
           }

           // Clamp the steering value between -1 and 1
           steer_value = pid_steer.clip(steer_value, -1, 1);

          // DEBUG
          std::cout << "CTE: " << cte << " Steering Value: " << steer_value
          << " Throttle Value: " << throttle << " Speed(mph): " << speed << std::endl;

          json msgJson;
          msgJson["steering_angle"] = steer_value;
          msgJson["throttle"] = throttle;
          auto msg = "42[\"steer\"," + msgJson.dump() + "]";
          std::cout << msg << std::endl;
          ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
        }  // end "telemetry" if
      } else {
        // Manual driving
        string msg = "42[\"manual\",{}]";
        ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
      }
    }  // end websocket message if
  }); // end h.onMessage

  h.onConnection([&h](uWS::WebSocket<uWS::SERVER> ws, uWS::HttpRequest req) {
    std::cout << "Connected!!!" << std::endl;
  });

  h.onDisconnection([&h](uWS::WebSocket<uWS::SERVER> ws, int code,
                         char *message, size_t length) {
    ws.close();
    std::cout << "Disconnected" << std::endl;
  });

  int port = 4567;
  if (h.listen(port)) {
    std::cout << "Listening to port " << port << std::endl;
  } else {
    std::cerr << "Failed to listen to port" << std::endl;
    return -1;
  }

  h.run();
}
