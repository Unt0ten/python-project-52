from django.forms import ModelForm

from .models import StatusModel


class StatusModelForm(ModelForm):

    error_messages = {
        "error_messages": "The two password fields didn’t match."
    }

    class Meta:
        model = StatusModel
        fields = ['name']
