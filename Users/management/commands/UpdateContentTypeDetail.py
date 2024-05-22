import re

from django.core.management.base import BaseCommand
from django.utils import timezone


from django.db.models import Q, Sum, Count

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

from Users.models import DjangoApp, ContentTypeDetail, PermissionDetail



class Command(BaseCommand):
    help = 'Updating ContentTypeDetail Data from ContentType Data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Update ContentTypeDetail Started")
        contenttypelist =ContentType.objects.all().select_related('contenttypedetails').annotate(n_details=Count('contenttypedetails')).filter(n_details=0)
        for contenttype in contenttypelist:
            appnamechunks = re.findall('[A-Z][^A-Z]*',  contenttype.app_label)
            appname = ' '.join(appnamechunks) if len(appnamechunks) > 1 else contenttype.app_label
            modelname = contenttype.model.capitalize()

            app, ac = DjangoApp.objects.get_or_create(app_label=contenttype.app_label, defaults={ 'name': appname, } )
            
            permission_r, pc_r = Permission.objects.get_or_create(codename="reports_" + contenttype.model, defaults={ 'name': "Can Report " + contenttype.name, 'content_type' : contenttype } )
            permission_e, pc_e = Permission.objects.get_or_create(codename="export_" + contenttype.model, defaults={ 'name': "Can Export " + contenttype.name, 'content_type' : contenttype } )
            permission_i, pc_i = Permission.objects.get_or_create(codename="import_" + contenttype.model, defaults={ 'name': "Can Import " + contenttype.name, 'content_type' : contenttype } )
            
            ContentTypeDetail.objects.create(contenttype=contenttype, name= modelname, app=app )

       
        self.stdout.write("Updating ContentTypeDetail Ended")

# python manage.py UpdateContentTypeDetail