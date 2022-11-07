from annotations.models import Author, Book, Publisher, Store

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render


DATA_PER_PAGE = 12


def books(request):
    book_author_store_query = Book.objects \
        .prefetch_related('authors') \
        .prefetch_related('store') \
        .select_related('publisher') \
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
    book = Book.objects \
        .prefetch_related('authors') \
        .prefetch_related('store') \
        .select_related('publisher') \
        .get(pk=pk)

    return render(request, 'annotations/book_info.html', {'book': book})


def authors(request):
    authors_books_query = Author.objects.prefetch_related('book').all()

    page = request.GET.get('page', 1)

    paginator = Paginator(authors_books_query, DATA_PER_PAGE)
    try:
        authors_books = paginator.page(page)
    except PageNotAnInteger:
        authors_books = paginator.page(1)
    except EmptyPage:
        authors_books = paginator.page(paginator.num_pages)

    context = {
        "page_obj": authors_books,
    }

    return render(request, 'annotations/author_list.html', context)


def author_info(request, pk):
    author = Author.objects.prefetch_related('book').get(pk=pk)
    return render(request, 'annotations/author_info.html', {'author': author})


def publishers(request):
    publishers_books_query = Publisher.objects.prefetch_related('book').all()

    page = request.GET.get('page', 1)

    paginator = Paginator(publishers_books_query, DATA_PER_PAGE)
    try:
        publishers_books = paginator.page(page)
    except PageNotAnInteger:
        publishers_books = paginator.page(1)
    except EmptyPage:
        publishers_books = paginator.page(paginator.num_pages)

    context = {
        "page_obj": publishers_books,
    }

    return render(request, 'annotations/publisher_list.html', context)


def publisher_info(request, pk):
    publisher = Publisher.objects.prefetch_related('book').get(pk=pk)
    return render(request, 'annotations/publisher_info.html', {'publisher': publisher})


def stores(request):
    stores_books_query = Store.objects.prefetch_related('books').all()

    page = request.GET.get('page', 1)

    paginator = Paginator(stores_books_query, DATA_PER_PAGE)
    try:
        stores_books = paginator.page(page)
    except PageNotAnInteger:
        stores_books = paginator.page(1)
    except EmptyPage:
        stores_books = paginator.page(paginator.num_pages)

    context = {
        "page_obj": stores_books,
    }

    return render(request, 'annotations/store_list.html', context)


def store_info(request, pk):
    store = Store.objects.prefetch_related('books').get(pk=pk)

    return render(request, 'annotations/store_info.html', {'store': store})
