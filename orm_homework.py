from datetime import timedelta
from django.utils import timezone
from apps.tasks.models import Task, SubTask

"""
Цель:
Освоение основных операций CRUD (Create, Read, Update, Delete) на примере заданных моделей."""

"""
Выполните запросы:
Создание записей:
Task:
title: "Prepare presentation".
description: "Prepare materials and slides for the presentation".
status: "New".
deadline: Today's date + 3 days.

SubTasks для "Prepare presentation":
title: "Gather information".
description: "Find necessary information for the presentation".
status: "New".
deadline: Today's date + 2 days.

title: "Create slides".
description: "Create presentation slides".
status: "New".
deadline: Today's date + 1 day.

Чтение записей:
Tasks со статусом "New":
Вывести все задачи, у которых статус "New".
SubTasks с просроченным статусом "Done":
Вывести все подзадачи, у которых статус "Done", но срок выполнения истек.

Изменение записей:
Измените статус "Prepare presentation" на "In progress".
Измените срок выполнения для "Gather information" на два дня назад.
Измените описание для "Create slides" на "Create and format presentation slides".

Удаление записей:
Удалите задачу "Prepare presentation" и все ее подзадачи.
"""

# 1. СОЗДАНИЕ ЗАПИСЕЙ (CREATE)

# Запоминаем текущую дату и время
today = timezone.now()

# Создаём главную задачу
task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status="new",
    deadline=today + timedelta(days=3),
)
print(task.title, task.status, task.deadline)

# Создаём первую подзадачу
subtask1 = SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status="new",
    deadline=today + timedelta(days=2),
    task=task,
)

print(subtask1.title, subtask1.status, subtask1.deadline)

# Создаём вторую подзадачу
subtask2 = SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status="new",
    deadline=today + timedelta(days=1),
    task=task,
)

print(subtask2.title, subtask2.status, subtask2.deadline)

# Выводим созданные объекты в консоль
print(task)
print(subtask1)
print(subtask2)

print(task.title, task.description, task.status, task.deadline)
for subtask in task.subtasks.all():
    print(subtask.title, "|", subtask.description, "|", subtask.status, "|", subtask.deadline)

# 2. READ (чтение записей).
# Все задачи со статусом New
new_task = Task.objects.filter(status="new")

print("\nTasks со статусом New:")
for task in new_task:
    print(task.title, task.status)

# Подзадачи со статусом Done,
# у которых срок выполнения уже прошёл
overdue_done_subtasks = SubTask.objects.filter(
    status="done",
    deadline__lt=timezone.now(),
)

print("\nПросроченные SubTasks со статусом Done:")
for subtask in overdue_done_subtasks:
    print(subtask.title, "|", subtask.deadline)


#3 UPDATE (обновление записей).
# Изменяем статус задачи Prepare presentation
Task.objects.filter(
    title="Prepare presentation"
).update(status="in_progress")

# Переносим срок Gather information на два дня назад
SubTask.objects.filter(
    title="Gather information"
).update(deadline=timezone.now() - timedelta(days=2))

# Изменяем описание Create slides
SubTask.objects.filter(
    title="Create slides"
).update(description="Create and format presentation slides"
)

print("\nДанные обновленны.")

# Проверяем
task_check = Task.objects.get(title="Prepare presentation")
print(task_check.title, "|", task_check.status)

subtask_check = SubTask.objects.get(title="Gather information")
print(subtask_check.title, "|", subtask_check.deadline)

subtask_check = SubTask.objects.get(title="Create slides")
print(subtask_check.title, "|", subtask_check.description)

# 4. DELETE — удаление задачи и её подзадач
Task.objects.filter(
    title="Prepare presentation"
).delete()

print("\n Task Prepare presentation и её SubTasks удаленны.")

# Проверяем удаление
Task.objects.filter(title="Prepare presentation").exists()

SubTask.objects.filter(
    title__in=["Gather information", "Create slides"]
).exists()