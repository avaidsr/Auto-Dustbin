from keras.models import load_model #To save and load model
import numpy as np
from keras.preprocessing import image

def prediction():
    classifier = load_model('pi_files/recycle_model_V2.h5')
    
    test_image = image.load_img('pi_files/bread11.jpg', target_size = (128, 128))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = classifier.predict(test_image)
    pred = {'class' : 'D'}
    print(result)
    print(int(result[0][0]))
    
    if result[0][0] == 1:
        pred['class'] = 'Recyclable'
    else:
        pred['class'] = 'Organic'

    print(pred)

prediction()