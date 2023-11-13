from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path('', views.TasksView.as_view(), name='tasks'),
    path('1/', views.TasksView.as_view(), name='view_task'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('1/update/', views.UpdateTaskView.as_view(), name='update_task'),
    path('1/delete/', views.DeleteTaskView.as_view(), name='delete_task')
]
