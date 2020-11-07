#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
from geometry_msgs.msg import PoseStamped, Pose
from styx_msgs.msg import TrafficLightArray, TrafficLight
from styx_msgs.msg import Lane
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from light_classification.tl_classifier import TLClassifier
from scipy.spatial import KDTree
import tf
import cv2
import yaml
import numpy as np
import PyKDL

STATE_COUNT_THRESHOLD = 3
ENABLE_TEST_MODE = False

class TLDetector(object):
    def __init__(self):
        rospy.init_node('tl_detector')

        self.pose = None
        self.waypoints = None
        self.camera_image = None
        self.lights = []

        sub1 = rospy.Subscriber('/current_pose', PoseStamped, self.pose_cb)
        sub2 = rospy.Subscriber('/base_waypoints', Lane, self.waypoints_cb)

        '''
        /vehicle/traffic_lights provides you with the location of the traffic light in 3D map space and
        helps you acquire an accurate ground truth data source for the traffic light
        classifier by sending the current color state of all traffic lights in the
        simulator. When testing on the vehicle, the color state will not be available. You'll need to
        rely on the position of the light and the camera image to predict it.
        '''
        sub3 = rospy.Subscriber('/vehicle/traffic_lights', TrafficLightArray, self.traffic_cb)
        sub6 = rospy.Subscriber('/image_color', Image, self.image_cb)

        config_string = rospy.get_param("/traffic_light_config")
        self.config = yaml.load(config_string)

        self.upcoming_red_light_pub = rospy.Publisher('/traffic_waypoint', Int32, queue_size=1)

        self.bridge = CvBridge()
        self.light_classifier = TLClassifier()
        self.listener = tf.TransformListener()

        self.state = TrafficLight.UNKNOWN
        self.last_state = TrafficLight.UNKNOWN
        self.last_wp = -1
        self.state_count = 0
        self.waypoints_2d = None
        self.waypoint_tree = None

        rospy.spin()

    def pose_cb(self, msg):
        self.pose = msg

    def waypoints_cb(self, waypoints):
        self.waypoints = waypoints
        if not self.waypoints_2d:
            self.waypoints_2d = [[waypoint.pose.pose.position.x, waypoint.pose.pose.position.y] \
                                  for waypoint in waypoints.waypoints]
            self.waypoint_tree = KDTree(self.waypoints_2d)

    def traffic_cb(self, msg):
        self.lights = msg.lights

    def image_cb(self, msg):
        """Identifies red lights in the incoming camera image and publishes the index
            of the waypoint closest to the red light's stop line to /traffic_waypoint

        Args:
            msg (Image): image from car-mounted camera

        """
        self.has_image = True
        self.camera_image = msg
        light_wp, state = self.process_traffic_lights()

	    # rospy.logwarn("Upcoming traffic light at index: {} is {}".format(light_wp, state))


        '''
        Publish upcoming red lights at camera frequency.
        Each predicted state has to occur `STATE_COUNT_THRESHOLD` number
        of times till we start using it. Otherwise the previous stable state is
        used.
        '''
        if self.state != state:
            self.state_count = 0
            self.state = state
        elif self.state_count >= STATE_COUNT_THRESHOLD:
            self.last_state = self.state
            light_wp = light_wp if state == TrafficLight.RED else -1
            self.last_wp = light_wp
            self.upcoming_red_light_pub.publish(Int32(light_wp))
        else:
            self.upcoming_red_light_pub.publish(Int32(self.last_wp))
        self.state_count += 1

    def get_closest_waypoint(self, x, y):
        """Identifies the closest path waypoint to the given position
            https://en.wikipedia.org/wiki/Closest_pair_of_points_problem
        Args:
            pose (Pose): position to match a waypoint to

        Returns:
            int: index of the closest waypoint in self.waypoints

        """
        #TODO implement
        closest_idx = self.waypoint_tree.query([x, y], 1)[1]
        return closest_idx

    def global_to_camera_coordinates(self, global_pos):
        """ Project a point from global space to camera coordinates

        Args:
            position (Point): 3D position of traffic light in global coordinates

        Returns:
            x (int): X coordinate of traffic light in image coordinates
            y (int): Y coordinate of traffic light in image coordinates
        """

        focal_length_x = self.config['camera_info']['focal_length_x']
        focal_length_y = self.config['camera_info']['focal_length_y']
        image_width = self.config['camera_info']['image_width']
        image_height = self.config['camera_info']['image_height']

        translation = None
        rotation = None

        try:
            now = rospy.Time.now()
            self.listener.waitForTransform("/base_link", "/world", now, rospy.Duration(1.0))
            (translation, rotation) = self.listener.lookupTransform("/base_link", "/world", now)

        except (tf.Exception):
            rospy.logerr("global_to_camera_coordinates() - Transformation Failed!")

        # HYPERPARAMETERS
        focal_point = 2300
        x_offset = -30
        y_offset = 340

        global_position = PyKDL.Vector(global_pos.x, global_pos.y, global_pos.z)
        rotated_camera = PyKDL.Rotation.Quaternion(*rotation)
        translated_camera = PyKDL.Vector(*translation)
        position_camera = rotated_camera * global_position + translated_camera

        x = -position_camera[1]/position_camera[0] * focal_point + image_width/2 + x_offset
        y = -position_camera[2]/position_camera[0] * focal_point + image_height/2 + y_offset

        return (int(x), int(y))

    def get_light_state(self, light):
        """Determines the current color of the traffic light

        Args:
            light (TrafficLight): light to classify

        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        # if(not self.has_image):
        #     self.prev_light_loc = None
        #     return False
        #
        # cv_image = self.bridge.imgmsg_to_cv2(self.camera_image, "bgr8")
        #
        # #Get classification
        # return self.light_classifier.get_classification(cv_image)

        if ENABLE_TEST_MODE:
            return light.state
        else:
            cv_image = self.bridge.imgmsg_to_cv2(self.camera_image, "bgr8")
            x, y = global_to_camera_coordinates(light.pose.pose.position)

            # If the transformed coordinates are outside of the image, return unknown
            if (x < 0) or (y < 0) or (x >= cv_image.shape[1]) or (y >= cv_image.shape[0]):
                return TrafficLight.UNKNOWN

            # Crop the image around the traffic light
            cropping_value = 90
            x_min = x - cropping_value if (x - cropping_value) >= 0 else 0
            y_min = y - cropping_value if (y - cropping_value) >=0 else 0
            x_max = x + cropping_value if (x + cropping_value) <= cv_image.shape[1] else cv_image.shape[1]
            y_max = y + cropping_value if (y + cropping_value) <= cv_image.shape[0] else cv_image.shape[0]

            image_cropped = cv_image[y_min:y_max, x_min:x_max]

            # Get classification
            return self.light_classifier.get_classification(image_cropped)

    def distance(self, waypoints, wp1, wp2):
        dist = 0
        dl = lambda a, b: math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2  + (a.z-b.z)**2)
        for i in range(wp1, wp2+1):
            dist += dl(waypoints[wp1].pose.pose.position, waypoints[i].pose.pose.position)
            wp1 = i
        return dist

    def process_traffic_lights(self):
        """Finds closest visible traffic light, if one exists, and determines its
            location and color

        Returns:
            int: index of waypoint closes to the upcoming stop line for a traffic light (-1 if none exists)
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)

        """
        closest_light = None
        line_wp_idx = None

        # List of positions that correspond to the line to stop in front of for a given intersection
        stop_line_positions = self.config['stop_line_positions']
        if(self.pose):
            car_wp_idx = self.get_closest_waypoint(self.pose.pose.position.x, self.pose.pose.position.y)

            #TODO find the closest visible traffic light (if one exists)
            diff = len(self.waypoints.waypoints)
            for i, light in enumerate(self.lights):
                # Get stop line waypoint index
                line = stop_line_positions[i]
                temp_wp_idx = self.get_closest_waypoint(line[0], line[1])

                # Find closest stop line waypoint index
                d = temp_wp_idx - car_wp_idx
                if d >= 0 and d < diff:
                    diff = d
                    closest_light = light
                    line_wp_idx = temp_wp_idx

        if closest_light:
            # If the light is within 50 meters, call the classifier to look for detection
            if self.distance(self.waypoints.waypoints, car_wp_idx, line_wp_idx) < 50:
                state = self.get_light_state(closest_light)
                return line_wp_idx, state
            else:
                return line_wp_idx, TrafficLight.UNKNOWN

        return -1, TrafficLight.UNKNOWN

if __name__ == '__main__':
    try:
        TLDetector()
    except rospy.ROSInterruptException:
        rospy.logerr('Could not start traffic node.')
