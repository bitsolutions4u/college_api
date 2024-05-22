import sys
import os
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.mail.backends.smtp import EmailBackend

from dynamic_preferences.registries import global_preferences_registry 


import urllib.request
import urllib.parse

import threading
import logging
from datetime import datetime

from PIL import Image
import json

log = logging.getLogger(__name__)


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class SMSThread(threading.Thread):

    def __init__(self, data):
        self.data = data
        threading.Thread.__init__(self)

    def run(self):
        GLOBAL_VARS = global_preferences_registry.manager().all()
        data =  urllib.parse.urlencode({GLOBAL_VARS['SMS__MSG_VAR']: self.data['message'], GLOBAL_VARS['SMS__NUMBER_VAR']:self.data['to_phone']})
        # data = data.encode('utf-8')
        # request = urllib.request.Request("http://text.justsms.co.in/vendorsms/pushsms.aspx?")
        # request = urllib.request.Request("http://164.52.195.161/API/SendMsg.aspx?uname=20160715&pass=srilalitha&send=SLEIPL&dest=7382766529&msg=Hi%20Gopi%0AREGARDS%2C%0ASRI%20LALITHA%20ENTERPRISES%20INDUSTRIES%20PVT%20LTD.%2C&priority=1")
        # request = urllib.request.Request("http://164.52.195.161/API/SendMsg.aspx?uname=20160715&pass=srilalitha&send=SLEIPL&"+msg+"&dest="+number)
        request = urllib.request.Request(GLOBAL_VARS['SMS__URL'] + data )
        f = urllib.request.urlopen(request)
        fr = f.read()
        return(fr)

class IOThread(threading.Thread):

    def __init__(self, url, data):
        self.url = url
        self.data = data
        threading.Thread.__init__(self)

    def run(self):
        IO_SERVER_URL = os.getenv("IO_SERVER_URL", default=settings.IO_SERVER_URL)
        if IO_SERVER_URL != None:
            data = json.dumps(self.data).encode('utf-8')
            request = urllib.request.Request(IO_SERVER_URL + self.url, data=data, headers={ 'Content-Type': 'application/json' })
            f = urllib.request.urlopen(request)
            fr = f.read()
            return(fr)
        else:
            return None


class Util:
    @staticmethod
    def send_email(data):
        log.info("======================================EMAIL======================================")
        log.info("subject: {subject}, body: {body}, to: {to}".format(subject=data['email_subject'], body=data['email_body'], to=data['to_email']))
        log.info("=================================================================================")

        GLOBAL_VARS = global_preferences_registry.manager().all()
        print(GLOBAL_VARS)
        GLOBAL_VARS['SMTP__USER']="bitsolutions4u@gmail.com"
        GLOBAL_VARS['SMTP__PASSWORD']="Ramesh007123##"
        backend = EmailBackend(host=GLOBAL_VARS['SMTP__HOST'], port=GLOBAL_VARS['SMTP__PORT'], username=GLOBAL_VARS['SMTP__USER'], 
                       password=GLOBAL_VARS['SMTP__PASSWORD'], use_tls=GLOBAL_VARS['SMTP__USE_TLS'])
            

        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']], connection=backend)
        EmailThread(email).start()

    @staticmethod
    def send_sms(data):
        log.info("======================================SMS======================================")
        log.info(""+data['to_phone']+" "+data['message'])
        log.info("=================================================================================")
        SMSThread(data).start()
        
    @staticmethod
    def send_live_notification(url, data):
        IOThread(url, data).start()
        




def getcode(model, prefix):
    lastRec = model.objects.last()
    if lastRec:
        nxtId = lastRec.id + 1
    else:
        nxtId = 1
    nxtIdlen = len(str(nxtId))
    if nxtIdlen == 1:
        prenum = '0000'
    elif nxtIdlen == 2:
        prenum = '000'
    elif nxtIdlen == 3:
        prenum = '00'
    elif nxtIdlen == 4:
        prenum = '0'
    else:
        prenum =''
        
    return str(prefix) + str(prenum) + str(nxtId)


def doccode(model, prefix):
    lastRec = model.objects.last()
    if lastRec:
        nxtId = lastRec.id + 1
    else:
        nxtId = 1
    now = datetime.now() 

    date_time = now.strftime("%y%m%d%H%M%S%f")[:-3]
    
        
    return str(prefix) + str(date_time )


def get_request_url(request):

    if settings.USE_GLOBAL_URL:
        return settings.GLOBAL_URL
    else:
        # current_site = get_current_site(self.context['request']).domain
        baseurl = "https://" if request.is_secure() else "http://"
        baseurl += request.get_host()
        return baseurl

        
def removeDuplicates(arr):
    temp = []
    for i in range(len(arr)):
        if arr[i] not in temp:
            temp.append(arr[i])
    return temp


    
def CompressImage(selectedfile):
    name_arr = selectedfile.name.split('.')
    valid_extensions = ['jpg', 'jpeg', 'png',]
    if len(name_arr) > 1 and name_arr[-1].lower() in valid_extensions:
        if selectedfile and not isinstance(selectedfile, str):

            im = Image.open(selectedfile)

            output = BytesIO()

            # Resize/modify the image
            # im = im.resize((100, 100))

            im = im.convert('RGB')
            im.save(output, format='JPEG',
                    optimize = True,  
                    quality = 30)
            output.seek(0)

            return InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % name_arr[0], 'image/jpeg',sys.getsizeof(output), None)
        else:
            return selectedfile
    else:
        return selectedfile
