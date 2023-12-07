from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .models import LabelModel
from .forms import LabelModelForm
from task_manager.mixins import CustomLoginRequiredMixin, CheckDependencyMixin


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


class DeleteLabel(CustomLoginRequiredMixin, CheckDependencyMixin, DeleteView):
    model = LabelModel
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels')
    msg_success = 'Label deleted successfully!'
    msg_error = 'Cannot remove label because it is in use'
    url_redirect = 'labels'
