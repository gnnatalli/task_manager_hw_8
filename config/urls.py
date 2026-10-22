
from django.contrib import admin
from django.urls import path

from apps.tasks.views import (
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    task_statistics,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Создание задачи
    path('api/tasks/create/', TaskCreateView.as_view(), name='task-create'),

    # Получение списка задач
    path('api/tasks/', TaskListView.as_view(), name='task-list'),

    # Получение задачи по ID
    path('api/tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    # Статистика задач
    path('api/tasks/statistics/', task_statistics, name='task-statistics'),
]
