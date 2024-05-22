from Common.utils import Util
from Common.Constants import  SMS
from .models import Notification as NotificationModel
# import firebase_admin
# from firebase_admin import credentials, messaging
import json
from django.db.models import Q
from Users.models import Device
from dynamic_preferences.registries import global_preferences_registry 

login = True
def firebase_init():
    global login
    if login:
        try:
            GLOBAL_VARS = global_preferences_registry.manager().all()
            # project_json = credentials.Certificate(json.loads(GLOBAL_VARS['JSON_DATA__JSONFILE'],strict=False))
            # firebase_admin.initialize_app(project_json)
            login=False
        except Exception as E:
            print("--Error--",E)
    else:
        pass
        
        
    



class Notification:
    
    def Send(user=None,subject="",body="",type=1,ref=0,):
        if user != None and subject != "":
            NotificationModel(user=user,subject=subject,body=body,type=type,ref=ref,).save()
            if user.phone:          
                sdata = {'to_phone': user.phone, 'message':  body + SMS.postfix }
                Util.send_sms(sdata)

    def SendToUsers(users=[],subject="",body="",type=1,ref=0,):
        if len(users) > 0 and subject != "":
            for user in users:
                NotificationModel(user=user,subject=subject,body=body,type=type,ref=ref,).save()
                if user.phone:          
                    sdata = {'to_phone': user.phone, 'message':  body + SMS.postfix }
                    Util.send_sms(sdata)



def get_dependent_models(model_class, in_models = []):
    if model_class != None:
        in_models.append(model_class)
        for related_object in model_class._meta.get_fields(include_hidden=True):
            if related_object.related_model != None and type(related_object).__name__ == "ManyToOneRel":
                if related_object.related_model not in in_models:
                    in_models += get_dependent_models(related_object.related_model, in_models)
                    # in_models.append(related_object.related_model)
                    
    return in_models


def send_counter_push_notification(id, counter, message, type, ref_id, modifiedon):
    firebase_init()
    alltokens=Device.objects.filter(Q(is_active=True) & (Q(socket =None) | Q(socket ='')) & ~Q(fcmtoken ='') & ~Q(fcmtoken =None) &Q(user__is_active=True ) & Q( Q(user__counters=counter) | Q(user__is_superuser = True))).values_list('fcmtoken', flat=True)       
    alltokens_split = [alltokens[i:i+500] for i in range(0, len(alltokens), 500)]
    for i, tokens in enumerate(alltokens_split):
        dataObject= { 'id':str(id), 'message': message,'type': str(type),'ref_id':str(ref_id), 'modifiedon': str(modifiedon) }
        # message = messaging.MulticastMessage(notification=messaging.Notification(title=str(counter),body=message,),data=dataObject,tokens=tokens)
        # response = messaging.send_multicast(message)
    print('successfully sent message', 'response')




def send_master_push_notification(id, message,type, ref_id, modifiedon,subject):
    firebase_init()
    alltokens=Device.objects.filter(Q(is_active=True) & (Q(socket =None) | Q(socket ='')) & ~Q(fcmtoken ='') & ~Q(fcmtoken =None)&Q(user__is_active=True ) & Q(user__is_superuser = True)).values_list('fcmtoken', flat=True)     
    alltokens_split = [alltokens[i:i+500] for i in range(0, len(alltokens), 500)]
    dataObject= { 'id':str(id), 'message': message,'type': str(type),'ref_id':str(ref_id), 'modifiedon': str(modifiedon) }
    # for i, tokens in enumerate(alltokens_split):
    #     # message = messaging.MulticastMessage(notification=messaging.Notification(title=subject,body=message,),data=dataObject,tokens=tokens)
    #     # response = messaging.send_multicast(message)
    print('successfully sent message', 'response')


def send_approval_push_notification(id, message,type, ref_id, modifiedon,subject,devices):
    firebase_init()
    print("only devices",devices)
    alltokens=devices.filter(Q(is_active=True) & (Q(socket =None) | Q(socket ='')) & ~Q(fcmtoken ='') & ~Q(fcmtoken =None)&Q(user__is_active=True ) & Q(user__is_superuser = True) & Q(user__manager__approval__levelno=2)).values_list('fcmtoken', flat=True)    
    print('alltokens',alltokens) 
    alltokens_split = [alltokens[i:i+500] for i in range(0, len(alltokens), 500)]
    dataObject= { 'id':str(id), 'message': message,'type': str(type),'ref_id':str(ref_id), 'modifiedon': str(modifiedon) }
    print(dataObject)
    print("all devices",alltokens)
    # for i, tokens in enumerate(alltokens_split):
    #     # message = messaging.MulticastMessage(notification=messaging.Notification(title=subject,body=message,),data=dataObject,tokens=tokens)
    #     # response = messaging.send_multicast(message)
    print('successfullyy sent message', 'response')
