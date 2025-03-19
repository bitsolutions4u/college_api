import os
import datetime
from pathlib import Path

from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = os.getenv("DEBUG", "False") == "True"

DEBUG =False



# ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,172.31.7.244").split(",")

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dynamic_preferences',


    'rest_framework_simplejwt.token_blacklist',

    'rest_framework',
    'drf_yasg',
    'django_filters',
    'dbbackup',
    'import_export',
    'imagekit',
    'django_admin_listfilter_dropdown',
    'rangefilter',
    'django_crontab',
    
    'Users',
    'System',
    'Masters',
    'Reports',
   

    
]

AUTH_USER_MODEL = 'Users.User'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 'Common.middleware.SqlPrintingMiddleware',
    'Common.middleware.allPermissionsMiddleware',
    'Common.middleware.ErrorMiddleware',

    'corsheaders.middleware.CorsMiddleware',
]

INSTALLED_APPS += [ 'corsheaders',]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",

]
# CORS_ORIGIN_WHITELIST = (
#   'http://localhost:8000',
# )

ROOT_URLCONF = 'anpmg.urls'

APPEND_SLASH = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'build'),os.path.join('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'dynamic_preferences.processors.global_preferences',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'common_tags': 'Common.CustomFilters',
            },
        },
    },
]

WSGI_APPLICATION = 'anpmg.wsgi.application'

if os.getenv("DEBUG", "False") == "True" and os.getenv("DB_NAME", None) is None:
    raise Exception("DB_NAME environment variable not defined")

DATABASES = {
    

    'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'anmpg-data.c81s0aomcw7h.us-east-1.rds.amazonaws.com',
        "OPTIONS": {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
            'charset': 'utf8mb4',
            "autocommit": True,
        },
        'NAME': 'college_data',
        'USER': 'root',
        'PASSWORD': 'Vanesh_007143',
        'HOST': 'localhost',
        'PORT': '3306',
        'TEST':{
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
        }
    },
}

# DATABASES = {
#
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'OPTIONS': {
#             'options': '-c search_path=django,anpmg'
#         },
#         'NAME': 'Vijaya_Diagnostic',
#         'USER': 'postgres',
#         'PASSWORD': 'Ramesh007123##',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#         'TEST': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(BASE_DIR, 'test_db.sqlite3'),
#         }
#     },
# }


import sys
if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db.sqlite3'
    }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    'NON_FIELD_ERRORS_KEY': 'error',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'Common.permissions.AllPermissions',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'Common.Paginations.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=1),#minutes=120
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=7),#days=1
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    # 'USE_SESSION_AUTH':False,
    'LOGIN_URL':'/admin/login/',
    'LOGOUT_URL':'/admin/logout/'
    
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = ('Common.Authentication.CustomAuthenticationBackend',)

SINGLE_MOBILE_DEVICE_PER_USER = False

# IMPORT_EXPORT_USE_TRANSACTIONS = True 

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_GLOBAL_URL = True


STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static_assets'),] #os.path.join(BASE_DIR, 'build/static'),
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/



# DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
# DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'media\\backup')}


USE_S3 = True


if USE_S3:
    # AWS S3 Configrations
    INSTALLED_APPS += ['storages']
    
    # AWS_ACCESS_KEY_ID = 'AKIA5BNOEKQKSVQ2B2TR'
    # AWS_ACCESS_KEY_ID = 'AKIAXPVZG5UPGRPNXU5Z'    #new
    # AWS_SECRET_ACCESS_KEY = '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'
    # AWS_SECRET_ACCESS_KEY = 'yKcxFLgSa91PoVFWnFIFqh6fmKXj2nFY282lpr++' #new
    # AWS_STORAGE_BUCKET_NAME = 'wheelsmart'
    # AWS_STORAGE_BUCKET_NAME = 'annapurnamatrimony' #new
    # WHEELSMART_DOMAIN = 'app.wheelsmart.in'
    # AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME #new

    # ap-south-1
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    AWS_S3_REGION_NAME = 'ap-south-1' #change to your region
    AWS_S3_SIGNATURE_VERSION = 's3v4'

    AWS_STATIC_LOCATION = 'static'
    # STATICFILES_STORAGE = 'Common.storage_backends.StaticStorage'
    # STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)
    STATIC_URL = 'static/'

    AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
    PUBLIC_FILE_STORAGE = 'Common.storage_backends.PublicMediaStorage'

    AWS_PRIVATE_MEDIA_LOCATION = 'media'
    PRIVATE_FILE_STORAGE = 'Common.storage_backends.PrivateMediaStorage'

    DEFAULT_FILE_STORAGE = PRIVATE_FILE_STORAGE
    #new
    # MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_PRIVATE_MEDIA_LOCATION)

    # IMAGEKIT_DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

    # STATICFILES_DIRS = [
    #     os.path.join(BASE_DIR, 'static'),
    # ]
    
    AWS_DBBACKUP_MEDIA_LOCATION = 'media/backups/'
    DBBACKUP_STORAGE = 'Common.storage_backends.DBBackupMediaStorage'
    # DBBACKUP_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DBBACKUP_STORAGE_OPTIONS = {
        # 'access_key': AWS_ACCESS_KEY_ID,
        # 'secret_key': AWS_SECRET_ACCESS_KEY,
        # 'bucket_name': AWS_STORAGE_BUCKET_NAME,
        'default_acl': 'private',
        'location': AWS_DBBACKUP_MEDIA_LOCATION
    }
else:
    # STATIC IN LOCALS
    STATIC_URL = 'static/'

    MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')
    MEDIA_URL = 'media/'

    DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'

    DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'media\\backup')}


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


## Removed After Dynamic Preferences Added
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # Has to enable low security clients in gmail
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'bitsolutions4u@gmail.com'
EMAIL_HOST_PASSWORD = 'Ramesh007123##'


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp-mail.outlook.com'
# EMAIL_USE_TLS = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'ramesh0805y@gmail.com'
# EMAIL_HOST_PASSWORD = 'Sailucky007123##'
# DEFAULT_FROM_EMAIL = ''
# SERVER_EMAIL = ''


CRONJOBS = [
    # ('*/5 * * * *', 'myapp.cron.other_scheduled_job', ['arg1', 'arg2'], {'verbose': 0}), # To call a function
    ('0  22 * * *', 'django.core.management.call_command', ['AutoOutTime']),# To call a Command
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':  "_log\DEBUG_LogFile.log",
        },
        'logfile_info':{
            'level':'INFO',
            'class':'logging.FileHandler',
            'formatter': 'standard',
            'filename':  "_log\INFO_LogFile.log",
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        # 'level':'DEBUG' if DEBUG else 'WARNING',
        'class':'logging.FileHandler',
        'filename': "_log\root_logfile.log",
        'maxBytes': 1024 * 1024 * 10, #Max 10MB
        'backupCount': 3,
        'formatter': 'standard',
    },
    'loggers': {
        # 'django': {
        #     'handlers':['console'],
        #     'propagate': True,
        #     'level':'WARN',
        # },
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
        'Common': {
            'level':'DEBUG' if DEBUG else 'WARNING',
            'handlers': ['logfile', 'console'],
        },
        'Common': {
            'level':'INFO',
            'handlers': ['logfile_info', 'console'],
        },
    }
}


IO_SERVER_URL = "http://localhost:5000"
IO_SECRET = "NV4387G0VESRRN6STZ0VC4KN8JTQA0"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'                                   
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_USE_TLS=True
EMAIL_HOST_USER="shanudjango1997@gmail.com"
EMAIL_HOST_PASSWORD="mperjnbcfrtqqwhp"