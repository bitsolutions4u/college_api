import os.path
from pyparsing import empty

from rest_framework import serializers
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from .import_export_models import *






class GenericImportExportSerializer(serializers.Serializer):
    model_name = serializers.CharField(required= True, allow_blank=False )

    class Meta:
        fields = ('model_name', )

class GenericImportSerializer(serializers.Serializer):
    import_file = serializers.FileField(required= True, )
    input_format = serializers.IntegerField(required= True, min_value=0, max_value=5 )

    class Meta:
        fields = ('import_file', 'input_format', )

class GenericConfirmImportSerializer(serializers.Serializer):
    import_file_name = serializers.CharField(required= True,)
    original_file_name = serializers.CharField(required= True,)
    input_format = serializers.IntegerField(required= True, min_value=0, max_value=5 )
    
    def validate_import_file_name(self, value):
        if not value:
            raise serializers.ValidationError("import_file_name required")
        value = os.path.basename(value)
        return value

    class Meta:
        fields = ('import_file_name', 'original_file_name', 'input_format', )



class GenericExportSerializer(serializers.Serializer):
    file_format = serializers.IntegerField(required= True, min_value=0, max_value=5 )

    class Meta:
        fields = ('file_format', )