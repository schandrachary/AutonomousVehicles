#ifndef BEHAVIORPLANNING_H
#define BEHAVIORPLANNING_H

#include "helpers.h"

void switchLanes(int& hostLane, const vector<vehicleObject_s>& predictedObjects,
                const double predictedHostSpeed, double& ref_vel,
                vector<double>& anchorPoints_s, vector<int>& anchorPoints_d)
{
  bool leading_vehicle_ahead = predictedObjects[hostLane].vehicle_ahead.dist < 35;

   if(leading_vehicle_ahead)
   {
     // If the lead vehicle is dangerously close, breake and match the speed
     if(predictedObjects[hostLane].vehicle_ahead.dist > 7 &&
      predictedObjects[hostLane].vehicle_ahead.dist < 17)
     {
       ref_vel -= 0.223;
     }
     else if(predictedObjects[hostLane].vehicle_ahead.dist < 7)
     {
       ref_vel = predictedObjects[hostLane].vehicle_ahead.speed;
     }
     // If lead vehicle is detected, slow down
     else if(predictedObjects[hostLane].vehicle_ahead.dist < 30 &&
        predictedHostSpeed > predictedObjects[hostLane].vehicle_ahead.speed)
     {
       double leading_vehicle_dist = predictedObjects[hostLane].vehicle_ahead.dist;
       double velocityScaleFactor = 1/(1+leading_vehicle_dist/6) + 0.5;
       ref_vel -= 0.228*velocityScaleFactor;
       std::cout <<"ref velocity decreased to: " << ref_vel << std::endl;
     }

     // Check for lane change from left lane
     if(hostLane == lane_e::LEFT)
     {
       // If there is no car in the middle lane for long distance, switch to middle lane
       if(predictedObjects[lane_e::MIDDLE].vehicle_ahead.dist > 55 &&
          predictedObjects[lane_e::MIDDLE].vehicle_behind.dist > 7)
          {
            hostLane = lane_e::MIDDLE;
          }

        // Check to see if right lane is free
        else if(predictedObjects[lane_e::RIGHT].vehicle_ahead.dist > 55 &&
                predictedObjects[lane_e::RIGHT].vehicle_behind.dist > 7 &&
                predictedObjects[lane_e::MIDDLE].vehicle_ahead.dist > 20 &&
                predictedObjects[lane_e::MIDDLE].vehicle_behind.dist > 7)
          {
            hostLane = lane_e::RIGHT;
            anchorPoints_s[0] = 55;
            anchorPoints_s[1] = 80;
            anchorPoints_s[2] = 110;

            anchorPoints_d[0] = 2+4*(lane_e::MIDDLE); // 6
            anchorPoints_d[1] = 4*(lane_e::RIGHT);    // 8
            anchorPoints_d[2] = 2+4*(lane_e::RIGHT);   //10
          }
      }

      // Check for lane change from middle lane
      else if(hostLane == lane_e::MIDDLE)
      {
        // change lane to either left or right only if there is no vehicle for a long distance
        if(predictedObjects[lane_e::LEFT].vehicle_ahead.dist > 55 &&
           predictedObjects[lane_e::LEFT].vehicle_behind.dist > 7)
           {
             hostLane = lane_e::LEFT;
           }
        else if(predictedObjects[lane_e::RIGHT].vehicle_ahead.dist > 55 &&
                predictedObjects[lane_e::RIGHT].vehicle_behind.dist > 7)
            {
                  hostLane = lane_e::RIGHT;
            }
      }

      // Check for lane change from right lane
      else if(hostLane == lane_e::RIGHT)
      {
        // If there is no car in the middle lane, switch to middle lane
        if(predictedObjects[lane_e::MIDDLE].vehicle_ahead.dist > 55 &&
          predictedObjects[lane_e::MIDDLE].vehicle_behind.dist > 7)
        {
          hostLane = lane_e::MIDDLE;
        }
        // Check to see if left lane is free
        else if(predictedObjects[lane_e::LEFT].vehicle_ahead.dist > 55 &&
                predictedObjects[lane_e::LEFT].vehicle_behind.dist > 7 &&
                predictedObjects[lane_e::MIDDLE].vehicle_ahead.dist > 20 &&
                predictedObjects[lane_e::MIDDLE].vehicle_behind.dist > 7)
        {
          hostLane = lane_e::LEFT;
          anchorPoints_s[0] = 55;
          anchorPoints_s[1] = 80;
          anchorPoints_s[2] = 110;

          anchorPoints_d[0] = 2+4*(lane_e::MIDDLE); // 6
          anchorPoints_d[1] = 4*(lane_e::MIDDLE);   // 4
          anchorPoints_d[2] = 2+4*(lane_e::LEFT);   // 2
        }
      }
    }

   // Mainting constant velocity if there is no vehicle ahead
   else if( ref_vel < 49.5)
   {
      double leading_vehicle_dist = predictedObjects[hostLane].vehicle_ahead.dist;
      double velocityScaleFactor = 1 - 1/(1+leading_vehicle_dist/6);
      ref_vel += 0.224*velocityScaleFactor;
    }

}

#endif // BEHAVIORPLANNING_H
