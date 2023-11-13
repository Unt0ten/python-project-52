from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import TaskModel


@admin.register(TaskModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'status',
        'executor',
    )
    search_fields = [
        'name',
        'description',
        'status',
        'executor',
        'author',
    ]
    list_filter = (('date_creation', DateFieldListFilter),)
