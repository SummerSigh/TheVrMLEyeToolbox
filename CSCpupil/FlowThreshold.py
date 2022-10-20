import cv2
import numpy as np
import scipy.signal as sp

"""By Summer#2406: CSCpupil (Countor Sample Consensus for Pupil detection)"""
cap = cv2.VideoCapture("demo2.mp4")  # change this to the video you want to test
if cap.isOpened() == False:
    print("Error opening video stream or file")

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
eyelashes = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
lowb = np.array(0)
#get image width 
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH) 
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  

#this is a demonstration of the the optical flow system that I will be using in CSCpupil


eyeoffset =100 #controls the pupil threshold
while cap.isOpened():
    ret, img = cap.read()
    img = cv2.resize(img, (300, 200)) #it must be this size for parameters consistency reasons
    if ret == True:
        newImage2 = img.copy()
        image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, img2 = cap.read()
        img2 = cv2.resize(img2, (300, 200))
        #make gray 
        image_gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        #run optical flow on the two images
        flow = cv2.calcOpticalFlowFarneback(image_gray, image_gray2, None, 0.5, 1, 15, 5, 5, 1.2, 0)
        #dense optical flow where intenisty is brightness
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv = np.zeros_like(img)
        hsv[..., 1] = 255
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        #convert to gray
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        histr = hist.ravel()
        prevelipse = None
        try:
            peaks, properties  = sp.find_peaks(histr, distance=5)
            minpeak = np.min(peaks)
            print(minpeak)
            thresholdoptics = np.array(minpeak + eyeoffset)
            flowthresh = cv2.inRange(image_gray,lowb,thresholdoptics)
            #find contours
            contours, hierarchy = cv2.findContours(flowthresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            #find the largest contour   
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            cnt = contours[max_index]
            #fit an ellipse to the contour
            ellipse = cv2.fitEllipse(cnt)
            prevelipse = ellipse
            #draw the ellipse
            cv2.ellipse(newImage2, ellipse, (0, 255, 0), 2)
        except:
            cv2.ellipse(newImage2, prevelipse, (0, 255, 0), 2)
 
        cv2.imshow("gray", gray)
        cv2.imshow("frame", newImage2)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
