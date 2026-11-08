
from django.contrib import admin
from django.urls import path

from apps.tasks.views import (
    TaskCreateView,
    TaskListView,
    TaskDetailView,
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
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

    # Получение списка и создание подзадач
    path(
        'api/subtasks/',
        SubTaskListCreateView.as_view(),
        name='subtask-list-create'
    ),

    # Получение, обновление и удаление подзадачи по ID
    path(
        'api/subtasks/<int:pk>/',
        SubTaskDetailUpdateDeleteView.as_view(),
        name='subtask-detail'
    ),
]