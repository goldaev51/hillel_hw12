# hillel_hw16 -- Django redis cache

## Description

Based on 15 hw add<br />
Fixtures for the model and its associated model (For example, posts and their author, quotes and their author, an author and his books, cities and their inhabitants, etc.)<br />
https://docs.djangoproject.com/en/4.1/ref/django-admin/#dumpdata<br />
Store fixtures in the fixtures folder<br />
Alternatively, write a management command to generate the same data from random values.<br />
The number of entries should be large - 500-1000+.<br />

Display it all on the page using queriset aggregation/annotation to get the missing data, in the form of a nested list, table or blocks.<br />

Implement pagination on the page by a large number of elements (100-1000)<br />
(all of the above is intentional deterioration of the page in order to somehow justify caching)<br />

Add caching to this page, and other pages for which it "really makes sense".<br />

For caching, use Redis + django-redis (or the built-in backend for redis if Django version 4+).<br />

--------

## Launch

* clone current repository
* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate
* Create superuser with 'python manage.py createsuperuser'
* Fill db with 'python manage.py fill_db' or use 'python manage.py loaddata fixtures/db.json'
* Run redis server in docker with docker run -d -p 6379:6379 redis
* python manage.py runserver
* Go to http://127.0.0.1:8000/annotations/classbased/books/
* Use site logic with cache on book-list and book-detail

--------

## Realized

* Added cache for book-list class and book-detail
