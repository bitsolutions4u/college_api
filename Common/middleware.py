# from django.core.urlresolvers import resolve
from django.urls import reverse, resolve
from System.models import Error
import json



from django.db import connection
from django.conf import settings
import os
from django.contrib.auth import get_user_model
# from Users.models import Device
User = get_user_model()

# import zoneinfo
from backports.zoneinfo import ZoneInfo
from django.utils import timezone


def terminal_width():
    """
    Function to compute the terminal width.
    WARNING: This is not my code, but I've been using it forever and
    I don't remember where it came from.
    """
    width = 0
    try:
        import struct, fcntl, termios
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
        width = struct.unpack('HHHH', x)[1]
    except:
        pass
    if width <= 0:
        try:
            width = int(os.environ['COLUMNS'])
        except:
            pass
    if width <= 0:
        width = 80
    return width
        
class SqlPrintingMiddleware(object):
    """
    Middleware which prints out a list of all SQL queries done
    for each view that is processed.  This is only useful for debugging.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        indentation = 2
        if len(connection.queries) > 0 and settings.DEBUG:
            width = terminal_width()
            total_time = 0.0
            for query in connection.queries:
                nice_sql = query['sql'].replace('"', '').replace(',',', ')
                sql = "\033[1;31m[%s]\033[0m %s" % (query['time'], nice_sql)
                total_time = total_time + float(query['time'])
                # while len(sql) > width-indentation:
                #     print("%s%s" % (" "*indentation, sql[:width-indentation]))
                #     sql = sql[width-indentation:]
                print("%s%s\n" % (" "*indentation, sql))
            replace_tuple = (" "*indentation, str(total_time))
            print("%s\033[1;32m[TOTAL TIME: %s seconds]\033[0m" % replace_tuple)
        return response

class allPermissionsMiddleware(object):
    """
    Middleware which Add all User Permissions and user 
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        
        l = request.user.get_all_permissions()
        l_as_list = list(l) 

        # ADDED NEW VARIABLES
        request.allPermissions =  l_as_list
        request.allScreenPermissions =  list(map(lambda x: x.split(".")[-1], l_as_list)) 
        response = self.get_response(request)

        return response


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.session.get('django_timezone')
        tzname = 'Asia/Kolkata'
        if tzname:
            timezone.activate(zoneinfo.ZoneInfo(tzname))
        else:
            timezone.deactivate()
        return self.get_response(request)
       
 

class ErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 500:
            current_url = request.path_info
            content = response.content
            code = response.status_code
            # request.query_params
            try:
                Error.objects.create(error_url = current_url, requestbody = "GET: {} BODY: {} POST: {}".format(request.GET.dict(), request.body.decode('utf-8'),request.POST.dict()), responsecontent = content, errorcode = code  ) # other data you want to store here
            except:
                Error.objects.create(error_url = current_url, requestbody = "GET: {} POST: {}".format(request.GET.dict(),request.POST.dict()), responsecontent = content, errorcode = code  ) # other data you want to store here

        return response