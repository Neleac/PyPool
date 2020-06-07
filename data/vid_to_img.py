import cv2
import numpy as np
import os
import sys
sys.path.append("../pool_aimbot")

from detect_balls import find_circles
from find_table_corners import hls_filter, table_corners

data_dir = "/home/wangc21/datasets/pool"

for n in range(16):

    print(n)

    cap = cv2.VideoCapture(os.path.join(data_dir, "videos/%d_ball.mp4" % n))
    #fps = 60

    os.mkdir(os.path.join(data_dir, "images/%d_ball" % n))

    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        h, w = frame.shape[0], frame.shape[1]

        table_mask, table_masked = hls_filter(frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        circles = find_circles(gray)
        if circles is not None:
            # only draw one ball
            ball = circles[0, 0]
            l1, l2 = int(ball[0]) - int(ball[2]), int(ball[1]) - int(ball[2])
            r1, r2 = int(ball[0]) + int(ball[2]), int(ball[1]) + int(ball[2])

            # save bounding box region
            bbox = frame[max(0, l2) : min(h, r2), max(0, l1) : min(w, r1)]
            bbox = cv2.resize(bbox, (40, 40), interpolation = cv2.INTER_AREA)
            cv2.imwrite(os.path.join(data_dir, "images/%d_ball/%d.png" % (n, idx)), bbox)
            idx += 1

        # find and draw circles
        circles = find_circles(table_mask)
        if circles is not None:
            # only draw one ball
            ball = circles[0, 0]
            l1, l2 = int(ball[0]) - int(ball[2]), int(ball[1]) - int(ball[2])
            r1, r2 = int(ball[0]) + int(ball[2]), int(ball[1]) + int(ball[2])

            # save bounding box region
            bbox = frame[max(0, l2) : min(h, r2), max(0, l1) : min(w, r1)]
            bbox = cv2.resize(bbox, (40, 40), interpolation = cv2.INTER_AREA)
            cv2.imwrite(os.path.join(data_dir, "images/%d_ball/%d.png" % (n, idx)), bbox)
            idx += 1
            '''
            cv2.circle(frame, (ball[0], ball[1]), ball[2], (0, 255, 0), 2)
            cv2.circle(frame, (ball[0], ball[1]), 2, (0, 0, 255), 3)
            cv2.rectangle(frame, (l1, l2), (r1, r2), (255, 0, 0), 2)
            '''
            '''
            # draw all balls
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(frame, (i[0], i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(frame, (i[0], i[1]), 2, (0, 0, 255), 3)
            '''

        #cv2.imshow('frame', table_mask)
        #cv2.imshow('frame', frame)

        # playback speed
        #cv2.waitKey(int(1000 / fps))
        if cv2.waitKey(1) == ord('q'):
            #cv2.imwrite("frame.png", frame)
            break

    cap.release()
    #cv2.destroyAllWindows()
