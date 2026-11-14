from django.utils import timezone
from django.db.models import Count
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Task, SubTask
from .serializers import (TaskSerializer,
                          TaskDetailSerializer,
                          TaskCreateSerializer,
                          SubTaskSerializer,
                          SubTaskCreateSerializer,
                          CategoryCreateSerializer)


class SubTaskPagination(PageNumberPagination):
    page_size = 5 # Максимум 5 объектов на странице
    # PageNumberPagination — встроенный класс DRF для пагинации.
    # page_size = 5 — количество объектов на одной странице.

# 1. Создание новой задачи
class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer


# 2. Получение списка задач
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Получаем все задачи
        queryset = Task.objects.all()

        # Получаем день недели из параметров URL
        weekday = self.request.query_params.get('weekday')

        # Если параметр передан, фильтруем задачи
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



# 3. Получение одной задачи по ID
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class SubTaskListCreateView(APIView):

    # GET - Получение списка всех подзадач с пагинацией
    def get(self, request):
        # Получаем все подзадачи в порядке от новых к старым
        sub_tasks = SubTask.objects.all().order_by('-created_at')
        # Получаем параметры фильтрации из URL
        task_title = request.query_params.get('task_title') # request.query_params.get() получает значение из URL.
        task_status = request.query_params.get('status')
        # Фильтруем по названию основной задачи
        if task_title:
            sub_tasks = sub_tasks.filter(task__title__icontains=task_title)
        # Фильтруем по статусу подзадачи
        if task_status:
            sub_tasks = sub_tasks.filter(status=task_status) # status=status оставляет подзадачи только с указанным статусом.
        # Создаём объект пагинации
        paginator = SubTaskPagination()
        # Разбиваем список на страницы
        page = paginator.paginate_queryset(sub_tasks, request)
        # Сериализуем объекты текущей страницы
        serializer = SubTaskSerializer(page, many=True)
        # Возвращаем данные вместе с информацией о страницах
        return paginator.get_paginated_response(serializer.data)

    # POST - Создание новой подзадачи/ создать объект
    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubTaskDetailUpdateDeleteView(APIView):

    # Получение одной подзадачи
    def get(self, request, pk):
        sub_task = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskSerializer(sub_task)
        return Response(serializer.data)

    # PUT - Полное обновление подзадачи
    def put(self, request, pk):
        sub_task = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(sub_task, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PATCH - Частичное обновление подзадачи
    def patch(self, request, pk):
        sub_task = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskCreateSerializer(sub_task, data=request.data, partial=True)
        # partial=True - разрешает передавать не все поля, а только те, которые нужно изменить

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE - Удаление подзадачи
    def delete(self, request, pk):
        sub_task = get_object_or_404(SubTask, pk=pk)
        sub_task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
