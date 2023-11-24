from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.views import View
from django.utils.translation import gettext as _
from django.urls import reverse_lazy

from task_manager.mixins_login import CustomLoginRequiredMixin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .mixins import CustomAccessMixin


class UsersView(ListView):

    template_name = 'users/users.html'
    model = User
    context_object_name = 'users'


class UserFormCreateView(CreateView):

    template_name = 'users/create.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(
            self.request, _('Your profile has been successfully created!')
        )
        return super().form_valid(form)


class UserFormUpdateView(
    CustomLoginRequiredMixin,
    CustomAccessMixin,
    UpdateView
):
    model = User
    template_name = 'users/update.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('users')

    def form_valid(self, form):
        messages.success(self.request, _('User successfully changed'))
        return super().form_valid(form)


class UserFormDeleteView(
    CustomLoginRequiredMixin,
    CustomAccessMixin,
    DeleteView
):
    model = User
    template_name = 'users/delete.html'
    success_url = 'users'

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.delete()
        messages.success(
            self.request,
            _('User deleted successfully!'))
        return redirect('users')
        # self.object = self.get_object()
        # success_url = self.get_success_url()
        # try:
        #     self.object.delete()
        #     messages.success(
        #         self.request,
        #         _('User deleted successfully!')
        #     )
        # except ProtectedError:
        #     messages.warning(
        #         self.request,
        #         _('User deleted successfully!')
        #     )
        # finally:
        #     return redirect(success_url)


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
