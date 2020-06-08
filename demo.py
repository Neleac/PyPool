import cv2
import numpy as np
import os
import torch

from conv_net import ConvNet
from detect_balls import find_circles
from find_table_corners import table_corners
from find_best_shot import *
from project_board import *


test_number = 1
ckpt_epoch = 9
player = "solid"

data_dir = "/home/wangc21/datasets/pool"
model_weights = os.path.join("epoch_%d.pt" % ckpt_epoch)
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
model = ConvNet().to(device)
model.eval()
model.load_state_dict(torch.load(model_weights))

cap = cv2.VideoCapture(os.path.join(data_dir, "full_test_%d.mp4" % test_number))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    h, w = frame.shape[0], frame.shape[1]
    
    # create modified image
    pool = np.copy(frame)


    # 1. find table region and corners
    corners, hls_mask = table_corners(pool)
    corners = order_corners(corners)

    # draw corners
    for corner in corners:
        [x,y] = corner
        cv2.circle(pool, (x, y), 30, (0,0,255), -1)

    # 1b. constrain mask to table
    only_table_mask = np.zeros(hls_mask.shape, dtype=np.uint8)
    cv2.fillPoly(only_table_mask, [corners], (255))
    hls_mask = cv2.bitwise_and(hls_mask, hls_mask, mask=only_table_mask)


    # 2. find and classify pool balls
    w_x, w_y = None, None
    b_x, b_y = None, None
    stripe_centers = []
    solid_centers = []

    circles = find_circles(hls_mask)
    if circles is not None:
        for circle in circles[0]:
            c_x, c_y, radius = circle[0], circle[1], circle[2]

            # bounding box region
            l1, l2 = int(c_x) - int(radius), int(c_y) - int(radius)
            r1, r2 = int(c_x) + int(radius), int(c_y) + int(radius)
            l1, l2, r1, r2 = max(0, l1), max(0, l2), min(w, r1), min(h, r2)
            bbox = frame[l2 : r2, l1 : r1]

            # make prediction with model
            bbox = cv2.resize(bbox, (40, 40), interpolation = cv2.INTER_AREA)
            bbox_tensor = torch.from_numpy(bbox).unsqueeze(0).to(device, dtype = torch.float)
            label = model(bbox_tensor).argmax(dim = 1).item()

            if label == 0:
                w_x, w_y = c_x, c_y
            elif label == 8:
                b_x, b_y = c_x, c_y
            elif label > 8:
                stripe_centers.append([c_x, c_y])
            else:
                solid_centers.append([c_x, c_y])

            # draw the circle and center
            cv2.circle(pool, (c_x, c_y), radius, (0, 255, 0), 2)
            cv2.circle(pool, (c_x, c_y), 2, (0, 0, 255), 3)


    # 3. homographic projection
    h = compute_homography(corners)
    for circle in circles[0]:
        circle[:2] = project(circle[:2], h)

    # Calculate coordinates of the pockets
    pockets = []
    for corner in corners:
        corner = project(corner, h)
        pockets.append(corner)
    pockets.append(((pockets[0] + pockets[3]) / 2).astype(int))
    pockets.append(((pockets[1] + pockets[2]) / 2).astype(int))
    pockets = np.array(pockets)


    # 4. shot calculation
    #   input: list of [x, y] coordinates for pockets, stripes, solids, white, black
    #   output: [x, y] coordinates for a pocket and a stripes ball
    pockets = np_coords_to_points(pockets)
    stripes = np_coords_to_points(np.asarray(stripe_centers))
    solids = np_coords_to_points(np.asarray(solid_centers))
    white = np_coord_to_point(np.asarray([w_x, w_y]))
    black = np_coord_to_point(np.asarray([b_x, b_y]))

    # increase last arg to allow for higher angle shots
    if player == "solid":
        target_ball, target_pocket, _ = find_closest_shot(white, black, solids, stripes, pockets, 1)
    else:
        target_ball, target_pocket, _ = find_closest_shot(white, black, stripes, solids, pockets, 0.1)

    if target_ball is not None and target_pocket is not None:

        # shot from white -> target_ball -> target_pocket
        target_ball = point_to_np_coord(target_ball)
        target_pocket = point_to_np_coord(target_pocket)


        # 5. projection back to player view
        target_ball = unproject(target_ball, h)
        target_pocket = unproject(target_pocket, h)
        target_ball = (target_ball[0], target_ball[1])
        target_pocket = (target_pocket[0], target_pocket[1])

        # 6. Draw shot
        cv2.line(pool, target_ball, target_pocket, (255, 255, 255), 2)  # ball -> hole
        cv2.line(pool, (w_x, w_y), target_ball, (255, 255, 255), 2)  # cue/white -> ball

    #cv2.line(pool, (w_x, w_y), (0, 0), (255, 0, 0), 2)
    cv2.imshow('pool frame', pool)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
