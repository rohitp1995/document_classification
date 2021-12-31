import tensorflow as tf


class ImagePreprocess:

    def __init__(self, shear_range, zoom_range, horizontal_flip =True):
        self.shear_range = shear_range
        self.zoom_range = zoom_range
        self.horizontal_flip = horizontal_flip

    def datagen(self, train_dir, val_dir, target_size, batch_size):

        train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255,
                                                                        shear_range= self.shear_range,
                                                                        zoom_range = self.zoom_range,
                                                                        horizontal_flip = self.horizontal_flip)

        test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1./255)


        
        training_set = train_datagen.flow_from_directory(train_dir,
                                                         target_size = (target_size, target_size),
                                                         batch_size = batch_size,
                                                         class_mode = 'categorical')


        validation_set = test_datagen.flow_from_directory(val_dir,
                                            target_size = (target_size, target_size),
                                            batch_size = batch_size,
                                            class_mode = 'categorical')


        return training_set, validation_set
