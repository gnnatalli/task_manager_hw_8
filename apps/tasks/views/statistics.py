from django.utils import timezone
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.tasks.models import Task


# Статистика задач
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
