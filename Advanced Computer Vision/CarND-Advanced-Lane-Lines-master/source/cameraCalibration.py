import pickle
import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt

nx = 9 # the number of inside corners in x
ny = 6 # the number of inside corners in y

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((ny*nx,3), np.float32)
objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane.

# Make a list of calibration images
images = glob.glob('../camera_cal/calibration*.jpg')

# Step through the list and search for chessboard corners
for idx, fname in enumerate(images):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (nx,ny), None)

    print('image {} has corners: {}'.format(fname, ret))

    # If found, add object points, image points
    if ret == True:
        objpoints.append(objp)
        imgpoints.append(corners)

        # Draw the corners
        cv2.drawChessboardCorners(img, (nx,ny), corners, ret)
        write_name = '../camera_cal/corners/corners_found'+str(idx)+'.jpg'
        cv2.imwrite(write_name, img)

calibration_pickle = {}
calibration_pickle["objpoints"] = objpoints
calibration_pickle["imgpoints"] = imgpoints
pickle.dump(calibration_pickle, open("../camera_cal/calibration.p","wb"))
cv2.destroyAllWindows()