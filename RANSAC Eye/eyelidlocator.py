import cv2
import numpy as np

from ransac_eyelids import ransac_line, ransac_parabola
from time import time
from math import pi



__y_pos_weight = 1                              # Try and weight sclera-boundary higher than eyelid crease
__parabola_y_offset = -10                       # Amount to shift eye-lid by after detection

__min_num_pts_u = 10

__gabor_params = {'ksize':(7, 7),
                  'sigma':3,
                  'theta':-pi / 2,
                  'lambd':pi * 3,
                  'gamma':2,
                  'psi':pi / 2,
                  'ktype':cv2.CV_32F}
__gabor_kern_horiz = cv2.getGaborKernel(**__gabor_params)

def find_upper_eyelid(eye_img, debug_index):

    u_2_win_rats_w = [0.0, 1.0, 0.0]              # Margins around ROI windows
    u_2_win_rats_h = [0.0, 0.5, 0.5]

    # FIXME - using r channel?
    img_blue = cv2.split(eye_img)[2]
    img_w, img_h = eye_img.shape[:2]
    
    # Indexes to extract window sub-images
    w_y1, w_y2 = int(img_h * u_2_win_rats_h[0]), int(img_h * sum(u_2_win_rats_h[:2]))
    w_x1, w_x2 = int(img_w * u_2_win_rats_w[0]), int(img_w * sum(u_2_win_rats_w[:2]))
    #show the sub-image

    # Split image into two halves
    window_img = img_blue
    
    # Supress eyelashes
    morph_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    window_img = cv2.morphologyEx(window_img, cv2.MORPH_CLOSE, morph_kernel)
 
    # Filter right half with inverse kernel of left half to ignore iris/sclera boundary    
    filter_img_win = cv2.filter2D(window_img, -1, __gabor_kern_horiz)
    
    # Copy windows back into correct places in full filter image
    filter_img = np.zeros(eye_img.shape[:2], dtype=np.uint8)
    filter_img[w_y1:w_y2, w_x1:w_x2] = filter_img_win
    
    # Mask with circles
    #cv2.circle(filter_img, (int(img_w * 0.5), int(img_h * 0.5)), int(img_w * 0.5), 0, -1)
    #cv2.circle(filter_img, (int(img_w * 0.5), int(img_h * 0.5)), int(img_w * 0.3), 255, -1)
    #show masks
    cv2.imshow('mask', filter_img)
    ys = np.argmax(filter_img, axis=0)
    xs = np.arange(filter_img.shape[1])[ys > 0]
    ys = (ys)[ys > 0]

    u_lid_pts = []
    
    for i, x in enumerate(xs):
        col = filter_img.T[x]
        start_ind, end_ind = ys[i] + 5, min(ys[i] + 100, len(col) - 2)
        col_window = col[start_ind:end_ind]
        max_col = np.max(col)
        max_win = np.max(col_window)
        if max_col - max_win < 50 :
            new_y = np.argmax(col_window) + ys[i] + 5
            u_lid_pts.append((x, new_y))
        else:u_lid_pts.append((x, ys[i]))
    
    # Only RANSAC fit eyelid if there are enough points
    if len(u_lid_pts) < __min_num_pts_u * 2:
        eyelid_upper_parabola = None
        u_lid_pts = []
    else:
        u_lid_pts_l = [(x,y) for (x,y) in u_lid_pts if x < filter_img.shape[1]/2]
        u_lid_pts_r = [(x,y) for (x,y) in u_lid_pts if x > filter_img.shape[1]/2]
        
        # Fit eye_img coord points of sclera-segs to degree 2 polynomial
        # a(x^2) + b(x) + c
        eyelid_upper_parabola = ransac_parabola(u_lid_pts_l, u_lid_pts_r,
                                                ransac_iters_max=5,
                                                refine_iters_max=2,
                                                max_err=4)
    if eyelid_upper_parabola is not None:
        a, b, c = eyelid_upper_parabola
        c = c - __parabola_y_offset
        eyelid_upper_parabola = a, b, c

    return eyelid_upper_parabola


cap = cv2.VideoCapture("test2.mp4")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    start = time()
    eyelid_upper_parabola = find_upper_eyelid(frame, 0)
    #draw the eyelid
    if eyelid_upper_parabola is not None:
        a, b, c = eyelid_upper_parabola
        x = np.arange(0, frame.shape[1])
        y = a * x**2 + b * x + c
        y = y.astype(np.int32)
        x = x.astype(np.int32)
        cv2.polylines(frame, [np.vstack((x, y)).T], False, (0, 255, 0), 2)

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break