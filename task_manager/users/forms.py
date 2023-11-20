from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

PASSWORD1 = forms.CharField(
    help_text=_('Your password must contain at least 3 characters.'),
    label=_('Password'),
    widget=forms.PasswordInput(
        attrs={'placeholder': _('Password'), 'class': 'form-control mb-3'}
    )
)
PASSWORD2 = forms.CharField(
    help_text=_('Enter the same password as before, for verification.'),
    label=_('Password confirmation'),
    widget=forms.PasswordInput(
        attrs={
            'placeholder': _('Password confirmation'),
            'class': 'form-control mb-3'
        }
    )
)
WIDGETS = {
    'first_name': forms.TextInput(
        attrs={
            'class': 'form-control mb-2',
            'placeholder': _('Fist name'),
        },
    ),
    'last_name': forms.TextInput(
        attrs={
            'class': 'form-control mb-2',
            'placeholder': _('Last name'),
        },
    ),
    'username': forms.TextInput(
        attrs={
            'class': 'form-control mb-2',
            'placeholder': _('Username'),
        },
    ),
}


class CustomUserCreationForm(UserCreationForm):
    password1 = PASSWORD1
    password2 = PASSWORD2

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
        ]
        widgets = WIDGETS


class CustomUserChangeForm(UserChangeForm):
    password1 = PASSWORD1
    password2 = PASSWORD2

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
        ]
        widgets = WIDGETS
