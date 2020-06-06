import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def show_image(img):
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

def hls_filter(img):
    #pool = cv2.imread(imgfile)
    # Convert BGR to HLS
    pool_hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    # define range of green color in HLS
    lower_green = np.array([85, 0, 0])
    upper_green = np.array([120, 255, 255])

    # Threshold the HLS image to get only green colors
    table_mask = cv2.inRange(pool_hls, lower_green, upper_green)
    return pool_hls, table_mask

# def remove_carpet(pool_hls, table_mask):
#     ## remove the carpet
#     carpet_lower_green = np.array([85,50,0])
#     carpet_upper_green = np.array([90,200,255])
#     carpetish_mask = cv2.inRange(pool_hls, carpet_lower_green, carpet_upper_green)
    
#     carpetless_table_mask = table_mask - carpetish_mask
#     return carpetless_table_mask

def close_open(carpetless_table_mask):
    kernel = np.ones((50,50),np.uint8)
    table_mask_closed = carpetless_table_mask #cv2.morphologyEx(carpetless_table_mask, cv2.MORPH_CLOSE, kernel)
    table_mask_cleaned = table_mask_closed #cv2.morphologyEx(table_mask_closed, cv2.MORPH_OPEN, kernel)
    return table_mask_cleaned

def reduce_noise(pool_hls, table_mask):
    carpetless_table_mask = table_mask #remove_carpet(pool_hls, table_mask)
    table_mask_cleaned = close_open(carpetless_table_mask)
    return table_mask_cleaned

def contour_convex_hull(table_mask_cleaned):
    # find contours (outline of white)
    contours, _ = cv2.findContours(table_mask_cleaned, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_drawing = np.zeros(table_mask_cleaned.shape, dtype=np.uint8)
    cv2.drawContours(contour_drawing, contours, -1, (255), 2)

    # find convex hull of contour (smooth the border)
    hulls = list(map(lambda x: cv2.convexHull(x), contours))
    # find largest hull
    largest = 0
    idx = -1
    for i in range(len(hulls)):
        hull = hulls[i]
        if (hull.shape[0] > largest):
            largest = hull.shape[0]
            idx = i
    hulls = [hulls[idx]] # largest hull
    hull_drawing = np.zeros(contour_drawing.shape, dtype=np.uint8)
    cv2.drawContours(hull_drawing, hulls, -1, (255), 2)

    plt.figure(figsize=(12, 4))
    plt.subplot(121), show_image(contour_drawing)
    plt.subplot(122), show_image(hull_drawing)
    plt.show()

    return contour_drawing, hull_drawing

def hough(hull_drawing):
    hough_drawing = np.zeros(hull_drawing.shape, dtype=np.uint8)
    lines = cv2.HoughLinesP(hull_drawing, 1, np.pi/180, 100, minLineLength=300, maxLineGap=100)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(hough_drawing, (x1,y1), (x2,y2), (255), 1)
    show_image(hough_drawing)
    plt.show()
    return lines, hough_drawing

def find_four_lines(lines):
    # get the slopes and intercepts for each line
    slope_ints = []
    for line in lines:
        x1,y1,x2,y2 = line[0]
        if x2-x1 != 0:
            m = (y2-y1)/(x2-x1)
            b = y1 - m*x1
            slope_ints.append([m,b])
    slope_ints = np.array(slope_ints)

    # find the lines that are basically identical
    m_thresh = 0.5
    b_thresh = 300
    remove_idxs = set()
    for i in range(slope_ints.shape[0]):
        pair1 = slope_ints[i]
        m1 = pair1[0]
        b1 = pair1[1]
        for j in range(i+1, slope_ints.shape[0]):
            pair2 = slope_ints[j]
            m2 = pair2[0]
            b2 = pair2[1]
            if abs(m2-m1) < m_thresh and abs(b2-b1) < b_thresh:
                remove_idxs.add(j)
    remove_idxs = sorted(remove_idxs)
    # remove the duplicates and find (4) unique lines
    unique_lines = slope_ints.copy()
    for i,idx in enumerate(remove_idxs):
        unique_lines = np.delete(unique_lines, idx-i, 0)
    #kmeans = KMeans(n_clusters=4).fit(slope_ints)
    #unique_lines = kmeans.cluster_centers_
    print('lines', len(unique_lines))
    print('lines', unique_lines)
    return unique_lines

def draw_lines(unique_lines, imgfile):
    pad = 300
    pool_lines = cv2.imread(imgfile)
    pool_lines_border = cv2.copyMakeBorder(pool_lines, pad, pad, pad, pad, cv2.BORDER_CONSTANT, None, (0,0,0))
    for pair in unique_lines:
        # get x1,y1,x2,y2 from the eq of the four lines
        m = pair[0]
        b = pair[1]
        x1 = 0
        x1b = 0
        x2 = pool_lines.shape[1]
        x2b = pool_lines_border.shape[1]
        y1 = int(m*x1 + b)
        y2 = int(m*x2 + b)
        y1b = int(m*(x1b-pad) + b) + pad
        y2b = int(m*(x2b-pad) + b) + pad
        cv2.line(pool_lines,(x1,y1),(x2,y2),(0,0,255),10)
        cv2.line(pool_lines_border,(x1b,y1b),(x2b,y2b),(0,0,255),10)

    return pool_lines, pool_lines_border

def find_draw_corners(unique_lines, pool_lines_border, imgfile):
    new_lines = unique_lines

    # now find corners
    corners = []
    for i in range(4):
        pair1 = new_lines[i]
        m1 = pair1[0]
        b1 = pair1[1]
        for j in range(i+1, 4):
            #if j-i != 2: # if 2 then opposite
            pair2 = new_lines[j]
            m2 = pair2[0]
            b2 = pair2[1]
            if (m1-m2 != 0):
                x = (b2-b1)/(m1-m2)
                y = m1*x+b1
            corners.append((x,y))
    print('corners', len(corners))
    print('corners', corners)

    pad = 300
    pool_corners = cv2.imread(imgfile)
    pool_corners_border = cv2.copyMakeBorder(pool_lines_border, 0, 0, 0, 0, cv2.BORDER_CONSTANT, None, (0,0,0))
    for corner in corners:
        x1, y1 = corner
        try:
            x1 = int(x1)
            y1 = int(y1)
            cv2.circle(pool_corners, (x1,y1), 30, (0,0,255), -1)
            cv2.circle(pool_corners_border, (x1+pad,y1+pad), 30, (0,0,255), -1)
        except OverflowError:
            continue
    
    plt.figure(figsize=(12, 4))
    plt.subplot(121), show_image(pool_corners)
    plt.subplot(122), show_image(pool_corners_border)
    plt.show()

    return corners, pool_corners, pool_corners_border

def table_corners(imgfile):
    pool_hls, table_mask = hls_filter(imgfile)
    table_mask_cleaned = reduce_noise(pool_hls, table_mask)
    contour_drawing, hull_drawing = contour_convex_hull(table_mask_cleaned)
    lines, hough_drawing = hough(hull_drawing)
    unique_lines = find_four_lines(lines)
    pool_lines, pool_lines_border = draw_lines(unique_lines, imgfile)
    corners, pool_corners, pool_corners_border = find_draw_corners(unique_lines, pool_lines_border, imgfile)
    # TODO: need to choose the 4 corners of the 6 intersection points
    return corners
