import io
import picamera
import cv2
import numpy
import datetime
import time
import os


while True:
    #Create a memory stream so photos doesn't need to be saved in a file
    stream = io.BytesIO()
    #Get the picture (low resolution, so it should be quite fast)
    #Here you can also specify other parameters (e.g.:rotate the image)
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.capture(stream, format='jpeg')

    #Convert the picture into a numpy array
    buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

    #Now creates an OpenCV image
    image = cv2.imdecode(buff, 1)

    #Load a cascade file for detecting faces
    face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

    #Convert to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    if len(faces) > 0:
        print("Found "+str(len(faces))+" face")
        break
    else:
        print("No face found")

#date_now = datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
#cv2.putText(image, date_now, (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)    
date_now = datetime.datetime.now().strftime("%A, %d %B %Y, %I:%M:%S%p")
today_is = 'Today is ' + date_now
    
#Draw a rectangle around every found face
for (x,y,w,h) in faces:
    cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
    
#Save the result image
cv2.imwrite('result.jpg',image)

os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/receipt/1-logo.png")
os.system("echo " + today_is + " | lp")
os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/receipt/2-thank-you.png")
os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/receipt/3-price.png")
os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/receipt/4-revenue.png")
os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/result.jpg")
os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/receipt/5-barcode.png")
