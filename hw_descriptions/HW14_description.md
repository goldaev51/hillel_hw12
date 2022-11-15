# hillel_hw14 -- Celery beat

## Description

Add the Authors and Citations models (not known about links), and register them in the admin.<br />
Use the resource https://quotes.toscrape.com/<br />
Create a periodic table that will be added 5 NEW quotes (and their authors with information) every odd hour.<br />
When the quotes are over - unsubscribe to "yourself".<br />

--------

## Launch

* clone current repository
* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate
* Make sure that you have rabbitmq and redis installed on machine 
* run command 'celery -A core worker -l INFO' in the Terminal #1
* run command 'celery -A core beat -l INFO' in the Terminal #2
* Wait until parser finish his job
* Check results on admin panel

--------

## Realized

* Created new app 'celery_beat'
* Created parser for quotes, authors and tags from site
* Created models for deta
* Created beat_scheduler task for parser
* Added models to admin panel 
