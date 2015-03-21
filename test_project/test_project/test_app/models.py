from django.db import models
from django_typograf.models import TypografModel


class TestAppModel(TypografModel):

    """ Simple models for test """

    text = models.CharField(max_length=200, blank=True, null=True)
    text2 = models.TextField(blank=True, null=True)
    integer = models.IntegerField(blank=True, null=True)

    class Meta:
        typograf = ('text', 'text2')
