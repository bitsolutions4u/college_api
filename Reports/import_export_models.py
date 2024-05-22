import os.path
from pyparsing import empty

from rest_framework import serializers
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from Common.permissions import GetPermission
from django.db.models import Q
from Masters import models as Mastermodels


from System.models import Menu,Submenu,Menuitem,Notification,Backup,Attachment
from System.resources import MenuResource,SubmenuResource,MenuitemResource,NotificationResource,BackupResource

from Users.models import User,Device
from Users.resources import UserResource,DeviceResource
from Users.views import UserFilter


only_import_models ={

   
}


only_export_models ={
    


   'User': {
      'model_class': User,
      'resource_class': UserResource,
      'filter_backends': [DjangoFilterBackend, SearchFilter, OrderingFilter],
      'filterset_class': UserFilter,
      'search_fields': [ 'username', 'email', 'phone', 'first_name', 'last_name', 'pincode', 'groups__name' ],
      'ordering_fields': [ 'username',],
      'queryset': User.objects.filter(is_active=True,)

   },


   'Device': {
      'model_class': Device,
      'resource_class': DeviceResource,
      'queryset': Device.objects.filter(status=1,),
   
   },


}


export_import_models ={
   
   # 'District': {
   #    'model_class': Mastermodels.District,
   #    'resource_class': DistrictResource,
   #    'queryset': Mastermodels.District.objects.filter(status=1,),
   #    'filter_backends': [DjangoFilterBackend, SearchFilter, OrderingFilter],
   #    'filterset_class': DistrictFilter,
   #    'search_fields': [ 'code', 'name','state__name' ],
   #    'ordering_fields': ['id', 'code', 'name','state' ]
   # },

  
}

#
# export_models =  export_import_models | only_export_models
# import_models = export_import_models | only_import_models

export_models = export_import_models.update(only_export_models)
import_models = export_import_models.update(only_import_models)