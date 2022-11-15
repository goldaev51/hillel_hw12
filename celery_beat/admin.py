from django.contrib import admin

from .models import Author, Quote, Tags


class AuthorsQuoteInline(admin.TabularInline):
    model = Quote
    extra = 0


class QuotesTagsInline(admin.TabularInline):
    model = Quote.tags.through
    extra = 0


@admin.register(Author)
class AuthorCeleryAdmin(admin.ModelAdmin):
    list_display = ['name', 'born_date', 'born_location']
    search_fields = ['name__icontains']
    inlines = [AuthorsQuoteInline]


@admin.register(Quote)
class QuoteCeleryAdmin(admin.ModelAdmin):
    list_display = ['text']
    search_fields = ['text__icontains']
    exclude = ['tags']
    inlines = [QuotesTagsInline]


@admin.register(Tags)
class TagsCeleryAdmin(admin.ModelAdmin):
    list_display = ['text']
    search_fields = ['text__icontains']
    inlines = [QuotesTagsInline]
