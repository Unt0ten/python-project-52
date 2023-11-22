from django import forms

from .models import LabelModel


class LabelModelForm(forms.ModelForm):

    class Meta:
        model = LabelModel
        fields = ['name']
