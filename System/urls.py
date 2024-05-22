from . import views
from django.urls import path , include

from rest_framework import routers


urlpatterns = [
    path('usermenu/', views.UserMenuList.as_view()),
    path('usermenu/<int:pk>', views.UserMenuDetail.as_view()),
    path('usermenu/<str:code>', views.UserMenuDetailByCode.as_view()),
    path('menu/', views.MenuList.as_view()),
    path("menu/<int:pk>", views.MenuDetail.as_view()),
    path('submenu/', views.SubmenuList.as_view()),
    path("submenu/<int:pk>", views.SubmenuDetail.as_view()),
    path('menuitem/', views.MenuitemList.as_view()),
    path("menuitem/<int:pk>", views.MenuitemDetail.as_view()),
    path('Notification/', views.NotificationList.as_view()),
    path('Notification/Clear/<int:pk>', views.NotificationClear.as_view()),
    path('Database/DoBackup', views.BackupNow.as_view()),
    path('Database/Backup', views.BackupList.as_view()),
    path('Database/downloadBackup/<int:pk>', views.BackupValidation.as_view()),
    path('Database/DoRestore/<int:pk>', views.RestoreNow.as_view()),
    path('Database/Restore', views.RestoreList.as_view()),

    path('RestoreById/<id>', views.RestoreById),
    
    path('Database/Reset/<str:dryrun>', views.ResetDatabase.as_view()),
    path('attachment/', views.AttachmentCreate.as_view()),
    path("attachment/<int:pk>", views.AttachmentDetail.as_view()),

    path('formula/', views.FormulaList.as_view()),
    path('allformuls/', views.AllFormulasList.as_view()), # with out pagination api
    path("formula/<int:pk>", views.FormulaDetail.as_view()),
    path('formulaexecuter/', views.FormulaExecuter.as_view()),
    path('formulavalidator/', views.FormulaValidator.as_view()),
    path('formulaupdate/<int:pk>', views.FormulaUpdateList.as_view()),


    path('dynamicsettings/', views.DynamicSettings.as_view({'get': 'get','post':"bulk"})),
    path('dynamicsettings/<str:section__name>', views.DynamicSettings.as_view({'get': 'retrieve', 'put': 'update',  'patch': 'partial_update' })),

    # path('variables/', views.FormulaVariablesList.as_view()),
    # path("variables/<int:pk>", views.FormulaVariablesDetail.as_view()),



    path('activitylog/', views.ActivityLogList.as_view()),
    path("activitylog/<int:pk>", views.ActivityLogDetail.as_view()),
    path('mini/activitylog/', views.ActivityLogMini.as_view()),
    path('activitylog/user/<int:pk>', views.ActivityLogByUser.as_view()),


    path('sms/', views.SmsList.as_view()),
    path('error/', views.ErrorList.as_view()),
    
    path('maintenance/', views.Maintenance_On.as_view()),
    path('maintenance_off/', views.Maintenance_Off.as_view()),
    
    path('io_login/', views.IO_LogIn.as_view()),
    path('io_logout/', views.IO_LogOut.as_view()),

    path('temp_otp/request/', views.TemporaryOTPRequestView.as_view()),
    path('temp_otp/verify/', views.TemporaryVerifyOTPView.as_view()),
    path('temp_otp/resend/', views.TemporaryOTPResendView.as_view()),

    


]
