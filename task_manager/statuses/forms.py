from django import forms

from .models import StatusModel


class StatusModelForm(forms.ModelForm):

    class Meta:
        model = StatusModel
        fields = ['name']
