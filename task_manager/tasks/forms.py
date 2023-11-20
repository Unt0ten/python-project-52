from django import forms
from django.utils.translation import gettext_lazy as _

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
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control mb-2', 'placeholder': _('Name')},
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control mb-2',
                    'placeholder': _('Description')
                }
            ),
            'status': forms.Select(
                attrs={'class': 'form-control mb-2 form-select'}
            ),
            'executor': forms.Select(
                attrs={'class': 'form-control mb-2 form-select'}
            ),
            'labels': forms.SelectMultiple(
                attrs={'class': 'form-control mb-2'}
            )
        }
