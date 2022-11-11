from abc import ABC

from annotations.models import Author, Book, Publisher, Store

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg, Count, Func
from django.shortcuts import get_object_or_404, render


DATA_PER_PAGE = 12


def books(request):
    book_author_store_query = Book.objects \
        .annotate(stores_cnt=Count('store')) \
        .prefetch_related('authors') \
        .select_related('publisher') \
        .order_by('id')\
        .all()

    page = request.GET.get('page', 1)

    paginator = Paginator(book_author_store_query, DATA_PER_PAGE)
    try:
        book_author_store = paginator.page(page)
    except PageNotAnInteger:
        book_author_store = paginator.page(1)
    except EmptyPage:
        book_author_store = paginator.page(paginator.num_pages)

    return render(request, 'annotations/book_list.html', {"page_obj": book_author_store})


def book_info(request, pk):
    book = get_object_or_404(Book.objects.select_related('publisher'), pk=pk)

    return render(request, 'annotations/book_info.html', {'book': book})


def authors(request):
    authors_books_query = Author.objects.annotate(books_cnt=Count('book')).all()

    page = request.GET.get('page', 1)

    paginator = Paginator(authors_books_query, DATA_PER_PAGE)
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

    paginator = Paginator(publishers_books_query, DATA_PER_PAGE)
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
    stores_books_query = Store.objects\
        .annotate(books_cnt=Count('books'))\
        .all()

    page = request.GET.get('page', 1)

    paginator = Paginator(stores_books_query, DATA_PER_PAGE)
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
