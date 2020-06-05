import cv2
import numpy as np

# params:
#   frame - input rgb image
# returns:
#   circles - detected circles
def find_circles(img):
    # smoothing
    frame = cv2.GaussianBlur(img, (5, 5), 0)

    # grayscale
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # circle detection
    dp = 1              # inverse ratio of accumulator resolution to image resolution
    min_dist = 30       # minimum distance between circle centers
    edge_grad = 40      # gradient value for edge detection
    acc_thresh = 20     # accumulator threshold (increase to get less circles)
    min_r = 20          # minimum circle radius
    max_r = 40          # maximum circle radius
    circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, dp, min_dist, param1=edge_grad, param2=acc_thresh, minRadius=min_r, maxRadius=max_r)
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
    return circles

'''
frame = cv2.imread("test.png")
circles = find_circles(frame)
for i in circles[0, :]:
    # draw the outer circle
    cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)

cv2.imshow('detected circles', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''