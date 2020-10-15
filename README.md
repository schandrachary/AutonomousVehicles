# **Traffic Sign Recognition**

## Writeup
---

The goals / steps of this project are the following:
* Load the data set (see below for links to the project data set)
* Explore, summarize and visualize the data set
* Design, train and test a model architecture
* Use the model to make predictions on new images
* Analyze the softmax probabilities of the new images
* Summarize the results with a written report


[//]: # (Image References)


[image1]: https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/original_dataset_chart.jpg "Original graph"
[image2]: https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/20kmphOriginal.png "Original image"
[image3]: https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/grayNorm.png "Grayscaled image"
[image4]: https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/20kmphAugmented.png "Augmented image"
[image5]: https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/augmented_dataset_chart.png "Augmented image"
[image6]: https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/accuracyGraph.png  "accuracy image"

[image5]: https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/test_images/original_images/stop-sign.png "stop"
[image6]: https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/test_images/original_images/animalCrossing.png "animalCrossing"
[image7]: https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/test_images/original_images/strightLeft.png "straightLeft"
[image8]: https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/test_images/original_images/pedestrian.png "pedestrian"
[image9]: https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/test_images/original_images/30kmph.png "30kmph"

### Data Set Summary & Exploration

#### 1. Provide a basic summary of the data set. In the code, the analysis should be done using python, numpy and/or pandas methods rather than hardcoding results manually.

I used the numpy library to calculate summary statistics of the traffic
signs data set:

* The size of training set is 34799
* The size of the validation set is 4410
* The size of test set is 12630
* The shape of a traffic sign image is (32, 32, 3)
* The number of unique classes/labels in the data set is 43

#### 2. Include an exploratory visualization of the dataset.

Here is an exploratory visualization of the data set. It is a bar chart showing how the data is distributed for various classes. You might keen to note that some classes have more images than the others. This makes a difference when we are training a network. For us to train the model well, we should strive to get a balanced data set. More on how we solve this problem down below.

![alt text][image1]

### Design and Test a Model Architecture

#### 1. Describe how you preprocessed the image data. What techniques were chosen and why did you choose these techniques? Consider including images showing the output of each preprocessing technique. Pre-processing refers to techniques such as converting to grayscale, normalization, etc. (OPTIONAL: As described in the "Stand Out Suggestions" part of the rubric, if you generated additional data for training, describe why you decided to generate additional data, how you generated the data, and provide example images of the additional data. Then describe the characteristics of the augmented training set like number of images in the set, number of images for each class, etc.)

As a first step, I decided to convert the images to grayscale because color is not an important factor in traffic sign recognition system. The network trains better when it is able to see contrast in the images and it learns the geometrical shapes of the signs. The image binarization will help in sharpening the image by identifying the light and dark areas. These variations are crucial to determine changes in the image.

It also important to normalize the dataset so the dataset has zero mean and equal variance.

Here is an example of an original traffic sign image and after grayscaling and normalizing.

![alt text][image2]
![alt text][image3]

As explanined in summary point No. 2, it was important for us to have balanced dataset. Therefore, I decided to generate additional data.

To add more data to the the data set, I used the following techniques:
1. Rotate the original image
2. Transform the original by an offset

Here is an example of an original image and an augmented image:

![alt text][image2]
![alt text][image4]

Although the resolution of the augmented image remains the same, I have introduced rotation and translation, which will be important when the car drives around in the real world and images are captured from an angel. When trained on these images, it is expected that the model generalizes for varying images of a particular class, striving for stretch pants solution without having to collect more data. 

A summary statistics of the augmented dataset:

* The size of augmented training set is 67415
* The size of the validation set is 4410
* The size of test set is 12630
* The shape of a traffic sign image is (32, 32, 3)
* The number of unique classes/labels in the data set is 43

![alt text][image5]


#### 2. Describe what your final model architecture looks like including model type, layers, layer sizes, connectivity, etc.) Consider including a diagram and/or table describing the final model.

My final model consisted of the following layers:

| Layer         		|     Description	        					|
|:---------------------:|:---------------------------------------------:|
| Input         		  | 32x32x1 grayscale image   							        |    
| Convolution 5x5     | 1x1 stride, valid padding, outputs 28x28x6 	    |
| RELU					      |												                          |
| Max pooling	      	| 2x2 stride, 2x2 size, outputs 14x14x6	          |
| Convolution 5x5	    | 1x1 stride, valid padding, outputs 10x10x16     |
| RELU					      |												                          |
| Max pooling	      	| 2x2 stride, 2x2 size, outputs 5x5x16	          |
| Fully connected		  | 400 input, output size 120					            |
| RELU					      |												                          |
| Dropout					    | 60%												                      |
| Fully connected		  | 120 input, output size 84					              |
| RELU					      |												                          |
| Dropout					    | 60%												                      |
| Fully connected		  | 84 input, output size 10					              |
| Softmax				      | output Probabilities, output size 10            |
|	Cross Entropy				|	output Loss, output size 10											|



#### 3. Describe how you trained your model. The discussion can include the type of optimizer, the batch size, number of epochs and any hyperparameters such as learning rate.

To train the model, I experimented with various hyperparameters, but here are the ones I settled on since it gave me the best result:
1. Batch size: 128
2. Epoch: 30
3. Learning rate: 0.00095
4. Dropout 0.60

#### 4. Describe the approach taken for finding a solution and getting the validation set accuracy to be at least 0.93. Include in the discussion the results on the training, validation and test sets and where in the code these were calculated. Your approach may have been an iterative process, in which case, outline the steps you took to get to the final solution and why you chose those steps. Perhaps your solution involved an already well known implementation or architecture. In this case, discuss why you think the architecture is suitable for the current problem.

My final model results were:
* training set accuracy of 98.0%
* validation set accuracy of 94.8%
* test set accuracy of 94.0%

![alt text][image6]

I chose lenet's architecture to train the traffic sign recognition model. The original architecture didn't suit my purpose(since it was first created for text recognition), so I modified some of the elements in this architecture.
* I chose RELU as my activation function at the end of each layer as it introduces non-linearity to the network
* After running the training set for a few iterations, I realized that validation accuracy was low and training accuracy was close to 100%. That gave me an indication that the network was overfitting the dataset. Therefore, I introduced dropout only on the fully connected layers, with keep probability of 60%. The weights are generally distributed well in the convolutional layer, since we are using a small filter. So, it didn't make sense to add a dropout layer in the convolutional layer.

### Test a Model on New Images

#### 1. Choose five German traffic signs found on the web and provide them in the report. For each image, discuss what quality or qualities might be difficult to classify.

Here are five German traffic signs that I found on the web:

<img src="https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/test_images/original_images/stop-sign.png" alt="drawing" width="200"/>
<img src="https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/test_images/original_images/animalCrossing.png" alt="drawing" width="300"/>
<img src="https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/test_images/original_images/strightLeft.png" alt="drawing" width="200"/>
<img src="https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/test_images/original_images/pedestrian.png" alt="drawing" width="170"/>
<img src="https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/test_images/original_images/30kmph.png" alt="drawing" width="250"/>


#### 2. Discuss the model's predictions on these new traffic signs and compare the results to predicting on the test set. At a minimum, discuss what the predictions were, the accuracy on these new predictions, and compare the accuracy to the accuracy on the test set (OPTIONAL: Discuss the results in more detail as described in the "Stand Out Suggestions" part of the rubric).

Here are the results of the prediction:

| Image			        |     Prediction	        					|
|:---------------------:|:---------------------------------------------:|
| Stop Sign      		    | Stop sign   									|
| Animal Crossing     		| Animal Crossing 										|
| Stright or left					| Stright or left											|
| 30 km/h	      		     | 30 km/h					 				|
| Pedestrian			       | Road narrows on the right    							|


The model was able to correctly guess 4 out of the 5 traffic signs, which gives an accuracy of 80%. I believe this model has been trained well to be generalized to new set of images but it also did poorly on images that have similar structure. As you can see, the top guess for pedestrian is 24, which is "Road narrows on the right". Guess no. 24 has long lines which was trained as legs on a person. Down below I plot featuremaps of this image.

Here's what this model is predicting as its top 5 choices for every class:

<img src="https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/top_k_5.png" alt="drawing" height="950"/>


#### 3. Describe how certain the model is when predicting on each of the five new images by looking at the softmax probabilities for each prediction. Provide the top 5 softmax probabilities for each image along with the sign type of each probability. (OPTIONAL: as described in the "Stand Out Suggestions" part of the rubric, visualizations can also be provided such as bar charts)

The code for making predictions on my final model is located in the Analyze Perfomace section of Ipython notebook

The model is 80% certain for test images. The top five soft max probabilities were

| Probability         	|     Prediction	        					|
|:---------------------:|:---------------------------------------------:|
| 1.0         			| Stright or left   									|
| 0.99     				| 30 km/h 										|
| 0.98					| Pedestrian											|
| 0.97	      			| Animal Crossing					 				|
| 0.99				    | Stop Sign      							|


<img src="https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/softmax.png" alt="drawing" height="950"/>


### (Optional) Visualizing the Neural Network (See Step 4 of the Ipython notebook for more details)
#### 1. Discuss the visual output of your trained network's feature maps. What characteristics did the neural network use to make classifications?

Here I would like to discuss what CNN looks for in terms of features while classifying an image. Let's take a look at wrongly classified image, Pedestrian. The output featuremap of RELU after first convolutional layer looks like this:

<img src="https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/featuremap1_relu.png" alt="drawing" width="650"/>

And featuremap after max-pool looks like this:

<img src="https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/featuremap1_pool.png" alt="drawing" width="650"/>

It appears that first convolutional layer was doing a good job in classifying for the right class, hence we still see some activations in softmax output. It is mostly interested in hight level details of the image here, like edges, sudden changes in the gradient, etc.

Lets dig a little deeper. Lets take a look at 15 layer featuremap output of second convolutional layer after RELU and Maxpool operations, respectively:

<img src="https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/featuremap2_relu.png" alt="drawing" width="650"/>

<img src="https://github.com/schandrachary/AutonomousVehicles/blob/traffic_sign_classifier/CarND-Traffic-Sign-Classifier-Project/writeup_images/featuremap2_pool.png" alt="drawing" width="650"/>

It appears that in the second layer, CNN is picking up on lower level details of the image, like gradients.
