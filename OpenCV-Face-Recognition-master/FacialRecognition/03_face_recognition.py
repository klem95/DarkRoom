''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''

import datetime
import time
import serial
import cv2
import numpy as np
import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

ser=serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate=9600

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Thomas'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

# Trigger
approvedUser = False

# Alcometer trigger
drunk = False;

# Distance sensor trigger
takeImg = False

# Google API
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

id_path = '1ddy8S_BBeZBc5hN5Q6bPuh6D-kys59gU'

timeStamp = datetime.datetime.now()

numberRecieved = 0

read_ser=0
print("Begin")

while True:
    #print("Reading...")

    ret, img =cam.read()
    img = cv2.flip(img, -1) # Flip vertically
    imgEx = cv2.flip(img, 1)
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    
        #break
    read_ser = ser.readline()
    if (len(read_ser) != 0):
        numberRecieved = int(read_ser)
        
    print(numberRecieved)
    if(numberRecieved == 2):
        drunk = True
 
    if(numberRecieved == 1):
        takeImg = True
    else:
        takeImg = False
   
    if approvedUser == False : 
        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                approvedUser = True
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
        
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
            
        
    if approvedUser == True & takeImg == True:
        read_ser=ser.readline()
        print(read_ser)
        print("Approved")
        cv2.imwrite(str(timeStamp) + ".jpg", imgEx)
        
        if drunk == False:
            f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": id_path}]})
            f.SetContentFile(str(timeStamp) + ".jpg")

        else:
            drunk_image = cv2.imread(str(timeStamp) + ".jpg")
            blurImg = cv2.blur(drunk_image,(30, 30)) # Kernel size
            cv2.imwrite("blur" + str(timeStamp) + ".jpg", blurImg)
            f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": id_path}]})
            f.SetContentFile("blur" + str(timeStamp) + ".jpg")
            drunk = False
    

        f.Upload()
        break
        
    cv2.imshow('camera',img)

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break 

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()

