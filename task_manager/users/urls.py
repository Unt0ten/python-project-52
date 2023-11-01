from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='users'),
    path('create/', views.UserFormCreateView.as_view(), name='create_user'),
]