from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.tasks.models import Category
from apps.tasks.serializers import (CategorySerializer, CategoryCreateSerializer,)


# CRUD для категорий
# ModelViewSet автоматически предоставляет CRUD: GET, POST, PUT, PATCH и DELETE.
class CategoryViewSet(viewsets.ModelViewSet):
    # Category.objects.all() возвращает только активные категории благодаря нашему менеджеру.
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return CategoryCreateSerializer
        return CategorySerializer

    # Дополнительный GET-запрос: количество задач в категории
    # @action(detail=True) создаёт дополнительный маршрут для конкретной категории.
    # request — информация о запросе клиента.
    # pk — это сокращение от Primary Key (первичный ключ).
    @action(methods=['GET'], detail=True)
    def count_tasks(self, request, pk=None): 
        category = self.get_object()

        return Response({
            'category': category.name,
            'tasks_count': category.tasks.count(), # category.tasks.count() считает задачи, связанные с этой категорией.
        })

