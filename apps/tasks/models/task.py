from django.db import models

""" Модель Task:
    Описание: Задача для выполнения.
    Поля:
    title: Название задачи. Уникально для даты.
    description: Описание задачи.
    categories: Категории задачи. Многие ко многим.
    status: Статус задачи. Выбор из: New, In progress, Pending, Blocked, Done
    deadline: Дата и время дедлайн.
    created_at: Дата и время создания. Автоматическое заполнение.

    Модель Task:
    Добавить метод str, который возвращает название задачи.
    Добавить класс Meta с настройками:
    Имя таблицы в базе данных: 'task_manager_task'.
    Сортировка по убыванию даты создания.
    Человекочитаемое имя модели: 'Task'.
    Уникальность по полю 'title'.
"""


class Task(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    # Связь ManyToMany: одна задача может иметь несколько категорий
    categories = models.ManyToManyField('Category', related_name='tasks')
    status = models.CharField(
        max_length=20,
        choices=[
            ('new', 'New'),
            ('in_progress', 'In Progress'),
            ('pending', 'Pending'),
            ('blocked', 'Blocked'),
            ('done', 'Done'),
        ],
        default='new',
    )

    deadline = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'
