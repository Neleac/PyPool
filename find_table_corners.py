import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# display BGR image
def show_image(img):
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# filter the image by table color
# returns the table mask and the table image
def hls_filter(img):
    # Convert BGR to HLS
    pool_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    # define range of green color in HLS
    lower_green = np.array([85, 0, 0])
    upper_green = np.array([120, 255, 255])

    # Threshold the HLS image to get only green colors
    table_mask = cv2.inRange(pool_hls, lower_green, upper_green)
    # Bitwise-AND mask and original image
    table_masked = cv2.bitwise_and(img, img, mask=table_mask)
    return table_mask, table_masked

# find contours then approximate polygon
# returns the contour drawing, polygon drawing, and approximated points in polygon
def contour_poly(table_mask):
    # find contours (outline of white)
    contours, _ = cv2.findContours(table_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_drawing = np.zeros(table_mask.shape, dtype=np.uint8)
    cv2.drawContours(contour_drawing, contours, -1, (255), 2)

    # find largest contour
    largest = 0
    idx = -1
    for i in range(len(contours)):
        contour = contours[i]
        area = cv2.contourArea(contour)
        if (area > largest):
            largest = area
            idx = i
    contour = contours[idx]

    # approx poly
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
    poly_drawing = np.zeros(contour_drawing.shape, dtype=np.uint8)
    cv2.drawContours(poly_drawing, [approx], -1, (255), 5)

    return contour_drawing, poly_drawing, approx

# draws corners as red circles on the pool image
# return the corners as a list of pair lists, and the image
def get_draw_corners(approx, img):
    pool_corners = np.copy(img)

    # create the list of corners
    corners = []
    for corner in approx:
        [[x,y]] = corner
        corners.append([x,y])

    if len(corners) == 5:
        # need to remove extra
        x_indices = []
        y_indices = []
        buff = 10
        for i in range(len(corners)):
            [x1, y1] = corners[i]
            for j in range(i+1, len(corners)):
                [x2, y2] = corners[j]
                x_max = pool_corners.shape[1] - 1 - buff
                y_max = pool_corners.shape[0] - 1 - buff
                x_edge = (x1 < buff and x2 < buff) or (x1 > x_max and x2 > x_max)
                y_edge = (y1 < buff and y2 < buff) or (y1 > y_max and y2 > y_max)
                if x_edge:
                    # both on edge (x-coord)
                    x_indices.append(i)
                    x_indices.append(j)
                elif y_edge:
                    # both on edge (y-coord)
                    y_indices.append(i)
                    y_indices.append(j)
        if len(x_indices) != 0:
            [i, j] = x_indices
            [x1, y1] = corners[i]
            [x2, y2] = corners[j]
            y_avg = int((y1 + y2) / 2) # average the y-values
            del corners[i]
            del corners[j - 1]
            corners.append([x1, y_avg]) # add in the avg
        elif len(y_indices) != 0:
            [i, j] = y_indices
            [x1, y1] = corners[i]
            [x2, y2] = corners[j]
            x_avg = int((x1 + x2) / 2) # average the x-values
            del corners[i]
            del corners[j - 1]
            corners.append([x_avg, y1]) # add in the avg

    # make the image
    for corner in corners:
        [x,y] = corner
        cv2.circle(img, (x, y), 30, (0,0,255), -1)
    return corners, img

# return 4x2 (ideally) numpy array of corners
def table_corners(img):
    table_mask, table_masked = hls_filter(img)
    contour_drawing, poly_drawing, approx = contour_poly(table_mask)
    corners, pool_corners = get_draw_corners(approx, img)

    if (len(corners) != 4):
        print('corners:', len(corners), corners)

        # plt.figure(figsize=(12, 4))
        # plt.subplot(121), show_image(poly_drawing)
        # plt.subplot(122), show_image(pool_corners)
        # plt.show()

    return np.array(corners) # return numpy array
