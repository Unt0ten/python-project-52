from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField()
    password_confirmation = forms.CharField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
        ]

    def clean_password_confirmation(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_confirmation']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password_confirmation']
