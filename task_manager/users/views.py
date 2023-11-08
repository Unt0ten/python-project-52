from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils.translation import gettext as _

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        return render(request, 'users/index.html', context={'users': users})


class UserFormCreateView(View):

    def get(self, request, *args, **kwargs):
        user_form = CustomUserCreationForm()
        return render(request, 'users/create.html', {'form': user_form})

    def post(self, request, *args, **kwargs):
        user_form = CustomUserCreationForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            messages.success(
                request, _('Your profile has been successfully created!')
            )
            return redirect('login')

        return render(request, 'users/create.html', {'form': user_form})


class UserFormUpdateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = CustomUser.objects.get(id=user_id)
        form = CustomUserChangeForm(instance=user)
        return render(
            request,
            'users/update.html',
            {'form': form, 'user_id': user_id}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = CustomUser.objects.get(id=user_id)
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, _('User successfully changed'))
            return redirect('users')
        return render(
            request,
            'users/update.html',
            {'form': form, 'user_id': user_id}
        )


class UserFormDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = CustomUser.objects.get(id=user_id)
        return render(
            request,
            'users/delete.html',
            {'user_id': user_id, 'user': user}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = CustomUser.objects.get(id=user_id)
        if user:
            user.delete()
            messages.success(
                request,
                _('User deleted successfully!'))
        return redirect('users')


class LoginUser(View):

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm
        return render(request, 'users/login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, _('You are logged in'))
            return redirect('index')

        return render(request, 'users/login.html', {'form': form})

    def logout_user(self):
        logout(self)
        messages.success(self, _('You are logged out'))
        return redirect('/')
