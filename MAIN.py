
# importing the requests library 
import requests 
import io
import picamera
import cv2
import numpy
import datetime
import time
import os
import argparse
import logging

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
    help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-l", "--log", type=str, default="log.txt",
    help="path to output log file")
args = vars(ap.parse_args())


# open the logging file
logging.basicConfig(filename=args["log"], level=logging.DEBUG)
logging.info("[{}] Waiting for camera to warmup".format(datetime.datetime.now()))

faceDetected = False

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
    face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/surv/haarcascade_frontalface_default.xml')

    #Convert to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    if len(faces) > 0:
        print("Found "+str(len(faces))+" face")
        logging.info("[{}] Face found".format(datetime.datetime.now()))
        faceDetected = True
        break
    else:
        print("No face found")

#date_now = datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")
#cv2.putText(image, date_now, (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        
if (faceDetected):
    date_now = datetime.datetime.now().strftime("%A, %d %B %Y, %I:%M:%S%p")
    today_is = 'Today is ' + date_now
        
    #Draw a rectangle around every found face
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)
        
    #Save the result image
    cv2.imwrite('/home/pi/Desktop/surv/result.jpg',image)

    logging.info("[{}] Sent to printer".format(datetime.datetime.now()))
    os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/receipt/1-logo.png")
    os.system("echo " + today_is + " | lp")
    os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/receipt/2-thank-you.png")
    os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/receipt/3-price.png")
    os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/receipt/4-revenue.png")
    os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/result.jpg")
    os.system("lp -o fit-to-page -o orientation-requested=1 /home/pi/Desktop/surv/receipt/5-barcode.png")

logging.info("[{}] Cleaning up".format(datetime.datetime.now()))

url = 'https://hm1973.itp.io/image-upload'  
files = {'image_name': open('/home/pi/Desktop/surv/receipt/5-barcode.png', 'rb')}
r = requests.post(url, files=files)

logging.info("[{}] POST status: ".r.status_code)
logging.info("[{}] POST response: ".r.text)









