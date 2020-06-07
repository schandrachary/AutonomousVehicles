#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML

#reading in an image
image = mpimg.imread('test_images/solidWhiteRight.jpg')

#printing out some stats and plotting
print('This image is:', type(image), 'with dimensions:', image.shape)
plt.imshow(image)  # if you wanted to show a single color channel image called 'gray', for example, call as plt.imshow(gray, cmap='gray')

import math

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_curved_lines(img, lines, color=[255, 0, 0], thickness=10):
	line_image = np.copy(img)*0
	# Iterate over the output "lines" and draw lines on a blank image
	for line in lines:
	    for x1,y1,x2,y2 in line:
	        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),10)

	# Draw the lines on the edge image
	lines_edges = cv2.addWeighted(img, 0.8, img, 1, 0) 
	plt.imshow(lines_edges)
	plt.show()

def draw_polyfit_lines(img,lines, color=[255, 0, 0], thickness=10):
	leftLaneLine_x = np.array([])
    leftLaneLine_y = np.array([])
    rightLaneLine_x = np.array([])
    rightLaneLine_y = np.array([])
    for line in lines:
        for x1,y1,x2,y2 in line:
            slope = (y2-y1)/(x2-x1)
            
            if(np.isnan(float(slope))):
                continue
            if(abs(slope) < 0.3):
                continue
            
            if(slope < 0):
                #Creat a list of left lane line parameters
                leftLaneLine_x = np.append(leftLaneLine_x, x1)
                leftLaneLine_x = np.append(leftLaneLine_x, x2)
                leftLaneLine_y = np.append(leftLaneLine_y, y1)
                leftLaneLine_y = np.append(leftLaneLine_y, y2)
            else:
                #Creat a list of right lane line parameters
                rightLaneLine_x = np.append(rightLaneLine_x, x1)
                rightLaneLine_x = np.append(rightLaneLine_x, x2)
                rightLaneLine_y = np.append(rightLaneLine_y, y1)
                rightLaneLine_y = np.append(rightLaneLine_y, y2)

    beta_right_lane = np.polyfit(rightLaneLine_x, rightLaneLine_y, 1)
    poly_right = np.poly1d(beta_right_lane)
    
    beta_left_lane = np.polyfit(leftLaneLine_x, leftLaneLine_y, 1)
    poly_left = np.poly1d(beta_left_lane)

    left_lane_x = np.linspace(141, 644, 300)
    right_lane_x = np.linspace(724, 1096, 300)

    for i in range(left_lane_x.size-1):
    	cv2.line(img, (left_lane_x[i], poly_left(left_lane_x[i])), (left_lane_x[i+1], poly_left(left_lane_x[i+1])), color, thickness)

    for i in range(right_lane_x.size-1):
    	cv2.line(img, (right_lane_x[i], poly_right(right_lane_x[i])), (right_lane_x[i+1], poly_right(right_lane_x[i+1])), color, thickness)

