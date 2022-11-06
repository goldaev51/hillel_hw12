from django.contrib import admin

from .models import Book, Author, Publisher, Store


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'pages', 'price', 'rating', 'pubdate']
    list_filter = ['pubdate']
    search_fields = ['name__contains']
    date_hierarchy = 'pubdate'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'age']
    list_filter = ['name']
    search_fields = ['name__contains']


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name__contains']


@admin.register(Store)
class LogsAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name__contains']
