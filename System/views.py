from pyexpat import model
from django.core import management
from django.http import Http404, HttpResponse
from django.db.models.deletion import RestrictedError
from django.http import HttpResponseRedirect

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, DjangoObjectPermissions, AllowAny, IsAdminUser

from dynamic_preferences.registries import global_preferences_registry 
from dynamic_preferences.api.viewsets import GlobalPreferencesViewSet

from dynamic_preferences.serializers import FileSerializer

from django.utils import timezone
import datetime
import time

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
User = get_user_model()

from Common.utils import Util
from Common.permissions import GetIOPermission

from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import filters
from rest_framework .filters import SearchFilter

from rest_framework import generics, status, permissions


from Common.utils import removeDuplicates
from Common.LexerBySly import formula_validator,formula_executer

from .models import Menu, Submenu, Menuitem, Notification, Attachment, Backup, Restore, Formula, FormulaUpdate, ActivityLog, FormulaVariables, NotificationUsers, Error, TemporaryVerification
from .serializers import MenuSerializer, SubmenuSerializer, MenuitemSerializer, UserMenuSerializer, NotificationSerializer, BackupSerializer, RestoreSerializer, AttachmentSerializer, ResetDatabaseSerializer, FormulaSerializer, FormulaValidationSerializer, FormulaValidation2Serializer, FormulaUpdateSerializer, ActivityLogSerializer, ActivityLogMiniSerializer, FormulaVariablesSerializer, SmsSerializer, NotificationUsersSerializer, ErrorSerializer, BackupValidationserializer, TemporaryOTPRequestSerializer, TemporaryVerifyOTPSerializer
from .services import get_dependent_models


from rest_framework.response import Response
from Common.Constants import  SMS


from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken,  OutstandingToken 
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import  status
from Users.models import User, Device

from System.forms import UserForm
from django.contrib import messages

import json

from System.socketio_app import maintenance_mode

class UserMenuList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.filter(status=1, ).order_by('name')
    serializer_class = UserMenuSerializer
    # def list(self, request, *args, **kwargs):
    #     print("user_permissions", request.user.user_permissions.all().distinct().values_list('id', flat=True))
    #     return Response({
    #         "user_permissions": "request.user.user_permissions.all()"
    #     })

class UserMenuDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.all().order_by('name')
    serializer_class = UserMenuSerializer

