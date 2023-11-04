from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from task_manager.users.models import User
from .forms import UserForm


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
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return redirect('login')

        return render(request, 'users/create.html', {'form': user_form})


class UserFormUpdateView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if request.user.is_authenticated:
            form = UserForm(instance=user)
            return render(request, 'users/update.html', {'form': form, 'user_id':user_id})
        return redirect('login')

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if request.user.is_authenticated:
            form = UserForm(instance=user)
            return render(request, 'users/update.html', {'form': form, 'user_id':user_id})
        return redirect('login')


class UserFormDeleteView(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if request.user.is_authenticated:
            return render(request, 'users/delete.html', {'user_id':user_id, 'user': user})
        return redirect('login')

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        user = User.objects.get(id=user_id)
        if user:
            user.delete()
        return redirect('users')
