from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import TaskModel


@admin.register(TaskModel)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'status',
        'executor',
        'author',
        'created_at'
    )
    search_fields = [
        'name',
        'description',
        'status',
        'executor',
        'author',
        'created_at',
    ]
    list_filter = (('created_at', DateFieldListFilter),)
