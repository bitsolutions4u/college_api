from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin, GroupAdmin as AuthGroupAdmin

from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportMixin, ExportMixin, ImportExportMixin
from import_export import resources, fields
from import_export.mixins import base_formats
from import_export.fields import Field

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from Users.models import User, Device,Groupdetails,PermissionDetail, ContentTypeDetail, DjangoApp, DeviceLog

from Users.resources import UserResource,DeviceResource, DjangoAppResource, ContentTypeDetailResource, PermissionDetailResource, GroupResource



class ExportMixinAdmin(ExportMixin):

    def get_export_formats(self):
        formats = (
            base_formats.CSV,
          )

        return [f for f in formats if f().can_export()]

    class Meta:
        abstract = True

class ImportMixinAdmin(ImportMixin):

    def get_import_formats(self):
        formats = (
            base_formats.CSV,
          )

        return [f for f in formats if f().can_export()]

    class Meta:
        abstract = True





class UserAdmin( ImportExportMixin,  admin.ModelAdmin):
    resource_class = UserResource
    list_display=('id','username','email','phone', 'otp','first_name','last_name','address', 'state','district','city','area','pincode','deviceaccess',  'is_email_verified','is_phone_verified','is_active','is_staff',  'created_at','updated_at','createdby','modifiedby', )
    fields=( 'first_name','last_name','username','email','phone','password', 'address', 'state','district','city','area','pincode','deviceaccess','is_active','is_staff','groups', 'is_phone_verified', 'is_email_verified')
    ordering=('username','created_at',)
    list_per_page=25



class DeviceResource(resources.ModelResource):
    user = Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, field='username'))
    type = fields.Field(
        attribute='get_type_display',
        column_name=('TYPE')
    )

    class Meta:
        model = Device
        fields=('id','code','user','uuid', 'type','fcmtoken','apntoken','accesstoken','session', 'is_active','createdon','createdby','modifiedon','modifiedby','status')
        

class DeviceAdmin( ImportExportMixin, ImportMixinAdmin, admin.ModelAdmin):
    resource_class = DeviceResource
    fields=('user','name','uuid', 'type','fcmtoken','apntoken','accesstoken','session', 'is_active','socket',)
    list_display=('code','user','name','uuid', 'type','fcmtoken','apntoken', 'is_active','socket','createdon','createdby','modifiedon','modifiedby', )
    search_fields=('code','user__username','name','uuid', 'type',)
    ordering=('code',)
    list_per_page=25


class DeviceLogAdmin( admin.ModelAdmin):
    fields=('device', 'user','ip_address','login','logout')
    list_display=('id', 'device', 'user','ip_address','login','logout','createdon','createdby','modifiedon','modifiedby', )
    search_fields=('user__username','device','ip_address', 'login',)
    # ordering=('id',)





class GroupdetailsAdmin(admin.ModelAdmin):
    list_display = ('group','reportingto', 'static',)
    fields = ('group','reportingto', 'static',)
    ordering=('id',)



class UserAddressVersionAdmin(admin.ModelAdmin):
    list_display = ('code','user','address', 'area','city','district','state','pincode','createdon','createdby','modifiedon','modifiedby')
    fields = ('code','user','address', 'area','city','district','state','pincode',)
    ordering=('id',)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name','content_type','codename',)
    fields = ('name','content_type','codename',)
    search_fields= ('name',"content_type__app_label", "content_type__model",'codename',)
    ordering=("content_type__app_label", "content_type__model", "codename",)

class PermissionDetailAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = PermissionDetailResource

    list_display = ('name','permission','hide',)
    fields = ('name','permission','hide',)
    search_fields=('name','permission__content_type__app_label','permission__content_type__model','hide',)
    ordering=('id',)


class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ('app_label','model')
    fields = ('app_label','model')
    ordering=('app_label',)


class ContentTypeDetailAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = ContentTypeDetailResource

    list_display = ('name','contenttype', 'app', 'hide',)
    fields = ('name','contenttype','app', 'hide',)
    ordering=('id',)


class DjangoAppAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = DjangoAppResource

    list_display = ('name','app_label', 'hide',)
    fields = ('name','app_label', 'hide',)
    readonly_fields =('app_label',)
    ordering=('id',)


class GroupAdmin(ImportExportMixin, AuthGroupAdmin):
    resource_class = GroupResource

    # list_display = ('id', 'name',)
    # fields = ( 'name', 'permissions', )
    # ordering=('id',)


admin.site.register(User, UserAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceLog, DeviceLogAdmin)
admin.site.register(Groupdetails, GroupdetailsAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(PermissionDetail, PermissionDetailAdmin)
admin.site.register(ContentType, ContentTypeAdmin)
admin.site.register(ContentTypeDetail, ContentTypeDetailAdmin)
admin.site.register(DjangoApp, DjangoAppAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)



