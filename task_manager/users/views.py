from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist
# gettext_lazy


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'users/index.html', context={'users': users})


class UserFormCreateView(View):

    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        return render(request, 'users/create.html', {'form': user_form})

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST)
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            messages.warning(
                request,
                _('A user with the same name already exists.')
                )
            return render(request, 'users/create.html', {'form': user_form})

        except ObjectDoesNotExist:
            if user_form.is_valid():
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                messages.success(
                    request, _('Your profile has been successfully created!')
                )
                return redirect('login')

            messages.warning(
                request,
                _('Сheck the correctness of data entry.')
            )
            return render(request, 'users/create.html', {'form': user_form})


class UserFormUpdateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = UserForm(instance=user)
        return render(
            request,
            'users/update.html',
            {'form': form, 'user_id': user_id}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        form = UserForm(request.POST, instance=user)
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
        user = User.objects.get(id=user_id)
        return render(
            request,
            'users/delete.html',
            {'user_id': user_id, 'user': user}
        )

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
            messages.success(
                request,
                _('User deleted successfully!'))
        return redirect('users')
