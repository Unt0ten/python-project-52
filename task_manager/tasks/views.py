from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from django.views.generic import CreateView

from task_manager.statuses.models import StatusModel
from .models import TaskModel
from .forms import TaskModelForm
from .mixins import CustomAccessMixin, CustomLoginRequiredMixin


class SpecificTaskView(View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(TaskModel, id=task_id)
        return render(request, 'tasks/view_task.html', {'task': task})


class TasksView(CustomLoginRequiredMixin, View):

    def get_queryset(self):
        if not self.request.GET:
            return TaskModel.objects.all()
        filters = Q()
        for key in ['status', 'executor', 'author']:
            value = self.request.GET.get(key)
            if value:
                if value == 'on':
                    value = self.request.user.id
                filters &= Q(**{f'{key}': value})

        return TaskModel.objects.filter(filters)

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        statuses = StatusModel.objects.all()
        tasks = self.get_queryset()
        return render(
            request,
            'tasks/tasks.html',
            {
                'tasks': tasks,
                'users': users,
                'statuses': statuses,
            },
        )


class CreateTaskView(CustomLoginRequiredMixin, CreateView):

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

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
        form = TaskModelForm(request.POST)
        if form.is_valid():
            self.form_valid(form)
            messages.success(
                request, _('Your task has been successfully created!')
            )
            return redirect('tasks')

        return render(request, 'tasks/create.html', {'form': form})


class UpdateTaskView(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        statuses = StatusModel.objects.all()
        tasks = TaskModel.objects.all()
        tags = ''
        task_id = kwargs.get('pk')
        task = get_object_or_404(TaskModel, id=task_id)
        form = TaskModelForm(instance=task)
        return render(
            request,
            'tasks/update.html',
            {
                'task': task,
                'form': form,
                'task_id': task_id,
                'tasks': tasks,
                'users': users,
                'statuses': statuses,
                'tags': tags
            }
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(TaskModel, id=task_id)
        form = TaskModelForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, _('Task successfully changed'))
            return redirect('tasks')

        return render(
            request,
            'tasks/update.html',
            {'form': form, 'task_id': task_id}
        )


class DeleteTaskView(CustomAccessMixin, View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(TaskModel, id=task_id)
        return render(
            request,
            'tasks/delete.html',
            {'task_id': task_id, 'task': task}
        )

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = get_object_or_404(TaskModel, id=task_id)
        task.delete()
        messages.success(request, _('Task deleted successfully!'))
        return redirect('tasks')
