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

class Task (models.Model):
    title = models.CharField(max_length=100, unique=True)
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

    def __str__(self):
        return self.title


    class Meta:
        db_table = 'task_manager_task'
        ordering = ['-created_at']
        verbose_name = 'Task'


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
    
    Модель SubTask:
    Добавить метод str, который возвращает название подзадачи.
    Добавить класс Meta с настройками:
    Имя таблицы в базе данных: 'task_manager_subtask'.
    Сортировка по убыванию даты создания.
    Человекочитаемое имя модели: 'SubTask'.
    Уникальность по полю 'title'.
"""

class SubTask (models.Model):
    title = models.CharField(max_length=100, unique=True)
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

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'

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

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'