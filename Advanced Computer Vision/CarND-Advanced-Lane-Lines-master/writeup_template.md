## Writeup

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./camera_cal/test_image3.jpg "Distorted"
[undist]: ./camera_cal/test_undist.jpg "Undistorted"
[persp]: ./camera_cal/undistorted_warped.jpg "PerspTrans"
[distCorrect]: ./camera_cal/dist_corrected.jpg "Dist Corrected"
[comparison]: ./camera_cal/color_and_gradent_thresolding.jpg "comparison"
[colorGrad]: ./camera_cal/color_gradient_thresh.jpg "Thresholdin"
[image2]: ./test_images/test1.jpg "Road Transformed"
[image3]: ./examples/binary_combo_example.jpg "Binary Example"
[image4]: ./examples/warped_straight_lines.jpg "Warp Example"
[image5]: ./examples/color_fit_lines.jpg "Fit Visual"
[image6]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in two files: [cameraCalibration.py](https://github.com/schandrachary/AutonomousVehicles/blob/advanced_computer_vision/Advanced%20Computer%20Vision/CarND-Advanced-Lane-Lines-master/source/cameraCalibration.py) and [distortionCorrection.py](https://github.com/schandrachary/AutonomousVehicles/blob/advanced_computer_vision/Advanced%20Computer%20Vision/CarND-Advanced-Lane-Lines-master/source/distortionCorrection.py). 

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection. Here's the distorted image that was chosen to be corrected: 
 
 ![alt text][image1]
 
`cameraCalibration.py` runs through all the images in `camera_cal` directory and stores image and object points for each of them. And then, those points are used in `distortionCorrection.py` to calibrate the camera and get the camera matrix and distortion coefficients. Using this, a test image is undistorted and chess board coners are found on the undistorted image. Here's the output image after undistortion:

![alt text][undist]

The final step of this process is to get a warped image using perspective transform. Perspective transform is performed down the line in the pipeline after performing thresholding on the images, but here's how a perspective transform would look like in comparison to original and undistorted image:

![alt_text][persp]




### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

Like explained in the above distortion correction step, the input image is corrected for distortion and an output of that looks like this:
![alt text][distCorrect]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image, and all these steps are performed in [this]((https://github.com/schandrachary/AutonomousVehicles/blob/c3ea8010675b3bb70fb8ca183ece17fbef46c0ec/Advanced%20Computer%20Vision/CarND-Advanced-Lane-Lines-master/source/thresholding.py#L37)) function. First, I applied sobel operator on the v-channel of HSV color space. This is does in line 40 through 48. Then I perform gradient thresholding on scaled sobel image. This is done in line 50 through 52. Now that I have sobel and a thresholded image, the next step is to get the best of both of these worlds. So I combine these two images in lines 54 through 61.  Here's an example of my output for this step.

![alt text][colorGrad]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warper()`, which appears in lines 1 through 8 in the file `example.py` (output_images/examples/example.py) (or, for example, in the 3rd code cell of the IPython notebook).  The `warper()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points. 

The code for perspective transform is performed in `thresholding.py` starting on line 64. By passing in source and desination points like below to `cv2.getPerspectiveTransform()` function, yields a transformation matrix. We can use that matrix to warp an image. I chose the hardcode the source and destination points in the following manner:

```python
img_size = (image.shape[1], image.shape[0])
source = np.float32([[260,688], [601,445], [675,445], [1030,688]])
destination = np.float32([[345, img_size[1]], [345, 0], [1000, 0], [1000, img_size[1]]])
```

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 260, 688      | 345, 720      | 
| 601, 445      | 345, 0        |
| 675, 445      | 1000, 0       |
| 1030, 688     | 1000, 720     |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image. Here's a comparision of all the steps thus far:

![alt text][comparison]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like this:

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in lines # through # in my code in `my_other_file.py`

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
