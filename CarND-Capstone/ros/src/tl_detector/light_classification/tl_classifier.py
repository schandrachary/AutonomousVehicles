from styx_msgs.msg import TrafficLight
import cv2
import numpy as np 

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        pass

    def get_classification(self, image):
        """Determines the color of the traffic light in the image

        Args:
            image (cv::Mat): image containing the traffic light

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        #TODO implement light color prediction

        # Convert the image to HSV color space
        image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

        # Create a threshold for RED pixels in the image
        RED_MIN = np.array([0, 120, 120], np.uint8)
        RED_MAX = np.array([10, 255, 255], np.uint8)
        threshold = cv2.inRange(image_hsv, RED_MIN, RED_MAX)
        red_pixels = cv2.countNonZero(threshold)
        if red_pixels > 60:
            return TrafficLight.RED

        # Create a threshold for YELLOW pixels in the image
        YELLOW_MIN = np.array([28, 120, 120], np.uint8)
        YELLOW_MAX = np.array([47, 255, 255], np.uint8)
        threshold = cv2.inRange(image_hsv, YELLOW_MIN, YELLOW_MAX)
        yellow_pixels = cv2.countNonZero(threshold)
        if yellow_pixels > 60:
            return TrafficLight.YELLOW

        # Create a threshold for GREEN pixels in the image
        GREEN_MIN = np.array([64, 120, 120], np.uint8)
        GREEN_MAX = np.array([100, 255, 255], np.uint8)
        threshold = cv2.inRange(image_hsv, GREEN_MIN, GREEN_MAX)
        green_pixels = cv2.countNonZero(threshold)
        if green_pixels > 60:
            return TrafficLight.GREEN


        return TrafficLight.UNKNOWN
