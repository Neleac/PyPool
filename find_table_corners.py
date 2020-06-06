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
    # create the list of corners
    corners = []
    for corner in approx:
        [[x,y]] = corner
        corners.append([x,y])

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

        plt.figure(figsize=(12, 4))
        plt.subplot(121), show_image(poly_drawing)
        plt.subplot(122), show_image(pool_corners)
        plt.show()

    return np.array(corners) # return numpy array

img = cv2.imread("frame.png")
corners = table_corners(img)
print(corners)