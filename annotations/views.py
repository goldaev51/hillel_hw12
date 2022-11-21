import datetime
from abc import ABC


from annotations.models import Author, Book, Publisher, Store

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Func
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.views.generic import CreateView, DeleteView, UpdateView


decorators = [cache_page(20), vary_on_cookie]


class BookCreate(LoginRequiredMixin, CreateView):
    initial = {'pubdate': datetime.datetime.today()}
    model = Book
    fields = ['name', 'pages', 'price', 'rating', 'pubdate', 'publisher', 'authors']


@method_decorator(decorators, 'dispatch')
class BookListView(generic.ListView):
    model = Book
    queryset = Book.objects \
        .annotate(stores_cnt=Count('store')) \
        .prefetch_related('authors') \
        .select_related('publisher') \
        .order_by('id') \
        .all()
    paginate_by = settings.PAGINATION_DATA_PER_PAGE


@method_decorator(decorators, 'dispatch')
class BookDetailView(generic.DetailView):
    model = Book
    queryset = Book.objects.select_related('publisher')


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['name', 'pages', 'price', 'rating', 'pubdate', 'publisher', 'authors']


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('annotations:books-list')


def books(request):
    book_author_store_query = Book.objects \
        .annotate(stores_cnt=Count('store')) \
        .prefetch_related('authors') \
        .select_related('publisher') \
        .order_by('id') \
        .all()

    page = request.GET.get('page', 1)

    paginator = Paginator(book_author_store_query, settings.PAGINATION_DATA_PER_PAGE)
    try:
        book_author_store = paginator.page(page)
    except PageNotAnInteger:
        book_author_store = paginator.page(1)
    except EmptyPage:
        book_author_store = paginator.page(paginator.num_pages)

    return render(request, 'annotations/books_list_data.html', {"page_obj": book_author_store})


def book_info(request, pk):
    book = get_object_or_404(Book.objects.select_related('publisher'), pk=pk)

    return render(request, 'annotations/book_info.html', {'book': book})


def authors(request):
    authors_books_query = Author.objects.annotate(books_cnt=Count('book')).all()

    page = request.GET.get('page', 1)

    paginator = Paginator(authors_books_query, settings.PAGINATION_DATA_PER_PAGE)
    try:
        authors_books = paginator.page(page)
    except PageNotAnInteger:
        authors_books = paginator.page(1)
    except EmptyPage:
        authors_books = paginator.page(paginator.num_pages)

    return render(request, 'annotations/author_list.html', {"page_obj": authors_books})


def author_info(request, pk):
    author = get_object_or_404(Author.objects.prefetch_related('book'), pk=pk)
    return render(request, 'annotations/author_info.html', {'author': author})


def publishers(request):
    publishers_books_query = Publisher.objects.annotate(books_cnt=Count('book')).all()

    page = request.GET.get('page', 1)

    paginator = Paginator(publishers_books_query, settings.PAGINATION_DATA_PER_PAGE)
    try:
        publishers_books = paginator.page(page)
    except PageNotAnInteger:
        publishers_books = paginator.page(1)
    except EmptyPage:
        publishers_books = paginator.page(paginator.num_pages)

    return render(request, 'annotations/publisher_list.html', {"page_obj": publishers_books})


def publisher_info(request, pk):
    # publisher = Publisher.objects.prefetch_related('book').get(pk=pk)
    publisher = get_object_or_404(Publisher, pk=pk)
    return render(request, 'annotations/publisher_info.html', {'publisher': publisher})


def stores(request):
    stores_books_query = Store.objects \
        .annotate(books_cnt=Count('books')) \
        .all()

    page = request.GET.get('page', 1)

    paginator = Paginator(stores_books_query, settings.PAGINATION_DATA_PER_PAGE)
    try:
        stores_books = paginator.page(page)
    except PageNotAnInteger:
        stores_books = paginator.page(1)
    except EmptyPage:
        stores_books = paginator.page(paginator.num_pages)

    return render(request, 'annotations/store_list.html', {"page_obj": stores_books})


def store_info(request, pk):
    store = get_object_or_404(Store, pk=pk)
    books_rating = store.books.aggregate(books_avg_rating=Round(Avg('rating')))
    store_books = store.books.all()
    return render(request, 'annotations/store_info.html',
                  {'store': store,
                   'books_rating': books_rating,
                   'store_books': store_books
                   })


class Round(Func, ABC):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 2)'
