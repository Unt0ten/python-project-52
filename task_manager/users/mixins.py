from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class CustomUserPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        user_id = self.kwargs.get('pk')
        return self.request.user.pk == user_id

    def handle_no_permission(self):
        messages.warning(
            self.request,
            _("You don't have permition to change other user.")
        )

        return redirect('users')
