from django.shortcuts import render
from django.views import View
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.utils.translation import gettext as _


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class MyLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_url = 'blog-home'
    success_message = _('You are logged in')
