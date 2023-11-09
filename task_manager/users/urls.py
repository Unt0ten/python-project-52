from django.urls import path
from task_manager.users import views

urlpatterns = [
    path('', views.CustomUsersView.as_view(), name='users'),
    path('create/', views.UserFormCreateView.as_view(), name='create_user'),
    path(
        '<int:pk>/update/', views.UserFormUpdateView.as_view(),
        name='update_user'
    ),
    path(
        '<int:pk>/delete/', views.UserFormDeleteView.as_view(),
        name='delete_user'
    )
]
