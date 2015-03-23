from django.db import models
from django.db.models.base import ModelBase

from django_typograf.exceptions import TypografFieldError
from django_typograf.utils import make_typograf, get_typograf_field_name, get_typograf_hash_field_name


class TypografModelBase(ModelBase):

    """ Base typograf metaclass """

    def __new__(cls, name, bases, attrs):
        """ On create new object - add helpers field for typograf """
        local_typograf_fields, inherited_typograf_fields = cls.get_typograf_fields(name, bases, attrs)
        # remove typograf param in meta calss
        if ('Meta' in attrs) and hasattr(attrs['Meta'], 'typograf'):
            delattr(attrs['Meta'], 'typograf')
        # create helpers fields for typograf usage
        attrs = cls.create_typograf_fields(local_typograf_fields, attrs)
        # create new object as super
        new_obj = super(TypografModelBase, cls).__new__(cls, name, bases, attrs)
        # update typografed fields of new object
        new_obj._meta.typografed_fields = inherited_typograf_fields + local_typograf_fields

        return new_obj

    @classmethod
    def get_typograf_fields(cls, name, bases, attrs):
        """ Get list fields for typograf it """
        local_typograf_fields = []
        inherited_typograf_fields = []
        # get local typograf fields
        if ('Meta' in attrs) and hasattr(attrs['Meta'], 'typograf'):
            local_typograf_fields = list(attrs['Meta'].typograf)
        # get typograf fields in parent classes
        for base in bases:
            if hasattr(base, '_meta') and hasattr(base._meta, 'typografed_fields'):
                inherited_typograf_fields.extend(list(base._meta.typografed_fields))
        # validate the local_typograf_fields
        for field in local_typograf_fields:
            if field not in attrs:
                raise TypografFieldError(
                    '"{field}" can\'t be typografed cause it is not a field on the model "{name}"'.format(
                        field=field, name=name))

        return local_typograf_fields, inherited_typograf_fields

    @classmethod
    def create_typograf_fields(cls, local_typograf_fields, attrs):
        """Create helpers to the local typografed fields """
        for field_name in local_typograf_fields:
            # check is text field
            field = attrs[field_name]
            if not isinstance(field, (models.CharField, models.TextField)):
                raise TypografFieldError(
                    'Can\'t be typografed field "{field}".'
                    ' This must be a text or char field.'.format(field=field_name))
            # create fields for store typografed text and typografed hash
            typograf_field = models.TextField(blank=True, null=True)
            typograf_field.creation_counter += 0.0001
            typograf_field_hash = models.CharField(max_length=32, blank=True, null=True)
            typograf_field_hash.creation_counter += 0.0001
            # create fields name's
            typograf_field_name = get_typograf_field_name(field_name)
            typograf_field_hash_name = get_typograf_hash_field_name(field_name)
            # update attrs
            attrs.update({typograf_field_name: typograf_field, typograf_field_hash_name: typograf_field_hash})

        return attrs


class TypografModel(models.Model, metaclass=TypografModelBase):

    """ Base typograf model class with typograf meta """

    class Meta:
        abstract = True

    def _make_typograf(self):
        """ Run typograf for each field in typografed_fields """
        typografed_fields = self._meta.typografed_fields
        return make_typograf(self, typografed_fields)

    def save(self, *args, **kwargs):
        """ make typograf before saving """
        self._make_typograf()
        super(TypografModel, self).save(*args, **kwargs)