class UserMenuDetailByCode(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.all().order_by('name')
    serializer_class = UserMenuSerializer
    lookup_field = 'code'


class MenuList(generics.ListCreateAPIView):
    queryset = Menu.objects.filter(status=1, ).order_by('name')
    serializer_class = MenuSerializer

    def perform_create(self, serializer):
        serializer.save(createdby=self.request.user)

class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def perform_update(self, serializer):
        serializer.save(modifiedby=self.request.user, modifiedon= datetime.datetime.now())


class SubmenuList(generics.ListCreateAPIView):
    queryset = Submenu.objects.filter(status=1, ).order_by('name')
    serializer_class = SubmenuSerializer

    def perform_create(self, serializer):
        serializer.save(createdby=self.request.user)

class SubmenuDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Submenu.objects.all()
    serializer_class = SubmenuSerializer

    def perform_update(self, serializer):
        serializer.save(modifiedby=self.request.user, modifiedon= datetime.datetime.now())


class MenuitemList(generics.ListCreateAPIView):
    queryset = Menuitem.objects.filter(status=1, ).order_by('-id')
    serializer_class = MenuitemSerializer

    def perform_create(self, serializer):
        serializer.save(createdby=self.request.user)

class MenuitemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menuitem.objects.all()
    serializer_class = MenuitemSerializer

    def perform_update(self, serializer):
        serializer.save(modifiedby=self.request.user, modifiedon= datetime.datetime.now())


class NotificationList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        queryset = Notification.objects.filter(status=1, notificationusers__seen= 0, notificationusers__user= self.request.user)
        return queryset.order_by('-id')
        

class NotificationClear(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer
    model = serializer_class.Meta.model
    queryset = Notification.objects.all()
    
    def update(self, request, *args, **kwargs ):
        user = request.user
        notification = self.get_object()
        print(user, notification)
        obj = NotificationUsers.objects.filter(user=user, notification=notification, ).update(seen=1, seen_time = timezone.now())
        print(obj)
        return Response({}, status=status.HTTP_200_OK)
        
 

def CreateBackup(user):
    
    timestr = time.strftime("%Y%m%d%H%M%S")
    filename = "DATABASE_BACKUP_" + timestr + ".psql.bin.gz"
    
    management.call_command('dbbackup', compress=True, interactive=False, output_filename=filename)

    serializer = BackupSerializer(data={ "name": filename, })
    if serializer.is_valid(raise_exception=True):
        serializer.save(createdby=user) 

def RestoreBackup(user, filename):
    CreateBackup(user)

    
    management.call_command('dbrestore', database='default', uncompress=True, interactive=False, input_filename=filename)
    management.call_command('migrate',)
    
    serializer = RestoreSerializer(data={ "name": filename, })
    if serializer.is_valid(raise_exception=True):
        serializer.save(createdby=user) 


class BackupNow(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BackupSerializer
        
    def get(self, request, format=None):
        try:
            CreateBackup(self.request.user)
            return Response({ }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({ }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


      
class BackupList(generics.ListAPIView):
    queryset = Backup.objects.filter(status=1, ).order_by('-id')
    serializer_class = BackupSerializer
    permission_classes = [IsAuthenticated]

class BackupValidation(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BackupValidationserializer
    queryset = Backup.objects.filter(status=1, ).order_by('-id')
        
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = BackupValidationserializer(obj,data=request.data,context={'request': request})
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
       
        return Response(serializer.data, status=status.HTTP_200_OK)    
        

  
class RestoreList(generics.ListAPIView):
    queryset = Restore.objects.filter(status=1, ).order_by('-id')
    serializer_class = RestoreSerializer
    permission_classes = [IsAuthenticated]
    
    
class RestoreNow(generics.UpdateAPIView):
    queryset = Backup.objects.all().order_by('-id')
    serializer_class = BackupSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            RestoreBackup(self.request.user, instance.name)
            return Response({ }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({ }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class ResetDatabase(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResetDatabaseSerializer
    queryset = Backup.objects.filter(status=1, ).order_by('-id')
        
    def post(self, request, *args, **kwargs):
        try:
            CreateBackup(request.user)
        except Exception as e:
            return Response({"error": "Failed to Create Backup"}, status=200)    

        dryrun = kwargs['dryrun']
        
        serializer_context = { 'request' : request }
        serializer = ResetDatabaseSerializer(data=request.data, context=serializer_context)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data

        apps = []
        successmodels = []
        failedmodels = []
        all_dependent_models = {}

        for contenttype in data['contenttype_ids']:
            print(contenttype.app_label, contenttype.model, contenttype)
            model_class = contenttype.model_class()
            models = get_dependent_models(model_class)
            # models.append(model_class)
            models = removeDuplicates(models)
            print(model_class)
            all_dependent_models[model_class._meta.verbose_name] = []
            
            for model in models:
                if dryrun == 'dryrun':

                    all_dependent_models[model_class._meta.verbose_name].append(model._meta.verbose_name)

                elif dryrun == 'process':
                    print("Deleting.. ",model._meta.app_label, model._meta.model_name, model._meta.verbose_name)
                    apps.append(model._meta.app_label)
                    try:
                        model.objects.all().delete()
                        successmodels.append(model._meta.verbose_name)
                        print("Deleted Successful")
                    except RestrictedError as e:
                        failedmodels.append(model._meta.verbose_name)
                        print("RestrictedError", e)
                        print("Delete Failed")

        if dryrun == 'dryrun':
            return Response({"all_dependent_models": all_dependent_models }, status=200)

        elif dryrun == 'process':
            apps = removeDuplicates(apps)
            sequenceresetres =management.call_command('sqlsequencereset', *apps, database='default')
            return Response({ "successmodels": successmodels, "failedmodels": failedmodels,  }, status=status.HTTP_200_OK)

        else:
            return Response({"error":"Invalid Dryrun type" }, status=400)




class AttachmentCreate(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Attachment.objects.all().order_by('-id')
    serializer_class = AttachmentSerializer

    def perform_create(self, serializer):
        serializer.save(createdby=self.request.user)

class AttachmentDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Attachment.objects.all().order_by('-id')
    serializer_class = AttachmentSerializer


class AllFormulasList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormulaSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter( status=1, ).order_by('-id')
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(createdby=self.request.user)


class FormulaList(generics.ListCreateAPIView):
    serializer_class = FormulaSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter( status=1, ).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(createdby=self.request.user)

class FormulaDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FormulaSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()

    def perform_update(self, serializer):
        serializer.save(modifiedby=self.request.user)
        
    def perform_destroy(self, instance):
        instance.status=3
        instance.modifiedby=self.request.user
        instance.save()


class DynamicSettings(GlobalPreferencesViewSet):
    lookup_field='section__name'
        
    def get(self, request, format=None):
        try:
            data = global_preferences_registry.manager().all()

            if data['COMPANY__LOGO'] != None:
                data['COMPANY__LOGO'] = data['COMPANY__LOGO'].url
            # else:
            #     url = "static/images/thumbnail/default_no_file.png"
            #     data['COMPANY__LOGO'] = request.build_absolute_uri(url)

            if data['COMPANY__SMALLLOGO'] != None:   
                data['COMPANY__SMALLLOGO'] = data['COMPANY__SMALLLOGO'].url
            # else:
            #     url = "static/images/thumbnail/default_no_file.png"
            #     data['COMPANY__SMALLLOGO'] = request.build_absolute_uri(url)

            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({ }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# class FormulaVariablesList(generics.ListCreateAPIView):
#     serializer_class = FormulaVariablesSerializer
#     model = serializer_class.Meta.model
#     queryset = model.objects.filter( status=1, ).order_by('-id')

#     def perform_create(self, serializer):
#         serializer.save(createdby=self.request.user)

# class FormulaVariablesDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = FormulaVariablesSerializer
#     model = serializer_class.Meta.model
#     queryset = model.objects.all()

#     def perform_update(self, serializer):
#         serializer.save(modifiedby=self.request.user)
        
#     def perform_destroy(self, instance):
#         instance.status=3
#         instance.save()






class FormulaValidator(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormulaValidationSerializer

    def create(self, request, *args, **kwargs):  
        serializer = FormulaValidationSerializer(data=request.data, )
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        
        formula = data['formula']

        res = formula_validator( formula, )

        return Response(res, status = status.HTTP_200_OK)


class FormulaExecuter(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FormulaValidation2Serializer

    def create(self, request, *args, **kwargs):  
        serializer = FormulaValidation2Serializer(data=request.data, )
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
        
        code = data['code']
        variables = data['variables']

        formula = Formula.objects.filter(code = code)[0].formula
        
        res = formula_executer( formula, variables)

        return Response(res, status = status.HTTP_200_OK)



class FormulaUpdateList(generics.RetrieveAPIView):
    queryset = FormulaUpdate.objects.all()
    serializer_class = FormulaUpdateSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = FormulaUpdate.objects.filter( formula = kwargs['pk'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ActivityLogFilter(FilterSet):

    class Meta:
        model = ActivityLog
        fields = ['tablename', 'type' ]


class ActivityLogMini(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ActivityLogMiniSerializer
    pagination_class= None
    model = serializer_class.Meta.model
    queryset = model.objects.filter( status=1, ).only('id','tablename').order_by('tablename')
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = ActivityLogFilter
    
class ActivityLogList(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.filter( status=1, ).order_by('-id')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ActivityLogFilter
    search_fields = ['tablename', ]
    ordering_fields = ['id',]

    # def perform_create(self, serializer):
    #     user = self.request.user

    #     serializer.save(user=user)
        
    # def get_queryset(self):
    #     user = self.request.user
    #     queryset = ActivityLog.objects.filter(status=1 )

    #     return queryset.order_by('-id')

class ActivityLogDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivityLogSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()

    def perform_update(self, serializer):
        serializer.save(modifiedby=self.request.user)
        
    def perform_destroy(self, instance):
        instance.status=3
        instance.modifiedby=self.request.user
        instance.save()



class SmsList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SmsSerializer
    
    def get(self, request, format=None):
        serializer = SmsSerializer()
        return Response({
            'messages':[
                SMS.welcome_touser + SMS.postfix,
                SMS.purchase_create_customer + SMS.postfix,
                SMS.sale_create_customer + SMS.postfix,
                SMS.salequotation_create_customer + SMS.postfix,
                SMS.purchasequotation_create_customer + SMS.postfix,
                SMS.ovfquotation_create_customer + SMS.postfix,
                SMS.enquiry_create_customer + SMS.postfix,
            ]
        } )

    def post(self, request, format=None):
        serializer = SmsSerializer(data=request.data,)

        if serializer.is_valid(raise_exception=True):

            Util.send_sms(serializer.data)

        return Response(status=status.HTTP_204_NO_CONTENT)




class ErrorList(generics.ListAPIView):
    serializer_class = ErrorSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.order_by('-id')


class ActivityLogByUser(generics.ListAPIView):
    serializer_class = ActivityLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ActivityLogFilter
    search_fields = ['user__username',]
    ordering_fields = ['id', 'login','device','user','logout']

    def get_queryset(self, **kwargs):
        return ActivityLog.objects.filter(user=self.kwargs['pk'],  status= 1).order_by('-id')





global_preferences = global_preferences_registry.manager()


class Maintenance_On(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # global_preferences.set('DEVLOPER__MAINTENANCEMODE', False)
        # # maintenance_mode(True)
        # Otokens=OutstandingToken.objects.exclude(user__is_superuser = True)
        # for Otoken in Otokens:
        #     try:
        #         RefreshToken(Otoken.token).blacklist()
        #     # except:
        #     #     print("RefreshToken")
        #     except Exception as e:
        #         print("%s : %s " % (type(e).__name__, e, ))
        #         pass
         
        return Response({'message':'Maintenance Mode Enable'},status=status.HTTP_200_OK )




class Maintenance_Off(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # global_preferences['DEVLOPER__MAINTENANCEMODE'] = False
        # maintenance_mode(False)
        return Response({'message':'Maintenance Mode Disable'},status=status.HTTP_200_OK )



def RestoreById(request,id):
    context={}
    if request.method=='POST':
        output=request.POST.get('output')
        if output=='YES':
            file=Backup.objects.get(id=id)
            filename=file.name
            management.call_command('dbrestore', database='default', uncompress=True, interactive=False, input_filename=filename)
            management.call_command('migrate',)
            serializer = RestoreSerializer(data={ "name": filename, })
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            messages.add_message(request, messages.INFO, 'Successfully Restored into Database')   
            return HttpResponseRedirect("/admin/System/backup/")
        else:
            messages.add_message(request, messages.INFO, 'Not Restored into Database') 
            return HttpResponseRedirect("/admin/System/backup/")
    return render(request, "Restorecheckbox.html",{'form':UserForm})


class IO_LogIn(APIView):
    permission_classes = [GetIOPermission()]
    
    def post(self, request, format=None):
        data=request.data

        access_token = data['access_token']
        device_uuid = data['device_uuid']
        
        try :
            jwtauthentication = JWTAuthentication()
            validated_token = jwtauthentication.get_validated_token(access_token)
            user = jwtauthentication.get_user(validated_token)

            if user :           
                devices=Device.objects.filter(user=user,uuid= device_uuid)
                if devices:
                    devices.update( socket = data['sid'], )

                    maintenance_mode(global_preferences['DEVLOPER__MAINTENANCEMODE'], user)

                    return Response({
                        'payload': { 'status':'success','data':'Socket Login successfully'}
                    },status=status.HTTP_200_OK )      
                else :               
                    return Response({
                        'payload': {'status':'failed','data':'login failed'}
                    },status=status.HTTP_200_OK )
            else:
                return Response({
                    'payload': {'status':'failed','data':'login failed'}
                },status=status.HTTP_200_OK )
        except :        
            return Response({
                'payload': {'status':'failed','data':'login failed'}
            },status=status.HTTP_200_OK )
            
            
class IO_LogOut(APIView):
    permission_classes = [GetIOPermission(),]
    
    def post(self, request, format=None):
        data=request.data
        Device.objects.filter(socket = data['sid'],).update( socket = '' )
        return Response({'payload': { 'status':'success','data':'Socket Logout successfully'}},status=status.HTTP_200_OK )


class TemporaryOTPRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TemporaryOTPRequestSerializer


class TemporaryVerifyOTPView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TemporaryVerifyOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'Message': 'Phone Number Verified'}, status=status.HTTP_200_OK)


class TemporaryOTPResendView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TemporaryOTPRequestSerializer
        
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        instance = get_object_or_404(TemporaryVerification, mobile=mobile, is_phone_verified=False)
        
        return Response({'message':'OTP Send successfully'},status=status.HTTP_200_OK )
    