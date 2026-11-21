from django.utils import timezone
from rest_framework.serializers import (ModelSerializer, ValidationError)

from apps.tasks.models import Task
from apps.tasks.serializers.subtasks import SubTaskSerializer


class TaskSerializer(ModelSerializer):
    # Преобразует модель Task в JSON и проверяет входящие данные.
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'owner']
        read_only_fields = ['owner']
# ModelSerializer автоматически создаёт поля на основе модели.
# model = Task указывает, с какой моделью работаем.
# fields определяет, какие поля будут доступны через API.
# id включён, чтобы видеть уникальный номер задачи в ответе.


class TaskDetailSerializer(ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']


class TaskCreateSerializer(ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner']

    def validate_deadline(self, value):
        if value and value < timezone.now():
            raise ValidationError(
                'Deadline не может быть в прошлом.'
            )
        return value