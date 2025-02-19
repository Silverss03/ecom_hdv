from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Customer

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        customer = Customer.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'customer/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)  # Debugging output
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('landing_page')
        else:
            print("Authentication failed!")  # Debugging output
            return render(request, 'customer/login.html', {'error': 'Invalid credentials'})

    return render(request, 'customer/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')
