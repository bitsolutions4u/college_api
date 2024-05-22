import os, zipfile, pathlib, shutil
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .models import *

from django import forms
from django.contrib import messages
from import_export.admin import ImportMixin, ExportMixin, ImportExportMixin
from import_export.mixins import base_formats
from django.urls import path
from django.utils.html import format_html
from django.urls import reverse
from .views import *
from django.shortcuts import render

from System.resources import MenuResource,SubmenuResource,MenuitemResource,NotificationResource,BackupResource, FormulaResource, ActivityLogResource, NotificationUsersResource
from System.menudata import export_menu_data, import_menu_data
from System.formuladata import export_formula_data, import_formula_data
from System.views import CreateBackup

from System.views import Maintenance_On, Maintenance_Off
from Common.storage_backends import DBBackupMediaStorage

from dynamic_preferences.registries import global_preferences_registry 

# Register your models here.

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




class MenuAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = MenuResource

    fields=('code','name')
    list_display=('id','code','name',  'createdon', 'createdby', 'modifiedon', 'modifiedby', 'status')
    list_display_links=None
    list_filter=('createdon',)
    search_fields=('code',)
    list_per_page=5
    ordering=('-code',)
    list_editable= ['code']

    # date_hierarchy='createdon'
    # empty_value_display = 'unknown'

    def get_queryset(self, request):
        queryset= super(MenuAdmin,self).get_queryset(request)
        queryset=queryset.order_by('-code',)
        return queryset



    
    # def get_queryset(self,request):
    #     user = request.user
    #     if user.is_superuser:
    #         queryset = Menu.objects.filter(status=1, )
    #     else:
    #         queryset = Menu.objects.filter(createdby = user, status=1 )
            
    #     return queryset.order_by('-id')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()



    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['show_save_and_continue'] = False
    #     extra_context['show_save'] = False
    #     extra_context['show_delete']=False
        
    #     return super(MenuAdmin, self).changeform_view(request, object_id, extra_context=extra_context)




    def view(self,obj):
        url = f'/admin/Invoice/invoice/view/{obj.id}'
        opensrt = f"window.open({url},'Invoiceview','width=600,height=400')"
        return format_html('<a href="{url}" target="popup" onclick="{opensrt}">View</a>', opensrt=opensrt, url=url)




    # def get_urls(self):
    #     urls = super().get_urls()
    #     my_urls = [
    #         path(r'view/<int:id>', self.view),
    #     ]
    #     return my_urls + urls




    # change_list_template = "initialdata.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
                path('export_menu_data/', self.set_menu_Data),
                path('import_menu_data/', self.Import_menu_data),
                path('ResetDatabase/', self.set_ResetDatabase),
                ]
        return my_urls + urls


    def set_ResetDatabase(self,request):
        dataset={}
        models=[]
        obj=ContentType.objects.all()
        for model in obj:
            dataset[model.id]=model.model
        return render(request, 'checkboxes.html', {'dataset':dataset})
      
    def set_menu_Data(self, request):
        print("export menu data")
        export_menu_data()

        return HttpResponseRedirect("../")

    def Import_menu_data(self, request):
        print("import menu data")    
        import_menu_data()     
        return HttpResponseRedirect("../")

    
		
	



class SubmenuAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = SubmenuResource

    fields=('code','name','sequence','menu', 'icon', 'click', 'submenu',)
    list_display=('code','name','sequence','menu', 'icon', 'click', 'submenu','createdon', 'createdby', 'modifiedon', 'modifiedby', 'status')
    # list_display_links=None
    list_filter=('createdon',)
    search_fields=('code',)
    list_per_page=5
    ordering=('-code',)
    # date_hierarchy='createdon'
    empty_value_display = 'unknown'

    def get_queryset(self, request):
        queryset= super(SubmenuAdmin,self).get_queryset(request)
        queryset=queryset.order_by('-code',)
        return queryset

    # def get_queryset(self,request):
    #     user = request.user
    #     if user.is_superuser:
    #         queryset = Submenu.objects.filter(status=1, )
    #     else:
    #         queryset = Submenu.objects.filter(createdby = user, status=1 )
            
    #     return queryset.order_by('-id')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()



    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['show_save_and_continue'] = False
    #     extra_context['show_save'] = False
    #     extra_context['show_delete']=False
        
    #     return super(SubmenuAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

    




class MenuitemAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = MenuitemResource

    fields=('code','title','icon','link','sequence','menu','submenu','click','permission','status')
    list_display=( 'code','title','icon','link','sequence','menu','submenu','click','permission','createdon', 'createdby', 'modifiedon', 'modifiedby', 'status')
    list_editable= ['sequence']
    list_filter=('menu','submenu')
    search_fields=('code','title',)
   

class NotificationAdmin(ImportExportMixin,  admin.ModelAdmin):
    resource_class = NotificationResource

    fields=('subject','body','type','ref',)
    list_display=('id','subject','body','type','ref', 'createdon')


class NotificationUsersAdmin(ImportExportMixin,  admin.ModelAdmin):
    resource_class = NotificationUsersResource

    fields=('user','notification','seen','seen_time',)
    list_display=('id','user','notification','seen','seen_time','status')



class BackupAdmin(ImportExportMixin,  admin.ModelAdmin):
    resource_class = BackupResource

    fields=('code','name')
    list_display=('code','name',  'createdon', 'createdby', 'modifiedon', 'modifiedby', 'status', 'RESTORE')
    list_display_links=['RESTORE']
    list_filter=('createdon',)
    search_fields=('code',)
    list_per_page=5
    ordering=('-code',)
    # date_hierarchy='createdon'
    empty_value_display = 'unknown'


    def get_queryset(self, request):
        queryset= super(BackupAdmin,self).get_queryset(request)
        queryset=queryset.order_by('-code',)
        return queryset

    def get_queryset(self,request):
        user = request.user
        if user.is_superuser:
            queryset = Backup.objects.filter(status=1, )
        else:
            queryset = Backup.objects.filter(createdby = user, status=1 )
            
        return queryset.order_by('-id')

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            instance.user = request.user
            instance.save()
        formset.save_m2m()
    
    def save_model(self, request, obj, form, change):
        obj.createdby = request.user
        obj.modifiedby = request.user
        obj.save()


    # def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['show_save_and_continue'] = False
    #     extra_context['show_save'] = False
    #     extra_context['show_delete']=False
        
    #     return super(BackupAdmin, self).changeform_view(request, object_id, extra_context=extra_context)

    global_preferences = global_preferences_registry.manager()
        
    def set_Maintainence_On(self, request):
        global_preferences['DEVLOPER__MAINTENANCEMODE'] = True
        # maintenance_mode(True)
        # Otokens=OutstandingToken.objects.exclude(user__is_superuser = True)
        # for Otoken in Otokens:
        #     try:
        #         RefreshToken(Otoken.token).blacklist()
        #     # except:
        #     #     print("RefreshToken")
        #     except Exception as e:
        #         print("%s : %s " % (type(e).__name__, e, ))
        #         pass

        return HttpResponseRedirect("../")

    def set_Maintainence_Off(self, request):
        global_preferences['DEVLOPER__MAINTENANCEMODE'] = False 
        return HttpResponseRedirect("../")

    def set_Databackup(self,request):
        CreateBackup(request.user)
        self.message_user(request, "Success")
        return HttpResponseRedirect("../")
    
    def RESTORE(self,queryset):
        url = f'/system/RestoreById/{queryset.id}'
        return format_html(f'<a href="{url}"> RESTORE</a>')


    change_list_template = "backup.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
                path('UploadBackupFile/', self.UploadBackupFile),
                path('Databackup/', self.set_Databackup),
                path('maintainence_on/', self.set_Maintainence_On),
                path('maintainence_off/', self.set_Maintainence_Off),

                path('upload_release_file/', self.upload_release_file,name='upload_release_file'),
                ]
        return my_urls + urls


    def UploadBackupFile(self, request, obj=None, **kwargs):
        print("UploadBackupFile")
        file_obj = request.FILES.get('file',None)
        print(file_obj,type(file_obj),request.POST, kwargs)
        # do your validation here e.g. file size/type check
        if file_obj !=None:
            # organize a path for the file in bucket
            file_directory_within_bucket =  settings.AWS_DBBACKUP_MEDIA_LOCATION

            # synthesize a full file path; note that we included the filename
            file_path_within_bucket = os.path.join(
                file_directory_within_bucket,
                file_obj.name
            )

            media_storage = DBBackupMediaStorage()
            if not media_storage.exists(file_path_within_bucket): # avoid overwriting existing file
                media_storage.save(file_path_within_bucket, file_obj)
                file_url = media_storage.url(file_path_within_bucket)

                serializer = BackupSerializer(data={ "name": file_obj.name, })
                if serializer.is_valid(raise_exception=True):
                    serializer.save(createdby=request.user)

                messages.success(request, 'file uploaded successfully .')
                return HttpResponseRedirect("../")
            
            else:
                messages.error(request, 'Filename already exits, please change the filename and try again')
                return HttpResponseRedirect("../")
        
            
        else:
            messages.error(request, 'File not exits')
            return HttpResponseRedirect("../")

    class FileUploadForm(forms.Form):
        release_file = forms.FileField(required=False, label="Please select a Release file")

    def changelist_view(self, *args, **kwargs):
        view = super().changelist_view(*args, **kwargs)
        view.context_data['file_upload_form'] = self.FileUploadForm
        return view

    def upload_release_file(self, request):
        file_obj = request.FILES.get('release_file',None)
        basepath = settings.BASE_DIR
        buildpath = os.path.join(settings.BASE_DIR, 'build')
        # try:
        # pathlib.Path(buildpath).rmdir()
        shutil.rmtree(buildpath)
        os.mkdir(buildpath)
        # except:
        #     pass
        
        print(file_obj,type(file_obj),request.POST)
        if file_obj !=None:
            #  and file_obj.extension == ".zip"
            zfobj = zipfile.ZipFile(file_obj)
            for name in zfobj.namelist():
                if name.endswith('/'):
                    try: # Don't try to create a directory if exists
                        os.mkdir(os.path.join(basepath, name))
                    except:
                        pass
                else:
                    outfile = open(os.path.join(basepath, name), 'wb')
                    outfile.write(zfobj.read(name))
                    outfile.close()
            
            management.call_command('collectstatic', '--clear', '--noinput')
            messages.success(request, 'Release Unzipped Successfully.')
            return HttpResponseRedirect("../")
        else:
            messages.error(request, 'Zip File not exits')
            return HttpResponseRedirect("../")

