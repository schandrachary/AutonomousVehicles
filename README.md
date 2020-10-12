# Autonomous Vehicles Nano Degree 
Udacity Nano-Degree program on Autonomous Vehicles. There are several projects in this nanodegree and each project has its own branch. All of these branches can be found within [AutonomousVehicles](https://github.com/schandrachary/AutonomousVehicles) repository. Listed below is brief description of each of those projects. 

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
1. The source code for this project is located [here](https://github.com/schandrachary/AutonomousVehicles/tree/particle_filter/CarND-Kidnapped-Vehicle-Project-master/src)
2. On the parent directory, clean.sh cleans the build
3. build.sh, builds the project
4. On successful build, the project can be run using run.sh
5. Turn on the simulator and navigate to "Kidnapped Vehicle" simulation and hit the start button
6. You should see blue and green lines almost align with each-other marking coherence to groundtruth
7. The project is marked successful if the error is within range and the car completes three loops within 100 seconds


## Path Planning
1. The source code for this project is located [here](https://github.com/schandrachary/AutonomousVehicles/tree/path_planning/CarND-Path-Planning-Project/src)
2. Please take a look at the [Readme](https://github.com/schandrachary/AutonomousVehicles/tree/path_planning) for this project, located on the main page of the path_planning branch
3. Read me contains the build instructions and algorithm overview

## PID Controller
1. The souce code for this project is located [here](https://github.com/schandrachary/AutonomousVehicles/tree/pid_control/CarND-PID-Control-Project/src)
2. Please take a look at the [Readme](https://github.com/schandrachary/AutonomousVehicles/blob/pid_control/README.md) for this project to get an overview of PID controller's implementation details



