from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from Common.Constants import SMS,Email
from django.conf import settings
from Common.utils import Util
from Common.Authentication import *
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed,NotAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import password_validation 
from django.contrib.auth.models import Group, Permission
import string
from django.utils.crypto import get_random_string
from django.db.models import Q
User = get_user_model()
from Users.models import Device,DeviceLog,Groupdetails,DjangoApp,ContentTypeDetail,PermissionDetail
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
import requests
from Common.Authentication import CustomAuthenticationBackend

class UserCommonSerializer(serializers.ModelSerializer):
    country_name = ReadOnlyField(source='country.name')
    state_name = ReadOnlyField(source='state.name')
    district_name = ReadOnlyField(source='district.name')
    city_name = ReadOnlyField(source='city.name')
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        # fields = ('username','email','phone','first_name','last_name','state','district','city','address')
        fields = '__all__'

    createdby = serializers.HiddenField(default=serializers.CurrentUserDefault())
    modifiedby = serializers.HiddenField(default=serializers.CurrentUserDefault())


class UserMiniSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'address', 'phone',)

class DeviceSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(many = False, read_only=True)
    type = serializers.ChoiceField(choices=Device.DEVICETYPE_CHOICES, )
    type_name =  serializers.SerializerMethodField()

    def get_type_name(self, obj):
        return obj.get_type_display()


    class Meta:
        model = Device
        fields = ( 'code','name', 'type', 'type_name','user', 'is_active' )



class RegisterSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(min_length=10,max_length=15)
    fullname = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, max_length=68, min_length=6, required=True)
    
    
    def get_fullname(self, user):

        return  '{} {}'.format(user.first_name, user.last_name )

    def validate(self, attrs):



        return super().validate(attrs)

    class Meta:
        model = User
        read_only_fields = ['otp']
        fields = ['username','fullname','email','phone','password','first_name','last_name','state','otp','district','city','area','address','pincode']

    def create(self, validated_data):

        #data, is_created = User.objects.update_or_create( phone= phone, defaults= validated_data)
        validated_data['otp'] =  get_random_string(4, allowed_chars= string.digits)
        object = User.objects.create_user(**validated_data)
        token = RefreshToken.for_user(object).access_token
        current_site = get_current_site(self.context['request']).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+object.username + \
            ' Use the link below to verify your email \n' + absurl
        edata = {'email_body': email_body, 'to_email': object.email,
                'email_subject': 'Verify your email'}

        Util.send_email(edata)

  
        
        # phone = validated_data.pop('phone', None)
        # swords = {'to_phone':phone,'otp':validated_data['otp']  }
        # sdata = {'to_phone':phone,'message':  SMS.loginotp.format(**swords) }
        #
        # Util.send_sms(sdata)
        
        return object 

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3, read_only=True)
    phone = serializers.CharField(max_length=15, min_length=10, read_only=True)
    full_name = serializers.CharField(max_length=255, min_length=6, read_only=True)
    password = serializers.CharField(max_length=68, min_length=4, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)
    device_name = serializers.CharField(max_length=100, required=False, allow_blank=True, write_only=True)
    device_uuid = serializers.CharField(max_length=1000, write_only=True)
    device_type = serializers.ChoiceField(choices=Device.DEVICETYPE_CHOICES, write_only=True)
    device_fcmtoken = serializers.CharField(max_length=1000, required=False, allow_blank=True, write_only=True)
    device_apntoken = serializers.CharField(max_length=1000, required=False, allow_blank=True,  write_only=True)
    group_name = serializers.CharField(max_length=255, min_length=6, read_only=True)
    tokens = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def get_role(self,obj):
        user = User.objects.get(username=obj['username'])
        if user.is_superuser:
            return 'Admin'
        elif user.is_staff:
            return 'Student'
        elif user.is_agent:
            return 'Teacher'
        elif user.is_branch:
            return 'Branch'
        elif user.is_customer:
            return 'Customer'
    

    class Meta:
        model = User
        read_only_fields = [ 'id','full_name', 'group_name']
        fields = ['id', 'email', 'phone', 'password', 'username','tokens','state','district','city','area', 'role', 'full_name', 'group_name','device_name','device_uuid','device_type', 'device_fcmtoken', 'device_apntoken']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        device_name = attrs.get('device_name', '')
        device_uuid = attrs.get('device_uuid', '')
        device_type = attrs.get('device_type', 0)
        device_fcmtoken = attrs.get('device_fcmtoken', '')
        device_apntoken = attrs.get('device_apntoken', '')
    
        
        user = auth.authenticate(username=username, password=password)
        print("ISER",user)

        if device_type == 0:
            raise serializers.ValidationError('Device type is required')

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        tokens = user.tokens()
        # role = user.findRole()
        if settings.SINGLE_MOBILE_DEVICE_PER_USER:
            mobile_devices_count = Device.objects.filter(
                user=user,
                type__in=[1, 2],
                is_active= True,
            ).count()
            devices = Device.objects.filter(
                user= user,
                uuid= device_uuid,
                type= device_type,
                is_active= True)

            if (mobile_devices_count == 0 and device_type != 3) or (device_type == 3 and devices.count() == 0): # First Mobile device or New Web device

                device, dc = Device.objects.get_or_create(
                user=user,
                uuid= device_uuid,
                is_active= True,
                defaults={
                    'name': device_name,
                    'type': device_type,
                        }
                    )
            elif mobile_devices_count > 0 and  device_type != 3 and devices.count()==0: # other new Mobile device
                device, dc = Device.objects.get_or_create(
                user=user,
                uuid= device_uuid,
                is_active= False,
                defaults={
                'name': device_name,
                'type': device_type,
                }
                )
                raise AuthenticationFailed('This device not allowed, contact admin')
            else: # old Active Devices
                device = devices[0]
        else:
            device, dc = Device.objects.get_or_create(
            user=user,
            uuid= device_uuid,
            is_active= True,
            defaults={
                'name': device_name,
                'type': device_type,
                })

        if user.is_superuser == True:
            userValue = True
        elif user.is_staff == True:
            userValue =True
        elif user.is_agent == True:
            userValue=True
        elif user.is_branch == True:
            userValue=True
        elif user.is_customer == True:
            userValue=True

        if not userValue == True and not ((device.type != 3 and ( user.deviceaccess == 1 or user.deviceaccess == 3)) or (device.type == 3 and ( user.deviceaccess == 2 or user.deviceaccess == 3)) ):
            raise AuthenticationFailed('This device type not allowed, contact admin')

        device.fcmtoken = device_fcmtoken
        device.apntoken = device_apntoken
        device.accesstoken = tokens['access']
        device.save()
            
        group_name = user.groups.all()[0].name if user.groups.count() > 0 else ""
        return {
            'full_name': user.first_name+" "+ user.last_name  ,
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            # 'role': role,
            'group_name': group_name,
            'tokens': user.tokens,
        }


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3, read_only=True)
    phone = serializers.CharField(max_length=15, min_length=10, read_only=True)
    full_name = serializers.CharField(max_length=255, min_length=6, read_only=True)
    password = serializers.CharField(max_length=68, min_length=4, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)
    device_name = serializers.CharField(max_length=100, required=False, allow_blank=True, write_only=True)
    device_uuid = serializers.CharField(max_length=1000, write_only=True)
    device_type = serializers.ChoiceField(choices=Device.DEVICETYPE_CHOICES, write_only=True)
    device_fcmtoken = serializers.CharField(max_length=1000, required=False, allow_blank=True, write_only=True)
    device_apntoken = serializers.CharField(max_length=1000, required=False, allow_blank=True, write_only=True)
    group_name = serializers.CharField(max_length=255, min_length=6, read_only=True)
    tokens = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        # user = None
        # # Try to authenticate the user using any of the provided identifiers
        # if '@' in obj['username']:
        #     # Treat input as email
        #     user = User.objects.get(email=obj['username'])
        # elif obj['username'].isdigit():
        #     # Treat input as mobile number
        #     user = User.objects.get(phone=obj['username'])
        # else:
        #     user = User.objects.get(username=obj['username'])

        user = User.objects.get(username=obj['username'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    def get_role(self, obj):
        # user = None
        # # Try to authenticate the user using any of the provided identifiers
        # if '@' in obj['username']:
        #     # Treat input as email
        #     user = User.objects.get(email=obj['username'])
        # elif obj['username'].isdigit():
        #     # Treat input as mobile number
        #     user = User.objects.get(phone=obj['username'])
        # else:
        #     user = User.objects.get(username=obj['username'])
        user = User.objects.get(username=obj['username'])
        if user.is_superuser:
            return 'Admin'
        elif user.is_staff:
            return 'Student'
        elif user.is_agent:
            return 'Teacher'
        elif user.is_branch:
            return 'Branch'
        elif user.is_customer:
            return 'Customer'

    class Meta:
        model = User
        read_only_fields = ['id', 'full_name', 'group_name']
        fields = ['id', 'email', 'phone', 'password', 'username', 'tokens', 'state', 'district', 'city', 'area', 'role',
                  'full_name', 'group_name', 'device_name', 'device_uuid', 'device_type', 'device_fcmtoken',
                  'device_apntoken']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        device_name = attrs.get('device_name', '')
        device_uuid = attrs.get('device_uuid', '')
        device_type = attrs.get('device_type', 0)
        device_fcmtoken = attrs.get('device_fcmtoken', '')
        device_apntoken = attrs.get('device_apntoken', '')

        # Create an instance of the custom authentication backend
        custom_auth_backend = CustomAuthenticationBackend()

        # user = None
        # # Try to authenticate the user using any of the provided identifiers
        # if '@' in username:
        #     # Treat input as email
        #     user = custom_auth_backend.authenticate(request=self.context.get('request'),username=username, password=password)
        # elif username.isdigit():
        #     # Treat input as mobile number
        #     user = custom_auth_backend.authenticate(request=self.context.get('request'),username=username, password=password)
        # else:
        #     user = custom_auth_backend.authenticate(request=self.context.get('request'), username=username,
        #                                             password=password)
        # user = auth.authenticate(username=username, password=password)
        user = custom_auth_backend.authenticate(request=self.context.get('request'), username=username,password=password)
        print("ISER", user)

        if device_type == 0:
            raise serializers.ValidationError('Device type is required')

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        tokens = user.tokens()
        # role = user.findRole()
        if settings.SINGLE_MOBILE_DEVICE_PER_USER:
            mobile_devices_count = Device.objects.filter(
                user=user,
                type__in=[1, 2],
                is_active=True,
            ).count()
            devices = Device.objects.filter(
                user=user,
                uuid=device_uuid,
                type=device_type,
                is_active=True)

            if (mobile_devices_count == 0 and device_type != 3) or (
                    device_type == 3 and devices.count() == 0):  # First Mobile device or New Web device

                device, dc = Device.objects.get_or_create(
                    user=user,
                    uuid=device_uuid,
                    is_active=True,
                    defaults={
                        'name': device_name,
                        'type': device_type,
                    }
                )
            elif mobile_devices_count > 0 and device_type != 3 and devices.count() == 0:  # other new Mobile device
                device, dc = Device.objects.get_or_create(
                    user=user,
                    uuid=device_uuid,
                    is_active=False,
                    defaults={
                        'name': device_name,
                        'type': device_type,
                    }
                )
                raise AuthenticationFailed('This device not allowed, contact admin')
            else:  # old Active Devices
                device = devices[0]
        else:
            device, dc = Device.objects.get_or_create(
                user=user,
                uuid=device_uuid,
                is_active=True,
                defaults={
                    'name': device_name,
                    'type': device_type,
                })

        if user.is_superuser == True:
            userValue = True
        elif user.is_staff == True:
            userValue = True
        elif user.is_agent == True:
            userValue = True
        elif user.is_branch == True:
            userValue = True
        elif user.is_customer == True:
            userValue = True

        if not userValue == True and not ((device.type != 3 and (user.deviceaccess == 1 or user.deviceaccess == 3)) or (
                device.type == 3 and (user.deviceaccess == 2 or user.deviceaccess == 3))):
            raise AuthenticationFailed('This device type not allowed, contact admin')

        device.fcmtoken = device_fcmtoken
        device.apntoken = device_apntoken
        device.accesstoken = tokens['access']
        device.save()

        group_name = user.groups.all()[0].name if user.groups.count() > 0 else ""
        return {
            'full_name': user.first_name + " " + user.last_name,
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.phone,
            # 'role': role,
            'group_name': group_name,
            'tokens': user.tokens,
        }

class OTPRequestSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255, min_length=10)

    class Meta:
        model = User
        fields = ['username','otp']

    def validate(self, attrs):
        username = attrs.get('username', '')

        try:
            user = User.objects.get(
                Q(  
                    Q(phone=username) 
                ) &
                Q(is_active = True)
            )

        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid credentials, try again')
        # except:
        #     raise AuthenticationFailed('Invalid credentials, Contact Admin')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
 
        user.otp = get_random_string(4, allowed_chars= string.digits)
        user.save()
        words = {'otp':user.otp  }
        sdata = {'to_phone': username, 'message':  SMS.loginotp.format(**words) }

        url="http://bhashsms.com/api/sendmsg.php?user =Annapurna Marriages&pass=123456 & sender = BHASH -(Promotional) & phone ="+str(username) +"& text = "+user.otp +"& priority = Priority & stype = smstype"

        # url = "https://www.fast2sms.com/dev/bulkV2"
        #
        # # payload = "variables_values=" + otp + "&route=otp&numbers=" + str(user.mobile)
        # payload = "variables_values=" + user.otp + "&route=otp&numbers=" + str(username)
        # headers = {
        #     'authorization': "PBoE0k23fkxnefwWFhDgS50vNxBstzmlT3eJC7FhVfczMG9hdws4jIZ3a9PP",
        #     'Content-Type': "application/x-www-form-urlencoded",
        #     'Cache-Control': "no-cache",
        # }

        response = requests.request("POST", url)

        # Util.send_sms(sdata)

        return {
            'username': user.phone,
            'otp':user.otp ,
            
        }

class OTPResendSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=255, min_length=10)

    class Meta:
        model = User
        fields = ['username','otp']

    def validate(self, attrs):
        username = attrs.get('username', '')

        try:
            user = User.objects.get(
                Q(  
                    Q(phone=username) 
                    # & Q(is_phone_verified=True) # removed to do login witrhout phone_verified  
                ) &
                Q(is_active = True)
            )

        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')

        
        user.otp = get_random_string(4, allowed_chars= string.digits)
        user.save()
        words = {'otp':user.otp  }
        sdata = {'to_phone': username, 'message':  SMS.loginotp.format(**words) }
        Util.send_sms(sdata)

        
        return {
            'username': user.phone,
            'otp':user.otp ,
        }



