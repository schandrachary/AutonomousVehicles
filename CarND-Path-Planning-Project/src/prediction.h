#ifndef PREDICTION_H
#define PREDICTION_H

#include "helpers.h"
#include <cmath>

using std::vector;

/*
 Check sensor fusion for other cars on the road
*/

vector<vehicleObject_s> predictObjects(const vector<vector<double>>& sensor_fusion,
                                       const int prev_size, const double car_s,
                                       double& predictedHostSpeed)
{
  vehicleObject_s leftLaneObjects;
  vehicleObject_s middleLaneObjects;
  vehicleObject_s rightLaneObjects;

  // Reset distance values to a max number
  leftLaneObjects.vehicle_ahead.dist = 9999;
  leftLaneObjects.vehicle_behind.dist = 9999;
  middleLaneObjects.vehicle_ahead.dist = 9999;
  middleLaneObjects.vehicle_behind.dist = 9999;
  rightLaneObjects.vehicle_ahead.dist = 9999;
  rightLaneObjects.vehicle_behind.dist = 9999;
  double check_speed = 0.0;

  // Go through the list of sensor fusion objects
  for(int i=0; i<sensor_fusion.size(); ++i)
  {
    float d = sensor_fusion[i][6];
    double vx = sensor_fusion[i][3];
    double vy = sensor_fusion[i][4];
    check_speed = sqrt(vx*vx + vy*vy);
    double check_car_s = sensor_fusion[i][5];

    // Predict where the car will be in the future
    check_car_s += (double)prev_size*0.02*check_speed;
    double object_distance = std::abs(check_car_s - car_s);

    // Check for cars in the Left Lane
    if(d > 0 && d < (2+4*lane_e::LEFT+2))
    {
      // grab the closest leading vehicle ahead
      if(check_car_s > car_s && leftLaneObjects.vehicle_ahead.dist > object_distance)
      {
        leftLaneObjects.vehicle_ahead.dist = object_distance;
        leftLaneObjects.vehicle_ahead.speed = check_speed;

        // Calculate predicted host speed wrt to leading vehicle
        predictedHostSpeed = leftLaneObjects.vehicle_ahead.dist/((prev_size)*0.02);        
      }

      // For vehicle behind
      else if(car_s > check_car_s && leftLaneObjects.vehicle_behind.dist > object_distance)
      {
        leftLaneObjects.vehicle_behind.dist = object_distance;
        leftLaneObjects.vehicle_behind.speed = check_speed;
      }
    }

    // Check for cars in the middle lane
    else if(d > (2+4*lane_e::MIDDLE-2) && d < (2+4*lane_e::MIDDLE+2))
    {
      // grab the closest leading vehicle ahead
      if(check_car_s > car_s && middleLaneObjects.vehicle_ahead.dist > object_distance)
      {
        middleLaneObjects.vehicle_ahead.dist = object_distance;
        middleLaneObjects.vehicle_ahead.speed = check_speed;

        // Calculate predicted host speed wrt to leading vehicle
        predictedHostSpeed = leftLaneObjects.vehicle_ahead.dist/((prev_size+10)*0.02);
      }

      // For vehicle behind
      else if(car_s > check_car_s && middleLaneObjects.vehicle_behind.dist > object_distance)
      {
        middleLaneObjects.vehicle_behind.dist = object_distance;
        middleLaneObjects.vehicle_behind.speed = check_speed;
      }
    }

    // Check for cars in the right lane
    else if(d > (2+4*lane_e::RIGHT-2) && d < (2+4*lane_e::RIGHT+2))
    {
      // grab the closest leading vehicle ahead
      if(check_car_s > car_s && rightLaneObjects.vehicle_ahead.dist > object_distance)
      {
        rightLaneObjects.vehicle_ahead.dist = object_distance;
        rightLaneObjects.vehicle_ahead.speed = check_speed;

        // Calculate predicted host speed wrt to leading vehicle
        predictedHostSpeed = leftLaneObjects.vehicle_ahead.dist/((prev_size+10)*0.02);
      }

      // For vehicle behind
      else if(car_s > check_car_s && rightLaneObjects.vehicle_behind.dist > object_distance)
      {
        rightLaneObjects.vehicle_behind.dist = object_distance;
        rightLaneObjects.vehicle_behind.speed = check_speed;
      }
    } // end if

  } // end for

  return {leftLaneObjects, middleLaneObjects, rightLaneObjects};

}




#endif //PREDICTION_H
