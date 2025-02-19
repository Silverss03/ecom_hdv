from django.shortcuts import render

# Create your views here.
# landing/views.py
from django.shortcuts import render
from book.models import Book
from phone.models import Phone
from shoes.models import Shoe
from clothes.models import Clothe

def landing_page(request):
    # Fetch all products from different apps
    books = Book.objects.all()
    mobile_phones = Phone.objects.all()
    shoes = Shoe.objects.all()
    clothes = Clothe.objects.all()

    # Combine all the products into a single context
    context = {
        'books': books,
        'mobile_phones': mobile_phones,
        'shoes': shoes,
        'clothes' : clothes
    }

    return render(request, 'landing_page.html', context)
