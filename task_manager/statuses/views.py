from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .models import StatusModel
from .forms import StatusModelForm
from task_manager.mixins import CustomLoginRequiredMixin, CheckDependencyMixin


class StatusesView(CustomLoginRequiredMixin, ListView):
    template_name = 'statuses/statuses.html'
    model = StatusModel
    context_object_name = 'statuses'


class CreateStatus(CustomLoginRequiredMixin, CreateView):
    template_name = 'statuses/create.html'
    form_class = StatusModelForm

    def form_valid(self, form):
        messages.success(
            self.request, _('Status successfully created')
        )
        return super().form_valid(form)


class UpdateStatus(CustomLoginRequiredMixin, UpdateView):
    template_name = 'statuses/update.html'
    form_class = StatusModelForm
    model = StatusModel

    def form_valid(self, form):
        messages.success(
            self.request, _('Status successfully changed')
        )
        return super().form_valid(form)


class DeleteStatus(CustomLoginRequiredMixin, CheckDependencyMixin, DeleteView):

    model = StatusModel
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')
    msg_success = 'Status deleted successfully!'
    msg_error = 'Cannot delete status because it is in use'
    url_redirect = 'statuses'
