from django.urls import path
from .views import book_list_create, book_detail, book_list

urlpatterns = [
    path('', book_list, name='book_list'),
    path('books/', book_list_create, name='book_list_create'),
    path('books/<int:book_id>/', book_detail, name='book_detail'),
]
