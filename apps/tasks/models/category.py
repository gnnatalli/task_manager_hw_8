from django.db import models
from django.utils import timezone


# Менеджер: по умолчанию показывает только неудалённые категории
class ActiveCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


"""
Модель Category:
Описание: Категория выполнения.
Поля:
name: Название категории.

Модель Category:
Добавить метод str, который возвращает название категории.
Добавить класс Meta с настройками:
Имя таблицы в базе данных: 'task_manager_category'.
Человекочитаемое имя модели: 'Category'.
Уникальность по полю 'name'.
"""


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    # Поля для мягкого удаления
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(blank=True, null=True)

    # Обычный менеджер — только активные категории
    objects = ActiveCategoryManager()

    # Дополнительный менеджер — все категории, включая удалённые
    all_objects = models.Manager()

    def __str__(self):
        return self.name

    # Вместо физического удаления помечаем категорию удалённой
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'