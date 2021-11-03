from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.resolution = (1920,1080)
#camera.framerate = 15
camera.start_preview()
#camera.start_recording('/home/pi/Desktop/video.h264')
sleep(15)
#camera.stop_recording()
camera.capture('/home/pi/auto_bin/foil.jpg')
camera.stop_preview()