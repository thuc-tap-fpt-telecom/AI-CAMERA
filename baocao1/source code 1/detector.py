import cv2
import numpy as np
from PIL import Image
#import pickle
#import sqlite3
from mysql.connector import MySQLConnection, Error
from mydatabase_dbconfig import read_db_config

faceDetect=cv2.CascadeClassifier('E:\\OpenCV\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_default.xml');
cam=cv2.VideoCapture(0);
rec=cv2.face.LBPHFaceRecognizer_create();
rec.read("recognizer\\trainningData.yml")
id=0
#set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 0.8
fontcolor = (203,23,252)

#get data from sqlite by ID
def getProfile(id):
    db_config = read_db_config()
    print('Connecting to MySQL database...')
    conn = MySQLConnection(**db_config)
    cursor = conn.cursor()
    cmd="SELECT * FROM employees WHERE ID="+str(id)
    cursor.execute(cmd)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile

while(True):
    #camera read
    ret,img=cam.read();
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=faceDetect.detectMultiScale(gray,1.3,5);
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        if conf < 70:
            profile=getProfile(id)
            #set text to window
            if(profile!=None):
                #cv2.PutText(cv2.fromarray(img),str(id),(x+y+h),font,(0,0,255),2);
                cv2.putText(img, "Name: " + str(profile[1]), (x,y+h+30), fontface, fontscale, fontcolor ,2)
                cv2.putText(img, "Age: " + str(profile[2]), (x,y+h+60), fontface, fontscale, fontcolor ,2)
                cv2.putText(img, "Gender: " + str(profile[3]), (x,y+h+90), fontface, fontscale, fontcolor ,2)
        else:
            cv2.putText(img, "Name: Unknown", (x, y + h + 30), fontface, fontscale, fontcolor ,2)
            cv2.putText(img, "Age: Unknown", (x, y + h + 50), fontface, fontscale, fontcolor ,2)
            cv2.putText(img, "Gender: Unknown", (x, y + h + 70), fontface, fontscale, fontcolor ,2)
        
    cv2.imshow('Face',img) 
    if cv2.waitKey(1)==ord('q'):
        break;
cam.release()
cv2.destroyAllWindows()