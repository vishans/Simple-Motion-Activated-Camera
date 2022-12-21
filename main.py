import cv2
from time import time
import numpy as np
from datetime import datetime
import pydrive

# import the opencv library
import cv2


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
gauth = GoogleAuth()           
drive = GoogleDrive(gauth)  
  
COOLDOWN = 5 # seconds
vidCount = 0
# define a video capture object
vid = cv2.VideoCapture(0)

width  = vid.get(3)   # float `width`
height = vid.get(4)  # float `height`

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = None # cv2.VideoWriter('output.avi', fourcc, 20, frameSize = (int(width), int(height)))

 
currentFrame = vid.read()[1]
currentFrame = cv2.resize(currentFrame, resizedFrameDim := (100, int(100 / (width/height))), interpolation = cv2.INTER_AREA)
gray = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (21, 21), 0)

currentFrame = gray
rec = False
timeStamp = time()
  
while(True):
    rec = False 
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    originalFrame = frame

    frame = cv2.resize(frame, resizedFrameDim, interpolation = cv2.INTER_AREA)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    frameDelta = cv2.absdiff(currentFrame, gray)
    thresh = cv2.threshold(frameDelta, 10, 255, cv2.THRESH_BINARY)[1]

   

    if not((thresh == np.zeros_like(thresh)).all()):
        # reset timer
        # print('Motion Detected')
        timeStamp = time()

    if time() - timeStamp < COOLDOWN:
        if not out:
            out = cv2.VideoWriter(f'output{vidCount}.avi', fourcc, 20, frameSize = (int(width), int(height)))


        displayFrame = cv2.putText(originalFrame,datetime.now().strftime('%b-%d-%G %H:%M:%S'),(50,50),cv2.FONT_HERSHEY_SIMPLEX, 1,color=(255,255,255), thickness=2)
        out.write(originalFrame)

    else:
        if out:
            # print('Cooled Down. Recording stopped.')
            gfile = drive.CreateFile({'parents': [{'id': '1PUKk8co6c2U4JKptKJ96UgaPEU1ss3gL'}]})
            gfile.SetContentFile(f'output{vidCount}.avi')
            gfile.Upload() # Upload the file.
            vidCount += 1
            out.release()
            out = None


  
    # cv2.imshow('frame', displayFrame)

    currentFrame = gray
     
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
vid.release()
cv2.destroyAllWindows()