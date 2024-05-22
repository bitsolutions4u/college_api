from django.shortcuts import render
from django.contrib.auth import login
from django.db.models import Q
from rest_framework import generics, status, viewsets
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
User = get_user_model()
from Users.models import Device,DeviceLog,Groupdetails,DjangoApp,ContentTypeDetail,PermissionDetail
from django_filters.filters import Filter
from rest_framework import filters
from django_filters import DateRangeFilter,DateFilter
from django.contrib import messages
from Common.permissions import GetPermission
from Users.serializers import RegisterSerializer, EmailVerificationSerializer, LoginSerializer, OTPRequestSerializer, \
    OTPResendSerializer, TokenRefreshSerializer, ChangePasswordSerializer, UserCommonSerializer, UserGroupSerializer, \
    PermissionJoinSerializer, GroupSerializer, DjangoAppSerializer, ContentTypeSerializer, DeviceLogSerializer, \
    GroupMini2Serializer, UserLoginSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken 
from rest_framework.views import APIView
from rest_framework import generics, status, views, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib import auth
from django.shortcuts import redirect
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from Common.utils import Util
from django.http import HttpResponsePermanentRedirect
import os
from urllib.parse import urlparse
from django.contrib.auth.models import Group, Permission, ContentType
from django.utils import timezone



class UserFilter(FilterSet):

    class Meta:
        model = User
        fields = ['state','district','city','area']

class DeviceLogFilter(FilterSet):
    
    start_date = DateFilter(field_name='createdon',lookup_expr=('gte'),) 
    end_date = DateFilter(field_name='createdon',lookup_expr=('lte'))
    date_range = DateRangeFilter(field_name='createdon')

    class Meta:
        model = DeviceLog
        fields = ['device', 'user','login','logout','start_date', 'end_date',]

class RegisterView(generics.ListCreateAPIView):
    
    permission_classes = (permissions.AllowAny,)
    
    serializer_class = RegisterSerializer

class VerifyEmail(views.APIView):

    permission_classes = [permissions.AllowAny]
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        serializer = self.serializer_class(data={'token': request.GET.get('token')})
        serializer.is_valid(raise_exception=True)
        return Response( {'email': 'Successfully activated'}, status=status.HTTP_200_OK)


class LoginAPIView(generics.GenericAPIView):
    
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        try:
            user_serializer = self.serializer_class(data=request.data, context={'request': request})
            user_serializer.is_valid(raise_exception=True)
            status_code = status.HTTP_200_OK
            response = {'status': 'success', 'status_code': status_code,
                        'message': 'user details retrived Successfully', 'user_details': user_serializer.data}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status': 'failure', 'status_code': status_code, 'message': str(error)}
        return Response(response, status=status_code)
        # serializer = self.serializer_class(data=request.data, context={'request': request})
        # serializer.is_valid(raise_exception=True)
        #
        # user = serializer.validated_data['user']
        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        # return Response(serializer.data, status=status.HTTP_200_OK)


