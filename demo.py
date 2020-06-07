import cv2
import numpy as np
import os
import sys
sys.path.append("../pool_aimbot")

from find_table_corners import table_corners


test_number = 1
cap = cv2.VideoCapture("/home/wangc21/datasets/pool/full_test_%d.mp4" % test_number)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # find table region and corners
    corners = table_corners(frame)

    # find pool balls

    # classify pool balls

    # homographic projection

    # shot calculation

    # projection back to player view

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
