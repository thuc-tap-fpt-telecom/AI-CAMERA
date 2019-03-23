import cv2
import mysql.connector
from mysql.connector import MySQLConnection, Error
from mydatabase_dbconfig import read_db_config
cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('E:\\OpenCV\\opencv\\build\\etc\\haarcascades\\haarcascade_frontalface_default.xml')

#insert/update data to sqlite
def insertOrUpdate(Id,Name):
    db_config = read_db_config()
    print('Connecting to MySQL database...')
    args = (Name, Id)
    conn = MySQLConnection(**db_config)
    cursor = conn.cursor()
 
    if conn.is_connected():
        print('connection established.')
    else:
        print('connection failed.')
    cmd="SELECT * FROM employees WHERE ID= "+str(Id)
    cursor.execute(cmd)
    myresult = cursor.fetchone()
    if myresult is not None:
        cmd=""" UPDATE employees
                SET Name = %s
                WHERE ID = %s """
        print("Updated!!!")
    else:
        cmd = "INSERT INTO employees(name,id) VALUES(%s,%s)"
        print("Inserted!!!")
    cursor.execute(cmd,args)
    conn.commit()
    conn.close()
    
id=input('enter your id ')
name=input('enter your name ')
insertOrUpdate(id,name)
sampleNum=0
while(True):
    #camera read
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        
        #incrementing sample number 
        sampleNum=sampleNum+1
        #saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User."+id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])

        cv2.imshow('frame',img)
    #wait for 100 miliseconds 
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 20
    elif sampleNum>30:
        break
cam.release()
cv2.destroyAllWindows()