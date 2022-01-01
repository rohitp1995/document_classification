import zipfile
import os 
from predict import doc_predict
import shutil

zip_dict = {'budget':[], 'email':[], 'form':[], 'invoice':[], 'letter':[]}

class Zip:
    def __init__(self, config):
        
        param = config["zip"]
        
        self.path_to_zip_file = param["path_to_zip_file"]
        self.directory_to_extract_to = param['directory_to_extract_to']
        self.zip_directory = param['zip_directory']

        os.makedirs(self.directory_to_extract_to, exist_ok = True)
        os.makedirs(self.zip_directory, exist_ok = True)

    def extract_data(self):

        with zipfile.ZipFile(self.path_to_zip_file, 'r') as zip_ref:
            zip_ref.extractall(self.directory_to_extract_to)

    def zip_data(self):

        for root,subdir,files in os.walk(self.directory_to_extract_to):
            for file in files:
                prediction = doc_predict(os.path.join(root,file))
                predicted = prediction.prediction()
                if predicted in zip_dict:
                    zip_dict[predicted].append(os.path.join(root,file))
                else:
                    pass

        for lst in zip_dict:
            with zipfile.ZipFile(os.path.join(self.zip_directory,f'{lst}.zip'), 'w') as zipF:
                for files in zip_dict[lst]:
                    zipF.write(files,compress_type=zipfile.ZIP_DEFLATED)