class AttachmentAdmin(admin.ModelAdmin):
    fields=('file',)
    list_display=('id', 'file','createdon', 'createdby')




class FormulaAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = FormulaResource

    fields=('code','name','formula',)
    list_display=('id','code','name','formula','createdon', 'createdby','status')


    change_list_template = "formuladata.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
                path('export_formula_data/', self.set_Formula_Data),
                path('import_formula_data/', self.Import_Formula_Data),
                ]
        return my_urls + urls
        
        
    def set_Formula_Data(self, request):
        print("export formula data")
        export_formula_data()        
        return HttpResponseRedirect("../")

    def Import_Formula_Data(self, request):
        print("import formula data")   
        import_formula_data()      
        return HttpResponseRedirect("../")




class ActivityLogAdmin(admin.ModelAdmin):
    resource_class = ActivityLogResource

    fields=( 'user', 'tablename', 'type', 'recordcode', )
    list_display=('id', 'user', 'tablename', 'type', 'recordcode', 'createdon','status')


class FormulaVariablesAdmin(admin.ModelAdmin):
  
    list_display=('id', 'name','description','active','formula','status')
    fields=( 'name','description','active', )


class ErrorAdmin(ImportExportMixin,  admin.ModelAdmin):

    # fields=('errorcode', 'requestbody','error_url')
    list_display=('id', 'errorcode', 'requestbody', 'error_url' )
    
    
class TemporaryVerificationAdmin(ImportExportMixin,  admin.ModelAdmin):

    # fields=('errorcode', 'requestbody','error_url')
    list_display=('id', 'mobile', 'otp', 'is_phone_verified', 'createdon' )


admin.site.register(Menu,MenuAdmin)
admin.site.register(Submenu,SubmenuAdmin)
admin.site.register(Menuitem,MenuitemAdmin)
admin.site.register(NotificationUsers,NotificationUsersAdmin)
admin.site.register(Notification,NotificationAdmin)
admin.site.register(Backup,BackupAdmin)
admin.site.register(Attachment,AttachmentAdmin)
admin.site.register(Formula,FormulaAdmin)
admin.site.register(FormulaUpdate,)
admin.site.register(ActivityLog,ActivityLogAdmin)
admin.site.register(FormulaVariables,FormulaVariablesAdmin)
admin.site.register(Error,ErrorAdmin)
admin.site.register(Restore)
admin.site.register(TemporaryVerification, TemporaryVerificationAdmin)



