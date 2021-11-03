# trial name - Mark
import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.cleanup()

"""
original model output
1 - Recyclable
0 - Organic

new model output
change as soon as output recieved
0 - Recyclable
1 - Organic
"""

# 1 or YES - Organic
# 0 or NO - Recyclable

print('----------------------------- START -----------------------------')

#variable declaration
global classifier
global user_in
global result
global new_result
global ir
global led
global yes
global no
global servo
user_in = 1 # for trash type input from user
# user_v = 'Recyclable' # for trash type input from user in string format
#result = 1 # for trash type detected by model in numerical format
new_result = 1 # change model prediction
ans = 'Recyclable' # for trash type detected by model in string format

print('----------------------------- IMPORTING LIBRARIES -----------------------------')
from keras.models import load_model #To save and load model
import numpy as np
from keras.preprocessing import image

import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode(IO.BCM)

# Pin numbers for components
# Pin 13 and 18 for PWM Audio
ir = 14
led = 2
yes = 22
no = 10
servo = 15

IO.setup(ir, IO.IN) # Primary IR Sensor
IO.setup(led, IO.OUT) # LED control
IO.setup(yes, IO.IN, pull_up_down=IO.PUD_DOWN) # Yes/ 1/ Organic Button
IO.setup(no, IO.IN, pull_up_down=IO.PUD_DOWN) # No/ 0/ Recyclable Button
IO.setup(servo, IO.OUT) # Servo control pin

IO.output(led,IO.HIGH)

import os
import time


from picamera import PiCamera
from time import sleep
print('----------------------------- FINISHED IMPORTING LIBRARIES -----------------------------')
print('----------------------------- IMPORTING MODEL -----------------------------')
classifier = load_model('recycle_model.h5')
print('----------------------------- FINISHED IMPORTING MODEL -----------------------------')
path = '/home/pi/auto_bin/detect.jpg'
print('----------------------------- INITIALIZING CAMERA -----------------------------')
camera = PiCamera()
camera.resolution = (1920,1080)
# camera.framerate = 15
print('----------------------------- CAMERA INITIALIZED -----------------------------')


#start functions
# 1st to record primary sensor data
def primary_IR():
    #insert primary sensor input code at pin no.- GPIO 23

    while True:
        if(IO.input(ir)==False): #object is detected
            break
    #condition 1 if not detected - no action
    #condition 2 if detected - start below sequence

# 2nd to greet user and start further operations
def greet():
    os.system('mpg321 audio_files/greet1.mp3')
    ask_in_type()

# 3rd to ask for input type
def ask_in_type():
    global user_in
    global result
    global new_result
    os.system('mpg321 audio_files/ask_type_waste1.mp3')
    #wait for button/sensor input and store in variable
    while True:
        if(IO.input(22)==True):
            user_in = 1
            print('organic -1')
            break

        elif(IO.input(10)==True):
            user_in = 0
            print('rec - 0')
            break

    os.system('mpg321 audio_files/insert1.mp3') # prompt user to insert trash
    input_detection_identificaion()

# 4th for trash detection and identification
def input_detection_identificaion():
    global classifier
    global user_in
    global result
    global new_result
    #os.system('mpg321 audio_files/insert1.mp3') # prompt user to insert trash ***********************************************
    # delay(5s)
    #sleep(5)

    #wait for secondary IR/Button sensor detection
    #BUtton
    while True:
        if(IO.input(22)==True):
            break

    #once detected
    #enable LEDs and Pi Camera
    #code for LEDs  **********************************************************************************************************
    print('------------------------------ switch on led ----------------------------------')
    IO.output(led,IO.LOW)
    camera.start_preview()
    sleep(5)
    camera.capture(path)
    camera.stop_preview()
    print('------------------------------ switch off led ---------------------------------')
    IO.output(led,IO.HIGH)
    #code for detection
    test_image = image.load_img(path, target_size = (128, 128))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = classifier.predict(test_image)
    if result[0][0] == 1:
        #pred['class'] = 'Recyclable'
        new_result = 0
    else:
        #pred['class'] = 'Organic'
        new_result = 1
    print('original prediction - ')
    print(result)
    print('------------------------ DONE PREDICTING --------------------------------')
    print('new predicted answer - ')
    print(new_result)
    print('user\'s answer - ')
    print(user_in)


    comp()

# 5th for comparison
def comp():
    # compare ans with user input
    # if wrong user input
    global user_in
    global result
    global new_result
    if(new_result != user_in):
        print('-------------------WRONG ANSWER----------------------')
        os.system('mpg321 audio_files/wrong_answer.mp3')
        if(new_result == 1):
            os.system('mpg321 audio_files/actual_O.mp3')
        elif(new_result == 0):
            os.system('mpg321 audio_files/actual_R.mp3')
        os.system('mpg321 audio_files/try_again.mp3')
        ask_in_type()
    # if correct input - perform following actions
    elif(new_result == user_in):
        print('----------------------------------RIGHT ANSWER-----------------------')
        os.system('mpg321 audio_files/applaud1.mp3')
        # ask for more trash
        # operate servo ****************************************************************************************************

        os.system('mpg321 audio_files/more_trash.mp3')
        # wait for button/sensor input
        while True:
            if(IO.input(10)==True):
                os.system('mpg321 audio_files/thanks.mp3')
                exit()
            elif(IO.input(22)==True):
                ask_in_type()

print('----------------------------- STARTING MAIN LOOP -----------------------------')

while True:
    #main loop
    primary_IR()
    greet()
