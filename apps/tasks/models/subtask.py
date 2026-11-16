from django.db import models

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


class SubTask(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    # Связь ForeignKey: много подзадач относятся к одной задаче
    task = models.ForeignKey('Task', on_delete=models.CASCADE, related_name='subtasks')
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
