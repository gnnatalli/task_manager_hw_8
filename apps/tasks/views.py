
from django.utils import timezone
from django.db.models import Count
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


# 1. Создание новой задачи
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# 2. Получение списка задач
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# 3. Получение одной задачи по ID
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


# 4. Статистика задач
@api_view(['GET'])
def task_statistics(request):
    # Общее количество задач
    total_tasks = Task.objects.count()

    # Количество задач по каждому статусу
    tasks_by_status = Task.objects.values('status').annotate(
        count=Count('id')
    )

    # Количество просроченных задач
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

# TaskCreateView	Создаёт задачу методом POST
# TaskListView	Возвращает список задач методом GET
# TaskDetailView	Возвращает задачу по ID методом GET
# task_statistics	Возвращает статистику методом GET