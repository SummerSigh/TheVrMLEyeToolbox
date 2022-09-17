from threading import Thread
import cv2
import numpy as np                             
from pye3dcustom.detector_3d import CameraModel, Detector3D, DetectorMode
from pythonosc import udp_client

OSCip="127.0.0.1" 
OSCport=9000 #VR Chat OSC port
client = udp_client.SimpleUDPClient(OSCip, OSCport)

def vc():
    vc.height = 1
    vc.width = 1
    vc.roicheck = 1
vc()





def fit_rotated_ellipse_ransac(
    data, iter=80, sample_num=10, offset=80    # 80.0, 10, 80
):  # before changing these values, please read up on the ransac algorithm
    # However if you want to change any value just know that higher iterations will make processing frames slower
    count_max = 0
    effective_sample = None

    for i in range(iter):
        sample = np.random.choice(len(data), sample_num, replace=False)

        xs = data[sample][:, 0].reshape(-1, 1)
        ys = data[sample][:, 1].reshape(-1, 1)

        J = np.mat(
            np.hstack((xs * ys, ys**2, xs, ys, np.ones_like(xs, dtype=np.float)))
        )
        Y = np.mat(-1 * xs**2)
        P = (J.T * J).I * J.T * Y

        # fitter a*x**2 + b*x*y + c*y**2 + d*x + e*y + f = 0
        a = 1.0
        b = P[0, 0]
        c = P[1, 0]
        d = P[2, 0]
        e = P[3, 0]
        f = P[4, 0]
        ellipse_model = (
            lambda x, y: a * x**2 + b * x * y + c * y**2 + d * x + e * y + f
        )

        # threshold
        ran_sample = np.array(
            [[x, y] for (x, y) in data if np.abs(ellipse_model(x, y)) < offset]
        )

        if len(ran_sample) > count_max:
            count_max = len(ran_sample)
            effective_sample = ran_sample

    return fit_rotated_ellipse(effective_sample)


def fit_rotated_ellipse(data):

    xs = data[:, 0].reshape(-1, 1)
    ys = data[:, 1].reshape(-1, 1)

    J = np.mat(np.hstack((xs * ys, ys**2, xs, ys, np.ones_like(xs, dtype=np.float))))
    Y = np.mat(-1 * xs**2)
    P = (J.T * J).I * J.T * Y

    a = 1.0
    b = P[0, 0]
    c = P[1, 0]
    d = P[2, 0]
    e = P[3, 0]
    f = P[4, 0]
    theta = 0.5 * np.arctan(b / (a - c))

    cx = (2 * c * d - b * e) / (b**2 - 4 * a * c)
    cy = (2 * a * e - b * d) / (b**2 - 4 * a * c)

    cu = a * cx**2 + b * cx * cy + c * cy**2 - f
    w = np.sqrt(
        cu
        / (
            a * np.cos(theta) ** 2
            + b * np.cos(theta) * np.sin(theta)
            + c * np.sin(theta) ** 2
        )
    )
    h = np.sqrt(
        cu
        / (
            a * np.sin(theta) ** 2
            - b * np.cos(theta) * np.sin(theta)
            + c * np.cos(theta) ** 2
        )
    )

    ellipse_model = lambda x, y: a * x**2 + b * x * y + c * y**2 + d * x + e * y + f

    error_sum = np.sum([ellipse_model(x, y) for x, y in data])

    return (cx, cy, w, h, theta)

cap = cv2.VideoCapture('demo2.mp4')  # change this to the video you want to test
result_2d = {}
result_2d_final = {}

ret, img = cap.read()
frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
fps = cap.get(cv2.CAP_PROP_FPS)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

camera = CameraModel(focal_length=30, resolution=[width,height])

detector_3d = Detector3D(camera=camera)

if cap.isOpened() == False:
    print("Error opening video stream or file")
while cap.isOpened():
    ret, img = cap.read()
    frame_number = cap.get(cv2.CAP_PROP_POS_FRAMES)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if ret == True:
        newImage2 = img.copy()
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(
            image_gray, 105, 255, cv2.THRESH_BINARY
        )  # this will need to be adjusted everytime hardwere is changed (brightness of IR, Camera postion, etc)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        image = 255 - closing
        contours, hierarchy = cv2.findContours(
            image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
        )
        hull = []
        for i in range(len(contours)):
            hull.append(cv2.convexHull(contours[i], False))
        try:
            cv2.drawContours(img, contours, -1, (255, 0, 0), 1)
            cnt = sorted(hull, key=cv2.contourArea)
            maxcnt = cnt[-1]
            ellipse = cv2.fitEllipse(maxcnt)
            cx, cy, w, h, theta = fit_rotated_ellipse_ransac(maxcnt.reshape(-1, 2))
            #get axis and angle of ellipse pupil labs 2d  
            result_2d["center"] = (cx, cy)
            result_2d["axes"] = (w, h) 
            result_2d["angle"] = theta * 180.0 / np.pi 
            result_2d_final["ellipse"] = result_2d
            result_2d_final["diam eter"] = w 
            result_2d_final["location"] = (cx, cy)
            result_2d_final["confidence"] = 0.99
            result_2d_final["timestamp"] = frame_number / fps
            result_3d = detector_3d.update_and_detect(result_2d_final, image_gray)
            ellipse_3d = result_3d["ellipse"]
            
            
            # draw pupil
            cv2.ellipse(
                image_gray,
                tuple(int(v) for v in ellipse_3d["center"]),
                tuple(int(v) for v in ellipse_3d["axes"]),
                ellipse_3d["angle"],
                0,
                360,  # start/end angle for drawing
                (0, 255, 0),  # color (BGR): red
            )
            projected_sphere = result_3d["projected_sphere"]
            
            # draw eyeball
            cv2.ellipse(
                image_gray,
                tuple(int(v) for v in projected_sphere["center"]),
                tuple(int(v) for v in projected_sphere["axes"]),
                projected_sphere["angle"],
                0,
                360,  # start/end angle for drawing
                (0, 255, 0),  # color (BGR): red
            )
            
            # draw line from center of eyeball to center of pupil
            cv2.line(
                image_gray,
                tuple(int(v) for v in projected_sphere["center"]),
                tuple(int(v) for v in ellipse_3d["center"]),
                (0, 255, 0),  # color (BGR): red
            )




            #print the x distance between center of eyeball and center of pupil in a float



            #print the y distance between center of eyeball and center of pupil as a float between -1 and 1 (0 is center)
            xrl = (cx - projected_sphere["center"][0]) / projected_sphere["axes"][0]
            eyey = (cy - projected_sphere["center"][1]) / projected_sphere["axes"][1]
            if xrl >= 0:
                client.send_message("/avatar/parameters/RightEyeX", -abs(xrl))
                client.send_message("/avatar/parameters/LeftEyeX", -abs(xrl))
            if xrl <= 0:
                client.send_message("/avatar/parameters/RightEyeX", abs(xrl))
                client.send_message("/avatar/parameters/LeftEyeX", abs(xrl))

            if eyey >= 0:
                print(eyey)
                client.send_message("/avatar/parameters/EyesY", -abs(eyey))
                client.send_message("/avatar/parameters/EyesY", -abs(eyey))
            if eyey <= 0:
                client.send_message("/avatar/parameters/EyesY", abs(eyey))
                client.send_message("/avatar/parameters/EyesY", abs(eyey))

            



        except:
             pass
        
        cv2.imshow("Ransac", image_gray)
        cv2.imshow("Original", thresh)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break