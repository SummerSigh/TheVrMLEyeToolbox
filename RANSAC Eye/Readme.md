## THIS IS RANSAC EYE 

__What is this?___
Ransac eye is the main 2d pupil fiting algorithm used in this repo!

__How do I use this?__
This Algorithm requries 2 main parameters to be set to work 

1. On line 92 please set cv2.VideoCapture() to your desiered source

2. On line 101 please set your threshold to the proper value (in the future this is will automated but at the time being you will have to play with the values for good results) 

3. **OPTIONAL** you can set line #5 to diffrent values however before changing these values, please read up on the ransac algorithm. The preset values should be good enough for most use cases though so I suggest you dont play with them. 

__RANSAC-AHA__

RANSAC-AHA is RANSAC + Always Have an Answer! This verson will make it so that RANSAC never loses tracking after a threshold is set! (do this in line 101). We use cv2.MinMaxLoc to find the darkest pixel in the image, then add a theshold value to capture the values in the rest of the eye! This way RANSAC will NEVER lose tracking! There are some disavantages to this, but in most cases this is really good! 
