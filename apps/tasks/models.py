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
"""

class Task (models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
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


    # В задании не уточнено, для какой даты должно быть уникальным название.
    # Поэтому уникальность определяется по дате создания задачи.
    class Meta:
        constraints = [
            models.UniqueConstraint(
                models.functions.TruncDate('created_at'),
                   'title',
                   name='unique_task_title_per_date'
            ),
        ]

    def __str__(self):
        return self.title


"""
    Модель SubTask:
    Описание: Отдельная часть основной задачи (Task).
    Поля:
    title: Название подзадачи.
    description: Описание подзадачи.
    task: Основная задача. Один ко многим.
    status: Статус задачи. Выбор из: New, In progress, Pending, Blocked, Done
    deadline: Дата и время дедлайн.
    created_at: Дата и время создания. Автоматическое заполнение.
"""

class SubTask (models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
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

"""
Модель Category:
Описание: Категория выполнения.
Поля:
name: Название категории.
"""


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
