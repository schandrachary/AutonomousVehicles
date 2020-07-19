# **Behavioral Cloning**

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[image1]: /writeup_images/multiple_cameras.png "Multiple Cameras"
[nn1]: /writeup_images/nn-1.png "NN 1"
[nn2]: /writeup_images/nn-2.png "NN 2"
[center]: /writeup_images/center.jpg "center"
[left]: /writeup_images/left.jpg "left"
[right]: /writeup_images/right.jpg "right"
[loss]: /writeup_images/loss_function.png "loss"

## Rubric Points
### Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.

---
### Files Submitted & Code Quality

#### 1. Submission includes all required files and can be used to run the simulator in autonomous mode

My project includes the following files:
* model.py containing the script to create and train the model
* drive.py for driving the car in autonomous mode
* model.h5 containing a trained convolution neural network
* writeup_behavioral_cloning.md summarizing the results

#### 2. Submission includes functional code
Using the Udacity provided simulator and my drive.py file, the car can be driven autonomously around the track by executing
```sh
python drive.py model.h5
```

#### 3. Submission code is usable and readable

The model.py file contains the code for training and saving the convolution neural network. The file shows the pipeline I used for training and validating the model, and it contains comments to explain how the code works.

### Model Architecture and Training Strategy

#### 1. An appropriate model architecture has been employed

My model consists of a total of 10 layers with five convolutional layers and 3 fully connected layers along with one normalization and cropping layer. The first three convolution layer
has a filter size of 5x5 and the remaining two has a filter size of 3x3 with depths ranging from 24 to 64 between these five layers. The pipeline of this architecture can be found in model.py between lines 77 and 128.

The model includes RELU activation layers to introduce nonlinearity for all the convolutional layers, and the data is normalized in the model using a Keras lambda layer (code line 80).

#### 2. Attempts to reduce overfitting in the model

The model contains three dropout layers in order to reduce overfitting (model.py lines 104, 113, and 119).

The model was trained and validated on different data sets to ensure that the model was not overfitting (code lines 67-68). The model was tested by running it through the simulator and ensuring that the vehicle could stay on the track.

#### 3. Model parameter tuning

The model used an adam optimizer, so the learning rate was not tuned manually (model.py line 129).

#### 4. Appropriate training data

Training data was chosen to keep the vehicle driving on the road. I used a combination of camera images from center, left and right camera. This helps in
recording recovery data from the side of the road. The principal behind this approach is that from the perspective of the left camera, the steering angle
would be less than the steering angle from the center camera to turn towards a destination on the left. And the from the perspective of the right camera,
the steering angle would be larger than than the angle from the center camera

![alt text][image1]

### Model Architecture and Training Strategy

#### 1. Solution Design Approach

The overall strategy for deriving a model architecture was to extract the information from the road images. CNN was not trained to drive down the middle of the
road, but simply asked to observe the steering wheel angle for a given image. CNN extracts road boundary and edges as a result of this training.

I started out with a simple neural network containing containing flattened layer. This architecture was primitive and was constantly outputting steering
wheel angles from negative max to positive max. But this gave me confirmation that I had set everything up correctly, until the model architecture.

Second natural step from here was to improve the model. I started out using just two convolutional layers with 42 filters and four fully connected layers. This architecture
worked quite well, I was able to run the car autonomously in track-1. A video of this file can be found in the workspace with name `shivArch_run1.mp4`
Since this architecture had only two convolutional layers, it wouldn't have been able to extract all the features required to complete both the tracks. We need a model that
can generalize to new data well. So, I moved on to a more sophisticated architecture from Nvidia. The details of this architecture can be found in the next section.


I also introduced three dropout layers to combat for overfitting.

In order to gauge how well the model was working, I split my image and steering angle data into a training and validation set. I used 20% of my data set as the validation set.

The final step was to run the simulator to see how well the car was driving around track one. There were a few spots where the vehicle fell off the track. To improve the driving behavior in these cases,
I varied the hyperparameter that determines the steering wheel angle from left and right camera. After experimenting with different values, I finally settled with `correction = 0.2`.

At the end of the process, the vehicle is able to drive autonomously around both the tracks without leaving the road.

#### 2. Final Model Architecture

The final architecture I settled on was from [Nvidia](http://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf). This architecture contains five convolution layers
followed by four fully connected layers. Here is a visualization of the model architecture:

<img src = "/writeup_images/nn-1.svg" height="1200" width="900" />
<img src = "/writeup_images/nn-2.svg" height="1200" width="900" />


The final model architecture consists of a total of 10 layers with five convolutional layers and 3 fully connected layers along with one normalization and cropping layer. The first three convolution layer
has a filter size of 5x5 and the remaining two has a filter size of 3x3 with depths ranging from 24 to 64 between these five layers. The pipeline of this architecture can be found in model.py between lines 77 and 128.

The model includes RELU activation layers to introduce nonlinearity for all the convolutional layers, and the data is normalized in the model using a Keras lambda layer (code line 80).


#### 3. Creation of the Training Set & Training Process

To capture good driving behavior, I first recorded one lap on track one using center lane driving behavior. Here is an example image of center lane driving:

![alt_text][center]

I then captured images from left and right camera for the same run. Here are the images from the perspective of left and right camera:

![alt text][left]
![alt text][right]

The data used for traning the network can be found in the workspace director: `CarND-Behavioral-Cloning-p3/ShivData`

Because track one has larger percentage of counter clockwise turns, the model biases the steering wheel angle to the left. To combat this issue,
I recorded one lap going in the opposite direction. This gave me a perfectly balanced data set and more data.


Then I repeated this process on track two in order to get more data points.

I did not need to flip the images since I recorded data on the track going in the opposite direction, which yielded me a balanced dataset.

After the collection process, I had 10130 number of data points. I then preprocessed this data by normalizing the images with zero mean. I also cropped
the top 50 pixels containing sky, mountains and trees and bottom 25 pixels containing the hood of the car. These are irrelevant information
to the neural network which makes it difficult to learn the patterns.


I finally randomly shuffled the data set and put 20% of the data into a validation set.

I used this training data for training the model. The validation set helped determine if the model was over or under fitting. The ideal number of epochs was 4 as evidenced by the plot below, which shows that the validation accuracy remains stagnant. I used an adam optimizer so that manually training the learning rate wasn't necessary.

![alt text][loss]
