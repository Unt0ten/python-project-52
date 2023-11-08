from django.contrib import admin
from django.contrib.admin import DateFieldListFilter

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'date_joined')
    search_fields = ['username', 'date_joined']
    list_filter = (('date_joined', DateFieldListFilter),)
