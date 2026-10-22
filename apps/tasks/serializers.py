from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    # Преобразует модель Task в JSON и проверяет входящие данные.
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline']

# ModelSerializer автоматически создаёт поля на основе модели.
# model = Task указывает, с какой моделью работаем.
# fields определяет, какие поля будут доступны через API.
# id включён, чтобы видеть уникальный номер задачи в ответе.
