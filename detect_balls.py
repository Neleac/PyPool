import cv2
import numpy as np

# params:
#   frame - input grayscale image
# returns:
#   circles - detected circles
def find_circles(img):
    # smoothing
    frame = cv2.GaussianBlur(img, (5, 5), 0)

    # grayscale
    #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # circle detection
    dp = 1              # inverse ratio of accumulator resolution to image resolution
    min_dist = 30       # minimum distance between circle centers
    edge_grad = 100     # gradient value for edge detection
    acc_thresh = 20     # accumulator threshold (increase to get less circles)
    min_r = 20          # minimum circle radius
    max_r = 40          # maximum circle radius
    circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, dp, min_dist, param1=edge_grad, param2=acc_thresh, minRadius=min_r, maxRadius=max_r)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
    return circles
