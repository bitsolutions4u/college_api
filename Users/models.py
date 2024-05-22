from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, Permission 
from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.utils import timezone
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
import datetime
from Common.utils import getcode





class UserManager(BaseUserManager):

    def create_user(self, username, password=None, **kwargs):
        if username is None:
            raise TypeError('Users should have a username')
    
        user = self.model(**kwargs, username=username, )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username,  password=None, **kwargs):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user



DEVICEACCESS_CHOICES = (
   (1, 'Only Mobile'),
   (2, 'Only Web'),
   (3, 'Both'),
  
)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, db_index=True, blank=True, null=True)
    phone = models.CharField(max_length=15, db_index=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    first_name = models.CharField( max_length=150, blank=True)
    last_name = models.CharField( max_length=150, blank=True)
    country = models.ForeignKey('Masters.Country', related_name='users', on_delete=models.RESTRICT, null=True, blank=True)
    state = models.ForeignKey('Masters.State', related_name='users', on_delete=models.RESTRICT, null=True, blank=True)
    district = models.ForeignKey('Masters.District', related_name='users', on_delete=models.RESTRICT, null=True, blank=True)
    city = models.ForeignKey('Masters.City', related_name='users', on_delete=models.RESTRICT, null=True, blank=True)
    area = models.ForeignKey('Masters.Area', related_name='users', on_delete=models.RESTRICT, null=True, blank=True)
    deviceaccess = models.SmallIntegerField( choices= DEVICEACCESS_CHOICES, blank=True, null=True, default=1,)
    address = models.TextField(blank=True, null=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_branch = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    created_at = models.DateTimeField(default= datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_created_by', on_delete=models.RESTRICT, null=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_modified_by', on_delete=models.RESTRICT,  null=True)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    # def findRole(self):
    #     if self.is_superuser:
    #         return 'Admin'
    #     elif self.is_staff:
    #         return 'Student'

class Device(models.Model):
    ANDROID = 1
    IOS = 2
    WEB = 3
    
    DEVICETYPE_CHOICES = (
        ( ANDROID, 'Android'),
        ( IOS, 'iOS'),
        ( WEB, 'Web'),
    )

    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    uuid = models.TextField(default='', blank=True, null=True)
    type = models.SmallIntegerField( choices= DEVICETYPE_CHOICES, blank=True, null=True, default=1,)
    fcmtoken = models.TextField(default='', blank=True, null=True)
    apntoken = models.TextField(default='', blank=True, null=True)
    accesstoken = models.TextField(default='', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='devices', on_delete=models.RESTRICT, null=True)
    session = models.TextField(default='', blank=True, null=True)
    socket = models.CharField(max_length=30, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='devicescreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='devicesupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)
    
    def save(self, *args, **kwargs):
        if self.id is None and (self.code == "" or self.code == None):
            self.code = getcode(Device,'DEV')
        super(Device, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.code)

class DeviceLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='devicelogins', on_delete=models.RESTRICT, null=True)
    device = models.ForeignKey(Device, related_name='devicelogs', on_delete=models.RESTRICT, null=True, blank=True)
    ip_address = models.GenericIPAddressField( null=True, blank=True)
    login = models.DateTimeField(auto_now_add=True, blank=True)
    logout = models.DateTimeField( null=True, blank=True)
    createdon = models.DateTimeField(auto_now_add=True, blank=True)
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='devicelogscreated', on_delete=models.RESTRICT, null=True)
    modifiedon = models.DateTimeField(blank=True, null=True, auto_now=True)
    modifiedby = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='devicelogsupdated', on_delete=models.RESTRICT,  null=True)
    status = models.SmallIntegerField(default=1, null=True)
    
    def save(self, *args, **kwargs):
        super(DeviceLog, self).save(*args, **kwargs)



class Groupdetails(models.Model):
    group = models.OneToOneField(Group, related_name='groupdetails', on_delete=models.CASCADE,  null=True)
    reportingto =  models.ForeignKey(Group, related_name='reportingby', on_delete=models.RESTRICT,  null=True)
    static = models.BooleanField(default=False)

    def __str__(self):
        return self.group.name+" details"


class DjangoApp(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    app_label = models.CharField(max_length=100, unique=True, null=True, blank=True)
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ContentTypeDetail(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True) # name of the model
    contenttype = models.OneToOneField(ContentType, related_name='contenttypedetails', on_delete=models.CASCADE,  null=True)
    app =  models.ForeignKey(DjangoApp, related_name='contenttypedetails', on_delete=models.RESTRICT,  null=True)
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PermissionDetail(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True) # name of the permission
    permission = models.OneToOneField(Permission, related_name='permissiondetails', on_delete=models.CASCADE,  null=True)
    hide = models.BooleanField(default=False)

    def __str__(self):
        return self.name
