from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS, cross_origin
from src.utils.utils import decodeImage
from predict import doc_predict
from get_zip import Zip
from src.utils.common import read_config
import json
import argparse
from emaildocs import mail

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)


class ClientApp:
    
    def __init__(self,config_path):
        
        self.filename = "inputImage.jpg"
        self.classifier = doc_predict(self.filename)
        self.config = read_config(config_path)
        self.zip_task = Zip(self.config) 
        self.mail_task = mail(self.config)


@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():
    image = request.json['image']
    decodeImage(image, clApp.filename)
    result = clApp.classifier.prediction()
    return jsonify(result)


@app.route("/email",  methods=['GET', 'POST'])
@cross_origin()
def EmailRoute():
    zip_file = '/zip_files/files.zip'
    os.makedirs(os.path.join('zip_files',zip_file),exist_ok=True)
    clApp.zip_task.extract_data()
    clApp.zip_task.zip_data()
     
     ### Email Part
    for file in os.listdir('zip_directory'):
        To , Subject = clApp.mail_task.get_email_data(file)
        clApp.mail_task.sendmail(To, Subject, os.path.join('zip_directory',file))

if __name__ == "__main__":
    
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="config.yaml")
    parsed_args = args.parse_args()

    clApp = ClientApp(parsed_args.config)
    app.run(host='127.0.0.1', port=8000, debug=True)
    
