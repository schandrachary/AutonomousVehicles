## Capstone Project - System Integration

This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

This project is an individual contribution project and all parts of this project was written by Shiva Chandrachary and I can be contacted on my email: shivchaitanya.vc@gmail.com

### Setup

Please use **one** of the two installation options, either native **or** docker installation.

#### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

#### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```

#### Port Forwarding
To set up port forwarding, please refer to the "uWebSocketIO Starter Guide" found in the classroom (see Extended Kalman Filter Project lesson).

#### Usage

1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

#### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images

#### Other library/driver information
Outside of `requirements.txt`, here is information on other driver/library versions used in the simulator and Carla:

Specific to these libraries, the simulator grader and Carla use the following:

|        | Simulator | Carla  |
| :-----------: |:-------------:| :-----:|
| Nvidia driver | 384.130 | 384.130 |
| CUDA | 8.0.61 | 8.0.61 |
| cuDNN | 6.0.21 | 6.0.21 |
| TensorRT | N/A | N/A |
| OpenCV | 3.2.0-dev | 2.4.8 |
| OpenMP | N/A | N/A |


### Project Overview

The system architecture can be subdivided into four major components: Sensors, Perception, Planning and Control. Here is an high level architecture diagram:

![alt_text](/imgs/systemArch1.png)

**Sensors:** There are many different kinds of sensors that an Autonomous Vehicle is equipped with, some of the well known and crucial ones are: _Camera, Radar, Lidar and GPS_. The data from these sensors are to be published at a frequency that can enable high level behavior planning and perception related computations with shortest latency to observe the current model of the world.

**Perception:** Object detection and localization is one of the most important aspects of an Autonomous Vehicle. It is very important that we detect and classify objects around the AV including lane lines, traffic signs, other vehicles, pedestrians, etc.. A number of techniques including classical computer vision and deep neural networks are used to perform perception related tasks.It is not only important to detect an object, like a traffic light but also to classify the color of the traffic light.

Localization module takes in GPS data and other on-board sensor data, along with a high definition map to accurately localize the vehicle within 10cm accuracy.

**Planning:** The output from perception subsystem is fed into planning subsystem to plan the route to the destination. This can get complicated as we want to model the behavior of objects around the host vehicle to determine the safe trajectory.Classified objects from the perception sub system is used in the prediction related tasks. We can model the behavior of the car vs. a pedestrian and predict where they will be in the next **t** seconds.

 We also need the data from the map to accurately localize the host vehicle and plan the route.

**Control:** Once planning is finished, the trajectory generated from the planning subsystem is passed on to control subsystem. There are many different types of controller and some of most popular ones are: PID and MPC. The controller makes sure that the host vehicle follows the trajectory very closely at the desired velocity.


### ROS architecture

The following is a system architecture diagram showing the ROS nodes and topics used in the project.

![alt_text](/imgs/ros-graph.png)

#### Waypoint Updater Node:
The purpose of this node is to update the target velocity property of each waypoint based on traffic light and obstacle detection data. This node will subscribe to the `/base_waypoints`, `/current_pose`, `/obstacle_waypoint`, and `/traffic_waypoint` topics, and publish a list of waypoints ahead of the car with target velocities to the `/final_waypoints` topic.

This node is run at 50 herts. Using the current pose, the waypoint associated with the vehicle's location is extracted. At all times, a hyperparameter tuned _LOOKAHEAD_WPS_ number of waypoints are extracted and published to the `/final_waypoints` topic. If the stop line is within the range, the velocities of the waypoints are gradually decreased as a function of stopping distance. If the stop line is outside of this range, the velocities of the waypoints are set to max velocity from the parameter server.

#### Waypoint Follower:
Once the waypoint updater node is publishing `/final_waypoints`, the waypoint_follower node will start publishing messages to the `/twist_cmd` topic
This allows the twist controller node to send appropriate amount of throttle, steering, and brake commands via `vehicle/throttle_cmd`, `/vehicle/steering_cmd`, and `/vehicle/Brake_cmd` topics. It is very important that twist controller node is running at 50 herts. At lower frequency, the driver by wire system assumes that ROS master has died is not publishing any messages, and it tries to give the control back to the driver.

#### Traffic Light Detection:

Traffic light detection can be split into three parts:

##### Detection

The simulator consists of many traffic lights throughout the track. The topic `/vehicle/traffic_lights` contains the exact location of all traffic lights. And status of all traffic lights is also provided in this topic to test against the classifier output.

At this point, we know the location of the traffic light in world coordinates. When camera captures this traffic light, we need to be able to associate this location with its location on the camera image. First the position of the traffic light is translated and rotated  to convert it to position in camera coordinates. But this will be a flipped image as we are using pin-hole camera model as shown below.

![alt_text](/imgs/pinhole-model.png)

With carefully tuned hyperparameter coefficients, I transform the image from world coordintes to camera coordinates. Note that a quick google search revealed the base hyperparameters and I had to tune it to work with my camera model.

Once we know the location of traffic light in camera coordinates, we can crop the image to look at exactly what we want to look without any background noise - the traffic light. Once the image is cropped, it is passed to the classification block to classify the color of the traffic light.

##### Classification
The RGB image is converted to HSV image. We are interested in only Hue value of the this image. Hue represent the color independent of any change in brightness. A bright red or a dar red has the same hue value. But looking for a threshold of within the range of Red, Green and Yellow pixels, we can determine the state of the traffic light. An example of Red traffic light separated from hue and converted to grayscale is show below:

![alt_text](/ros/src/tl_detector/light_classification/data/redLight.png)
![alt_text](/ros/src/tl_detector/light_classification/data/red_hValue.png)

##### Waypoint Publishing

Once the state of the light is determined, the stop line waypoints and state of the light is published. Note that only if the state of the traffic light is Red, the waypoint to stop at the stop line is published on `/traffic_waypoint` topic, otherwise the previous waypoint is published.

### Result and future work

Traffic light detector and classifier only works in the simulator as this setup needs the location of the traffic light in world coordinates. With this setup, the vehicle in the simulator follows the waypoints and the desired velocity and stops at red light promptly.

In the future, I plan to combine the classical computer vision techniques I used for classifying the traffic light with neural network approach so the detection and classification is robust and can be scalable.

[Here](https://youtu.be/AQ7hin4k33A) is a link to a short clip for demonstration.
