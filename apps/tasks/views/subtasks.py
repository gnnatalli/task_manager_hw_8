from rest_framework import generics

from apps.tasks.models import SubTask
from apps.tasks.serializers import (
    SubTaskSerializer,
    SubTaskCreateSerializer,
)
from apps.tasks.permissions import IsOwnerOrReadOnly

# # Пагинация: по 5 подзадач на страницу
# class SubTaskPagination(PageNumberPagination):
#     page_size = 5

# 1. Список и создание подзадач
class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    #pagination_class = SubTaskPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Фильтрация по названию задачи
    def get_queryset(self):
        queryset = SubTask.objects.filter(owner=self.request.user)

        task_title = self.request.query_params.get('task_title')

        if task_title:
            queryset = queryset.filter(
                task__title__icontains=task_title
            )

        return queryset

    # Фильтрация.
    filterset_fields = ['status', 'deadline']

    # Поиск.
    search_fields = ['title', 'description']

    # Сортировка.
    ordering_fields = ['created_at']
    ordering = ['-created_at']


# 2. Просмотр, изменение и удаление подзадачи
class SubTaskDetailUpdateDeleteView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = SubTask.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SubTaskCreateSerializer
        return SubTaskSerializer