from django import forms
from django.utils.translation import gettext_lazy as _

from .models import LabelModel


class LabelModelForm(forms.ModelForm):

    class Meta:
        model = LabelModel
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control mb-2', 'placeholder': _('Name')},
            ),
        }
