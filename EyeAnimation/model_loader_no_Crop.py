import mobilenetv2
import cv2 
import torch
import matplotlib.pyplot as plt
import time
from pythonosc import udp_client


OSCip="127.0.0.1" 
OSCport= 9000 #VR Chat OSC port
client = udp_client.SimpleUDPClient(OSCip, OSCport)



def vc():
    vc.height = 1
    vc.width = 1
    vc.roicheck = 1
vc()
#check if cuda is available
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

#cheekPuff,cheekSquint_L,cheekSquint_R,noseSneer_L,noseSneer_R,jawOpen,jawForward,jawLeft,jawRight,mouthFunnel,mouthPucker,mouthLeft,mouthRight,mouthRollUpper,mouthRollLower,mouthShrugUpper,mouthShrugLower,mouthClose,mouthSmile_L,mouthSmile_R,mouthFrown_L,mouthFrown_R,mouthDimple_L,mouthDimple_R,mouthUpperUp_L,mouthUpperUp_R,mouthLowerDown_L,mouthLowerDown_R,mouthPress_L,mouthPress_R,mouthStretch_L,mouthStretch_R,tongueOut
classes = ["browInnerUp", "browDownRight", "browOuterUpRight", "eyeLookUpRight", "eyeLookDownv", "eyeLookInRight", "eyeLookOutRight", "eyeBlinkRight", "eyeSquintRight", "eyeWideRight"]
model = mobilenetv2.mobilenetv2().to(device)
model.load_state_dict(torch.load('Eye1.pt'))
model.eval()
cap = cv2.VideoCapture("demo3.mp4") #change this to 0 for webcam
while True:
    #read the frame
    ret, frame = cap.read()
    #convert the frame to gr ayscale
    frame = cv2.resize(frame, (100,100))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = gray
    img = cv2.resize(img, (100,100))
    gray = cv2.GaussianBlur(img, (3, 3), 0)
    image = gray.reshape(1,1, 100, 100) 
    image = torch.from_numpy(image).to(device)
    image = image.float()
    start = time.time()
    output = model(image)
    end = time.time()
    output = output.detach().cpu().numpy()
    #get the avatar/parameter/jawOpen'
    output = output[0]
    output = output.tolist()     
    output = [x * 100 for x in output]
    for i in range(len(output)):
        client.send_message(f"/{classes[i]}", output[i])
    cv2.imshow("image", gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()