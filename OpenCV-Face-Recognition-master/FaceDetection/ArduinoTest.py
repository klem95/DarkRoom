'''
Haar Cascade Face detection with OpenCV  
    Based on tutorial by pythonprogramming.net
    Visit original post: https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/  
Adapted by Marcelo Rovai - MJRoBot.org @ 7Feb2018 
'''

import numpy as np
import cv2
import serial
import RPi.GPIO as GPIO

ser=serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate=9600
GPIO.setmode(GPIO.BOARD)

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

while True:
    read_ser=ser.readline()
    print(read_ser)
    if read_ser == "TRIGGERED!":
        ret, img = cap.read()
        img = cv2.flip(img, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,     
            minSize=(20, 20)
        )

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
        

        cv2.imshow('video',img)

        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break

cap.release()
cv2.destroyAllWindows()
import serial
import RPi.GPIO as GPIO

ser=serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate=9600


GPIO.setmode(GPIO.BOARD)

while True:
    read_ser=ser.readline()
    print(read_ser)
   
    