from import_export import resources
from import_export.mixins import base_formats
from import_export.fields import Field
from import_export.mixins import base_formats
from import_export.widgets import Widget
from django.core.exceptions import ObjectDoesNotExist





class ModelImportExportResource(resources.ModelResource):

    def get_import_fields(self):
        if hasattr(self._meta, 'import_fields'):
            return [self.fields[f] for f in self._meta.import_fields]
        else:
            return super().get_import_fields()



class ChoicesWidget(Widget):
    """
    Widget that uses choice display values in place of database values
    """
    def __init__(self, choices, *args, **kwargs):
        """
        Creates a self.choices dict with a key, display value, and value,
        db value, e.g. {'Chocolate': 'CHOC'}
        """
        self.choices = dict(choices)
        self.revert_choices = dict((v, k) for k, v in self.choices.items())

    def clean(self, value, row=None, *args, **kwargs):
        """Returns the db value given the display value"""
        return self.revert_choices.get(value, value) if value else None

    def render(self, value, obj=None):
        """Returns the display value given the db value"""
        return self.choices.get(value, '')




class PermissionCodeWidget(Widget):
   
    def __init__(self, model, field='pk', *args, **kwargs):
        self.model = model
        self.field = field
        super().__init__(*args, **kwargs)

    def get_queryset(self, value, row, *args, **kwargs):
        return self.model.objects.all()

    def clean(self, value, row=None, *args, **kwargs):
        val = super().clean(value)
        if val:
            args = val.split('.')
            if len(args) > 0:
                return self.get_queryset(value, row, *args, **kwargs).get(content_type__app_label = args[0], codename = args[1])
            else:
                return None
        else:
            return None

    def render(self, value, obj=None):
        if value is None:
            return ""

        if value:
            return '%s.%s' % (value.content_type.app_label, value.codename)
        else:
            return ""

        # attrs = self.field.split('__')
        # for attr in attrs:
        #     try:
        #         value = getattr(value, attr, None)
        #     except (ValueError, ObjectDoesNotExist):
        #         # needs to have a primary key value before a many-to-many
        #         # relationship can be used.
        #         return None
        #     if value is None:
        #         return None

        # return value
