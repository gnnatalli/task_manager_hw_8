from django.utils import timezone
from django.db.models import Count
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Task, SubTask
from .serializers import (
    TaskSerializer,
    TaskDetailSerializer,
    TaskCreateSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
)


class SubTaskPagination(PageNumberPagination):
    page_size = 5


# 1. Список и создание задач
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()

    # GET — список, POST — создание.
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    # Сохраняем фильтр weekday из предыдущего задания.
    def get_queryset(self):
        queryset = Task.objects.all()

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

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskCreateSerializer
        return TaskDetailSerializer


# 3. Список и создание подзадач
class SubTaskListCreateView(generics.ListCreateAPIView):
    queryset = SubTask.objects.all()
    pagination_class = SubTaskPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer

    # Сохраняем фильтр task_title из предыдущего задания.
    def get_queryset(self):
        queryset = SubTask.objects.all()

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


# 4. Просмотр, изменение и удаление подзадачи
class SubTaskDetailUpdateDeleteView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = SubTask.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SubTaskCreateSerializer
        return SubTaskSerializer


# 5. Статистика задач
@api_view(['GET'])
def task_statistics(request):
    total_tasks = Task.objects.count()

    tasks_by_status = Task.objects.values('status').annotate(
        count=Count('id')
    )

    overdue_tasks = Task.objects.filter(
        deadline__lt=timezone.now()
    ).exclude(
        status='done'
    ).count()

    return Response({
        'total_tasks': total_tasks,
        'tasks_by_status': list(tasks_by_status),
        'overdue_tasks': overdue_tasks,
    })
