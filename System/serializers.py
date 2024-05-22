from urllib import request
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from pkg_resources import require

from Common.LexerBySly import formula_validator
User = get_user_model()
from django.utils import timezone

import string
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable
from django.utils.crypto import get_random_string

from rest_framework import serializers, permissions
from Users.models import User
from Users.serializers import PermissionJoinSerializer, UserMiniSerializer
from .models import Menu, Submenu, Menuitem, Notification, NotificationUsers, Backup, Restore, Attachment,Formula, FormulaUpdate, ActivityLog, FormulaVariables,TemporaryVerification, ACTION_TYPES_CHOICES, SEEN_CHOICES, Error

from Common.storage_backends import DBBackupMediaStorage
media_storage = DBBackupMediaStorage()


from Common.Constants import Note, Email, SMS
from Common.utils import Util

from rest_framework import status


class SubmenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Submenu
        fields = ('id', 'code', 'name', 'sequence', 'icon', 'click', 'submenu' )

class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        # fields = ('id', 'code', 'name', 'submenus', 'menuitems')
        fields = '__all__'

class MenuitemSerializer(serializers.ModelSerializer):
    permission = PermissionJoinSerializer(many=False,  read_only=True)
    menu = MenuSerializer(many=False,  read_only=True)
    submenu = SubmenuSerializer(many=False,  read_only=True)
    menu_id = serializers.PrimaryKeyRelatedField(write_only=True, source='menu', queryset=Menu.objects.all())
    submenu_id = serializers.PrimaryKeyRelatedField(write_only=True, source='submenu',  queryset=Submenu.objects.all(), required=False,)


    class Meta:
        model = Menuitem
        fields = '__all__'
        
class UserMenuitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menuitem
        fields = ('id', 'title', 'icon', 'link', 'sequence', 'click')

class RecursiveField(serializers.ModelSerializer): 
    def to_representation(self, value):
        serializer_data = UserSubmenuSerializer(value, context=self.context).data
        return serializer_data
    class Meta:
            model = Submenu
            fields = '__all__'


class UserSubmenuSerializer(serializers.ModelSerializer):
    menuitems = serializers.SerializerMethodField('get_menuitems')
    submenus = serializers.SerializerMethodField()


    def get_menuitems(self, submenu):

        filters= {}
        user = self.context['request'].user
        if user.is_superuser:
            pass
        else:
            l = user.get_all_permissions()
            l_as_list = list(l)
            allPermissions =  l_as_list
            allScreenPermissions =  list(map(lambda x: x.split(".")[-1], l_as_list))
            filters['permission__codename__in'] = allScreenPermissions
        qs = Menuitem.objects.filter(submenu=submenu, **filters )
        serializer = UserMenuitemSerializer(instance=qs, many=True)
        return serializer.data
    
    def get_submenus(self, obj):
        queryset = Submenu.objects.filter( submenu= obj.id).order_by('sequence')
        request = self.context['request']
        return RecursiveField(queryset, many=True,  read_only=True, context=self.context).data
        
    class Meta:
        model = Submenu
        fields = ('id', 'code', 'name', 'menuitems', 'sequence', 'icon', 'click', 'submenus')

class UserMenuSerializer(serializers.ModelSerializer):
    submenus = serializers.PrimaryKeyRelatedField(many=True,  read_only=True)
    submenus = UserSubmenuSerializer(many=True,  read_only=True)
    menuitems = serializers.SerializerMethodField('get_menuitems')

    def get_menuitems(self, menu):
        filters= {}
        user = self.context['request'].user
        if user.is_superuser:
            pass
        else:
            l = user.get_all_permissions()
            l_as_list = list(l)
            allPermissions =  l_as_list
            allScreenPermissions =  list(map(lambda x: x.split(".")[-1], l_as_list))
            filters['permission__codename__in'] = allScreenPermissions
            print(allScreenPermissions)
        qs = Menuitem.objects.filter(submenu__isnull=True, menu=menu, **filters).order_by('sequence')
        serializer = UserMenuitemSerializer(instance=qs, many=True)
        return serializer.data
        # return self.context['request'].user.get_all_permissions()

    class Meta:
        model = Menu
        fields = '__all__'



class NotificationSerializer(serializers.ModelSerializer):
    createdon=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",input_formats=['%Y-%m-%d',], required = False)
    class Meta:
        model = Notification
        readonly = ['subject', 'body', 'type', 'ref',  'createdon']
        fields = ('id', 'subject', 'body', 'type', 'ref',  'createdon')

    def create(self, validated_data): 
        obj = super().create(validated_data)

        return obj
    

class NotificationUsersSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(many = False,  read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, source='user', queryset= User.objects.filter(is_active=True,))
    notification = NotificationSerializer(many=False, read_only=True)
    notification_id = serializers.PrimaryKeyRelatedField(write_only=True, source='notification', required=False, queryset=Notification.objects.filter(status=1,))
    seen = serializers.ChoiceField(choices=SEEN_CHOICES, )
    seen_name =  serializers.SerializerMethodField()

    def get_seen_name(self, obj):
        return obj.get_seen_display()

    class Meta:
        model = NotificationUsers
        fields = ( 'user', 'user_id', 'notification', 'notification_id', 'seen', 'seen_name', 'seen_time',)


    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        notification = validated_data.get('notification',None)

        obj = super().create(validated_data)

        return obj



class BackupSerializer(serializers.ModelSerializer):
    createdby_user = UserMiniSerializer(many=False, read_only=True)


    class Meta:
        model = Backup
        read_only_fields = ['code', 'createdon', 'createdby_user']
        fields = ('id', 'code', 'name', 'createdon', 'createdby', 'createdby_user')

class RestoreSerializer(serializers.ModelSerializer):
    createdby_user = UserMiniSerializer(many=False, read_only=True)
    file_url = serializers.SerializerMethodField()


    def get_file_url(self, obj):
        try:
            return media_storage.url(obj.name)
        except:
            return obj.name

    class Meta:
        model = Restore
        read_only_fields = ['code', 'createdon', 'createdby_user']
        fields = ('id', 'code', 'name', 'file_url', 'createdon', 'createdby', 'createdby_user')


class ResetDatabaseSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=100, required=True, allow_blank=False, write_only=True, )
    contenttype_ids = serializers.ListField(write_only=True, child=serializers.PrimaryKeyRelatedField(write_only=True, queryset=ContentType.objects.all()), required=False)

    
    def validate(self, attrs):
        password = attrs.get('password', '')
        user = self.context['request'].user

        if password != '':
            
            if not user.is_superuser:
                raise serializers.ValidationError("You are not allowed to reset the database")

            if not user.check_password(password):
                raise serializers.ValidationError({"password": "Password check failed, try again."})

        return super().validate(attrs)


    class Meta:
        read_only_fields = []
        fields = ( 'password', 'contenttype_ids', )

class BackupValidationserializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=100, required=True, allow_blank=False, write_only=True, )
    file_url = serializers.SerializerMethodField()


    def get_file_url(self, obj):
        try:
            return media_storage.url(obj.name)
        except:
            return obj.name

    
    def validate(self, attrs):
        password = attrs.get('password', '')
        user = self.context['request'].user

        if password != '':
            
            if not user.check_password(password):
                raise serializers.ValidationError({"password": "Password check failed, try again."})

        return super().validate(attrs)
    


    class Meta:
        model= Backup
        read_only_fields = []
        fields = ( 'password', 'file_url' )

    

        
class AttachmentSerializer(serializers.ModelSerializer):
    createdby_user = UserMiniSerializer(many=False, read_only=True)
    file_thumbnail_url = serializers.SerializerMethodField()
    
    def get_file_thumbnail_url(self, obj):
        
        try:
            url = obj.file_thumbnail.url
        except Exception as e:
            # print('=====================================================',e,)
            url = "static/images/thumbnail/default_no_file.png"

        res =self.context['request'].build_absolute_uri(url)
        
        return res

    class Meta:
        model = Attachment
        read_only_fields = ['createdon', 'createdby_user']
        fields = ('id', 'file', 'createdon','file_thumbnail_url', 'createdby', 'createdby_user')

        
class AttachmentMiniSerializer(serializers.ModelSerializer):

    file_thumbnail = serializers.SerializerMethodField()
    
    def get_file_thumbnail(self, obj):
        
        try:
            url = obj.file_thumbnail.url
        except Exception as e:
            # print('=====================================================',e,)
            url = "static/images/thumbnail/default_no_file.png"

        res =self.context['request'].build_absolute_uri(url)
        
        return res

    class Meta:
        model = Attachment
        read_only_fields = ['createdon', 'createdby_user',]
        fields = ('id','file', 'createdon','file_thumbnail',)