class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    device_uuid = serializers.CharField(max_length=1000, write_only=True)
    device_type = serializers.ChoiceField(choices=Device.DEVICETYPE_CHOICES, write_only=True)
    access = serializers.CharField(read_only=True)

    token_class = RefreshToken

    def validate(self, attrs):
        # user = self.context['request'].user
        refresh = self.token_class(attrs["refresh"])

        access_token = str(refresh.access_token)

        data = {"access": access_token}

        jwtauthentication = JWTAuthentication()
        validated_token = jwtauthentication.get_validated_token(access_token)
        user = jwtauthentication.get_user(validated_token)

        device_uuid = attrs['device_uuid']
        device_type = attrs['device_type']
        devices = Device.objects.filter(
            user=user,
            uuid= device_uuid,
            type= device_type,
            is_active= True,
        ).update(
            accesstoken= access_token,
        )

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

            data["refresh"] = str(refresh)

        return data

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=68, min_length=6, required=True)
    old_password = serializers.CharField(write_only=True,max_length=68, min_length=6, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password',)


    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance



class EmailVerificationSerializer(serializers.Serializer):

    token = serializers.CharField()
    
    def validate(self, data):
        try:
            payload = jwt.decode(data['token'],settings.SECRET_KEY, 'HS256')
            user = User.objects.get(id=payload['user_id'])
            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
        except jwt.ExpiredSignatureError as identifier:
            raise serializers.ValidationError({'error': 'Activation Expired'})
        except jwt.exceptions.DecodeError as identifier:
            raise serializers.ValidationError({'error': 'Invalid token'})
        
        return data

    class Meta:

        fields = ('token',)


    
class GroupdetailsSerializer(serializers.ModelSerializer):

    reportingto_name= serializers.SerializerMethodField()

    def get_reportingto_name(self, obj):
        return obj.reportingto.name if obj.reportingto else ''


    class Meta:
        model =Groupdetails
        read_only_fields =()
        fields=('group','reportingto', 'reportingto_name' )


class GroupSerializer(serializers.ModelSerializer):

    permission_ids = serializers.ListField(write_only=True, child=serializers.PrimaryKeyRelatedField(write_only=True, queryset=Permission.objects.all()), )
    groupdetails= GroupdetailsSerializer(many=False, read_only=True)
    reportingto_id = serializers.PrimaryKeyRelatedField(write_only=True, source='reportingto', queryset=Group.objects.all())


    class Meta:
        model = Group
        read_only_fields = [ 'permissions','groupdetails']
        fields = ['id', 'name', 'permissions', 'permission_ids','reportingto_id','groupdetails']

    def create(self, validated_data):
        if 'permission_ids' in validated_data:
            validated_data['permissions'] = validated_data.pop('permission_ids')
        
        reportingto = None
        if 'reportingto' in validated_data:
            reportingto = validated_data.pop('reportingto')

        group = super().create(validated_data)

        if reportingto != None:
            Groupdetails.objects.create( group=group, reportingto=reportingto)
               
        return group

    def update(self, instance, validated_data):
        if 'permission_ids' in validated_data:
            validated_data['permissions'] = validated_data.pop('permission_ids')
  
        
        reportingto = None
        if 'reportingto' in validated_data:
            reportingto = validated_data.pop('reportingto')

        group = super().update(instance, validated_data)
        
        if reportingto != None:
            
            Groupdetails.objects.update_or_create( group=group,defaults={'reportingto':reportingto})
        
        return group

class PermissionJoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class GroupMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')



class UserGroupSerializer(serializers.ModelSerializer):

    user_permissions = PermissionJoinSerializer(many=True)
    groups = GroupMiniSerializer(many=True)
    
    class Meta:
        model = User
        fields = '__all__'

class GroupMini2Serializer(serializers.ModelSerializer):
    permission_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Permission.objects.all())

    class Meta:
        model = Group
        read_only_fields = [  'name',]
        fields = ('id', 'name','permission_id')

class PermissionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = PermissionDetail
        fields = ( 'id', 'name', )

class ContentTypeSerializer(serializers.ModelSerializer):   
    permissions = serializers.SerializerMethodField('get_permissions')
    
    def get_permissions(self, contenttype):
        qs = Permission.objects.filter(content_type=contenttype)
        serializer = PermissionJoinSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = ContentType
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    permissiondetails = PermissionDetailSerializer(many=False)

    class Meta:
        model = Permission
        fields = ( 'id', 'name', 'codename', 'content_type', 'permissiondetails', )


class ContentTypeDetailSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField('get_permissions')
    contenttype = ContentTypeSerializer(many=False)
    
    def get_permissions(self, obj):
        qs = Permission.objects.filter(content_type=obj.contenttype, permissiondetails__hide=False )
        serializer = PermissionSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = ContentTypeDetail
        fields = ( 'id', 'name', 'contenttype', 'permissions')


class DjangoAppSerializer(serializers.ModelSerializer):

    contenttypedetails = serializers.SerializerMethodField('get_contenttypedetails')
    
    def get_contenttypedetails(self, obj):
        qs = ContentTypeDetail.objects.filter(app=obj, hide=False)
        serializer = ContentTypeDetailSerializer(instance=qs, many=True)
        return serializer.data


    class Meta:
        model = DjangoApp
        fields = ( 'id', 'name', 'app_label', 'contenttypedetails')

class DeviceLogSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(many=False, read_only=True)
    device_id = serializers.PrimaryKeyRelatedField(write_only=True, required=False, source='device', queryset=Device.objects.filter(status=1,))
    user = UserMiniSerializer(many = False, read_only=True)


    class Meta:
        model = DeviceLog
        fields = ( 'device','device_id','user','ip_address','login','logout' )
