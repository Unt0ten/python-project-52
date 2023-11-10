from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import AccessMixin


class CustomAccessMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                self.request,
                _("You are not authorized! Please log in.")
                )
            return redirect('login')

        user_id = self.kwargs.get('pk')
        if self.request.user.pk != user_id:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        messages.warning(
            self.request,
            _("You don't have permition to change other user.")
        )

        return redirect('users')
