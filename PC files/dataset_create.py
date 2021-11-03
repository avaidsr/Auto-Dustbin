import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode(IO.BCM)

i = '0' #rc
j = '0' #og
num = ''

# 1 or YES - Recyclable
# 0 or NO - Organic

#variable declaration
user_in = '1' # default value 1 # for trash type input from user
r_path = '/home/pi/auto_bin/dataset/rc/' # for 1
o_path = '/home/pi/auto_bin/dataset/og/' # for 0

img_path = ''

IO.setup(22, IO.IN, pull_up_down=IO.PUD_DOWN) # Capture image button (YES)

from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (1920,1080)
    

while True:
    user_in = input('Enter choice 1 - Recyclable and 0 - Organic')
    if user_in == '1':
        img_path = r_path
        num = i
        print(user_in)
        print(img_path)
        print(num)
    elif user_in == '0':
        img_path = o_path
        num = j
        print(user_in)
        print(img_path)
        print(num)
    else:
        print('Loop terminated')
        break
    camera.start_preview()
    while True:
        if(IO.input(22)==True):
            camera.capture(img_path + num + '.jpg')
            print(img_path + num + '.jpg')
            num = str(int(num)+1)
            if user_in == '1':
                i = num
            elif user_in == '0':
                path = o_path
                j = num
            camera.stop_preview()
            break

IO.cleanup()
