from django.urls import path
from task_manager.tasks import views

urlpatterns = [
    path('', views.TasksView.as_view(), name='tasks'),
    path('<int:pk>/', views.SpecificTaskView.as_view(), name='view_task'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
    path('<int:pk>/update/', views.UpdateTaskView.as_view(), name='update_task'),
    path('<int:pk>/delete/', views.DeleteTaskView.as_view(), name='delete_task')
]
