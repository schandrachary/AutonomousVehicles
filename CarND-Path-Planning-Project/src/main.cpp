#include <uWS/uWS.h>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include "Eigen-3.3/Eigen/Core"
#include "Eigen-3.3/Eigen/QR"
#include "helpers.h"
#include "json.hpp"
#include "spline.h"

// for convenience
using nlohmann::json;
using std::string;
using std::vector;

int main() {
  uWS::Hub h;

  // Load up map values for waypoint's x,y,s and d normalized normal vectors
  vector<double> map_waypoints_x;
  vector<double> map_waypoints_y;
  vector<double> map_waypoints_s;
  vector<double> map_waypoints_dx;
  vector<double> map_waypoints_dy;

  // Waypoint map to read from
  string map_file_ = "../data/highway_map.csv";
  // The max s value before wrapping around the track back to 0
  double max_s = 6945.554;

  std::ifstream in_map_(map_file_.c_str(), std::ifstream::in);

  string line;
  while (getline(in_map_, line)) {
    std::istringstream iss(line);
    double x;
    double y;
    float s;
    float d_x;
    float d_y;
    iss >> x;
    iss >> y;
    iss >> s;
    iss >> d_x;
    iss >> d_y;
    map_waypoints_x.push_back(x);
    map_waypoints_y.push_back(y);
    map_waypoints_s.push_back(s);
    map_waypoints_dx.push_back(d_x);
    map_waypoints_dy.push_back(d_y);
  }

  // Have a reference velocity to target
  double ref_vel = 0.0; //mph
  // Start in lane 1
  int lane = 1;

  // Host lane vehicleObject_s
  vehicleObject_s hostLaneObjects;
  vehicleObject_s leftLaneObjects;
  vehicleObject_s rightLaneObjects;

  h.onMessage([&ref_vel,&lane,&hostLaneObjects,&leftLaneObjects,&rightLaneObjects,&map_waypoints_x,
              &map_waypoints_y,&map_waypoints_s,&map_waypoints_dx,&map_waypoints_dy]
              (uWS::WebSocket<uWS::SERVER> ws, char *data, size_t length,
               uWS::OpCode opCode) {
    // "42" at the start of the message means there's a websocket message event.
    // The 4 signifies a websocket message
    // The 2 signifies a websocket event
    if (length && length > 2 && data[0] == '4' && data[1] == '2') {

      auto s = hasData(data);

      if (s != "") {
        auto j = json::parse(s);

        string event = j[0].get<string>();

        if (event == "telemetry") {
          // j[1] is the data JSON object

          // Main car's localization Data
          double car_x = j[1]["x"];
          double car_y = j[1]["y"];
          double car_s = j[1]["s"];
          double car_d = j[1]["d"];
          double car_yaw = j[1]["yaw"];
          double car_speed = j[1]["speed"];

          // Previous path data given to the Planner
          auto previous_path_x = j[1]["previous_path_x"];
          auto previous_path_y = j[1]["previous_path_y"];
          // Previous path's end s and d values
          double end_path_s = j[1]["end_path_s"];
          double end_path_d = j[1]["end_path_d"];

          // Sensor Fusion Data, a list of all other cars on the same side
          //   of the road.
          auto sensor_fusion = j[1]["sensor_fusion"];

          json msgJson;

          /**
           * TODO: define a path made up of (x,y) points that the car will visit
           *   sequentially every .02 seconds
           */
           int prev_size = previous_path_x.size();


           /* --------------------------------------------------*/
           /* ------------------Prediction----------------------*/
           /* --------------------------------------------------*/

           /*
            Check sensor fusion for other cars on the road
           */
           // project the location of the car to the end of the path
           if(prev_size > 0)
           {
             car_s = end_path_s;
           }

           // Reset distance values to a max number
           hostLaneObjects.vehicle_ahead.dist = 9999;
           hostLaneObjects.vehicle_behind.dist = 9999;
           leftLaneObjects.vehicle_ahead.dist = 9999;
           leftLaneObjects.vehicle_behind.dist = 9999;
           rightLaneObjects.vehicle_ahead.dist = 9999;
           rightLaneObjects.vehicle_behind.dist = 9999;

           // check if any car is in same lane and too close to us
           bool vehicle_ahead = false;
           double check_speed = 0.0;
           for(int i=0; i<sensor_fusion.size(); ++i)
           {
             float d = sensor_fusion[i][6];
             double vx = sensor_fusion[i][3];
             double vy = sensor_fusion[i][4];
             check_speed = sqrt(vx*vx + vy*vy);
             double check_car_s = sensor_fusion[i][5];

             // Predict where the car will be in the future
             check_car_s += (double)prev_size*0.02*check_speed;

             // Check for cars in the host lane
             if(d < (2+4*lane+2) && d > (2+4*lane-2))
             {
               if((check_car_s > car_s) && (check_car_s - car_s) < 30)
               {
                 hostLaneObjects.vehicle_ahead.speed = check_speed;
                 hostLaneObjects.vehicle_ahead.dist = check_car_s-car_s;
                 hostLaneObjects.vehicle_ahead.hostVehicleSpeed =
                                          hostLaneObjects.vehicle_ahead.dist/((prev_size+10)*0.02);
                 vehicle_ahead = true;
               }
             }

             // Check for cars in the left lane, if it exists
             int left_lane = lane - 1;
             if(left_lane >= 0 && d < (2+4*left_lane+2) && d > (2+4*left_lane-2))
             {
               // grab the closest leading vehicle ahead
               if(check_car_s > car_s && leftLaneObjects.vehicle_ahead.dist > check_car_s - car_s)
               {
                 leftLaneObjects.vehicle_ahead.dist = check_car_s - car_s;
                 // std::cout << "shortest dist selected in left lane and ahead at:  " << leftLaneObjects.vehicle_ahead.dist << "m\n";
               }

               // For vehicle behind
               else if(car_s > check_car_s && leftLaneObjects.vehicle_behind.dist > car_s - check_car_s)
               {
                 leftLaneObjects.vehicle_behind.dist = car_s - check_car_s;
                 // std::cout << "shortest dist selected in left lane and behind at:  " << leftLaneObjects.vehicle_behind.dist << "m\n";
               }

             }

             // Check for cars in the right lane, if it exists
             int right_lane = lane + 1;
             if (right_lane <=2 && d < (2+4*right_lane+2) && d > (2+4*right_lane-2))
             {
               // grab the closest leading vehicle ahead
               if(check_car_s > car_s && rightLaneObjects.vehicle_ahead.dist > check_car_s - car_s)
               {
                 rightLaneObjects.vehicle_ahead.dist = check_car_s - car_s;
                 // std::cout << "shortest dist selected in right lane and ahead at:  " << rightLaneObjects.vehicle_ahead.dist << "m\n";
               }

               // For vehicle behind
               else if(car_s > check_car_s && rightLaneObjects.vehicle_behind.dist > car_s - check_car_s)
               {
                 rightLaneObjects.vehicle_behind.dist = car_s - check_car_s;
                 // std::cout << "shortest dist selected in right lane and behind at:  " << rightLaneObjects.vehicle_behind.dist << "m\n";
               }
             }

           }

           // If too close, slow down by 10mph
           float max_cutoff = 30;
           float min_cutoff = 10;
           if(vehicle_ahead)
           {
             // If lead vehicle detected, slow down
             if(hostLaneObjects.vehicle_ahead.dist < max_cutoff &&
               hostLaneObjects.vehicle_ahead.hostVehicleSpeed > hostLaneObjects.vehicle_ahead.speed)
             {
               double leading_vehicle_dist = hostLaneObjects.vehicle_ahead.dist;
               double velocityScaleFactor = 1/(1+leading_vehicle_dist/6) + 0.3;
               // ref_vel -= 0.114;
               ref_vel -= 0.224*velocityScaleFactor;
             }
             // If lead vehicle is further away and host vehicle is slower, keep accelerating
             else if(hostLaneObjects.vehicle_ahead.dist > min_cutoff &&
                    hostLaneObjects.vehicle_ahead.hostVehicleSpeed < hostLaneObjects.vehicle_ahead.speed &&
                    hostLaneObjects.vehicle_ahead.hostVehicleSpeed < 49.5)
             {
               // ref_vel +=0.094;
               double leading_vehicle_dist = hostLaneObjects.vehicle_ahead.dist;
               double velocityScaleFactor = 0.8 - 1/(1+leading_vehicle_dist/6);
               ref_vel += 0.224*velocityScaleFactor;
             }
             // If the lead vehicle is dangerously close, match the speed
             else if(hostLaneObjects.vehicle_ahead.dist < min_cutoff)
             {
               ref_vel = hostLaneObjects.vehicle_ahead.speed;
             }

             // If there is a left lane, look for a gap
             int left_lane = lane - 1;
             int right_lane = lane + 1;
             if(left_lane >= 0 &&
               leftLaneObjects.vehicle_behind.dist > 5 &&
               leftLaneObjects.vehicle_ahead.dist > 30)
             {
               //std::cout << "\nlane change suggested: " << left_lane;
               lane = left_lane;
             }
            // Otherwise, look for a gap in the right lane
            else if(right_lane <= 2 &&
                    rightLaneObjects.vehicle_behind.dist > 5 &&
                    rightLaneObjects.vehicle_ahead.dist > 30)
            {
              //std::cout << "\nlane change suggested: " << right_lane;
              lane = right_lane;
            }

           }

           // If we are slow, speed up by 10 mph
           else if(ref_vel < 49.5)
           {
             ref_vel += 0.224;
           }

           /* --------------------------------------------------*/
           /* ------------------Trajectory generation-----------*/
           /* --------------------------------------------------*/

           // Reset the position of the car to current car's s position
           //car_s = j[1]["s"];

           // Create a list of sparsedly spced (x,y) waypoints
           vector<double> ptsx;
           vector<double> ptsy;

           // Reference x,y, yaw states
           double ref_x = car_x;
           double ref_y = car_y;
           double ref_yaw = deg2rad(car_yaw);

           //If previous size is almost empty, use the car as starting points
           if(prev_size < 2)
           {
             //Use two points that make the path tangent to the car
             double prev_car_x = car_x - cos(car_yaw);
             double prev_car_y = car_y - sin(car_yaw);

             ptsx.push_back(prev_car_x);
             ptsx.push_back(car_x);

             ptsy.push_back(prev_car_y);
             ptsy.push_back(car_y);
           }
           // If there are more points available, add them
           else if(prev_size > 10)
           {
             // Redefine reference states to be previous path end points
             ref_x = previous_path_x[prev_size-1];
             ref_y = previous_path_y[prev_size-1];

             double ref_x_prev10 = previous_path_x[prev_size-10];
             double ref_y_prev10 = previous_path_y[prev_size-10];

             double ref_x_prev8 = previous_path_x[prev_size-8];
             double ref_y_prev8 = previous_path_y[prev_size-8];

             double ref_x_prev5 = previous_path_x[prev_size-5];
             double ref_y_prev5 = previous_path_y[prev_size-5];

             double ref_x_prev = previous_path_x[prev_size-2];
             double ref_y_prev = previous_path_y[prev_size-2];
             ref_yaw = atan2(ref_y - ref_y_prev, ref_x - ref_x_prev);

             // Use two points that make the path tangent to the previous path's end point
             ptsx.push_back(ref_x_prev10);
             ptsx.push_back(ref_x_prev8);
             ptsx.push_back(ref_x_prev5);
             ptsx.push_back(ref_x_prev);
             ptsx.push_back(ref_x);

             ptsy.push_back(ref_y_prev10);
             ptsy.push_back(ref_y_prev8);
             ptsy.push_back(ref_y_prev5);
             ptsy.push_back(ref_y_prev);
             ptsy.push_back(ref_y);
           }
           // Otherwise, use prevous path's end point as starting Reference
           else
           {
             // Redefine reference states to be previous path end points
             ref_x = previous_path_x[prev_size-1];
             ref_y = previous_path_y[prev_size-1];

             double ref_x_prev = previous_path_x[prev_size-2];
             double ref_y_prev = previous_path_y[prev_size-2];
             ref_yaw = atan2(ref_y - ref_y_prev, ref_x - ref_x_prev);

             // Push x points
             ptsx.push_back(ref_x_prev);
             ptsx.push_back(ref_x);

             // Push y points
             ptsy.push_back(ref_y_prev);
             ptsy.push_back(ref_y);
           }

           // Add evenly distributed points at 10m intervals
           vector<double> next_wp0 = getXY(car_s+20, (2+4*lane), map_waypoints_s, map_waypoints_x,  map_waypoints_y);
           vector<double> next_wp1 = getXY(car_s+30, (2+4*lane), map_waypoints_s, map_waypoints_x,  map_waypoints_y);
           vector<double> next_wp2 = getXY(car_s+40, (2+4*lane), map_waypoints_s, map_waypoints_x,  map_waypoints_y);
           vector<double> next_wp3 = getXY(car_s+50, (2+4*lane), map_waypoints_s, map_waypoints_x,  map_waypoints_y);
           vector<double> next_wp4 = getXY(car_s+60, (2+4*lane), map_waypoints_s, map_waypoints_x,  map_waypoints_y);
           vector<double> next_wp5 = getXY(car_s+70, (2+4*lane), map_waypoints_s, map_waypoints_x,  map_waypoints_y);
           vector<double> next_wp6 = getXY(car_s+90, (2+4*lane), map_waypoints_s, map_waypoints_x,  map_waypoints_y);

           // Push x-waypoint
           ptsx.push_back(next_wp0[0]);
           ptsx.push_back(next_wp1[0]);
           ptsx.push_back(next_wp2[0]);
           ptsx.push_back(next_wp3[0]);
           ptsx.push_back(next_wp4[0]);
           ptsx.push_back(next_wp5[0]);
           ptsx.push_back(next_wp6[0]);

           // Push y-waypoint
           ptsy.push_back(next_wp0[1]);
           ptsy.push_back(next_wp1[1]);
           ptsy.push_back(next_wp2[1]);
           ptsy.push_back(next_wp3[1]);
           ptsy.push_back(next_wp4[1]);
           ptsy.push_back(next_wp5[1]);
           ptsy.push_back(next_wp6[1]);

           // convert the waypoints to vehicle coordinates
           for(int i = 0; i < ptsx.size(); ++i)
           {
             // Translation component
             double shift_x = ptsx[i] - ref_x;
             double shift_y = ptsy[i] - ref_y;

             ptsx[i] = (shift_x*cos(0-ref_yaw) - shift_y*sin(0-ref_yaw));
             ptsy[i] = (shift_x*sin(0-ref_yaw) + shift_y*cos(0-ref_yaw));
           }

           // Creat a spline
           tk::spline s;

           // set(x,y) points to the spline
           s.set_points(ptsx, ptsy);

           // Define the path points to be used for the planner
           vector<double> next_x_vals;
           vector<double> next_y_vals;

           // Push the remaining points in previous path from last time
           for(int i=0; i<previous_path_x.size(); ++i)
           {
             next_x_vals.push_back(previous_path_x[i]);
             next_y_vals.push_back(previous_path_y[i]);
           }

           // Calculate how to break up spline points so that we travel at our desired reference velocity
           double target_x = 30.0;
           double target_y = s(target_x);
           double target_dist = sqrt((target_x*target_x) + (target_y*target_y));

           double x_add_on = 0;

           // Fill up 50 points of path planner adding to previous points
           for(int i=0; i<=50-previous_path_x.size(); ++i)
           {
             double N = (target_dist/(0.02*ref_vel/2.24));
             double x_point = x_add_on + (target_x/N);
             double y_point = s(x_point);

             x_add_on = x_point;

             double x_ref = x_point;
             double y_ref = y_point;

             // Rotate the points back to global coordinates
             x_point = x_ref*cos(ref_yaw) - y_ref*sin(ref_yaw);
             y_point = x_ref*sin(ref_yaw) + y_ref*cos(ref_yaw);

             // Translate to global coordinates
             x_point += ref_x;
             y_point += ref_y;

             next_x_vals.push_back(x_point);
             next_y_vals.push_back(y_point);
           }

          msgJson["next_x"] = next_x_vals;
          msgJson["next_y"] = next_y_vals;

          auto msg = "42[\"control\","+ msgJson.dump()+"]";

          ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
        }  // end "telemetry" if
      } else {
        // Manual driving
        std::string msg = "42[\"manual\",{}]";
        ws.send(msg.data(), msg.length(), uWS::OpCode::TEXT);
      }
    }  // end websocket if
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
