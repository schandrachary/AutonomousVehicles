import pickle
import numpy as np
import cv2
import matplotlib.pyplot as plt

nx = 9 # the number of inside corners in x
ny = 6 # the number of inside corners in y

# Test undistortion on an image
img = cv2.imread('../camera_cal/test_image3.jpg')
img_size = (img.shape[1], img.shape[0])

# Extract relevant calibration information from pickle file
calibration_pickle = pickle.load(open("../camera_cal/calibration.p","rb"))
objpoints = calibration_pickle["objpoints"]
imgpoints = calibration_pickle["imgpoints"]

# Do camera calibration from extracted object points and image points
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size,None,None)

# Undistort the image using camera matrix and distortion coeff
undistort = cv2.undistort(img, mtx, dist, None, mtx)
gray = cv2.cvtColor(undistort, cv2.COLOR_BGR2GRAY)
cv2.imwrite('../camera_cal/test_undist.jpg',undistort)

# Store the camera matrix and distortion coeff for future use
dist_coefficients = {}
dist_coefficients["mtx"] = mtx
dist_coefficients["dist"] = dist
pickle.dump(dist_coefficients, open("../camera_cal/distortion_coeff.p","wb"))

# Visualize undistortion
# f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
# ax1.imshow(img)
# ax1.set_title('Original Image', fontsize=30)
# ax2.imshow(undistort)
# ax2.set_title('Undistorted Image', fontsize=30)
# plt.show()
# f.savefig("../camera_cal/undistorted_image.jpg")


# Find corners in the test image and draw it on undistorted image
ret, corners = cv2.findChessboardCorners(gray, (nx,ny), None)
print("corners found: {}".format(ret))
cv2.drawChessboardCorners(undistort, (nx,ny), corners, ret)
# plt.imshow(undistort)
# plt.show()

# Declare an offset and get four source corners and four destination corners
offset = 100
src = np.float32([corners[0], corners[nx-1], corners[-1], corners[-nx]])
dst = np.float32([[offset, offset], [img_size[0]-offset, offset],[img_size[0]-offset, img_size[1]-offset], [offset, img_size[1]-offset]])

# Get transformation matrix by performing perspective transform
M = cv2.getPerspectiveTransform(src, dst)

# Plot and save the comparison image
warped = cv2.warpPerspective(undistort, M, img_size, flags=cv2.INTER_LINEAR)
f, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(30, 9))
f.tight_layout()
ax1.imshow(img)
ax1.set_title('Original Image', fontsize=25)
ax2.imshow(undistort)
ax2.set_title('Undistorted Image', fontsize=25)
ax3.imshow(warped)
ax3.set_title('Undistorted and Warped Image', fontsize=25)
plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
plt.show()
f.savefig("../camera_cal/undistorted_warped.jpg")