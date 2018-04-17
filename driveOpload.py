import cv2
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

ret,img = cam.read()

cv2.imwrite("party2.jpg", img)
cv2.imshow('image', img)

id_path = '1ddy8S_BBeZBc5hN5Q6bPuh6D-kys59gU'

#file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
#for file1 in file_list:       
#    print ('title: %s, id: %s' % (file1['title'], file1['id']))
#sys.exit()




f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": id_path}]})
f.SetContentFile("party2.jpg")
f.Upload()
