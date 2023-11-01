from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from task_manager.users.models import User


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(
            request, 'users/index.html', context={'users': users})


class UserFormCreateView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'users/create.html')

    def post(self, request, *args, **kwargs):
        pass
        # form = ArticleForm(request.POST)
        # if form.is_valid():  # Если данные корректные, то сохраняем данные формы
        #     form.save()
        #     return redirect('/articles')  # Редирект на указанный маршрут
        # # Если данные некорректные, то возвращаем человека обратно на страницу с заполненной формой
        # return render(request, 'articles/create.html', {'form': form})
