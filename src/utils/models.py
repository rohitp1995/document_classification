import tensorflow as tf 
import time
import os 
from src.utils.utils import get_unique_filename


class model:
    
    def __init__(self,loss, optimizer, epochs, batch_size):

        self.loss = loss
        self.optimizer = optimizer 
        self.epochs = epochs

    def vgg16(self, img_width, img_height, trainable = bool):

        model = tf.keras.applications.vgg16.VGG16(weights = "imagenet", include_top=False, input_shape = (img_width, img_height, 3))

        for layer in model.layers:
            layer.trainable = trainable

        model_clf = tf.keras.models.Sequential(model.layers[:-1])

        model_clf.add(tf.keras.layers.Flatten())    
        model_clf.add(tf.keras.layers.Dense(128, activation='relu'))
        model_clf.add(tf.keras.layers.Dense(64, activation = 'relu'))
        model_clf.add(tf.keras.layers.Dense(5, activation = 'softmax'))
    
        model_clf.compile(optimizer = self.optimizer,  loss = self.loss, metrics = ['accuracy'])

        return model_clf

    
    def save_model(self, model, model_name, model_dir):
        unique_filename = get_unique_filename(model_name)
        path_to_model = os.path.join(model_dir, unique_filename)
        model.save(path_to_model)







        

        
        