# hillel_hw12 -- Annotate aggregate

## Description

populate the database with more data and let me populate the database just as quickly: <br />
1) create a management team
2) create fixtures (dumpdata loaddata command management) (only user model and new models from app)

Add models to admin. Try to use more functionality (inline, filters, search, output and group fields in the form, filter_vertical, date_hierarchy, etc)<br />

Create several templates, views, URLs for displaying data on models.<br />

In views and templates, you should try to minimize the number of requests to the database.<br />
(Prefetch, selects, annotations, aggregations)<br />

Display lists (in tables) or a single element on pages - for example, a list of stores or one author.<br />
In addition to the fields from the model, it is imperative to display something else obtained using “Prefetch, selects, annotations, aggregations”.<br />

number of available pages - 8 (list page and element page for each model)<br />

--------

## Launch

* clone current repository
* pip install -r requirements.txt
* python manage.py makemigrations
* python manage.py migrate
* Create superuser with 'python manage.py createsuperuser'
* Fill db with 'python manage.py fill_db' or use 'python manage.py loaddata db.json'
* python manage.py runserver
* Go to http://127.0.0.1:8000/
* Use site logic
* Go to http://127.0.0.1:8000/admin and check admin panel

--------

## Realized

* added Django debug toolbar to the project
* Created a custom command fill_db.py which fill db with random data.
* Created 8 views, by 2 for each model to show model data in table and info about each element in model
* Set a admin panel for models
