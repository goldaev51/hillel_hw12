# hillel_hw13 -- Celery

## Description

Add a page with a form (do not save anything to the database, the design is not important - the main thing is performance).<br />
The form accepts three fields - mail, reminder text and datetime when this reminder will be received.<br />
When submitting the form, a task is created and postponed, which will have to be completed at the time specified in the<br />
form and send a reminder to the mail specified in the form.

In the subject of the letter, you can simply indicate "reminder"<br />
Datetime - take into account the difference in timezones, but for this task it will not be critical. <br />
DateTime cannot be in the past, and cannot be more than 2 days ahead.<br />
celeryproject.org/en/master/userguide/calling.html#eta-and-countdown<br />
Use send mail to console.<br />

--------

## Launch

* clone current repository
* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate
* Make sure that you have rabbitmq and redis installed on machine 
* run command 'python manage.py runserver' in the Terminal #1
* run command 'celery -A core worker -l INFO' in the Terminal #2
* Go to http://127.0.0.1:8000/notification/email-notification/
* Use notification logic
* Check results of email notification sending in the Terminal #2

--------

## Realized

* Celery added to the project
* Created new app 'notification'
* Created page with form to get data for notification
* Created Celery task that sends notifications at inputted time
