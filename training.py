from src.utils.common import read_config
from src.utils.models import model
from src.image_preprocess import ImagePreprocess
from src.utils.callbacks import get_callbacks
import argparse
import logging
import os
import tensorflow as tf


logging_str = "[%(asctime)s: %(levelname)s: %(module)s] %(message)s"
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename= os.path.join(log_dir,"running_logs.log"),level=logging.INFO, format=logging_str, filemode="a")


def training(config_path):

     config = read_config(config_path)

    ## training Parameters
     Loss = config['PARAMS']['LOSS']
     metrics = config['PARAMS']['METRICS']
     optimizer = config['PARAMS']['OPTIMIZER']
     epochs = config['PARAMS']['EPOCHS']
     batch_size = config['PARAMS']['BATCH_SIZE']

    ## model Parameter
     model_name =config["artifacts"]["model_name"]
     model_dir = config['artifacts']['model_dir']
     artifacts_dir = config["artifacts"]["artifacts_dir"]

    ## vgg16 parameters
     img_width = config['VGG16_PAR']['IMG_WIDTH']
     img_height = config['VGG16_PAR']['IMG_HEIGHT']
     trainable = config['VGG16_PAR']['TRAINABLE']

    ## image parameters
     shear_range = config['IMAGE_PREPROCESS']['SHEAR_RANGE']
     zoom_range = config['IMAGE_PREPROCESS']['ZOOM_RANGE']
     target_size = config['IMAGE_PREPROCESS']['TARGET_SIZE']
     img_batch_size = config ['IMAGE_PREPROCESS']['BATCH_SIZE']

   ## train and val_dir
     train_dir = config['IMAGE_DIR']['TRAIN_DIR']
     validation_dir = config['IMAGE_DIR']['VALIDATION_DIR']

     model_dir_path = os.path.join(artifacts_dir, model_dir)
     os.makedirs(model_dir_path, exist_ok=True)

     model_obj = model(Loss,optimizer,epochs,batch_size)
     model_clf = model_obj.vgg16(img_width, img_height, False)

     img_pre = ImagePreprocess(shear_range, zoom_range)
     training_set , validation_set = img_pre.datagen(train_dir ,validation_dir,target_size, img_batch_size)

     CALLBACK_LIST = get_callbacks(config, training_set)
     
     history = model_clf.fit_generator(training_set,
                         steps_per_epoch = 75005/batch_size,
                         epochs = epochs,
                         validation_data = validation_set,    
                         validation_steps = 24969/batch_size,
                         callbacks = CALLBACK_LIST)

    # model_clf.save('model_test.h5')

     model_obj.save_model(model_clf, model_name, model_dir_path)


if __name__ == '__main__':
    args = argparse.ArgumentParser()

    args.add_argument("--config", "-c", default="config.yaml")

    parsed_args = args.parse_args()
    logging.info(">>>>> starting training >>>>>")
    training(config_path=parsed_args.config)
    logging.info(">>>>> Ended training >>>>>") 

     