def draw_lines(img, lines, color=[255, 0, 0], thickness=10):
    """
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  
    
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.
    
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    leftLaneLine_x = np.array([])
    leftLaneLine_y = np.array([])
    rightLaneLine_x = np.array([])
    rightLaneLine_y = np.array([])
    for line in lines:
        for x1,y1,x2,y2 in line:
            slope = (y2-y1)/(x2-x1)
            
            if(np.isnan(float(slope))):
                continue
            if(abs(slope) < 0.3):
                continue
            
            if(slope < 0):
                #Creat a list of left lane line parameters
                leftLaneLine_x = np.append(leftLaneLine_x, x1)
                leftLaneLine_x = np.append(leftLaneLine_x, x2)
                leftLaneLine_y = np.append(leftLaneLine_y, y1)
                leftLaneLine_y = np.append(leftLaneLine_y, y2)
            else:
                #Creat a list of right lane line parameters
                rightLaneLine_x = np.append(rightLaneLine_x, x1)
                rightLaneLine_x = np.append(rightLaneLine_x, x2)
                rightLaneLine_y = np.append(rightLaneLine_y, y1)
                rightLaneLine_y = np.append(rightLaneLine_y, y2)
                
    # All the lane data needs to be a Nx1 vector
    rightLaneLine_x = rightLaneLine_x.reshape((rightLaneLine_x.size,1))
    rightLaneLine_y = rightLaneLine_y.reshape((rightLaneLine_y.size,1))
    leftLaneLine_x = leftLaneLine_x.reshape((leftLaneLine_x.size,1))
    leftLaneLine_y = leftLaneLine_y.reshape((leftLaneLine_y.size,1))
    
    # Using least squares, fit the model
    # First, create design matrix    
    ones_vector_right = np.ones((rightLaneLine_x.size,1), dtype='int32')
    ones_vector_left = np.ones((leftLaneLine_x.size,1), dtype='int32')
    
    # Create 2 design matrix for left and right lane each. One to fit the model, another for prediction
    X_rightLaneLine = np.hstack([ones_vector_right, rightLaneLine_x])
    # Add extremeties and create design matrix for right lane line
    rightLaneLine_x_extremeties = rightLaneLine_x.copy()      
    rightLaneLine_x_extremeties = np.append(rightLaneLine_x_extremeties, 495)
    rightLaneLine_x_extremeties = np.append(rightLaneLine_x_extremeties, 900)
    # Reshape to be a vector
    rightLaneLine_x_extremeties = rightLaneLine_x_extremeties.reshape((rightLaneLine_x_extremeties.size,1))
    #create a vector of ones and create the design matrix
    ones_vector_right = np.ones((rightLaneLine_x_extremeties.size,1), dtype='int32')
    X_rightLaneLine_extremeties = np.hstack([ones_vector_right, rightLaneLine_x_extremeties])
    
    X_leftLaneLine = np.hstack([ones_vector_left, leftLaneLine_x])
    # Add extremeties and create design matrix for left lane line
    leftLaneLine_x_extremeties = leftLaneLine_x.copy()
    leftLaneLine_x_extremeties = np.append(leftLaneLine_x_extremeties, 140)
    leftLaneLine_x_extremeties = np.append(leftLaneLine_x_extremeties, 455)
    # Reshape to be a vector    
    leftLaneLine_x_extremeties = leftLaneLine_x_extremeties.reshape((leftLaneLine_x_extremeties.size,1))
    #create a vector of ones and create the design matrix
    ones_vector_left = np.ones((leftLaneLine_x_extremeties.size,1), dtype='int32')
    X_leftLaneLine_extremeties = np.hstack([ones_vector_left, leftLaneLine_x_extremeties])
    
    # Fit the model
    b_rightLaneLine = np.matmul(np.linalg.pinv(np.matmul(np.transpose(X_rightLaneLine), X_rightLaneLine)), np.matmul(np.transpose(X_rightLaneLine), rightLaneLine_y))
    b_leftLaneLine = np.matmul(np.linalg.pinv(np.matmul(np.transpose(X_leftLaneLine), X_leftLaneLine)), np.matmul(np.transpose(X_leftLaneLine), leftLaneLine_y))

    yHat_rightLaneLine = np.matmul(X_rightLaneLine_extremeties, b_rightLaneLine)
    yHat_leftLaneLine = np.matmul(X_leftLaneLine_extremeties, b_leftLaneLine)

    # sort before drawing the line
    # rightLaneLine_x_extremeties = rightLaneLine_x_extremeties.sort()
    # yHat_rightLaneLine = yHat_rightLaneLine.sort()
    # leftLaneLine_x_extremeties = leftLaneLine_x_extremeties.sort()
    # yHat_leftLaneLine = yHat_leftLaneLine.sort()
    
    for i in range(yHat_rightLaneLine.size-1):
        cv2.line(img, (rightLaneLine_x_extremeties[i], yHat_rightLaneLine[i]), (rightLaneLine_x_extremeties[i+1], yHat_rightLaneLine[i+1]), color, thickness=10)
    
    for i in range(yHat_leftLaneLine.size-1):
        cv2.line(img, (leftLaneLine_x_extremeties[i], yHat_leftLaneLine[i]), (leftLaneLine_x_extremeties[i+1], yHat_leftLaneLine[i+1]), color, thickness=10)         


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    #draw_curved_lines(img, lines)
    return line_img

# Python 3 has support for cool math symbols.
def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)


def process_image(image):
    # NOTE: The output you return should be a color image (3 channel) for processing video below
    # TODO: put your pipeline here,
    # you should return the final output (image where lines are drawn on lanes)
    
    # Lets perform Canny Edge detection now
    kernel_size = 5
    blur_image = gaussian_blur(image, kernel_size)

    # Run Canny on the blurred image
    low_threshold = 50
    high_threshold = 150
    edges = canny(blur_image, low_threshold, high_threshold)
    
    # Create a masked image with vertices of a polygon
    imshape = image.shape
    vertices = np.array([[(50, imshape[0]), (450, 330), (510, 330), (imshape[1]-50, imshape[0])]])
    masked_edges = region_of_interest(edges, vertices)
    plt.imshow(masked_edges, cmap='gray')
    
    # Lets perform Hough Transform on edge detected image
    rho = 1
    theta = np.pi/180
    threshold = 25
    min_line_length = 5
    max_line_gap = 5

    line_image = hough_lines(masked_edges, rho, theta, threshold, min_line_length, max_line_gap)

    # Create a color binary image to combine with the line_image
    color_edges = np.dstack((edges, edges, edges))

    lines_edges = weighted_img(line_image, image)
    
    return lines_edges

# process all the images in the test directory
import glob
import os
for image in glob.glob('test_images/*.jpg'):
    img = cv2.imread(image)
    print('Processing image {}'.format(image))
    filename = image.split('\\')[1]
    lines = process_image(img)
    if not cv2.imwrite('test_image_output/'+filename,lines):
        raise Exception("Could not write image")