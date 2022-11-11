from django.contrib import admin

from .models import Author, Book, Publisher, Store


class BooksAuthorInline(admin.TabularInline):
    model = Book.authors.through
    extra = 0


class BookStoresInLine(admin.TabularInline):
    model = Store.books.through
    extra = 0


class PublisherBooksInLine(admin.StackedInline):
    model = Book
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'pages', 'price', 'rating', 'pubdate']
    list_filter = ['pubdate']
    search_fields = ['name__icontains']
    date_hierarchy = 'pubdate'
    exclude = ('authors',)
    inlines = [BooksAuthorInline, BookStoresInLine]


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'age']
    list_filter = ['age']
    search_fields = ['name__icontains']
    inlines = [BooksAuthorInline]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name__icontains']
    inlines = [PublisherBooksInLine]


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name__icontains']
    exclude = ('books',)
    inlines = [BookStoresInLine]
