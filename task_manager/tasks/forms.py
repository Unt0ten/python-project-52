from django import forms

from .models import TaskModel


class TaskModelForm(forms.ModelForm):

    class Meta:
        model = TaskModel
        fields = [
            'name',
            'description',
            'status',
            'executor',
            'labels'
        ]
