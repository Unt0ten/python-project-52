from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
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


class CreateTaskView(LoginRequiredMixin, CreateView):

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        form.instance.author = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({
    #         'author': self.request.user if self.request.user.is_authenticated else None,
    #     })
    #     return kwargs

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
            form.save()
            messages.success(
                request, _('Your task has been successfully created!')
                )
            return redirect('tasks')

        return render(request, 'tasks/create.html', {'form': form})


class UpdateTaskView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'tasks/update.html')


class DeleteTaskView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'tasks/delete.html')
