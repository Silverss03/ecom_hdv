from django.urls import path
from .views import order_history, place_order

urlpatterns = [
    path('history/', order_history, name='order_history'),
    path('place/', place_order, name='place_order'),
]
