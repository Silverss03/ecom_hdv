from django.shortcuts import render

# Create your views here.
# landing/views.py
from django.shortcuts import render
from book.models import Book
from phone.models import Phone
from shoes.models import Shoe
from clothes.models import Clothe

def landing_page(request):
    query = request.GET.get('q', '')  # Get the search query from request
    if query:
        # Filter products based on the search query
        books = Book.objects.using('mongo_db').filter(title__icontains=query)
        mobile_phones = Phone.objects.using('mongo_db').filter(name__icontains=query)
        shoes = Shoe.objects.using('mongo_db').filter(name__icontains=query)
        clothes = Clothe.objects.using('mongo_db').filter(name__icontains=query)  # Removed redundant .all()
    else:
        # No search query, return all products
        books = Book.objects.using('mongo_db').all()
        mobile_phones = Phone.objects.using('mongo_db').all()
        shoes = Shoe.objects.using('mongo_db').all()
        clothes = Clothe.objects.using('mongo_db').all()

    context = {
        'books': books,
        'mobile_phones': mobile_phones,
        'shoes': shoes,
        'clothes': clothes,
        'query': query  # Keep the search term in the search bar
    }
    return render(request, 'landing_page.html', context)