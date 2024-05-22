import re

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import datetime


from django.db.models import Q, Sum, Count

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError

from Users.models import DjangoApp, ContentTypeDetail, PermissionDetail

class Command(BaseCommand):
    help = 'Closes out_time that have NO end time'
    
    def handle(self, *args, **options):
        
        self.stdout.write(self.style.SUCCESS('Successfully closed the timesheet'))

    





# python manage.py AutoOutTime