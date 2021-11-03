# trial name - Mark
import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.cleanup()

# 1 or YES - Recyclable
# 0 or NO - Organic

#variable declaration
user_in = 1 # for trash type input from user
# user_v = 'Recyclable' # for trash type input from user in string format
result = 1 # for trash type detected by model in numerical format
ans = 'Recyclable' # for trash type detected by model in string format

print('Importing Libraries')
from keras.models import load_model #To save and load model
import numpy as np
from keras.preprocessing import image

import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode(IO.BCM)

IO.setup(23, IO.IN) # Primary IR Sensor
IO.setup(24, IO.IN) # Secondary IR Sensor
IO.setup(22, IO.IN, pull_up_down=IO.PUD_DOWN) # Yes Button
IO.setup(27, IO.IN, pull_up_down=IO.PUD_DOWN) # No Button

import os
import time


from picamera import PiCamera
from time import sleep
print('Finished Importing Libraries')
print('Importing Model')
classifier = load_model('recycle_model.h5')
print('Fininshed Importing Model')
path = '/home/pi/auto_bin/detect.jpg'
print('Initializing Camera')
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15
print('Camera Initialized')

print('Starting Main loop')

while True:
    #main loop
    primary_IR()
    greet()


#start functions
# 1st to record primary sensor data
def primary_IR():
    #insert primary sensor input code at pin no.- GPIO 23

    if(IO.input(23)==True): #object is far away
        primary_IR()
    elif(IO.input(23)==False): # object detected
        return
    #condition 1 if not detected - no action
    #condition 2 if detected - start below sequence

# 2nd to greet user and start further operations
def greet():
    os.system('mpg321 greet1.mp3')
    ask_in_type()

# 3rd to ask for input type
def ask_in_type():
    os.system('mpg321 ask_type_waste1.mp3')
    #wait for button/sensor input and store in variable
    if(IO.input(22)==True):
        user_in = 1

    elif(IO.input(27)==True):
        user_in = 0

    input_detection_identificaion()

# 4th for trash detection and identification
def input_detection_identificaion():
    os.system('mpg321 insert1.mp3') # prompt user to insert trash
    # delay(5s)
    sleep(5)

    #wait for secondary IR sensor detection
    if(IO.input(24)==True):
        input_detection_identificaion()

    elif(IO.input(24)==False):
        #once detected
        #enable LEDs and Pi Camera
        #code for LEDs
        camera.start_preview()
        sleep(5)
        camera.capture(path)
        camera.stop_preview()
        #code for detection
        test_image = image.load_img(path, target_size = (128, 128))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = classifier.predict(test_image)
        pred = {'class' : 'D'}

        if result[0][0] == 1:
            pred['class'] = 'Recyclable'
            ans = 'Recyclable'
        else:
            pred['class'] = 'Organic'
            ans = 'Organic'

    comp()

# 5th for comparison
def comp():
    # compare ans with user input
    # if wrong user input
    if(result != user_in):
        os.system('mpg321 wrong_answer.mp3')
        if(result == 1):
            os.system('mpg321 actual_R.mp3')
        elif(result == 0):
            os.system('mpg321 actual_O.mp3')
        os.system('mpg321 try_again.mp3')
        ask_in_type()
    # if correct input - perform following actions
    if(result == user_in):
        os.system('mpg321 applaud1.mp3')
        # ask for more trash
        os.system('mpg321 more_trash.mp3')
        # wait for button/sensor input
        if(IO.input(27)==True):
            os.system('mpg321 thanks.mp3')
            return
        elif(IO.input(22)==True):
            ask_in_type()
