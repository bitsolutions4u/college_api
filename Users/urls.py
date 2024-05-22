"""UserManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from rest_framework_simplejwt.views import ( TokenRefreshView,)
from django.urls import path

urlpatterns = [

    path('registration/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginAPIView.as_view(), name="login"),
    path('otprequest/', views.OTPRequestAPIView.as_view(), name="otprequest"),
    path('resendotp/', views.OTPResendAPIView.as_view(), name="otpresend"),
    path('changepassword/', views.ChangePasswordView.as_view(), name="changepassword"),


    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),

    path('iamuser/', views.IamUserDetails.as_view(), name='iamuser'),
    path('userinactive/<int:id>', views.UserInActive.as_view()),
    path('list/', views.UserList.as_view(), name='users'),

    path('email-verify/', views.VerifyEmail.as_view(), name="email-verify"),

    path('groups/', views.GroupList.as_view(), name='groups'),
    path('groups/<int:pk>', views.GroupDetails.as_view(), name='groups'),

    path('groupspermissionadd/<int:pk>', views.GroupPermissionAdd.as_view(), name='groups'),
    path('groupspermissionrermove/<int:pk>', views.GroupPermissionRemove.as_view(), name='groups'),

    path('usergroups/', views.UserGroupList.as_view(), name='usergroups'),
    path('permissions/', views.PermissionList.as_view(), name='permissions'),

    path('apps/permissions/', views.DjangoAppPermissionList.as_view(), name='DjangoAppPermissionList'),
    path('contenttypes/', views.ContentTypeList.as_view(), name='contenttypes'),
    path('userpermissions/', views.UserPermissionList.as_view(), name='userpermissions'),

    path('devicelog/', views.DeviceLogs.as_view(), name='devicelogall'),
    path('devicelog/me/', views.DeviceLogByMe.as_view(), name='devicelog'),
    path('devicelog/user/<int:pk>', views.DeviceLogByUser.as_view()),


    path('userLogin/', views.UserLoginAPIView.as_view(), name="login"),

]
