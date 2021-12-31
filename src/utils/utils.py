import base64
import time
import os 


def decodeImage(imgstring, fileName):
    imgdata = base64.b64decode(imgstring)
    with open(fileName, 'wb') as f:
        f.write(imgdata)
        f.close()

def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        return base64.b64encode(f.read())


def get_unique_filename(filename):
      unique_name = time.strftime(f"%Y%m%d_%H%M%S_{filename}")
      return unique_name