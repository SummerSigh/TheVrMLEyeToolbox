from re import X
from tkinter import Y
import cv2

cap = cv2.VideoCapture("demo2.mp4")
ret, img = cap.read()
roibb = cv2.selectROI("image", img, fromCenter=False, showCrosshair=True)

print('X', roibb[0])
print('Y', roibb[1])
print('Width', roibb[2])
print('Height', roibb[3])

with open('roi.cfg', 'w+') as rf:
    rf.write(str(roibb[0]))
    rf.write('\n')
    rf.write(str(roibb[1]))
    rf.write('\n')
    rf.write(str(roibb[2]))
    rf.write('\n')
    rf.write(str(roibb[3]))