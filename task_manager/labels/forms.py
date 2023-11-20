from django.forms import ModelForm

from .models import LabelModel


class LabelModelForm(ModelForm):

    class Meta:
        model = LabelModel
        fields = ['name']
