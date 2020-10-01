# AutonomousVehicles
Udacity Nano-Degree program on Autonomous Vehicles

## Path Planning
---

![ezgif com-optimize](https://user-images.githubusercontent.com/8539470/94864071-72130d00-0409-11eb-898b-7ad755ce8f80.gif)


### Goal
The goal of this project is to safely navigate around a virtual highway with other traffic that is driving +-10 MPH of the 50 MPH speed limit. Provided is the car's localization and sensor fusion data, there is also a sparse map list of waypoints around the highway. The car should try to go as close as possible to the 50 MPH speed limit, which means passing slower traffic when possible, note that other cars will try to change lanes too. The car should avoid hitting other cars at all cost as well as driving inside of the marked road lanes at all times, unless going from one lane to another. The car should be able to make one complete loop around the 6946m highway. Since the car is trying to go 50 MPH, it should take a little over 5 minutes to complete 1 loop. Also the car should not experience total acceleration over 10 m/s^2 and jerk that is greater than 10 m/s^3.

### Basic Build Instructions
1. Clone this repo.
2. Make a build directory: mkdir build && cd build
3. Compile: cmake .. && make
4. Run it: ./path_planning.




![pass-2lanes-480p](https://user-images.githubusercontent.com/8539470/94862945-b0a7c800-0407-11eb-999d-7dba75e88f1e.gif)
## Lane Line Detection

1. Finding lane lines on the road project is located [here](https://github.com/schandrachary/AutonomousVehicles/tree/finding_lane_lines/Fundamentals_of_computer_vision/CarND-LaneLines-P1-master).
2. The first part of the challenge, which includes detecting the lane lines and extrapolating the segmented lines to a solid line and running lane detection pipeline on a video stream can be found in [FindingLaneLines.py](https://github.com/schandrachary/AutonomousVehicles/blob/finding_lane_lines/Fundamentals_of_computer_vision/CarND-LaneLines-P1-master/FindingLaneLines.py)
3. The second part of the challenge, which include detecting the lane lines for curved lane scenraio can be found in [curvedLaneFinding.py](https://github.com/schandrachary/AutonomousVehicles/blob/finding_lane_lines/Fundamentals_of_computer_vision/CarND-LaneLines-P1-master/curvedLaneFinding.py)

## Advanced Lane Line Finding

1. Source code for Advanced Lane Line finding algorithm is found [here](https://github.com/schandrachary/AutonomousVehicles/tree/advanced_computer_vision/Advanced%20Computer%20Vision/CarND-Advanced-Lane-Lines-master/source)
2. Output images from the algorithm are saved [here](https://github.com/schandrachary/AutonomousVehicles/tree/advanced_computer_vision/Advanced%20Computer%20Vision/CarND-Advanced-Lane-Lines-master/output_images)
3. Follow the [writeup](https://github.com/schandrachary/AutonomousVehicles/blob/advanced_computer_vision/Advanced%20Computer%20Vision/CarND-Advanced-Lane-Lines-master/writeup_template.md) here to get a brief explanation of the algorithm and how to run the code

## Traffic Sign Classifier

1. This project was developed on Ipython notebook and it located [here](https://github.com/schandrachary/AutonomousVehicles/tree/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project)
2. The test images downloaded from web to test on the model is located [here](https://github.com/schandrachary/AutonomousVehicles/tree/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/test_images)
3. The writeup for this project is located [here](https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_traffic_sign_recognition.md)
4. Note that the pickle file with augmented data set is not uploaded on the repository due to file size constraints. If you want to download this project and run, please contact me.

## Behavioral Cloning

1. Source code for this project and its neural network architecture can be found inside [source](https://github.com/schandrachary/AutonomousVehicles/tree/behavioral_cloning/source) directory
2. Data used to train the model can be found inside [data](https://github.com/schandrachary/AutonomousVehicles/tree/behavioral_cloning/data) directory
3. A writeup for this project can be in the markdown file named writeup_behavioral_cloning
4. The images used for the writeup can be found in the directory writeup_images
5. An output video of the car driving autonomously in two tracks can be found in the directory [video](https://github.com/schandrachary/AutonomousVehicles/tree/behavioral_cloning/video)

## Extended Kalman Filter
1. Source code for EKF algorithm can be found in the [src](https://github.com/schandrachary/AutonomousVehicles/tree/ekf/CarND-Extended-Kalman-Filter-Project-master/src) directory
2. Once the install for uWebSocketIO is complete, the main program can be built and run by doing the following from the project top directory.  
   * mkdir build
   * cd build
   * cmake ..
   * make
   * ./ExtendedKF
   
## Particle Filter
1. The source code for this project can be located [here](https://github.com/schandrachary/AutonomousVehicles/tree/particle_filter/CarND-Kidnapped-Vehicle-Project-master/src)
2. On the parent directory, clean.sh cleans the build
3. build.sh, builds the project
4. On successful build, the project can be run using run.sh
5. Turn on the simulator and navigate to "Kidnapped Vehicle" simulation and hit the start button
6. You should see blue and green lines almost align with each-other marking coherence to groundtruth
7. The project is marked successful if the error is within range and the car completes three loops within 100 seconds






