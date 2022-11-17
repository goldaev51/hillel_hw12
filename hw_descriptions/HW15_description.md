# hillel_hw14 -- Celery beat

## Description

Based on 12 DZ add using only classbased views<br />
An object creation page, an object editing page, an object deletion page, an object view page,<br />
a page for viewing a list of objects with pagination.<br />
(For one model of your choice) Create, modify and delete page - login required. (use a mixin)<br />

--------

## Launch

* clone current repository
* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate
* Create superuser with 'python manage.py createsuperuser'
* Fill db with 'python manage.py fill_db' or use 'python manage.py loaddata db.json'
* python manage.py runserver
* Go to http://127.0.0.1:8000/annotations/classbased/books/
* Use site logic
* You can login with superuser to use more logic like Add new Nook, Update Book, Delete Book

--------

## Realized

* Created class based views for Book model
* New code for list books, create/update/delete book
* Add authentication logic which allow crud logic for book model on site 
