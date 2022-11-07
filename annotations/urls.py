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
]
