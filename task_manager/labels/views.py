from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .models import LabelModel
from .forms import LabelModelForm
from task_manager.mixins_login import CustomLoginRequiredMixin
from task_manager.tasks.models import TaskModel


class LabelsView(CustomLoginRequiredMixin, ListView):
    template_name = 'labels/labels.html'
    model = LabelModel
    context_object_name = 'labels'


class CreateLabel(CustomLoginRequiredMixin, CreateView):
    template_name = 'labels/create.html'
    form_class = LabelModelForm

    def form_valid(self, form):
        messages.success(
            self.request, _('Label successfully created')
        )
        return super().form_valid(form)


class UpdateLabel(CustomLoginRequiredMixin, UpdateView):
    model = LabelModel
    form_class = LabelModelForm
    template_name = 'labels/update.html'

    def form_valid(self, form):
        messages.success(
            self.request, _('Label successfully changed')
        )
        return super().form_valid(form)


class DeleteLabel(CustomLoginRequiredMixin, DeleteView):
    model = LabelModel
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')

    def form_valid(self, form):
        label = self.object
        task_status = TaskModel.objects.filter(author_id=label.id)
        if task_status:
            messages.warning(
                self.request, _('Cannot remove label because it is in use')
            )
            return redirect('labels')

        messages.success(self.request, _('Label deleted successfully!'))
        return super().form_valid(form)
