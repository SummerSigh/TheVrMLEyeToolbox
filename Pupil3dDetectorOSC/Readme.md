__RANSAC OSC__

*What does this do?*

This takes the already existing 3D RANSAC implementation and gives it OSC powers for full VRC intergration!

*How do I set this up?*

1. install requirements.txt with ``` pip install -r requirements.txt ```

2. In SetROI.py set cv2.VideoCapture() line 5 to your Esp32 url stream, webcam (use cv2.VideoCapture(0)), or a video! 

3. Click and drag to set ROI on window that pops up, once your satisfied press ENTER. (The program will then exit) 

4. Set cv2.VideoCapture() on line 107 to your Esp32 url stream, webcam (use cv2.VideoCapture(0)), or a video. 

5. Open up VRC with your OSC compatible avatar (make sure to turn on OSC by going to the radial menu ----> options ----> OSC ----> hit the Enable button)
  NOTE: If you cant get/find an OSC avatar go to "jerrys mod" in vrc and get one there

6. Run the program and enjoy eye tracking in VRC! 

_NOTE THIS WILL ONLY RUN IN PYTHON 3.6!!!_
 
