# Create your tasks here
from celery import shared_task

from django.core.mail import send_mail


@shared_task
def send_email_notification(email_body, email):
    send_mail(
        'Notification',
        email_body,
        'no-reply@gmail.com',
        [email],
        fail_silently=False,
    )
