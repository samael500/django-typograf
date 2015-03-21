from django.contrib import admin
from test_app.models import TestAppModel

from django_typograf.admin import TypografAdmin


class TestAppModelAdmin(TypografAdmin):

    """ Admin class for hide typograf fields from admin site """


admin.site.register(TestAppModel, TestAppModelAdmin)
