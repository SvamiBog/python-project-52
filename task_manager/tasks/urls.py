from django.urls import path
from .views import (
    TasksIndexView,
    TasksCreateView,
    TasksUpdateView,
    TasksDeleteView,
    TasksDetailView
)


urlpatterns = [
    path('', TasksIndexView.as_view(), name='tasks_index'),
    path('create/', TasksCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TasksUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TasksDeleteView.as_view(), name='task_delete'),
    path('<int:pk>', TasksDetailView.as_view(), name="task_detail"),
]
