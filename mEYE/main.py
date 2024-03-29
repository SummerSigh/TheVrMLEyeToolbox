import os
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
import cv2
from skimage.measure import label, regionprops
from tensorflow.keras.models import load_model
import tensorflow as tf
import time
MODELPATH = 'meye.hdf5'
tf.config.threading.set_intra_op_parallelism_threads(2)
model = load_model(MODELPATH)
VIDEOPATH = "demo3.mp4"
cap = cv2.VideoCapture(VIDEOPATH)
THRESHOLD = 30
def morphProcessing(sourceImg, THRESHOLD):
    # Binarize 
    binarized = sourceImg > THRESHOLD
    # Divide in regions and keep only the biggest
    label_img = label(binarized)
    regions = regionprops(label_img)
    if len(regions)==0:
        morph = np.zeros(sourceImg.shape, dtype='uint8')
        centroid = (np.nan, np.nan)
        return (morph, centroid)
    regions.sort(key=lambda x: x.area, reverse=True)
    centroid = regions[0].centroid # centroid coordinates of the biggest object
    if len(regions) > 1:
        for rg in regions[1:]:
            label_img[rg.coords[:,0], rg.coords[:,1]] = 0
    label_img[label_img!=0] = 1
    biggestRegion = (label_img*255).astype(np.uint8)
    # Morphological
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(IMCLOSING,IMCLOSING))
    morph = cv2.morphologyEx(biggestRegion, cv2.MORPH_CLOSE, kernel)
    return (morph, centroid)



while cap.isOpened(): 
    ret,frame = cap.read()
    start = time.time()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame, (128, 128))
    networkInput = frame.astype(np.float32) / 255.0
    networkInput = networkInput[None, :, :, None]
    mask, info = model(networkInput)
    prediction = mask[0,:,:,0]
    morphedMask, centroid = morphProcessing(prediction,THRESHOLD)
    eyeProbability = info[0,0]
    blinkProbability = info[0,1]
    print("eyeProbability:" + str(eyeProbability))
    print("blinkProbability:" + str(blinkProbability))
    print("pupCntr_x" + str(centroid[1]))
    print("pupCntr_y" + str(centroid[0]))
    print("pupilSize:" + str(np.sum(morphedMask)/255))
    print("\n")
    #plot pupil center on frame
    try:
        cv2.circle(frame, (int(centroid[1]), int(centroid[0])), 5, (0,0,255), -1)
    except:
        pass
    #put mask on frame
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    #fit a ellipse to the mask using the contour of the biggest region
    try:
        contours, hierarchy = cv2.findContours(morphedMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        ellipse = cv2.fitEllipse(cnt)
        cv2.ellipse(frame, ellipse, (0,255,0), 2)
    except:
        pass
    cv2.imshow("frame", frame)
    endtime = time.time()
    print("fps: " + str(1/(endtime-start)))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()