
import os
from django.db.models import Q
from dynamic_preferences.registries import global_preferences_registry 
from Users.models import Device, User

from Common.utils import Util



def send_counter_notification( id, counter, message, type, ref_id, modifiedon):

    try:
        devices=Device.objects.filter(Q(is_active=True) & ~Q( socket =None) & ~Q( socket ='') & Q(user__is_active=True ) & Q( Q(user__counters=counter) | Q(user__is_superuser = True)))
        for device in devices:
            sid = device.socket
            Util.send_live_notification('send_notification',  { 
                'sid':sid,
                'payload': { 'id':id, 'message': message,'type': type,'ref_id':ref_id, 'modifiedon': str(modifiedon) }}, )
        
    
    except:
        print('failed counter notification')




def send_master_notification( id, message, type, ref_id, modifiedon):

    try:
        devices=Device.objects.filter(Q(is_active=True) & ~Q( socket =None) & ~Q( socket ='') & Q(user__is_active=True ) & Q(user__is_superuser = True))
        for device in devices:
            sid = device.socket
            Util.send_live_notification('send_notification',  {
                'sid':sid,
                'payload': { 'id':id, 'message': message,'type': type,'ref_id':ref_id, 'modifiedon': str(modifiedon) },}  )

    except:
        print('failed master notification')


def send_approval_notification( id, message, type, ref_id, modifiedon, devices):

    try:
        devices=devices.filter(Q(is_active=True) & ~Q( socket =None) & ~Q( socket ='') & Q(user__is_active=True ))
        for device in devices:
            sid = device.socket
            Util.send_live_notification('send_notification',  {
                'sid':sid,
                'payload': { 'id':id, 'message': message,'type': type,'ref_id':ref_id, 'modifiedon': str(modifiedon) },}  )

    except:
        print('failed master notification')

def maintenance_mode(status, user = None):

    try:
        if user==None:
            devices=Device.objects.filter(Q(is_active=True) & ~Q( socket =None) & ~Q( socket ='') & Q(user__is_active=True ) & Q(user__is_superuser = False ))
        else:
            devices=Device.objects.filter(Q(is_active=True) & ~Q( socket =None) & ~Q( socket ='') & Q(user__is_active=True ) & Q(user__is_superuser = False ) & Q(user = user))
        for device in devices:
            sid = device.socket
            Util.send_live_notification('update_maintenance_mode',  {
                'sid':sid,
                'payload': {'maintenance_mode_status': status}}  )

    except:
        print('failed to update maintenance_mode')

def auto_reload( id, type, ref_id, devices):

    try:
        devices=devices.filter(Q(is_active=True) & ~Q( socket =None) & ~Q( socket ='') & Q(user__is_active=True ))
        for device in devices:
            sid = device.socket
            Util.send_live_notification('auto_reload',  {
                'sid':sid,
                'payload': { 'id':id, 'type': type,'ref_id':ref_id, },}  )

    except:
        print('failed auto_reload notification')