class UserLoginAPIView(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        try:
            user_serializer = self.serializer_class(data=request.data, context={'request': request})
            user_serializer.is_valid(raise_exception=True)
            status_code = status.HTTP_200_OK
            response = {'status': 'success', 'status_code': status_code,
                        'message': 'user details retrived Successfully', 'user_details': user_serializer.data}
        except Exception as error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response = {'status': 'failure', 'status_code': status_code, 'message': str(error)}
        return Response(response, status=status_code)
        # serializer = self.serializer_class(data=request.data, context={'request': request})
        # serializer.is_valid(raise_exception=True)
        #
        # user = serializer.validated_data['user']
        # serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        # return Response(serializer.data, status=status.HTTP_200_OK)


class OTPRequestAPIView(generics.GenericAPIView):
    
    permission_classes = (permissions.AllowAny,)
    serializer_class = OTPRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class OTPResendAPIView(generics.GenericAPIView):
    
    permission_classes = (permissions.AllowAny,)
    serializer_class = OTPResendSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenRefreshView(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()
    serializer_class = TokenRefreshSerializer


    def post(self, request, *args, **kwargs):

        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data =serializer.validated_data
        
        return Response(data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):

    permission_classes =[permissions.IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    
    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(id=user.id)
        
    def get_object(self):
        user = self.request.user
        return User.objects.get(id=user.id)


class UserInActive(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request,*args, **kwargs):
    
        id = kwargs['id']
        try:
            user = User.objects.get(id=id)
            Otokens=OutstandingToken.objects.filter(user=user)
            for Otoken in Otokens:
                try:
                    RefreshToken(Otoken.token).blacklist()
                except:
                    pass
        
            user.is_active = False
            user.save()
            user.devices.update(
                accesstoken= '',
                fcmtoken='',
                apntoken='',
                socket='',
            )

        except User.DoesNotExist:
            return Response({"user":'user does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        

class UserList(generics.ListCreateAPIView):

    permission_classes = [permissions.AllowAny]

    queryset = User.objects.filter( is_superuser = False)
    serializer_class = UserCommonSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,]
    filterset_class = UserFilter
    search_fields = ['username', 'email', 'phone', 'first_name', 'last_name', 'pincode', 'groups__name' ]



class IamUserDetails(generics.RetrieveAPIView):
    permission_classes =[permissions.IsAuthenticated]
    serializer_class = UserCommonSerializer
    queryset = User.objects.all()

    def get_object(self):
        obj = User.objects.get(pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj



class GroupDetails(generics.RetrieveUpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupPermissionAdd(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupMini2Serializer

    def put(self, request, *args, **kwargs, ):   

        obj = self.get_object()
        obj.permissions.add(request.data['permission_id'])

        return Response({}, status=status.HTTP_200_OK)

class GroupPermissionRemove(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupMini2Serializer

    def put(self, request, *args, **kwargs, ):   

        obj = self.get_object()
        obj.permissions.remove(request.data['permission_id'])
        
        return Response({}, status=status.HTTP_200_OK)



class UserGroupList(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserGroupSerializer

class PermissionList(generics.ListAPIView):

    queryset = Permission.objects.all()
    serializer_class = PermissionJoinSerializer


class GroupList(generics.ListCreateAPIView):
    #permission_classes = [GetPermission('Masters.add_employee')]
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer
    filter_backends = [filters.SearchFilter,]
    search_fields = ['name',]


class DjangoAppPermissionList(generics.ListAPIView):
    permission_classes = [GetPermission('auth.add_group')]
    queryset = DjangoApp.objects.filter(hide=False)
    serializer_class = DjangoAppSerializer
    pagination_class= None

class ContentTypeList(generics.ListAPIView):
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    permission_lables ={
        "add_village":"Add",
        "change_village":"Update",
        "delete_village":"Delete",
        "view_village":"View",
    }
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            qs = ContentType.objects.filter(Q(~Q(app_label__in=['admin','contenttypes','sessions','token_blacklist','System']) & ~Q(model__in=['country','district','village',])))
        else:
            qs = ContentType.objects.filter(Q(~Q(app_label__in=['admin','contenttypes','sessions','token_blacklist']) & ~Q(model__in=['country','district','village',])))
        serializer = ContentTypeSerializer( instance=qs, many=True)
        data = serializer.data
        return Response({"data":data, "permission_lables":self.permission_lables }, status=status.HTTP_200_OK)

class UserPermissionList(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        l = request.user.get_all_permissions()
        l_as_list = list(l)  
        return Response(l_as_list, status=status.HTTP_200_OK)




class DeviceLogs(generics.ListAPIView):
    serializer_class = DeviceLogSerializer
    model = serializer_class.Meta.model
    queryset = model.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DeviceLogFilter
    search_fields = ['user__username', ]
    ordering_fields = ['id','login','device','user','logout']

class DeviceLogByMe(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeviceLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DeviceLogFilter
    search_fields = ['user__username',]
    ordering_fields = ['id', 'login','device','user','logout']

    
    def get_queryset(self):
        user = self.request.user
        queryset = DeviceLog.objects.filter( user = user, )

        return queryset.order_by('-id')
        

class DeviceLogByUser(generics.ListAPIView):
    serializer_class = DeviceLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = DeviceLogFilter
    search_fields = ['user__username',]
    ordering_fields = ['id', 'login','device','user','logout']

    def get_queryset(self, **kwargs):
        return DeviceLog.objects.filter(user=self.kwargs['pk'],  status= 1).order_by('id')