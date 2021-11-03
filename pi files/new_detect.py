from keras.models import load_model #To save and load model
import numpy as np
from keras.preprocessing import image

from picamera import PiCamera
from time import sleep
classifier = load_model('recycle_model.h5')
path = '/home/pi/auto_bin/detect.jpg'
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.framerate = 15

def prediction():
    
    camera.start_preview()
    sleep(5)
    camera.capture(path)
    camera.stop_preview()
    
    test_image = image.load_img(path, target_size = (128, 128))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = classifier.predict(test_image)
    pred = {'class' : 'D'}
    
    if result[0][0] == 1:
        pred['class'] = 'Recyclable'
    else:
        pred['class'] = 'Organic'

    print(pred)
    #return pred

for i in range(10):
    prediction()
