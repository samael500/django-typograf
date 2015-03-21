from django.db import models
from django.test import TestCase

from django_typograf.models import TypografModel
from django_typograf.exceptions import TypografFieldError


class TypografTests(TestCase):

    """ Test typograf models """

    def test_error_int_field(self):
        """ Check is error raises if not text field typografed """
        with self.assertRaises(TypografFieldError):

            class TestAppModelErr(TypografModel):
                integer = models.IntegerField(blank=True, null=True)

                class Meta:
                    typograf = ('integer', )

        class TestAppModelOk(TypografModel):
            text = models.TextField(blank=True, null=True)

            class Meta:
                typograf = ('text', )
