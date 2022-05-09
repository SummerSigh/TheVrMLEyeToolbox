***DISCLAIMER: I DO NOT OWN THE LINCENCE TO THIS CODE. 
Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details. ***

Copyright (C) 2018 Pupil Labs

All Rights Reserved.


**This is the Pye3d system by Pupil Labs**


*What does this do?*

This takes in data regarding 2d ellipse and point data (plus the focal_length, and resolution of that ROI croped image and outputs a 3d gaze vector! 

We can also improve the predictions of RANSAC by excluding all false posotives outside the eyeball

*How do I use this?* 

Please refer to RANSAC3d.py for an implemetation example

__How do I use this?__
This Algorithm requries 2 main parameters to be set to work 

1. On line 92 please set cv2.VideoCapture() to your desiered source

2. On line 102 please set your focal_length so that the big circle is about the same size of your eyeball (just know your value for this is going to be between 10 - 50) 

3.In line 118 please set your threshold to the proper value (in the future this is will automated but at the time being you will have to play with the values for good results) 

4. **OPTIONAL** you can set line #5 to diffrent values however before changing these values, please read up on the ransac algorithm. The preset values should be good enough for most use cases though so I suggest you dont play with them. 

***NOTE, THIS WILL ONLY WORK IN PYTHON 3.6***