class FormulaSerializer(serializers.ModelSerializer):
    variables = serializers.ListField(child = serializers.CharField(), write_only=True, required=True )
    
    def validate_formula(self, value):
        res = formula_validator( value, )
        if res['error']:
            raise serializers.ValidationError(res)
        return value
        

    class Meta:
        model = Formula
        read_only_fields = ['createdon', 'createdby_user']
        fields = ('id', 'code','name','formula','variables')


    def create(self, validated_data):
        user = self.context['request'].user

        variables = validated_data.pop('variables',)
        print(variables)

        instance = super().create(validated_data)

        print(instance, instance.formula, user)
        FormulaUpdate.objects.create(formula=instance, formula_txt = instance.formula,  createdby= user)

        for variable in variables:
            FormulaVariables.objects.create(formula=instance,   name = variable  )

 
        return instance



    def update(self, instance, validated_data):
        user = self.context['request'].user
        
        variables = validated_data.pop('variables',)
        if validated_data['formula'] != instance.formula:
            FormulaUpdate.objects.create(formula=instance, formula_txt = validated_data['formula'], createdby= user )

        
        FormulaVariables.objects.filter(formula=instance).delete() 
        
        for variable in variables:
            FormulaVariables.objects.create(formula=instance,   name = variable  )

       
        formula = super().update(instance, validated_data,) 
        
        return formula




class FormulaValidationSerializer(serializers.Serializer):
    formula = serializers.CharField(required = True)

    class Meta:
        read_only_fields = []
        fields = ('formula',)


        

class FormulaValidation2Serializer(serializers.Serializer):
    code = serializers.CharField(required = True)
    variables = serializers.JSONField(required = True)

    def validate_code(self, value):
        count = Formula.objects.filter(code= value ).count()
        if count == 0:
            raise serializers.ValidationError({"code": "This code is not alowed."})
        return value

    class Meta:
        read_only_fields = []
        fields = ('code','variables')



class FormulaVariablesSerializer(serializers.ModelSerializer):
    formula = FormulaSerializer(many=False, read_only=True)
    formula_id = serializers.PrimaryKeyRelatedField(write_only=True, source='formulas', queryset=Formula.objects.filter(status=1,))
    
    def validate_new_formula(self, value):
        res = formula_validator( value, )
        if res['error']:
            raise serializers.ValidationError(res)
        return value

    class Meta:
        model = FormulaVariables
        read_only_fields = []
        fields = ('name','description','active','formula','formula_id')



class FormulaUpdateSerializer(serializers.ModelSerializer):
    formula = FormulaSerializer(many=False, read_only=True)
    formula_id = serializers.PrimaryKeyRelatedField(write_only=True, source='formulas', queryset=Formula.objects.filter(status=1,))
    
    def validate_new_formula(self, value):
        res = formula_validator( value, )
        if res['error']:
            raise serializers.ValidationError(res)
        return value

    class Meta:
        model = FormulaUpdate
        read_only_fields = ['createdon', 'createdby_user']
        fields = ( 'formula_txt','formula','formula_id')



class ActivityLogSerializer(serializers.ModelSerializer):
    user = UserMiniSerializer(many = False, read_only=True)
    type = serializers.ChoiceField(choices=ACTION_TYPES_CHOICES, )
    type_name =  serializers.SerializerMethodField()

    def get_type_name(self, obj):
        return obj.get_type_display()

    class Meta:
        model = ActivityLog
        read_only_fields = [ 'createdon',]
        fields = ( 'id', 'user',  'type', 'type_name', 'tablename', 'recordcode', 'createdon',  )



class ActivityLogMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = ('id', 'tablename')



class SmsSerializer(serializers.Serializer):
    to_phone = serializers.CharField( max_length=10)
    message = serializers.CharField(max_length=255)

    class Meta:
        fields = ( 'to_phone','message',)



class ErrorSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Error
        fields = ( 'id',   'errorcode', 'requestbody','error_url'   )


class TemporaryOTPRequestSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=255, min_length=10)

    class Meta:
        model = TemporaryVerification
        fields = ['mobile',]

    
    def create(self, validated_data):
        
        otp = get_random_string(4, allowed_chars= string.digits)
        instance, is_created = TemporaryVerification.objects.update_or_create( mobile = validated_data['mobile'], defaults= { 'otp': otp})

        return instance

class TemporaryVerifyOTPSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = TemporaryVerification
        fields = ['mobile', 'otp',]

    def validate(self, attrs):

        otp = attrs.get('otp', '')
        mobile = attrs.get('mobile', '')

        instance =  TemporaryVerification.objects.get(mobile = mobile)

        if instance.otp == otp:
           
            instance.is_phone_verified = True
            instance.save()

        else:
            raise NotAcceptable('Invalid OTP, try again')       

        return Response({'message':'phone number verified successfully'},status=status.HTTP_200_OK )   