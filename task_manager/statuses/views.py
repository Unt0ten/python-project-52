from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from django.utils.translation import gettext as _
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from tasks.models import TaskModel
from .models import StatusModel
from .forms import StatusModelForm
from task_manager.mixins_login import CustomLoginRequiredMixin


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


class DeleteStatus(CustomLoginRequiredMixin, DeleteView):
    model = StatusModel
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses')

    def form_valid(self, form):
        status = self.object
        task_status = TaskModel.objects.filter(author_id=status.id)
        if task_status:
            messages.warning(
                self.request, _('Cannot delete status because it is in use')
            )
            return redirect('statuses')

        messages.success(self.request, _('Status deleted successfully!'))
        return super().form_valid(form)
