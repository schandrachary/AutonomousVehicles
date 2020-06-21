import numpy as np
import cv2
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip
import thresholding as thresholding
from line import Line

################### HYPERPARAMETERS  ####################
# Choose the number of sliding windows
nwindows = 9
# Set the width of the windows +/- margin
margin = 115
# Set minimum number of pixels found to recenter window
minpix = 50
# Lane offset from the center while searching for lane pixles
lane_offset = 460

# Define conversions in x and y from pixels space to meters
ym_per_pix = 30/720 # meters per pixel in y dimension
xm_per_pix = 3.7/700 # meters per pixel in x dimension

#######################################################


def processImages(image):
    img_size = (image.shape[1], image.shape[0])

    # Create an instance of left and right lane
    left_line = Line(img_size[0],img_size[1])
    right_line = Line(img_size[0],img_size[1])


    # Source and destination points for perspective transform
    source = np.float32([[260,688], [601,445], [675,445], [1030,688]])
    destination = np.float32([[345, img_size[1]], [345, 0], [1000, 0], [1000, img_size[1]]])

    # Undistort the incoming image
    undistort = thresholding.distortionCorrection(image)
    # Pass in undistorted image to perform thresolding
    undistored_binary = thresholding.colorAndGradientThreshold(undistort)
    # Get warped image by performing perspective transform
    warped_binary = thresholding.perspectiveTransform(undistored_binary, img_size, source, destination)
    # Find lane pixels, and fit and a polynomial
    out_img = fitPolynomial(warped_binary, left_line, right_line)


    ########################### Visualization #########################
    # Create an image to draw the lines on
    warp_zero = np.zeros_like(warped_binary).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

    # Recast the x and y points into usable format for cv2.fillPoly()
    pts_left = np.array([np.transpose(np.vstack([left_line.fitx, left_line.fity]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_line.fitx, right_line.fity])))])
    pts = np.hstack((pts_left, pts_right))

    # Draw the lane onto the warped blank image
    cv2.fillPoly(color_warp, np.int_([pts]), (0,255, 0))

    # Warp the blank back to original image space using inverse perspective matrix (Minv)
    Minv = cv2.getPerspectiveTransform(destination, source)
    newwarp = cv2.warpPerspective(color_warp, Minv, (image.shape[1], image.shape[0])) 
    # Combine the result with the original image
    result = cv2.addWeighted(undistort, 1, newwarp, 0.3, 0)

    # Add radius of curvature overlay to resul image
    text(result, 'Radius of Curvature: {}m'.format(averageRadius(left_line,right_line)), 50, 100)
    
    # Add distance from center of the image to resul image
    lane_width = left_line.distance + right_line.distance
    center_offset = right_line.distance - lane_width/2
    text(result, 'Distane from Center: {:.2f}m'.format(center_offset), 50,130)

    # Add an overlay of lane pixel detections    
    lane_pixels = cv2.resize(out_img, None, fx=0.3, fy=0.3)
    x_offset = 850
    y_offset = 25
    result[y_offset:y_offset+lane_pixels.shape[0], x_offset:x_offset+lane_pixels.shape[1], :] = lane_pixels

    ########################### End visualization #########################

    return result

