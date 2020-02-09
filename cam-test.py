from picamera import PiCamera
from time import sleep

camera = PiCamera()

##camera.start_preview()
##sleep(10)
##camera.stop_preview()


##camera.start_preview()
##sleep(5)
##camera.capture('/home/pi/Desktop/image.jpg')
##camera.stop_preview()


camera.start_preview()
for i in range(5):
    sleep(1)
    camera.capture('/home/pi/Desktop/image%s.jpg' % i)
camera.stop_preview()
