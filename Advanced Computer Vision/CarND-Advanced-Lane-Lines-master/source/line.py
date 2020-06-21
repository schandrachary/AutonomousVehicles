'''
Line class to receive the characteristics of each line detection
'''
import numpy as np
from collections import deque

class Line():
    def __init__(self, width, height):
        # dimensions of the image
        self.width = width
        self.height = height
        # was the line detected in the last iteration?
        self.detected = False  
        # x values of the last n fits of the line
        self.recent_xfitted = deque(maxlen=5) 
        #average x values of the fitted line over the last n iterations
        self.bestx = deque(maxlen=5)     
        #polynomial coefficients averaged over the last n iterations
        self.best_fit = deque(maxlen=10)
        #polynomial coefficients for the most recent fit
        self.current_fit = [np.array([False])]  
        #radius of curvature of the line in some units
        self.radius_of_curvature = None 
        #distance in meters of vehicle center from the line
        self.line_base_pos = None 
        #difference in fit coefficients between last and new fits
        self.diffs = np.array([0,0,0], dtype='float') 
        #x values for detected line pixels
        self.allx = None  
        #y values for detected line pixels
        self.ally = None
        #fitted x values
        self.fitx = None
        #fitted y values
        self.fity = None
        #y-points used for plotting
        self.ploty = np.linspace(0, self.height-1, self.height)
        #radius of curvature
        self.radius = None
        #distance from center of the image
        self.distance = None

    def fitPolynomial(self):
        self.best_fit.append(np.polyfit(self.ally, self.allx, 2))

    def generatePoints(self, xm_per_pix):
        # ploty = np.linspace(0, self.height-1, self.height)
        # Get a best fit which is an average of last n iterations
        fit = np.array(self.best_fit).mean(axis=0)
        self.fitx = fit[0]*self.ploty**2 + fit[1]*self.ploty + fit[2]
        self.fity = self.ploty

        #record the camera distance from image center
        y_eval = np.max(self.fity).astype(np.int)
        self.distance = np.absolute((self.width//2 - self.fitx[y_eval])*xm_per_pix)

        # Return an array of (720,2) containing fitted points
        return np.stack((self.fitx, self.fity)).astype(np.int).T

    def radiusOfCurvature(self,ym_per_pix,xm_per_pix):
        # Fit new polynomials to x,y in world space #####
        fit_circle = np.polyfit(self.fity*ym_per_pix, self.fitx*xm_per_pix, 2)

        # We'll choose the maximum y-value, corresponding to the bottom of the image
        y_eval = np.max(self.ploty)

        ##### Calculate of R_curve (radius of curvature) #####
        self.radius = (1 + (2*fit_circle[0]*(y_eval*ym_per_pix) + fit_circle[1])**2)**1.5/np.absolute(2*fit_circle[0])


