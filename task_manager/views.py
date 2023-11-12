from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


def tr_handler403(request, exception):
    return render(request, 'errors/404.html', status=404)


def tr_handler500(request):
    return render(request, 'errors/500.html', status=500)
