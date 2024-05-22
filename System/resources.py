from datetime import datetime,timedelta
from import_export import resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget, DateWidget, DateTimeWidget,BooleanWidget
from import_export.mixins import base_formats
from import_export.fields import Field
from .models import Menu,Submenu,Menuitem,Notification,Backup,Attachment, Formula, ActivityLog, NotificationUsers, Restore, FormulaVariables, FormulaUpdate
from Users.models import Permission
from django.contrib.auth import get_user_model
User = get_user_model()
from Common.Imports_Exports import ModelImportExportResource, PermissionCodeWidget




class MenuResource(ModelImportExportResource):
    code = Field(column_name='Code', attribute='code', )
    name = Field(column_name='Name', attribute='name', )
    createdon = Field(column_name='Created On', attribute='createdon',widget=DateTimeWidget())
    modifiedon = Field(column_name='Modified On', attribute='modifiedon',widget=DateTimeWidget())
    createdby = Field(column_name='Created By', attribute='createdby', widget=ForeignKeyWidget(User, field='username'))
    modifiedby = Field(column_name='Modified By', attribute='modifiedby', widget=ForeignKeyWidget(User, field='username'))


    class Meta:
        model = Menu
        fields = ('code', 'name', 'createdby', 'createdon', 'modifiedby', 'modifiedon')
        export_order =('code', 'name', 'createdby', 'createdon', 'modifiedby', 'modifiedon')
        import_id_fields = ('code',)



class SubmenuResource(ModelImportExportResource):
    code = Field(column_name='Code', attribute='code', )
    name = Field(column_name='Name', attribute='name', )
    sequence = Field(column_name='Sequence', attribute='sequence', )
    icon = Field(column_name='Icon', attribute='icon', )
    click = Field(column_name='Click', attribute='click', )
    menu = Field(column_name='Menu', attribute='menu', widget=ForeignKeyWidget(Menu, field='code'))
    submenu = Field(column_name='Submenu', attribute='submenu', widget=ForeignKeyWidget(Submenu, field='code'))
    createdon = Field(column_name='Created On', attribute='createdon',widget=DateTimeWidget())
    modifiedon = Field(column_name='Modified On', attribute='modifiedon',widget=DateTimeWidget())
    createdby = Field(column_name='Created By', attribute='createdby', widget=ForeignKeyWidget(User, field='username'))
    modifiedby = Field(column_name='Modified By', attribute='modifiedby', widget=ForeignKeyWidget(User, field='username'))
    

    class Meta:
        model = Submenu
        fields = ('code', 'name', 'sequence', 'icon', 'click', 'menu', 'submenu', 'createdby', 'createdon', 'modifiedby', 'modifiedon')
        export_order =('code', 'name', 'sequence', 'icon', 'click', 'menu', 'submenu', 'createdby', 'createdon', 'modifiedby', 'modifiedon')
        import_id_fields = ('code',)



class MenuitemResource(ModelImportExportResource):
    code = Field(column_name='Code', attribute='code', )
    title = Field(column_name='Title', attribute='title', )
    icon = Field(column_name='Icon', attribute='icon', )
    link = Field(column_name='Link', attribute='link', )
    sequence = Field(column_name='Sequence', attribute='sequence', )
    click = Field(column_name='Click', attribute='click', )
    menu = Field(column_name='Menu', attribute='menu', widget=ForeignKeyWidget(Menu, field='code'))
    submenu = Field(column_name='Submenu', attribute='submenu', widget=ForeignKeyWidget(Submenu, field='code'))
    permission = Field(column_name='Permission', attribute='permission', widget=PermissionCodeWidget(Permission,))
    # permission = Field(column_name='Permission', attribute='permission', widget=ForeignKeyWidget(Permission, field='codename'))

    createdon = Field(column_name='Created On', attribute='createdon',widget=DateTimeWidget())
    modifiedon = Field(column_name='Modified On', attribute='modifiedon',widget=DateTimeWidget())
    createdby = Field(column_name='Created By', attribute='createdby', widget=ForeignKeyWidget(User, field='username'))
    modifiedby = Field(column_name='Modified By', attribute='modifiedby', widget=ForeignKeyWidget(User, field='username'))
    # permission = Field()
    
    # def dehydrate_permission(self, Menuitem):
    #     # print("dehydrate......",Menuitem)
    #     if Menuitem.permission:
    #         return '%s.%s' % (Menuitem.permission.content_type.app_label, Menuitem.permission.codename)
    #     else:
    #         ''

    class Meta:
        model = Menuitem
        fields = ('code', 'title', 'icon', 'link', 'sequence', 'click', 'menu', 'submenu', 'permission',)
        export_order =('code', 'title', 'icon', 'link', 'sequence', 'click', 'menu', 'submenu', 'permission', )
        import_id_fields = ('code',)





