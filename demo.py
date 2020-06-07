import cv2
import numpy as np
import os

from detect_balls import find_circles
from find_table_corners import table_corners


test_number = 1
data_dir = "/home/wangc21/datasets/pool"

cap = cv2.VideoCapture(os.path.join(data_dir, "full_test_%d.mp4" % test_number))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # find table region and corners
    corners, hls_mask = table_corners(frame)

    # find pool balls
    circles = find_circles(hls_mask)
    if circles is not None:
        # draw all balls
        for circle in circles[0, :]:
            center, radius = (circle[0], circle[1]), circle[2]

            # TODO: discard centers outside of table region

            # draw the outer circle
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            # draw the center of the circle
            cv2.circle(frame, center, 2, (0, 0, 255), 3)

    # classify pool balls

    # homographic projection

    # shot calculation

    # projection back to player view

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