# Find lane pixels using sliding window
def findLanePixels(warped_binary):
    # Take a histogram of the bottom half of the image
    histogram = np.sum(warped_binary[warped_binary.shape[0]//2:,:], axis=0)
    # Create an output image to draw on and visualize the result
    out_img = np.dstack((warped_binary, warped_binary, warped_binary))
    # Find the peak of the left and right halves of the histogram
    # These will be the starting point for the left and right lines
    midpoint = np.int(histogram.shape[0]//2)
    leftx_base = np.argmax(histogram[midpoint-lane_offset:midpoint]) + midpoint-lane_offset
    rightx_base = np.argmax(histogram[midpoint:midpoint+lane_offset]) + midpoint

    # Set height of windows - based on nwindows above and image shape
    window_height = np.int(warped_binary.shape[0]//nwindows)
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = warped_binary.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    # Current positions to be updated later for each window in nwindows
    leftx_current = leftx_base
    rightx_current = rightx_base

    # Create empty lists to receive left and right lane pixel indices
    left_lane_inds = []
    right_lane_inds = []

    # Step through the windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = warped_binary.shape[0] - (window+1)*window_height
        win_y_high = warped_binary.shape[0] - window*window_height
        
        # Find the four below boundaries of the window 
        win_xleft_low = leftx_current - margin  
        win_xleft_high = leftx_current + margin 
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        
        # Draw the windows on the visualization image
        cv2.rectangle(out_img,(win_xleft_low,win_y_low),
        (win_xleft_high,win_y_high),(0,255,0), 2) 
        cv2.rectangle(out_img,(win_xright_low,win_y_low),
        (win_xright_high,win_y_high),(0,255,0), 2) 
        
        ### Identify the nonzero pixels in x and y within the window ###
        good_left_inds = ((nonzerox >= win_xleft_low) & (nonzerox < win_xleft_high) 
                            & (nonzeroy >= win_y_low) & (nonzeroy < win_y_high)).nonzero()[0]
        good_right_inds = ((nonzerox >= win_xright_low) & (nonzerox < win_xright_high) 
                            & (nonzeroy >= win_y_low) & (nonzeroy < win_y_high)).nonzero()[0]
        
        # Append these indices to the lists
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)
        
        ### If you found > minpix pixels, recenter next window ###
        ### (`right` or `leftx_current`) on their mean position ###
        if len(good_left_inds) > minpix:
            leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:
            rightx_current = np.int(np.mean(nonzerox[good_right_inds]))

    # Concatenate the arrays of indices (previously was a list of lists of pixels)
    try:
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)
    except ValueError:
        # Avoids an error if the above is not implemented fully
        print('Error concatenating lane indices')
        pass

    # Extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds] 
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]

    return leftx, lefty, rightx, righty, out_img

def fitPolynomial(warped_binary, left_line, right_line):
    # Find our lane pixels first
    left_line.allx, left_line.ally, right_line.allx, right_line.ally, out_img = findLanePixels(warped_binary)

    ### Fit a second order polynomial to each using `np.polyfit` ###
    left_line.fitPolynomial()
    right_line.fitPolynomial()

    # Generate x and y values for plotting
    ploty = np.linspace(0, warped_binary.shape[0]-1, warped_binary.shape[0] )
    try:
        left_points = left_line.generatePoints(xm_per_pix)
        right_points = right_line.generatePoints(xm_per_pix)


    except TypeError:
        # Avoids an error if `left` and `right_fit` are still none or incorrect
        print('The function failed to fit a line!')
        left_points = np.stack((1*ploty**2 + 1*ploty, ploty)).astype(np.int).T        
        right_points = np.stack((1*ploty**2 + 1*ploty, ploty)).astype(np.int).T


    # Fit new polynomials to x,y in world space and save the radius of curvature #####
    left_line.radiusOfCurvature(ym_per_pix,xm_per_pix)
    right_line.radiusOfCurvature(ym_per_pix,xm_per_pix)

    ## Visualization ##
    # Colors in the left and right lane regions
    out_img[left_line.ally, left_line.allx] = [255, 0, 0]
    out_img[right_line.ally, right_line.allx] = [0, 0, 255]

    # Plots the left and right polynomials on the lane lines
    cv2.polylines(out_img, [left_points], False, (255, 255, 0), 2)
    cv2.polylines(out_img, [right_points], False, (255, 255, 0),2)

    return out_img

def averageRadius(left_line, right_line):
    return np.average([left_line.radius, right_line.radius]).astype(np.int)

def text(frame, text, x, y):
    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255,255), 2)

# Run a given video file
output_video = '../output_images/project_video_output.mp4'
#  clip1 = VideoFileClip("../project_video.mp4").subclip(0,5)
clip1 = VideoFileClip("../project_video.mp4")
project_clip = clip1.fl_image(processImages)
project_clip.write_videofile(output_video, audio=False)

# Uncomment below lines to run on a set of images
# image = mpimg.imread('../test_images/straight_lines2.jpg')
# result = processImages(image)
# plt.imshow(result)
# plt.show()

    
