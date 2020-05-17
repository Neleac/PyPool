import cv2
import numpy as np

# params:
#   frame - input rgb image
# returns:
#   
def find_circles(frame):
    # smoothing
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # circle detection
    dp = 1          # inverse ratio of accumulator resolution to image resolution
    min_dist = 20   # minimum distance between circle centers
    param1 = 50     # gradient value for edge detection
    param2 = 30     # accumulator threshold (increase to get more circles)
    min_radius = 0  # minimum circle radius
    max_radius = 0  # maximum circle radius
    circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, dp, min_dist, param1, param2, min_radius, max_radius)
