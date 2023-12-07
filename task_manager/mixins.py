from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

from task_manager.tasks.models import TaskModel


class CustomLoginRequiredMixin(LoginRequiredMixin):

    redirect_field_name = None
    login_url = '/login/'
    permission_denied_message = _("You are not authorized! Please log in.")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, self.permission_denied_message)
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class CheckDependencyMixin:

    msg_success = None
    msg_error = None
    url_redirect = None

    def form_valid(self, form):
        find_obj = None
        obj = self.object
        if self.url_redirect == 'statuses':
            find_obj = TaskModel.objects.filter(status_id=obj.id)
        elif self.url_redirect == 'labels':
            find_obj = TaskModel.objects.filter(labels=obj.id)

        if find_obj:
            messages.warning(
                self.request, _(self.msg_error)
            )
            return redirect(self.url_redirect)

        messages.success(self.request, _(self.msg_success))
        return super().form_valid(form)