class NotificationResource(resources.ModelResource):

    class Meta:
        model = Notification
        fields = ('id', 'subject', 'body', 'type','ref',)

class NotificationUsersResource(resources.ModelResource):

    class Meta:
        model = NotificationUsers
        fields = ('id','user','body','notification','seen','seen_time','status')



class BackupResource(resources.ModelResource):

    class Meta:
        model = Backup
        fields = ( 'id', 'code', 'name','createdby__username','modifiedby__username')


class RestoreResource(resources.ModelResource):

    class Meta:
        model = Restore
        fields = ( 'id', 'code', 'name','createdby__username','modifiedby__username')



class FormulaResource(ModelImportExportResource):
    code = Field(column_name='Code', attribute='code', )
    name = Field(column_name='Name', attribute='name', )
    formula = Field(column_name='Formula', attribute='formula', )
    createdon = Field(column_name='Created On', attribute='createdon',widget=DateTimeWidget())
    modifiedon = Field(column_name='Modified On', attribute='modifiedon',widget=DateTimeWidget())
    createdby = Field(column_name='Created By', attribute='createdby', widget=ForeignKeyWidget(User, field='username'))
    modifiedby = Field(column_name='Modified By', attribute='modifiedby', widget=ForeignKeyWidget(User, field='username'))

    class Meta:
        model = Formula
        fields = ( 'id', 'code', 'name','formula', 'createdby','createdon','modifiedby','modifiedon')
        export_order =('code', 'name','formula', 'createdby','createdon','modifiedby','modifiedon')
        import_id_fields = ('code',)



class FormulaVariablesResource(ModelImportExportResource):
    id = Field(column_name='Id', attribute='id', )
    name = Field(column_name='Name', attribute='name', )
    description = Field(column_name='Description', attribute='description', )
    active = Field(column_name='Active', attribute='active',widget=BooleanWidget())
    formula = Field(column_name='Formula', attribute='formula', widget=ForeignKeyWidget(Formula, field='code') )

    class Meta:
        model = FormulaVariables
        fields = ( 'id', 'name','description', 'active','formula')
        export_order =( 'id', 'name','description', 'active','formula')
        import_id_fields = ('id',)


class FormulaUpdateResource(ModelImportExportResource):
    id = Field(column_name='Id', attribute='id', )
    formula_txt = Field(column_name='Formula Txt', attribute='formula_txt', )
    formula = Field(column_name='Formula', attribute='formula', widget=ForeignKeyWidget(Formula, field='code') )
    createdon = Field(column_name='Created On', attribute='createdon',widget=DateTimeWidget())
    createdby = Field(column_name='Created By', attribute='createdby', widget=ForeignKeyWidget(User, field='username'))

    class Meta:
        model = FormulaUpdate
        fields = ( 'id', 'formula', 'formula_txt','createdby','createdon',)
        export_order =( 'id', 'formula', 'formula_txt','createdby','createdon',)
        import_id_fields = ('id',)
        

class ActivityLogResource(resources.ModelResource):

    class Meta:
        model = ActivityLog
        fields = ( 'id', 'type', 'tablename', 'recordcode' , 'user__username')