from django.urls import path
from .views import add_to_cart, cart_detail
from .views import increase_quantity, decrease_quantity, order_history, checkout
from landing.views import landing_page

urlpatterns = [
    path('add/<str:product_type>/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('detail/', cart_detail, name='cart_detail'),
    path('increase/<int:cart_id>/', increase_quantity, name='increase_quantity'),
    path('decrease/<int:cart_id>/', decrease_quantity, name='decrease_quantity'),
    path('history/', order_history, name='order_history'),
    path('checkout/', checkout, name='checkout'),
    path('', landing_page, name='landing_page'),
]
