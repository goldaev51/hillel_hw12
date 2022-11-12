import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class NotificatorForm(forms.Form):
    email = forms.EmailField(label='Email')
    notification_text = forms.CharField(label='Notification text', max_length=200)
    notification_date = forms.DateTimeField(help_text="Enter time from now to now+2 days max")

    def clean_notification_date(self):
        date = self.cleaned_data['notification_date']

        if date <= timezone.now():
            raise ValidationError('Invalid date -- date in the past ')

        elif date > timezone.now() + datetime.timedelta(days=2):
            raise ValidationError('Invalid date -- more than 2 days')

        return date
