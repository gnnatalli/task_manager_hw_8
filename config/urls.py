
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.tasks.views.tasks import (
    TaskListCreateView,
    TaskDetailView,
    MyTaskListView,
)
from apps.tasks.views.subtasks import (
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)
from apps.tasks.views.statistics import task_statistics
from apps.tasks.views.categories import CategoryViewSet


schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version='v1',
        description="API documentation for Task Manager",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# get_schema_view() — создаёт схему документации API.
# AllowAny — разрешает открывать документацию без авторизации.

# Роутер для CategoryViewSet
# DefaultRouter() создаёт специальный роутер (избавляет нас от необходимости вручную прописывать CRUD-маршруты.)
# register() регистрирует наш CategoryViewSet.
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Список и создание задач
    # Tasks
    path(
        'api/tasks/',
        TaskListCreateView.as_view(),
        name='task-list-create'
    ),

    # Просмотр, изменение и удаление задачи. /api/tasks/	Все задачи (пока без ограничения по владельцу)
    path(
        'api/tasks/<int:pk>/',
        TaskDetailView.as_view(),
        name='task-detail'
    ),

    # /api/my-tasks/	Только задачи текущего пользователя
    path(
        'api/my-tasks/',
        MyTaskListView.as_view(),
        name='my-task'
    ),

    # Статистика задач
    path(
        'api/tasks/statistics/',
        task_statistics,
        name='task-statistics'
    ),

    # Список и создание подзадач
    # SubTasks
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

    # Categories
    path('api/', include(router.urls)),
    path('api/', include('apps.users.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui', ),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc', ),
]

# include() — подключает набор маршрутов.
# include(router.urls) - подключи все URL, которые создал роутер.

# path() — задаёт URL.
# router.urls — маршруты, автоматически созданные роутером.

# POST /api/token/ — проверяет логин и пароль пользователя и возвращает Access и Refresh Token.
# POST /api/token/refresh/ — принимает Refresh Token и выдаёт новый Access Token.
