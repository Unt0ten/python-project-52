from django.views import generic
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from task_manager.statuses.models import StatusModel
from task_manager.labels.models import LabelModel
from task_manager.mixins_login import CustomLoginRequiredMixin
from .models import TaskModel
from .forms import TaskModelForm
from .mixins import CustomAccessMixin


class SpecificTaskView(generic.DetailView):
    model = TaskModel
    template_name = 'tasks/view_task.html'
    context_object_name = 'task'


class TasksView(CustomLoginRequiredMixin, generic.ListView):

    template_name = 'tasks/tasks.html'
    model = TaskModel
    context_object_name = 'tasks'

    def get_queryset(self):
        if not self.request.GET:
            return TaskModel.objects.all()
        filters = Q()
        for key in ['status', 'executor', 'label', 'author']:
            value = self.request.GET.get(key)
            if value:
                if value == 'on':
                    value = self.request.user.id
                elif key == 'label':
                    key = 'labels'
                filters &= Q(**{f'{key}': value})

        return TaskModel.objects.filter(filters)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = StatusModel.objects.all()
        context['executors'] = User.objects.all()
        context['labels'] = LabelModel.objects.all()
        return context


class CreateTaskView(CustomLoginRequiredMixin, generic.CreateView):

    template_name = 'tasks/create.html'
    form_class = TaskModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(
            self.request, _('Your task has been successfully created!')
        )
        return super().form_valid(form)


class UpdateTaskView(CustomLoginRequiredMixin, generic.UpdateView):

    model = TaskModel
    template_name = 'tasks/update.html'
    form_class = TaskModelForm

    def form_valid(self, form):
        messages.success(self.request, _('Task successfully changed'))
        return super().form_valid(form)


class DeleteTaskView(CustomAccessMixin, generic.DeleteView):

    model = TaskModel
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        messages.success(self.request, _('Task deleted successfully!'))
        return super().form_valid(form)
