print('Initializing')
import RPi.GPIO as IO
IO.setwarnings(False)
IO.setmode(IO.BCM)

IO.setup(22, IO.IN, pull_up_down=IO.PUD_DOWN) # Capture image button (YES)

inp = ''
p = ''
ch = ''
pred = ''

from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (1920,1080)

from keras.models import load_model #To save and load model
import numpy as np
from keras.preprocessing import image

classifier = load_model('recycle_model.h5')
print('Initialization finished')
print('Loop start')

while True:
    ch = raw_input('Enter choice 0 - Detect from stored image and 1 - Detect from new image')
    if ch == '0':
        p = raw_input('Enter image path : ')
    elif ch == '1':
        print('Start camera preview')
        camera.start_preview()
        while True:
            if(IO.input(22)==True):
                camera.capture('/home/pi/auto_bin/test_image_1.jpg')
                camera.stop_preview()
                p = '/home/pi/auto_bin/test_image_1.jpg'
                break
    else:
        print('Terminating program')
        break

    test_image = image.load_img(p, target_size = (128, 128))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = classifier.predict(test_image)

    if result[0][0] == 1:
        pred = 'Recyclable'
    else:
        pred = 'Organic'

    print(pred)

    inp = raw_input('Predict more images(y/n) ?')
    if inp.lower() == 'n':
        print('Terminating program')
        break

IO.cleanup()