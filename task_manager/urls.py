"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from task_manager import views
from django.conf.urls.static import static
from django.conf import settings

import task_manager.users.views as view

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('users/', include('task_manager.users.urls')),
    path('login/', view.LoginUser.as_view(), name='login'),
    path('logout/', view.LoginUser.logout_user, name='logout'),
    path('statuses/', include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('admin/', admin.site.urls),
]

handler404 = "task_manager.views.tr_handler403"
handler500 = "task_manager.views.tr_handler500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
