from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from apps.tasks.models.task import Task


@receiver(pre_save, sender=Task)
def remember_old_task_status(sender, instance, **kwargs):
    # Для новой задачи предыдущего статуса ещё нет
    if instance.pk:
        try:
            old_task = Task.objects.get(pk=instance.pk)
            instance._old_status = old_task.status
        except Task.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Task)
def send_task_status_email(sender, instance, created, **kwargs):
    # При создании задачи уведомление не отправляем
    if created:
        return

    old_status = getattr(instance, '_old_status', None)
    new_status = instance.status

    # Если статус не изменился, уведомление не отправляем
    if old_status == new_status:
        return

    # Формируем тему и текст письма
    subject = f'Изменение статуса задачи: {instance.title}'

    message = (
        f'Здравствуйте, {instance.owner.username}!\n\n'
        f'Статус вашей задачи "{instance.title}" изменился.\n'
        f'Предыдущий статус: {old_status}\n'
        f'Новый статус: {new_status}\n'
    )

    # Если задача закрыта, добавляем сообщение
    if new_status == 'done':
        message += '\nВаша задача закрыта!'

    # Отправляем письмо владельцу задачи
    if instance.owner.email:
        send_mail(
            subject,
            message,
            None,
            [instance.owner.email],
            fail_silently=False,
        )

# pre_save — срабатывает перед сохранением задачи. Мы запоминаем старый статус.
# post_save — срабатывает после сохранения. Проверяем, изменился ли статус.
# send_mail() — отправляет письмо на электронную почту владельца.
# created — позволяет отличить создание задачи от изменения существующей.