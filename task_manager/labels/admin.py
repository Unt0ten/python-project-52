from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import LabelModel


@admin.register(LabelModel)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'created_at')
    search_fields = ['name', 'created_at']
    list_filter = (('created_at', DateFieldListFilter),)
