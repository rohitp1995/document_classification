import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class dogcat:
    def __init__(self,filename):
        self.filename =filename


    def predictiondogcat(self):
        
        model = load_model('/artifcats/model/model_vgg16.h5')

        imagename = self.filename
        test_image = image.load_img(imagename, target_size = (256, 256))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        result = model.predict(test_image)
        print(result[0].argmax())

        if result[0].argmax() == 0:
            prediction = 'budget'
        elif result[0].argmax() == 1: 
            prediction = 'email'
        elif result[0].argmax() == 2: 
            prediction = 'form'
        elif result[0].argmax() == 3: 
            prediction = 'invoice'
        elif result[0].argmax() == 4: 
            prediction = 'letter'

        return (f" The image belongs to the {prediction} class")

    