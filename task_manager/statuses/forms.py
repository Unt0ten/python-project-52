from django import forms
from django.utils.translation import gettext_lazy as _

from .models import StatusModel


class StatusModelForm(forms.ModelForm):

    class Meta:
        model = StatusModel
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control mb-2', 'placeholder': _('Name')},
            ),
        }
