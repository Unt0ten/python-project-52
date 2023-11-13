from django.forms import ModelForm

from .models import StatusModel


class StatusModelForm(ModelForm):

    class Meta:
        model = StatusModel
        fields = ['name']
