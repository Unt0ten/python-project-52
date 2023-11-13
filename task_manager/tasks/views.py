from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.views.generic import CreateView

from task_manager.statuses.models import StatusModel
from .models import TaskModel
from .forms import TaskModelForm
from  .mixins import CustomAccessMixin, CustomLoginRequiredMixin


class SpecificTaskView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'tasks/view_task.html')


class TasksView(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        statuses = StatusModel.objects.all()
        tasks = TaskModel.objects.all()
        # for task in tasks:
        #     print(task.author.get_full_name())
        return render(
            request,
            'tasks/tasks.html',
            {'tasks': tasks, 'users': users, 'statuses': statuses},
        )


class CreateTaskView(CustomLoginRequiredMixin, CreateView):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        statuses = StatusModel.objects.all()
        tasks = TaskModel.objects.all()
        tags = ''
        return render(
            request,
            'tasks/create.html',
            {
                'tasks': tasks,
                'users': users,
                'statuses': statuses,
                'tags': tags
            },
        )

    def post(self, request, *args, **kwargs):
        task_form = TaskModelForm(request.POST)

        if task_form.is_valid():
            print('No')
            task_form.save()
            messages.success(
                request, _('Your task has been successfully created!')
                )
            return redirect('tasks')

        return render(request, 'tasks/create.html', {'form': task_form})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'author': self.request.user.username})
        return kwargs


class UpdateTaskView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'tasks/update.html')


class DeleteTaskView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'tasks/delete.html')
