import cv2
import numpy as np
import scipy.signal as sp

"""By Summer#2406: CSCpupil (Countor Sample Consensus for Pupil detection)"""
cap = cv2.VideoCapture("pro.mp4")  # change this to the video you want to test
if cap.isOpened() == False:
    print("Error opening video stream or file")

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
eyelashes = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
lowb = np.array(0)
#get image width 
width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH) 
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  

eyeoffset = 40 #controls the pupil threshold
glintoffset = 1 #dont mess with this unless you know what you are doing
blur_size = 1 #only if you image is noisy. 1 is no blur. if you change this, only use odd numbers
while cap.isOpened():
    ret, img = cap.read()
    img = cv2.resize(img, (300, 200)) #it must be this size for parameters consistency reasons
    if ret == True:
        newImage2 = img.copy()
        image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #Calculate a histogram
        hist = cv2.calcHist([image_gray], [0], None, [256], [0, 256])
        histr = hist.ravel()
        peaks, properties   = sp.find_peaks(histr, distance=5)
        #get the smallest and largest peaks from the sp.find_peaks function
        minpeak = np.min(peaks)
        maxpeak = np.max(peaks)
        thresholdpupil = np.array(minpeak + eyeoffset)
        thresholdspec = np.array(maxpeak - glintoffset)
        #threshold pupil and process image for glints and eyelashes
        pupil = cv2.inRange(image_gray,lowb,thresholdpupil)
        pupil = cv2.dilate(pupil, kernel,(-1,-1), iterations = 2)
        spec = cv2.inRange(image_gray,lowb,thresholdspec)
        spec = cv2.erode(spec, kernel)
        image_gray = cv2.morphologyEx(image_gray, cv2.MORPH_OPEN, eyelashes)
        if blur_size > 1:
            image_gray = cv2.medianBlur(image_gray, blur_size)
        #find edges and fit contours
        edges = cv2.Canny(image_gray, 0, 1,apertureSize=3)
        edges = cv2.min(edges,spec)
        edges = cv2.min(edges,pupil)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, eyelashes)
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, eyelashes)
        contouredge, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        #pupil criteria for contour fitting or the "Consensus" part of the algorithm (NOT DONE, current state is very basic) 
        try: 
            for countor in contouredge:
                pem  = cv2.arcLength(countor,False)
                if pem > 100 and pem < 900: #the countor must be between 100 and 900 pixels long
                    ellipse = cv2.fitEllipse(countor) 
                    area = np.pi * ellipse[1][0] * ellipse[1][1]
                    if area > 4000 and area < 20000: # the area of the ellipse must be between 4000 and 20000 pixels
                        cv2.ellipse(newImage2, ellipse, (0, 0, 255), 2)
                    
        
        except:
            pass
        
        cv2.imshow('image', newImage2)
        cv2.imshow('pupil', pupil)
        cv2.imshow('edges', edges)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
