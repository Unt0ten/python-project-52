from django import forms

from .models import TaskModel


class TaskModelForm(forms.ModelForm):

    # def __init__(self, user_info, *args, **kwargs):
    #     self.user_info = user_info
    #     super().__init__(*args, **kwargs)
    #
    # def save(self, *args, **kwargs):
    #     self.instance.author = self.user_info
    #     return super().save(*args, **kwargs)

    class Meta:
        model = TaskModel
        fields = [
            'name',
            'description',
            'status',
            'executor',
        ]
        # widgets = {'author': forms.HiddenInput()}
