import cv2
import numpy as np
import os

WIDTH = 232
HEIGHT = 466

"""
    Given the corners of an image, returns a homography matrix (numpy array)
    that can be used to project coordinates in the original image to a top-down
    view and back
"""
def compute_homography(corners):
    # Order the corner in top-left, top-right, bottom-left, bottom-right
    # Begin by sorting on x coordinate
    sorted_x = corners[np.argsort(corners[:, 0]), :]
    ordered_corners = np.zeros((4, 2))
    
    # Get leftmost and rightmost points
    leftmost = sorted_x[:2, :]
    rightmost = sorted_x[2:, :]

    # get top-left and bottom-left based on y-coordinates of leftmost
    leftmost = leftmost[np.argsort(leftmost[:, 1]), :]
    ordered_corners[0] = leftmost[0]
    ordered_corners[3] = leftmost[1]

    # bottom-right is farthest from top-left
    dist1 = np.linalg.norm(ordered_corners[0] - rightmost[0])
    dist2 = np.linalg.norm(ordered_corners[0] - rightmost[1])
    if dist1 > dist2:
        ordered_corners[2] = rightmost[0]
        ordered_corners[1] = rightmost[1]
    else:
        ordered_corners[2] = rightmost[1]
        ordered_corners[1] = rightmost[0]

    # Rotate so that top-left->top-right is shorter than top-left->bottom-left
    tltr = np.linalg.norm(ordered_corners[0] - ordered_corners[1])
    tlbl = np.linalg.norm(ordered_corners[0] - ordered_corners[3])
    if tltr > tlbl:
        print(ordered_corners)
        ordered_corners = np.roll(ordered_corners, -1, axis=0)
        print(ordered_corners)

    # Four corners of the overhead view
    corners_dst = np.array([[0, 0],[WIDTH, 0],[WIDTH, HEIGHT],[0, HEIGHT]])

    # Calculate Homography
    h, status = cv2.findHomography(ordered_corners, corners_dst)

    return h

"""
    Given a numpy array point [x, y] and a homography, returns the
    projected coordinates
"""
def project(coord, homography):
    augmented_coord = np.array([coord[0], coord[1], 1]).reshape((3, 1))
    temp = homography @ augmented_coord
    temp_p = homography.dot(augmented_coord)
    sum = np.sum(temp_p ,1)
    px = int(round(sum[0]/sum[2]))
    py = int(round(sum[1]/sum[2]))
    return np.array([px, py])

"""
    Given a projected numpy array point [x', y'] and a homography, returns
    the original (before projection) coordinates
"""
def unproject(coord, homography):
    inverse_homography = np.linalg.inv(homography)
    return project(coord, inverse_homography)
