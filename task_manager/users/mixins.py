from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class CustomAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(
                self.request,
                _("You are not authorized! Please log in.")
            )
            return redirect('login')

        user_id = self.kwargs.get('pk')

        if self.request.user.pk != user_id:
            messages.warning(
                self.request,
                _("You don't have permition to change other user.")
            )
            return redirect('users')

        return super().dispatch(request, *args, **kwargs)
