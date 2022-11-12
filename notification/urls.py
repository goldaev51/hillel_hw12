from django.urls import path

from . import views

app_name = 'notification'
urlpatterns = [
    path('email-notification/', views.email_notification, name='email-notification'),
]
