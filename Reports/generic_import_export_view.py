from tablib import Dataset

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.encoding import force_str

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import  GenericAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated, AllowAny

from import_export.formats import base_formats
from import_export.resources import modelresource_factory
from import_export.tmp_storages import TempFolderStorage
from import_export.results import RowResult
from import_export.mixins import ExportViewMixin

from Common.permissions import GetPermission
import pandas as pd





from Reports.serializers import GenericImportExportSerializer, GenericImportSerializer, GenericConfirmImportSerializer, GenericExportSerializer
from .import_export_models import import_models, export_models

def get_model_class(model_name):
    
    model = None
    resource_class = None
    resource = None
    if model_name in import_models.keys() :
        print('model_name:', model_name)
        model = import_models[model_name]['model_class']
        if 'resource_class' in import_models[model_name].keys():
            resource_class = import_models[model_name]['resource_class']
            resource =  resource_class()

    if resource_class == None and model != None:
        resource_class =  modelresource_factory(model)
        resource =  resource_class()

    return (model, resource,)



class GenericExportModelsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        models = export_models.keys()
        return Response(models)


class GenericImportModelsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        models = import_models.keys()
        return Response(models)


class GenericImportView(APIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = GenericImportSerializer
    formats = base_formats.DEFAULT_FORMATS
    from_encoding = "utf-8"

    
    def write_to_tmp_storage(self, import_file, input_format):
        tmp_storage = TempFolderStorage()
        data = bytes()
        for chunk in import_file.chunks():
            data += chunk

        tmp_storage.save(data, input_format.get_read_mode())
        return tmp_storage

    def post(self, request, *args, **kwargs):
        # file_obj = request.data['import_file']
        dryrun = kwargs['dryrun']
        
        model = None
        resource = None

        # dataset = Dataset()
        import_formats = [f for f in self.formats if f().can_import()]

        
        serializer = GenericImportExportSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            model_name = serializer.validated_data['model_name']
            model, resource = get_model_class(model_name)

        if model is None:
            return Response({"error":"Invalid Model type" }, status=400)
        
        
        permission = GetPermission(model._meta.app_label + ".import_"+ model._meta.model_name)()
        if not permission.has_permission(request, self):
            return Response({"error":"You do not have permission to perform this action." }, status=403)


        if resource is None:
            return Response({"error":"Invalid Model Resource type" }, status=400)

        if dryrun == 'dryrun':
            serializer = GenericImportSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                cleaned_data = serializer.validated_data
        elif dryrun == 'process':
            serializer = GenericConfirmImportSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                cleaned_data = serializer.validated_data
        else:
            cleaned_data = {}
            return Response({"error":"Invalid Dryrun type" }, status=400)


        try:
            input_format = import_formats[
                cleaned_data['input_format']
            ]()

            if dryrun == 'dryrun':
                import_file = cleaned_data['import_file']
                tmp_storage = self.write_to_tmp_storage(import_file, input_format)
                import_file_name = import_file.name
            if dryrun == 'process':
                tmp_storage = TempFolderStorage(name=cleaned_data['import_file_name'])
                import_file_name = cleaned_data['import_file_name']

            data = tmp_storage.read(input_format.get_read_mode())
            if not input_format.is_binary() and self.from_encoding:
                data = force_str(data, self.from_encoding)
            
            dataset = input_format.create_dataset(data)

        except UnicodeDecodeError as e:
            return JsonResponse({"error":"Imported file has a wrong encoding: %s" % e })
        except Exception as e:
            return JsonResponse({"error":"%s : %s , encountered while trying to read file: %s" % (type(e).__name__, e, import_file_name)})
        
        try:
            result = resource.import_data(dataset, dry_run=True, raise_errors=False, file_name=import_file_name, )  # Test the import data
        except Exception as e:
            return JsonResponse({"error":"%s : %s , encountered while trying to read file: %s" % (type(e).__name__, e, import_file_name,)})

        context = {}
        context['has_errors'] = result.has_errors()
        context['has_validation_errors'] = result.has_validation_errors()

        context['diff_headers'] = result.diff_headers
        
        context['app_label'] = model._meta.app_label
        context['model_name'] = model._meta.model_name
        context['verbose_name'] = model._meta.verbose_name
        context['verbose_name_plural'] = model._meta.verbose_name_plural
        

        if context['has_errors']:
            context['base_errors'] = []
            context['row_errors'] = []
            for error in result.base_errors:
                
                e = error.error
                e = "%s : %s " % (type(e).__name__, e)
                t = error.traceback,
                t = list(t)
                
                context['base_errors'].append({
                    "error": t,
                    "traceback": t,
                })
            for line, errors in result.row_errors():
                out_errors =[]
                for error in errors:
                    r = error.row.values()
                    r = list(r)
                    e = error.error
                    e = "%s : %s " % (type(e).__name__, e)
                    t = error.traceback,
                    t = list(t)
                    out_errors.append({
                        "error": e,
                        "traceback": t,
                        "row": r,
                    })
                    
                context['row_errors'].append({
                    "line": line,
                    "errors": out_errors,
                })
        elif context['has_validation_errors']:
            context['invalid_rows'] = []
            for row in result.invalid_rows:
                error_list_data = {}
                for field_name, error_list in row.field_specific_errors.items():
                    error_list_data[field_name] = error_list
                if row.non_field_specific_errors:
                    error_list_data["non_field_specific_errors"] = row.non_field_specific_errors

                row_data ={
                    "row": row.number,
                    "errors":{
                        "error_count": row.error_count,
                        "error_list":error_list_data
                    }
                }
                for i in  range(len(result.diff_headers)):
                    row_data[result.diff_headers[i]] = row.values[i]


                context['invalid_rows'].append(row_data)
        elif dryrun == 'dryrun':
            context['valid_rows'] = []
            for row in result.valid_rows():
                row_data ={
                    "import_type": row.import_type,
                }
                for i in range(len(result.diff_headers)):
                    row_data[result.diff_headers[i]] = row.diff[i]
                context['valid_rows'].append(row_data)

            initial = {
                'import_file_name': tmp_storage.name,
                'original_file_name': import_file.name,
                'input_format': cleaned_data['input_format'],
            }
            context['initial'] = initial
        elif dryrun == 'process':
            result = resource.import_data(dataset, dry_run=False, raise_errors=True, file_name=import_file_name, )  # Import the data from the file

            tmp_storage.remove()
            opts = model._meta
            context['success_message'] = 'Import finished, with {} new and ' \
                    '{} updated {}.'.format(result.totals[RowResult.IMPORT_TYPE_NEW],
                                                result.totals[RowResult.IMPORT_TYPE_UPDATE],
                                                opts.verbose_name_plural)


        return JsonResponse(context)


# choices = []
# for i, f in enumerate(formats):
#     choices.append((str(i), f().get_title(),))
# if len(formats) > 1:
#     choices.insert(0, ('', '---'))


def get_export_model_class(model_name):
    
    model = None
    resource_class = None
    filter_backends = None
    queryset = None
    filterset_class = None
    search_fields = None
    ordering_fields = None
    request_filters = []
    permissions = []


    if model_name in export_models.keys() :
        model = export_models[model_name]['model_class']
        if 'resource_class' in export_models[model_name].keys():
            resource_class = export_models[model_name]['resource_class']
        if 'queryset' in export_models[model_name].keys():
            queryset = export_models[model_name]['queryset']
        if 'filter_backends' in export_models[model_name].keys():
            filter_backends = export_models[model_name]['filter_backends']
        if 'filterset_class' in export_models[model_name].keys():
            filterset_class = export_models[model_name]['filterset_class']
        if 'search_fields' in export_models[model_name].keys():
            search_fields = export_models[model_name]['search_fields']
        if 'ordering_fields' in export_models[model_name].keys():
            ordering_fields = export_models[model_name]['ordering_fields']
        if 'request_filters' in export_models[model_name].keys():
            request_filters = export_models[model_name]['request_filters']
        if 'permissions' in export_models[model_name].keys():
            permissions = export_models[model_name]['permissions']
            

    if resource_class == None and model != None:
        resource_class =  modelresource_factory(model)

    return (model, resource_class, queryset, filter_backends, filterset_class, search_fields, ordering_fields, request_filters, permissions)

class GenericExportView(GenericAPIView,ExportViewMixin):
    permission_classes = [IsAuthenticated]
    formats = base_formats.DEFAULT_FORMATS

    def post(self, request, *args, **kwargs):

        
        serializer = GenericImportExportSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            model_name = serializer.validated_data['model_name']
            model, resource_class, queryset, filter_backends, filterset_class, search_fields, ordering_fields, request_filters, permissions  = get_export_model_class(model_name)
        
        if model is None:
            return Response({"error":"Invalid Model type" }, status=400)
        
        permission_check = False
        
        permissions = permissions + [ GetPermission(model._meta.app_label + ".export_"+ model._meta.model_name), GetPermission(model._meta.app_label + ".reports_"+ model._meta.model_name), ]
        for permission in permissions:
            if permission().has_permission(request, self):
                permission_check = True
        
        if not permission_check:
            return Response({"error":"You do not have permission to perform this action." }, status=403)
        
        if resource_class is None:
            return Response({"error":"Invalid Model Resource type" }, status=400)

        if queryset is None:
            return Response({"error":"Queryset not Defined" }, status=400)

        self.model = model
        self.resource_class = resource_class
        queryset = queryset
        
        for request_filter in request_filters:
            queryset = request_filter(request, queryset)
    
        if filter_backends is not None:
            self.filter_backends = filter_backends
        if filterset_class is not None:
            self.filterset_class = filterset_class
        if search_fields is not None:
            self.search_fields = search_fields
        if ordering_fields is not None:
            self.ordering_fields = ordering_fields

        serializer = GenericExportSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            cleaned_data = serializer.validated_data

        formats = self.get_export_formats()

        file_format = formats[
            int(cleaned_data['file_format'])
        ]()

        if hasattr(self, 'filter_queryset'):
            queryset = self.filter_queryset(queryset)

        export_data = self.get_export_data(file_format, queryset)
        content_type = file_format.get_content_type()

        try:
            response = HttpResponse(export_data, content_type=content_type)
        except TypeError:
            response = HttpResponse(export_data, mimetype=content_type)
        response['Content-Disposition'] = 'attachment; filename="%s"' % (
            self.get_export_filename(file_format),
        )

        # post_export.send(sender=None, model=self.model)
        return response



#  New_import type get_model_class_serializers  2



def get_model_class_2(model_name):
    
    
    model = None
    SerializerClass = None
    queryset = None
    if model_name in import_models.keys() :
        print('model_name:', model_name)
        model = import_models[model_name]['model_class']
        SerializerClass = import_models[model_name].get('serializer_class', None )
        queryset = import_models[model_name].get('queryset', None )
        if import_models[model_name].get('import_type',1) == 1:
            model = None


    return (model, SerializerClass, queryset)




class ImportView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated]

    # SerializerClass = GenericImportSerializer
    formats = base_formats.DEFAULT_FORMATS
    from_encoding = "utf-8"

    
    def write_to_tmp_storage(self, import_file, input_format):
        tmp_storage = TempFolderStorage()
        data = bytes()
        for chunk in import_file.chunks():
            data += chunk

        tmp_storage.save(data, input_format.get_read_mode())
        return tmp_storage

    
    def format_row(self, index, row, import_fields, outobj={}, Notfoundlist=[]):
        for field in import_fields:
            try:
                if field.get("is_serializer", False) and not field.get("is_serializer_many", False): # if many False
                    Notfoundlist, outobj[field["key"]] = self.format_row(index, row, field["serializer_fields"], {}, Notfoundlist)

                elif field.get("is_serializer", False) and field.get("is_serializer_many", False): # if many True
                    Notfoundlist, obj = self.format_row(index, row, field["serializer_fields"], {}, Notfoundlist)
                    outobj[field["key"]] = [obj,]

                elif field.get("is_many_to_many", False):
                    value = row[field["label"]]
                    if value != '':
                        value = value.split(',')
                    else:
                        value = []
                    outobj[field["key"]] = value
                else:
                    outobj[field["key"]] = row[field["label"]]

            except KeyError:
                Notfoundlist.append(field["label"]) 
        
        # print(index, len(Notfoundlist))
        return (Notfoundlist, outobj )

    def get_field_by_key(self, import_fields, key):
        return next((sub for sub in import_fields if sub['key'] == key), None)

    def get_instance(self, queryset, import_fields, SerializerClass, row):
        params = {}
        NotFoundKeys2 = []
        for key in self.get_import_id_fields(SerializerClass):
            try:
                field = self.get_field_by_key(import_fields, key)
                params[key] = row[field["label"]]
            except KeyError:
                NotFoundKeys2.append(field["label"]) 
        if params and len(NotFoundKeys2) ==0:
            try:
                return queryset.get(**params), NotFoundKeys2
            except:
                return None, NotFoundKeys2
        else:
            return None, NotFoundKeys2

    def get_import_id_fields(self, SerializerClass):
        if hasattr(SerializerClass.Meta, "import_id_fields"):
            return SerializerClass.Meta.import_id_fields
        else:
            return ( 'id', )

    def import_dataframe(self, model, SerializerClass, queryset, request, df, import_fields, dryrun= True ):
        data_list = []
        has_errors = False
        for index, row in df.iterrows():
            NotFoundKeys, data_obj = self.format_row(index, row, import_fields, {}, [] )
            # queryset = State.objects.all()
            instance, NotFoundKeys2 = self.get_instance(queryset, import_fields, SerializerClass, row)
            # print("instance", instance)
            
            serializer_context = { 'request' : request }

            if len(NotFoundKeys2) > 0:
                has_errors = True
            serializer = SerializerClass(data= data_obj, instance= instance, many= False, context= serializer_context )
            is_valid = serializer.is_valid(raise_exception=False)
            if not is_valid :
                has_errors = True
            elif dryrun == False and has_errors == False:
                serializer.save()
            
            data_list.append({
                # "input": data_obj,
                "import_status":  "New" if instance == None else "Update" ,
                "has_errors": not is_valid,
                "errors": serializer.errors,
                "validated_data": serializer.validated_data,
                "output_data": serializer.data,
                "keys_notfound": NotFoundKeys,
                "import_id_keys_notfound": NotFoundKeys2,
            })
        return (data_list, has_errors)
        
    def post(self, request, *args, **kwargs):
        dryrun = kwargs['dryrun']
        
        model = None
        SerializerClass = None
        queryset = None

        import_formats = [f for f in self.formats if f().can_import()]
        
        serializer = GenericImportExportSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            model_name = serializer.validated_data['model_name']
            model, SerializerClass, queryset = get_model_class_2(model_name)
           
        if model is None:
            return Response({"error":"Invalid Model type" }, status=400)
        
        
        # permission = GetPermission(model._meta.app_label + ".import_"+ model._meta.model_name)()
        # if not permission.has_permission(request, self):
        #     return Response({"error":"You do not have permission to perform this action." }, status=403)


        if SerializerClass is None:
            return Response({"error":"Invalid Model Serializer type" }, status=400)

        if dryrun == 'dryrun':
            serializer = GenericImportSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                cleaned_data = serializer.validated_data
        elif dryrun == 'process':
            serializer = GenericConfirmImportSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                cleaned_data = serializer.validated_data
        else:
            cleaned_data = {}
            return Response({"error":"Invalid Dryrun type" }, status=400)

        try:
            input_format = import_formats[
                cleaned_data['input_format']
            ]()
            # import_file = cleaned_data['import_file']
            # tmp_storage = self.write_to_tmp_storage(import_file, input_format)
            # import_file_name = import_file.name
            # data = tmp_storage.read('r')
            
            if dryrun == 'dryrun':
                import_file = cleaned_data['import_file']
                tmp_storage = self.write_to_tmp_storage(import_file, input_format)
                import_file_name = import_file.name
                original_file_name = import_file.name
            if dryrun == 'process':
                tmp_storage = TempFolderStorage(name=cleaned_data['import_file_name'])
                import_file_name = cleaned_data['import_file_name']
                original_file_name = cleaned_data['original_file_name']
            

            import_fields = SerializerClass.Meta.import_fields

            df = pd.read_csv(tmp_storage.get_full_path() ,keep_default_na = '')
            
        except UnicodeDecodeError as e:
            return JsonResponse({"error":"Imported file has a wrong encoding: %s" % e })
        except Exception as e:
            return JsonResponse({"error":"%s : %s , encountered while trying to read file: %s" % (type(e).__name__, e, import_file_name)})
        
        data_list, has_errors = self.import_dataframe( model, SerializerClass, queryset, request, df, import_fields, dryrun = True )
        # print(data_list)
        initial= {
            'import_file_name': tmp_storage.name,
            'original_file_name': original_file_name,
            'input_format': cleaned_data['input_format'],
        }
        if dryrun == 'process' and has_errors == False:
            data_list = self.import_dataframe( model, SerializerClass, queryset, request, df, import_fields, dryrun = False )

            
        # print("data_list", data_list)

        return Response( {'initial': initial, 'data_list': data_list, "import_fields" : import_fields, "has_errors" : has_errors})