# Welcome to The VR ML EYE Toolbox web page!

***This site is a work-in progress*** 
if you feel like there is somthing that I have to include, please contact me on discord at Summer#2406 and I will get back to you!

### What is this page for?

This page is to hopefully explain some of the math in algorithms such as RANSAC and Pye3d for people who are interseted in stuff like this. Lots of people were asking me how certain things within RANSAC and Pye3d work so in order to have some sort of concisent responce this website has been created.

____

# RANSAC

RANSAC (RANdom SAmple Consensus) is an algorithm make in 1981 traditionaly meant for SLAM (simultaneous localization and mapping). It's a general parameter estimation approach designed to cope with a large proportion of outliers in the input data. Unlike many of the common robust estimation techniques such as M-estimators and least-median squares that have been adopted by the computer vision community from the statistics literature, RANSAC was developed from within the computer vision community. RANSAC is a resampling technique that generates candidate solutions by using
the minimum number observations (data points) required to estimate the underlying model parameters. 

***As a rundown of the processes of the algorithm:***

1. Select randomly the minimum number of points required to determine the model parameters.
2. Solve for the parameters of the model.
3. Determine how many points from the set of all points fit with a predefined tolerance.
4. If the fraction of the number of inliers over the total number points in the set exceeds a predefined threshold τ , re-estimate the model parameters using all the identified inliers and terminate.
5. Otherwise, repeat steps 1 through 4 (maximum of N times).

Here is the RANSAC implementation from https://github.com/SummerSigh/TheVrMLEyeToolbox/blob/main/RANSAC%20Eye/pupiltest.py

```markdown
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

```


For more details see [Basic writing and formatting syntax](https://docs.github.com/en/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/SummerSigh/TheVrMLEyeToolbox/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
