import datetime

from django.contrib import messages
from django.shortcuts import redirect, render

from notification.forms import NotificatorForm

from .tasks import send_email_notification as celery_send_email


def email_notification(request):
    if request.method == 'POST':
        form = NotificatorForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            notification_text = form.cleaned_data['notification_text']
            notification_date = form.cleaned_data['notification_date']

            celery_send_email.apply_async((notification_text, email), eta=notification_date)

            messages.success(request, 'Message sent.')

            return redirect('notification:email-notification')
    else:
        proposed_notification_date = datetime.datetime.now() + datetime.timedelta(minutes=2)
        form = NotificatorForm(initial={'notification_date': proposed_notification_date})
    return render(request, 'notification/email_notificator.html', {'form': form})
