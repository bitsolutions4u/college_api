"""anpmg URL Configuration

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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include,re_path
from django.views.generic import TemplateView





schema_view = get_schema_view(
    openapi.Info(
        title="ANNAPURNA MARRIAGES API",
        default_version='v1',
        description="ANMPG API",
        # terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="admin@bitsolutions4u.com"),
        license=openapi.License(name="Closed License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('Users.urls')),
    path('masters/', include('Masters.urls')),
    path('system/', include('System.urls')),
    path('reports/', include('Reports.urls')),

    

] 
if  settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Workes Only in Development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Workes Only in Development
else:
    urlpatterns += [ path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),]

# if not settings.USE_S3:
#     # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Workes Only in Development
#     urlpatterns += [ path(settings.MEDIA_URL+'<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),]

urlpatterns += [ 

    path('swagger/ZDFSFDDSFSDF213123ERWERWEFSDDSF/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/ZDFSFDDSFSDF213123ERWERWEFSDDSF/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
