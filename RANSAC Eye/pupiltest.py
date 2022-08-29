import cv2
import numpy as np
def fit_rotated_ellipse_ransac(
    data, iter=100, sample_num=10, offset=80    # 80.0, 10, 80
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
    print("fitting error = %.3f" % (error_sum))

    return (cx, cy, w, h, theta)

cap = cv2.VideoCapture("demo2.mp4")  # change this to the video you want to test
if cap.isOpened() == False:
    print("Error opening video stream or file")
while cap.isOpened():
    ret, img = cap.read()
    if ret == True:
        newImage2 = img.copy()
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        image_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #remove 10 pixels from the bottom of the image
        image_gray = image_gray[0:img.shape[0]-10, :]
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(image_gray)
        #find threshold value
        threshold_value = min_val + 20
        ret, thresh = cv2.threshold(
            image_gray, threshold_value, 255, cv2.THRESH_BINARY
        )  # this will need to be adjusted everytime hardwere is changed (brightness of IR, Camera postion, etc)
        #find the darkest point in the image using minMaxLoc
        #plot the darkest point on the image
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        image = 255 - closing
        contours, hierarchy = cv2.findContours(
            image, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
        )
        hull = []
        for i in range(len(contours)):
            hull.append(cv2.convexHull(contours[i], False))
        # try:
        #     cv2.drawContours(img, contours, -1, (255, 0, 0), 1)
        #     cnt = sorted(hull, key=cv2.contourArea)
        #     maxcnt = cnt[-1]
        #     ellipse = cv2.fitEllipse(maxcnt)
        #     cx, cy, w, h, theta = fit_rotated_ellipse_ransac(maxcnt.reshape(-1, 2))
        #     print(cx, cy)
        #     cv2.circle(newImage2, (int(cx), int(cy)), 2, (0, 0, 255), -1)
        #     cx1, cy1, w1, h1, theta1 = fit_rotated_ellipse(maxcnt.reshape(-1, 2))
        #     cv2.ellipse(
        #         newImage2,
        #         (int(cx), int(cy)),
        #         (int(w), int(h)),
        #         theta * 180.0 / np.pi,
        #         0.0,
        #         360.0,
        #         (50, 250, 200),
        #         1,
        #     )       
        # except:
        #     pass
        cv2.circle(newImage2, min_loc, 2, (0, 0, 255), -1)
        cv2.imshow("Ransac", newImage2)
        cv2.imshow("Thresh", thresh)
        #make it into a video

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
out.release()
cap.release()
cv2.destroyAllWindows()