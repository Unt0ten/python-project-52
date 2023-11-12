from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import StatusModel


@admin.register(StatusModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'date_creation')
    search_fields = ['name', 'date_creation']
    list_filter = (('date_creation', DateFieldListFilter),)
