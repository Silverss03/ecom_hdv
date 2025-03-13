from django.shortcuts import render
from .models import Book
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BookSerializer
from rest_framework import status  # ✅ Add this line

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book/book_list.html', {'books': books})

# 🟢 GET all books & CREATE new clothe
@api_view(['GET', 'POST'])
def book_list_create(request):
    if request.method == 'GET':  # Get all books
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':  # Create new book
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response({"error": "book not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':  # Retrieve one book
        serializer = BookSerializer(book)
        return Response(serializer.data)

    elif request.method == 'PUT':  # Update book
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':  # Delete book
        book.delete()
        return Response({"message": "book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)