
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.tasks.views.tasks import (
    TaskListCreateView,
    TaskDetailView,
)
from apps.tasks.views.subtasks import (
    SubTaskListCreateView,
    SubTaskDetailUpdateDeleteView,
)
from apps.tasks.views.statistics import task_statistics
from apps.tasks.views.categories import CategoryViewSet

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
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

# include() — подключает набор маршрутов.
# include(router.urls) - подключи все URL, которые создал роутер.

# path() — задаёт URL.
# router.urls — маршруты, автоматически созданные роутером.

# POST /api/token/ — проверяет логин и пароль пользователя и возвращает Access и Refresh Token.
# POST /api/token/refresh/ — принимает Refresh Token и выдаёт новый Access Token.
