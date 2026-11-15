
from django.contrib import admin
from django.urls import path

from apps.tasks.views import (
    TaskListCreateView,
    TaskDetailView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
    task_statistics,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Список и создание задач
    path(
        'api/tasks/',
        TaskListCreateView.as_view(),
        name='task-list-create'
    ),

    # Просмотр, изменение и удаление задачи
    path(
        'api/tasks/<int:pk>/',
        TaskDetailView.as_view(),
        name='task-detail'
    ),

    # Статистика задач
    path(
        'api/tasks/statistics/',
        task_statistics,
        name='task-statistics'
    ),

    # Список и создание подзадач
    path(
        'api/subtasks/',
        SubTaskListCreateView.as_view(),
        name='subtask-list-create'
    ),

    # Просмотр, изменение и удаление подзадачи
    path(
        'api/subtasks/<int:pk>/',
        SubTaskDetailUpdateDeleteView.as_view(),
        name='subtask-detail'
    ),
]
