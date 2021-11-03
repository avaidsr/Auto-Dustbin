import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.cleanup()

from picamera import PiCamera
from time import sleep
camera = PiCamera()
camera.resolution = (1920,1080)

global yes
global count
global led
global path

path = ''

led = 2
yes = 22
IO.setup(yes, IO.IN, pull_up_down=IO.PUD_DOWN) # save image button
IO.setup(led, IO.OUT) # LED control

IO.output(led,IO.HIGH)

while True:
    if(IO.input(22)==True):
        break

    file1 = open("ct.txt","r+")  
    
    print("Output of Read function is ")
    #print(file1.read())
    count = int(file1.read())
    print('count')
    print(count)
    file1.close()

    while True:
        if(IO.input(22)==True):
            break
    print('------------------------------ switch on led ----------------------------------')
    IO.output(led,IO.LOW)
    camera.start_preview()
    sleep(5)
    path = 'new_set/'+str(count)+'.jpg'
    camera.capture(path)
    camera.stop_preview()
    print('------------------------------ switch off led ---------------------------------')
    IO.output(led,IO.HIGH)

    file1 = open("ct.txt","w")
    file1.writelines(str(count+1))
    file1.close()
    
    sleep(3)