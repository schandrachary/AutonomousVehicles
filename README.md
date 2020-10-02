# AutonomousVehicles
Udacity Nano-Degree program on Autonomous Vehicles

## Path Planning
---

![ezgif com-optimize](https://user-images.githubusercontent.com/8539470/94864071-72130d00-0409-11eb-898b-7ad755ce8f80.gif)

[//]: # (Image References)

[image1]: CarND-Path-Planning-Project/writeup_pictures/prediction-approaches.png "prediction"
[image2]: CarND-Path-Planning-Project/writeup_pictures/frenet.png "frenet"
[image3]: CarND-Path-Planning-Project/writeup_pictures/behavior.png "behavior"
[image4]: CarND-Path-Planning-Project/writeup_pictures/spline.png "spline"

### Objective
The goal of this project is to safely navigate around a virtual highway with other traffic that is driving `+-10 MPH` of the `50 MPH` speed limit. Provided is the car's localization and sensor fusion data, there is also a sparse map list of waypoints around the highway. The car should try to go as close as possible to the `50 MPH` speed limit, which means passing slower traffic when possible, note that other cars will try to change lanes too. The car should avoid hitting other cars at all cost as well as driving inside of the marked road lanes at all times, unless going from one lane to another. The car should be able to make one complete loop around the `6946m` highway. Since the car is trying to go `50 MPH`, it should take a little over 5 minutes to complete 1 loop. Also the car should not experience total acceleration over `10 m/s^2` and jerk that is greater than `10 m/s^3`.

### Basic Build Instructions
1. Clone this repo.
2. Make a build directory: mkdir build && cd build
3. Compile: cmake .. && make
4. Run it: ./path_planning.

### Algorithm overview

#### Prediction

There are two main types of prediction, Model-based and Data-driven (and hybrid approach which we won't talk about here). In model based approach, we have a bank of possible behaviors and each has a mathematical model of motion which takes into account the physical capabilities of the object as well as the constraints imposed by the road traffic law and other restrictions.

Data based approaches have a model that is trained on lots of data and observed behavior is fed to the model to make predictions.

![alt text][image1]

The car in the simulator uses a perfect controller and will visit every `(x,y)` point it recieves in the list every `.02` seconds. The units for the `(x,y)` points are in meters and the spacing of the points determines the speed of the car. The vector going from a point to the next point in the list dictates the angle of the car. Acceleration both in the tangential and normal directions is measured along with the jerk, the rate of change of total Acceleration.

Therefore, we now have a formual:   
  ```
  N * 0.02 * velocity = distance
  ```
  where `N`is the number of points.

With this, we can predict the location of cars around the ego-vehicle for in terms of distance away from it. This happens on `line-40` of `prediction.h`.

#### Frenet Coordinates
Frenet Coordinates are a way of representing position on a road in a more intuitive way than traditional `(x,y)` Cartesian Coordinates.


With Frenet coordinates, we use the variables *s* and *d* to describe a vehicle's position on the road. The *s* coordinate represents distance along the road (also known as **longitudinal displacement**) and the *d* coordinate represents side-to-side position on the road (also known as **lateral displacement**).

![alt text][image2]


In the prediciton step, Frenet Cooridnates are used to determine the location of other objects with respect to ego vehicle and the rest of the logic in `prediction.h` follows to  predicit and record objects in every lane. These objects are then passed to `behaviorPlanning.h` to make high level decision about which lane the ego-vehicle should take.

#### Behavior Planning

As shown in the diagram below, behavior planner sit at the top of the decision tree and hence, the frequency at which this module operates is fairly low. The decision passed by behavior planner can span for multiple cycles before the planner gets to make corrections, if any. Therefore, the planning has to take into account the predicion of objects around it for several seconds into the future.

![alt text][image3]


There will be some latency between the simulator running and the path planner returning a path, with optimized code usually its not very long maybe just 1-3 time steps. During this delay the simulator will continue using points that it was last given, therefore, it's a good idea to store the last points you have used so you can have a smooth transition.

All of the remaining previous points, `previous_path_x`, and `previous_path_y` are loaded as this can be helpful for this transition. This logic is reflected in code lines `254-259` in `main.cpp`. This returns a path that extends this previous path.

The rest of the code in `behaviorPlanning.h` decides which lane the car should take for an optimal and safe path to complete the loop in shortest amount of time.

`behaviorPlanning.h` also contains logic that determines if jumping two lanes is appropriate and does so by adding custom anchor points to be used by the `spline` library. This helps in creating a smooth trajectory.

![ezgif com-2-lane](https://user-images.githubusercontent.com/8539470/94874828-0a68bc00-0421-11eb-8371-988123f076ea.gif)


#### Spline for Trajectory Generation

The anchor points generated from behavior planning gets appended to `previous_path_x` and `previous_path_y` in `(s,d)` coordinates. All of these points are then converted to vehicle coordinates, this happens in lines `234-242` of `main.cpp`. These points are used to generate a trajectory. For this, we are going to use spline library. `Spline.h` is a single header file that helps to get the corresponding `y` coordinate on the spline for the provided `x` coordinate.  The below is a depiction of how spline generates a continuous path.

![alt text][image4]
(image sourced from internet)

### Dependencies
___

* cmake >= 3.5
  * All OSes: [click here for installation instructions](https://cmake.org/install/)
* make >= 4.1
  * Linux: make is installed by default on most Linux distros
  * Mac: [install Xcode command line tools to get make](https://developer.apple.com/xcode/features/)
  * Windows: [Click here for installation instructions](http://gnuwin32.sourceforge.net/packages/make.htm)
* gcc/g++ >= 5.4
  * Linux: gcc / g++ is installed by default on most Linux distros
  * Mac: same deal as make - [install Xcode command line tools]((https://developer.apple.com/xcode/features/)
  * Windows: recommend using [MinGW](http://www.mingw.org/)
* [uWebSockets](https://github.com/uWebSockets/uWebSockets)
  * Run either `install-mac.sh` or `install-ubuntu.sh`.
  * If you install from source, checkout to commit `e94b6e1`, i.e.
    ```
    git clone https://github.com/uWebSockets/uWebSockets
    cd uWebSockets
    git checkout e94b6e1
    ```
