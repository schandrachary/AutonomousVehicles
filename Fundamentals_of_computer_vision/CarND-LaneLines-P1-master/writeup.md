# **Finding Lane Lines on the Road** 

## Writeup

---

**Finding Lane Lines on the Road**

The goals of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report

---

## Reflection

#### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

First, I converted the images to grayscale. A gray scale image looks like this:
![image](https://user-images.githubusercontent.com/8539470/83980667-917bac80-a8e5-11ea-8bc9-39204e1bd023.png)

Then, I blurred the image using gaussian_blur() with a kernel size of 5. Next, I detected the edges using canny edge detection. This returns the edges in the image which has a steep color gradient. Here's how the output of canny edge detection look like:

![image](https://user-images.githubusercontent.com/8539470/83980694-bd972d80-a8e5-11ea-936d-ae260e701d64.png)

Next, we want to isoloate lane information in the image from the noise. Here the noise would be everything but the lane lines. To do that, we mask the image to focus only on the ground and eliminate the rest from the image. This is the output of masking the image in my pipeline:

![image](https://user-images.githubusercontent.com/8539470/83980722-ee776280-a8e5-11ea-9cdc-591f6703fa9d.png)

Once this is performed, we get the edge detected image that is focused on the ground plane. We most likely have lane information to deal with in this step. Performing Hough Transform on this image produces lines that closely matches the lane line information. I take hough lines from this step and draw them on top of input image, which produces red lines on top of lane lines. Output of this step looks like this: 
![image](https://user-images.githubusercontent.com/8539470/83980617-38137d80-a8e5-11ea-9d92-33378c266581.png)

Next challenge is to connect the segmented lines and draw one single solid line. To do this, we have to think about the slopes of each of the hough lines. Hough lines with a slope that is negative indicate it belong to left lane line and a positive slope indicate a line from right lane line. I use this technique to build a list of lines for left and right lane line. From here, I found two ways to deal with the problem. 

First option is to use the built in polyfit() function that returns the coefficients of the polynomial. And use those coefficients to plot lines for any given `(x,y)`. Here, we would plot it with `x` ranging from left lane to right lane plus some offset. 

The second option, though might sound complicated, it gives us the flexibility to control the algorithm. I built a model to linearly fit the data using least squares approximation. To do this, first, we have to build a design matrix, `X`. My design matrix consisted of `Nx2` matrix with slope and intercept. Next, we fit the model and find the beta coefficient using the formula:
`beta = (X^T * X)^-1 * X^T*y`
                                          
With beta coefficient, we can calculate yHat, that gives the close approximation to original line. I have used both the methods separately to fit the line and they almost look alike. In my code, the function that uses python's polyfit function to draw solid lines is called `draw_polyfit_lines()`. And the function that uses least squares approximation is written inside `draw_lines()`. 

Here is the output of this step: 
![image](https://user-images.githubusercontent.com/8539470/83981243-2aacc200-a8ea-11ea-9fdb-56bc2a009634.png)



There was an additional challenge in this project, to detect lines for the curved road scenario. The code for this part of the challenge is located in `curvedLaneFinding.py`. The images in this video were of different resolution, and after masking the noise out of the canny edge detected image, I tried to fit hough lines with first, second and third degree polynomial fit operation. After many passes, the first degree polynomial appeared to result in a stable output. The output of this operation looks like this:
![image](https://user-images.githubusercontent.com/8539470/83981479-297c9480-a8ec-11ea-9f4b-43584179bf26.png)


### 2. Identify potential shortcomings with your current pipeline


One potential shortcoming would be what would happen when the lane lines bend. I have used linear approximation to fit the points here and it will not work when there is curved lane lines.

Another shortcoming that I see in my result is that the extrapolated lines doesn't seem to the stable. It is jittery and wobbles through out the test video. 


### 3. Suggest possible improvements to your pipeline

A possible improvement would be to use non-linear approximation to fit the lane lines that would attempt to fix the approximation issues we had in the curved lane line scenario. 

