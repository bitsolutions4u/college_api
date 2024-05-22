

from xmlrpc.client import Boolean
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry 
from dynamic_preferences.types import  StringPreference, BooleanPreference, FilePreference, LongStringPreference

from System.views import Maintenance_On, Maintenance_Off
sendemail = Section('SMTP')
sendsms = Section('SMS')
company = Section('COMPANY')
devloper = Section('DEVLOPER')
thirdparty = Section('THIRDPARTY')
jsonpushfile = Section('JSON_DATA')



@global_preferences_registry.register
class HostUser(StringPreference):
    section = sendemail
    name = 'USER'
    default = 'yrameshkumar123@gmail.com'
    required = True
    verbose_name ='HOST_USER'


@global_preferences_registry.register
class Password(StringPreference):
    section = sendemail
    name = 'PASSWORD'
    default = ''
    required = True
    verbose_name ='PASSWORD'


@global_preferences_registry.register
class Port(StringPreference):
    section = sendemail
    name = 'PORT'
    default = '587'
    required = True
    verbose_name ='PORT'


@global_preferences_registry.register
class Tls(BooleanPreference):
    section = sendemail
    name = 'USE_TLS'
    default = True
    required = True
    verbose_name ='TLS'


@global_preferences_registry.register
class EmailHost(StringPreference):
    section = sendemail
    name = 'HOST'
    default = 'smtp.gmail.com'
    required = True
    verbose_name ='EMAIL_HOST'


@global_preferences_registry.register
class EmailBackend(StringPreference):
    section = sendemail
    name = 'BACKEND'
    default = 'django.core.mail.backends.smtp.EmailBackend'
    required = True
    verbose_name ='EMAIL_BACKEND'


@global_preferences_registry.register
class Url(StringPreference):
    section = sendsms
    name = 'URL'
    default = ''
    required = True
    verbose_name ='URL'


@global_preferences_registry.register
class Message(StringPreference):
    section = sendsms
    name = 'MSG_VAR'
    default = ''
    required = True
    verbose_name ='MSG_VAR'


@global_preferences_registry.register
class Number(StringPreference):
    section = sendsms
    name = 'NUMBER_VAR'
    default = ''
    required = True
    verbose_name ='NUMBER_VAR'


@global_preferences_registry.register
class Logo(FilePreference):
    section = company
    name = 'LOGO'
    default = ''
    required = True
    verbose_name ='LOGO'


@global_preferences_registry.register
class SmallLogo(FilePreference):
    section = company
    name = 'SMALLLOGO'
    default = ''
    required = True
    verbose_name ='SMALLLOGO'


@global_preferences_registry.register
class Name(StringPreference):
    section = company
    name = 'NAME'
    default = ''
    required = True
    verbose_name ='NAME'


@global_preferences_registry.register
class SimpleName(StringPreference):
    section = company
    name = 'SIMPLENAME'
    default = ''
    required = True
    verbose_name ='SIMPLENAME'


@global_preferences_registry.register
class Email(StringPreference):
    section = company
    name = 'EMAIL'
    default = ''
    required = True
    verbose_name ='EMAIL'


@global_preferences_registry.register
class Mobile(StringPreference):
    section = company
    name = 'MOBILE'
    default = ''
    required = True
    verbose_name ='MOBILE'


@global_preferences_registry.register
class AlternateMobile(StringPreference):
    section = company
    name = 'ALTERNATEMOBILE'
    default = ''
    required = False
    verbose_name ='ALTERNATEMOBILE'



@global_preferences_registry.register
class Website(StringPreference):
    section = company
    name = 'WEBSITE'
    default = ''
    required = True
    verbose_name ='WEBSITE'


@global_preferences_registry.register
class GstNo(StringPreference):
    section = company
    name = 'GSTNO'
    default = ''
    required = True
    verbose_name ='GSTNO'


@global_preferences_registry.register
class Address(LongStringPreference):
    section = company
    name = 'ADDRESS'
    default = ''
    required = True
    verbose_name ='ADDRESS'


@global_preferences_registry.register
class Email(StringPreference):
    section = devloper
    name = 'EMAIL'
    default = ''
    required = True
    verbose_name ='EMAIL'


@global_preferences_registry.register
class Mobile(StringPreference):
    section = devloper
    name = 'MOBILE'
    default = ''
    required = True
    verbose_name ='MOBILE'



@global_preferences_registry.register
class MaintenanceMode(BooleanPreference):
    section = devloper
    name = 'MAINTENANCEMODE'
    default = False
    required = True
    verbose_name ='Maintenance Mode'



@global_preferences_registry.register
class Url(StringPreference):
    section = thirdparty
    name = 'URL'
    default = ''
    required = True
    verbose_name ='URL'



@global_preferences_registry.register
class Token(StringPreference):
    section = thirdparty
    name = 'TOKEN'
    default = ''
    required = True
    verbose_name ='TOKEN'


@global_preferences_registry.register
class JsonData(StringPreference):
    section = jsonpushfile
    name = 'JSONFILE'
    default = '{}'
    required = True
    verbose_name ='JSONFILE'