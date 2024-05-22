from . import views
from . import generic_import_export_view
# from . import importviews

from django.urls import path

urlpatterns = [
    path('generic_import/<str:dryrun>', generic_import_export_view.GenericImportView.as_view(), name='GenericImport'), # dryrun ='dryrun' or 'process'
    path('generic_import_models/', generic_import_export_view.GenericImportModelsView.as_view(), name='GenericImportModels'),
    path('generic_export_models/', generic_import_export_view.GenericExportModelsView.as_view(), name='GenericExportModels'), 
    path('generic_export/', generic_import_export_view.GenericExportView.as_view(), name='GenericExport'),
    path('generic_import_2/<str:dryrun>/', generic_import_export_view.ImportView.as_view())

    # path('upload/<str:filename>/', importviews.FileUploadView.as_view()),

]
