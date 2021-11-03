
import tensorflow as tf
# from keras.models import load_model #To save and load model
import numpy as np
from keras import backend as K
from keras.preprocessing import image
from keras.models import load_model

class CNN: 
    def __init__(self):
        self.path = 'recycle/model.h5'
    def prediction(self, img):
        classifier = load_model(self.path)
        test_image = image.load_img(img, target_size = (128, 128))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = classifier.predict(test_image)
        pred = {'class' : 'UNDEFINED'}
        if result[0][0] == 1:
            pred['class'] = 'Dog'
        else:
            pred['class'] = 'Cat'

        return pred
