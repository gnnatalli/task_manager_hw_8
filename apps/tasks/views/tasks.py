from rest_framework import generics

from apps.tasks.models import Task
from apps.tasks.serializers import (
    TaskSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer
)
from apps.tasks.permissions import IsOwnerOrReadOnly

# 1. Список и создание задач
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()

    # GET — список, POST — создание.
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # self.request.user — текущий авторизованный пользователь.
        # serializer.save() — сохраняет новую задачу.
        # owner=self.request.user — записывает этого пользователя владельцем задачи.


    # Фильтрация задач по дню недели
    def get_queryset(self):
        queryset = Task.objects.filter(owner=self.request.user)
        weekday = self.request.query_params.get('weekday')

        if weekday:
            weekdays = {
                'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6,
            }

            day_number = weekdays.get(weekday.lower())

            if day_number is not None:
                queryset = queryset.filter(
                    deadline__week_day=day_number + 2
                )

        return queryset

    # Фильтрация.
    filterset_fields = ['status', 'deadline']

    # Поиск.
    search_fields = ['title', 'description']

    # Сортировка.
    ordering_fields = ['created_at']
    ordering = ['-created_at']


# 2. Просмотр, изменение и удаление задачи
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateSerializer
        return TaskDetailSerializer

# 3. Получение задач текущего пользователя
class MyTaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
    # self.request.user — пользователь, который отправил запрос.
    # filter(owner=self.request.user) — выбирает только его задачи.
    # ListAPIView — предоставляет GET-запрос для получения списка.
