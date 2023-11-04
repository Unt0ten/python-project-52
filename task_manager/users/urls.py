from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='users'),
    path('create/', views.UserFormCreateView.as_view(), name='create_user'),
    path(
        '<int:id>/update/', views.UserFormUpdateView.as_view(),
        name='update_user'
    ),
    path(
        '<int:id>/delete/', views.UserFormDeleteView.as_view(),
        name='delete_user'
    )
]
