from django.urls import path

from . import views

app_name = 'annotations'
urlpatterns = [
    path('authors/', views.authors, name='authors'),
    path('authors/<int:pk>', views.author_info, name='author-info'),
    path('books/', views.books, name='books'),
    path('book/<int:pk>', views.book_info, name='book-info'),
    path('publishers/', views.publishers, name='publishers'),
    path('publisher/<int:pk>', views.publisher_info, name='publisher-info'),
    path('stores/', views.stores, name='stores'),
    path('store/<int:pk>', views.store_info, name='store-info'),

    # path('classbased/books/', cache_page(10)(views.BookListView.as_view()), name='books-list'),
    path('classbased/books/', views.BookListView.as_view(), name='books-list'),
    path('classbased/books/<int:pk>', views.BookDetailView.as_view(), name='book-details'),
    path('classbased/books/create', views.BookCreate.as_view(), name='book-create'),
    path('classbased/books/<int:pk>/update', views.BookUpdate.as_view(), name='book-update'),
    path('classbased/books/<int:pk>/delete', views.BookDelete.as_view(), name='book-delete'),
]
