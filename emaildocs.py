import smtplib
import zipfile
import time
from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase 
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate 
from email import encoders
import os
import json

textMessage = 'Attached are the documents for processing'

class mail:
    def __init__(self, config):

        param = config['EMAIL']

        self.user = param['USER']
        self.pwd =  param['PWD']
        self.From = param['FROM']

       
    def sendmail(self, To, Subject, filename):

        zf = open(filename, 'rb')

        msg = MIMEMultipart()
        msg['From'] = self.From
        msg['To'] = To
        msg['Date'] = formatdate(localtime = True)
        msg['Subject'] = Subject
        msg.attach (MIMEText(textMessage))

        part = MIMEBase('application', "octet-stream")
        part.set_payload(zf.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={filename}')
        msg.attach(part)
        
        
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
            server.login(self.user, self.pwd)
            server.sendmail(self.From, To, str(msg))
            server.close()
            print ('successfully sent the mail')
        except Exception as e:
            print(e)

    
    def get_email_data(self, file):

        f = open('emails.json')
        data = json.load(f)

        TO = data[file][1]
        SUBJECT = data[file][0]

        return TO, SUBJECT


