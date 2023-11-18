from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from .models import TaskModel


class CustomLoginRequiredMixin(LoginRequiredMixin):

    login_url = '/login/'
    permission_denied_message = _("You are not authorized! Please log in.")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, self.permission_denied_message)
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)


class CustomAccessMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                request,
                _("You are not authorized! Please log in.")
            )
            return redirect('login')

        task_id = kwargs.get('pk')
        task = TaskModel.objects.get(id=task_id)
        task_author_id = task.author.id
        if request.user.pk != task_author_id:
            messages.warning(
                request,
                _("Only its author can delete a task")
            )
            return redirect('tasks')

        return super().dispatch(request, *args, **kwargs)
