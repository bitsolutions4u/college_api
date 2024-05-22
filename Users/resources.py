from datetime import datetime,timedelta
from import_export import resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget, DateWidget, BooleanWidget, DateTimeWidget, DecimalWidget
from import_export.mixins import base_formats
from import_export.fields import Field
from django.contrib.auth import get_user_model
User = get_user_model()
from Users.models import Device,DeviceLog,Groupdetails,DjangoApp,ContentTypeDetail,PermissionDetail,DEVICEACCESS_CHOICES
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from Common.Imports_Exports import ModelImportExportResource, ChoicesWidget
from Masters.models import *

from Common.Imports_Exports import ModelImportExportResource, PermissionCodeWidget
from django.contrib.auth.models import Group, Permission 








class UserResource(ModelImportExportResource):
    username = Field(column_name='User Name', attribute='username',)
    email = Field(column_name='Email', attribute='email', )
    phone = Field(column_name='Phone', attribute='phone', )
    otp = Field(column_name='Otp', attribute='otp', )
    first_name = Field(column_name='First Name', attribute='first_name', )
    last_name = Field(column_name='Last Name', attribute='last_name', )
    Role = Field()
    area = Field(column_name='Area', attribute='area', widget=ForeignKeyWidget(Area, field='name'))
    area_code = Field(column_name='Area Code', attribute='area', widget=ForeignKeyWidget(Area, field='code'))
    city = Field(column_name='City', attribute='city', widget=ForeignKeyWidget(City, field='name'))
    city_code = Field(column_name='City Code', attribute='city', widget=ForeignKeyWidget(City, field='code'))
    district = Field(column_name='District', attribute='district', widget=ForeignKeyWidget(District, field='name'))
    district_code = Field(column_name='District Code', attribute='district', widget=ForeignKeyWidget(District, field='code'))
    state = Field(column_name='State', attribute='state', widget=ForeignKeyWidget(State, field='name'))
    state_code = Field(column_name='State Code', attribute='state', widget=ForeignKeyWidget(State, field='code'))
    deviceaccess = Field(column_name='Device Access', attribute='deviceaccess', widget = ChoicesWidget(DEVICEACCESS_CHOICES))
    address = Field(column_name='Address', attribute='address', )
    pincode = Field(column_name='Pincode', attribute='pincode', )
    is_email_verified = Field(column_name='Is Email Verified', attribute='is_email_verified', widget=BooleanWidget())
    is_phone_verified = Field(column_name='Is Phone Verified', attribute='is_phone_verified', widget=BooleanWidget())
    is_employee = Field(column_name='Is Employee', attribute='is_employee', widget=BooleanWidget())
    is_dealer = Field(column_name='Is Dealer', attribute='is_dealer', widget=BooleanWidget())
    is_active = Field(column_name='Is Active', attribute='is_active', widget=BooleanWidget())
    is_staff = Field(column_name='Is Staff', attribute='is_staff', widget=BooleanWidget())
    # created_at = Field(column_name='Created At', attribute='created_at',widget=DateTimeWidget())
    # updated_at = Field(column_name='Updated At', attribute='updated_at',widget=DateTimeWidget())
    createdby = Field(column_name='Created By', attribute='createdby', widget=ForeignKeyWidget(User, field='username'))
    modifiedby = Field(column_name='Modified By', attribute='modifiedby', widget=ForeignKeyWidget(User, field='username'))

    class Meta:
        model = User
        fields = ('username','email','phone','otp','first_name','last_name','area','area_code','city','city_code','district','district_code','state','state_code','deviceaccess','address','pincode', 'is_email_verified','is_phone_verified','is_employee','is_dealer','is_active','is_staff','created_at','updated_at','createdby','modifiedby')
        import_fields = ( 'username','email','phone','otp','first_name','last_name','area_code','city_code','district_code','state_code','deviceaccess','address','pincode', 'is_email_verified','is_phone_verified','is_employee','is_dealer','is_active','is_staff','createdby','modifiedby')
        export_order = ( 'username','email','phone','otp','first_name','last_name','Role','area','area_code','city','city_code','district','district_code','state','state_code','deviceaccess','address','pincode', 'is_email_verified','is_phone_verified','is_employee','is_dealer','is_active','is_staff','createdby','modifiedby')
        import_id_fields = ('username', )
    
    def dehydrate_Role(self, obj):
        groups = obj.groups.all().values_list('name', flat=True)
        return ",".join(groups)


class DeviceResource(resources.ModelResource):

    class Meta:
        model = Device
        fields = ( 'id', 'code', 'name','uuid','type','fcmtoken','apntoken','accesstoken','session', 'user__username','is_active', 'createdby__username','modifiedby__username')



class DeviceLogResource(resources.ModelResource):

    class Meta:
        model = DeviceLog
        fields = ( 'id', 'user__username', 'device__name','ip_address','login','logout', 'createdby__username','modifiedby__username')





class DjangoAppResource(ModelImportExportResource):
    name = Field(column_name='Name', attribute='name', )
    app_label = Field(column_name='App_Label', attribute='app_label', )
    hide = Field(column_name='Hide', attribute='hide', widget=BooleanWidget())


    class Meta:
        model = DjangoApp
        fields = ( 'name','app_label','hide')
        export_order =('name','app_label','hide')
        import_id_fields = ('app_label',)


class ContentTypeDetailResource(ModelImportExportResource):
    name = Field(column_name='Name', attribute='name', )
    contenttype = Field(column_name='ContentType', attribute='contenttype', widget=ForeignKeyWidget(ContentType, field='model'))
    app = Field(column_name='App', attribute='app', widget=ForeignKeyWidget(DjangoApp, field='app_label'))
    hide = Field(column_name='Hide', attribute='hide', widget=BooleanWidget())


    class Meta:
        model = ContentTypeDetail
        fields = ( 'name', 'contenttype', 'app', 'hide')
        export_order =('name', 'contenttype', 'app', 'hide')
        import_id_fields = ('contenttype',)


class PermissionDetailResource(ModelImportExportResource):
    name = Field(column_name='Name', attribute='name', )
    permission = Field(column_name='Permission', attribute='permission', widget=PermissionCodeWidget(Permission, ))
    hide = Field(column_name='Hide', attribute='hide', widget=BooleanWidget())


    class Meta:
        model = PermissionDetail
        fields = ( 'name', 'permission', 'hide')
        export_order =('name', 'permission', 'hide')
        import_id_fields = ('permission',)


class GroupResource(ModelImportExportResource):
    name = Field(column_name='Name', attribute='name', )
    permission = Field(column_name='Permission', attribute='permission', widget=PermissionCodeWidget(Permission, ))
    locationtype = Field(column_name='Location Type', attribute='locationtype', )
    reportingto_id = Field(column_name='Reportingto Id', attribute='reportingto_id', )


    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions','locationtype','reportingto_id',)
        export_order =('id', 'name', 'permissions','locationtype','reportingto_id',)


