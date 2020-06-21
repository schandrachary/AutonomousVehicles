###########################################################################
# Three step process to get the images ready to be processed further
# down the pipeline. 
# 1. Distortion correction
# 2. Color and Gradient thresholding
# 3. Perspective transform the thresholded binary image
#
# Usage: First call distortionCorrection() which returns undistorted
# image. Pass the undistorted image to colorAndGradientThreshold()
# to get a thresholded binary image. This image can be perspective
# transformed using perspectiveTransform().
###########################################################################


import pickle
import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

image = mpimg.imread('../test_images/test2.jpg')
img_size = (image.shape[1], image.shape[0])
# Source and destination points for perspective transform
source = np.float32([[260,688], [601,445], [675,445], [1030,688]])
destination = np.float32([[345, img_size[1]], [345, 0], [1000, 0], [1000, img_size[1]]])

def distortionCorrection(image):
    # Load the pickle file containing camera matrix and distortion coefficients
    dist_coefficients = pickle.load(open("../camera_cal/distortion_coeff.p","rb"))
    mtx = dist_coefficients["mtx"]
    dist = dist_coefficients["dist"]

    # Undistort the incomig image
    undistort = cv2.undistort(image, mtx, dist, None, mtx)
    return undistort

def colorAndGradientThreshold(img, color_threshold=(170,255), gradient_threshold=(20,100)):
    img = np.copy(img)

    # Convert to HSV color space and separate the V channel
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    s_channel = hsv[:,:,1]
    v_channel = hsv[:,:,2]

    # Sobel x
    sobelx = cv2.Sobel(v_channel, cv2.CV_64F, 1, 0, ksize=5) # Take the derivative in x
    abs_sobelx = np.absolute(sobelx) # Absolute x derivative to accentuate lines away from horizontal
    scaled_sobel = np.uint8(255*abs_sobelx/np.max(abs_sobelx))

    # Threshold x gradient
    gradient_binary = np.zeros_like(scaled_sobel)
    gradient_binary[(scaled_sobel >= gradient_threshold[0]) & (scaled_sobel <= gradient_threshold[1])] = 1

    # Threshold color channel
    color_binary = np.zeros_like(s_channel)
    color_binary[(s_channel >= color_threshold[0]) & (s_channel <= color_threshold[1])] = 1

    # Combine color and gradient binary images
    combined_binary = np.zeros_like(gradient_binary)
    combined_binary[(gradient_binary==1) | (color_binary==1)] = 1

    return combined_binary

def perspectiveTransform(undistored_binary, img_size, source, destination):    
    # Get transformation matrix by performing perspective transform and warp the image
    M = cv2.getPerspectiveTransform(source, destination)
    warped = cv2.warpPerspective(undistored_binary, M, img_size, flags=cv2.INTER_LINEAR)
    return warped


# # Undistort the incoming image
# undistort = distortionCorrection(image)

# # Pass in undistorted image to perform thresolding
# undistored_binary = colorAndGradientThreshold(undistort)
# warped_binary = perspectiveTransform(undistored_binary, img_size, source, destination)
# # Uncomment the below two lines to save a color warped image
# # warped_binary = perspectiveTransform(image, img_size, source, destination)
# # plt.imsave("../output_images/warped_color.jpg", warped_binary)

# # Save the binary image in the output_images dir
# plt.imsave("../output_images/dist_corrected.jpg", undistort)
# plt.imsave("../output_images/warped_binary.jpg", warped_binary, cmap='gray')
# plt.imsave("../output_images/original_image.jpg", image)
# plt.imsave("../output_images/color_gradient_thresh.jpg", undistored_binary, cmap='gray')


# #Plot the result
# f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30, 9))
# f.tight_layout()

# ax1.imshow(image)
# ax1.set_title('Original Image',fontsize=25)
# ax2.imshow(undistored_binary, cmap='gray')
# ax2.set_title('ColorAndGradentThresolding', fontsize=25)
# ax3.imshow(warped_binary, cmap='gray')
# ax3.set_title('Warped image', fontsize=25)
# plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
# f.savefig("../output_images/color_and_gradent_thresolding.jpg")
# plt.show()
