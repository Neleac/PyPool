import cv2
import numpy as np
import os

from detect_balls import find_circles
from find_table_corners import table_corners
from find_best_shot import *
from project_board import *

test_number = 1
data_dir = "/home/wangc21/datasets/pool"

cap = cv2.VideoCapture(os.path.join(data_dir, "full_test_%d.mp4" % test_number))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # 1. find table region and corners
    corners, hls_mask = table_corners(frame)
    corners = order_corners(corners)

    # 1b. constrain mask to table
    only_table_mask = np.zeros(hls_mask.shape, dtype=np.uint8)
    cv2.fillPoly(only_table_mask, [corners], (255))
    hls_mask = cv2.bitwise_and(hls_mask, hls_mask, mask=only_table_mask)

    # 2. find pool balls
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

    # 3. classify pool balls

    # 4. homographic projection
    h = compute_homography(corners)
    for circle in circles[0]:
        circle[:2] = project(circle[:2], h)
    for corner in corners:
        corner = project(corner, h)

    # Calculate coordinates of the pockets
    corners = order_corners(corners)
    for corner in corners:
        corner = project(corner, h)
    pockets = np.append(corners,
                        np.array([(corners[0] + corners[3]) / 2,
                                (corners[1] + corners[2]) / 2]),
                        axis=0)

    # 5. shot calculation
    #   input: list of [x, y] coordinates for pockets, stripes, solids, white, black
    #   output: [x, y] coordinates for a pocket and a stripes ball
    pockets = np_coords_to_points(pockets)
    stripes = np_coords_to_points([None])
    solids = np_coords_to_points([None])
    white = np_coord_to_point(np.array([None, None]))
    black = np_coord_to_point(np.array([None, None]))

    # increase last arg to allow for higher angle shots
    target_ball, target_pocket, _ = find_closest_shot(white, black, stripes, solids, pockets, 0.01)

    # shot from white -> target_ball -> target_pocket
    target_ball = point_to_np_coord(target_ball)
    target_pocket = point_to_np_coord(target_pocket)

    # 6. projection back to player view
    target_ball = unproject(target_ball, h)
    target_pocket = unproject(target_pocket, h)
    
    # 7. Draw shot
    cv2.line(frame, target_ball, target_pocket, (0, 0, 255), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
