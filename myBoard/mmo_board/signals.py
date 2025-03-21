from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Response


@receiver(post_save, sender=Response)
def notify_about_response(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Новый отклик на ваше объявление',
            f'Пользователь {instance.author.username} оставил отклик на ваше объявление "{instance.post.title}".',
            'from@example.com',
            [instance.post.author.email],
            fail_silently=False,
        )
    elif instance.accepted:
        send_mail(
            'Ваш отклик принят',
            f'Пользователь {instance.post.author.username} принял ваш отклик на объявление "{instance.post.title}".',
            'from@example.com',
            [instance.author.email],
            fail_silently=False,
        )
