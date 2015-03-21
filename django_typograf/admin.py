from django.contrib import admin
from django_typograf.utils import get_typograf_field_name, get_typograf_hash_field_name


class TypografAdmin(admin.ModelAdmin):

    """ Admin class for hide typograf fields from admin site """

    def _exclude(self, obj=None):
        """ Mark typograf fields as exclude """
        exclude = ()
        if obj:
            exclude += tuple((get_typograf_field_name(field) for field in obj._meta.typografed_fields))
            exclude += tuple((get_typograf_hash_field_name(field) for field in obj._meta.typografed_fields))
        return exclude

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = self.exclude or ()
        self.exclude += self._exclude(obj)
        return super().get_form(request, obj, **kwargs)
