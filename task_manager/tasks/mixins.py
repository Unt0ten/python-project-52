from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class CustomLoginRequiredMixin(LoginRequiredMixin):

    login_url = '/login/'
    permission_denied_message = _("You are not authorized! Please log in.")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, self.permission_denied_message)
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class CustomAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                self.request,
                _("You are not authorized! Please log in.")
            )
            return redirect('login')

        author_id = self.kwargs.get('pk')

        if self.request.user.pk != author_id:
            messages.warning(
                self.request,
                _("You don't have permition to delte other task.")
            )
            return redirect('users')

        return super().dispatch(request, *args, **kwargs)