# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from .models import Order, OrderItem
from book.models import Book
from clothes.models import Clothe
from phone.models import Phone
from shoes.models import Shoe

@login_required
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')  # Chuyển hướng về giỏ hàng nếu rỗng

    order = Order.objects.create(user=request.user, total_price=0)
    total_price = 0

    for product_key, item in cart.items():
        model_name, product_id = product_key.split('_')  # Tách "book_1" thành ("book", 1)
        model_class = {
            'book': Book,
            'clothes': Clothe,
            'phone': Phone,
            'shoe': Shoe
        }.get(model_name)

        if model_class:
            product = model_class.objects.get(id=int(product_id))
            content_type = ContentType.objects.get_for_model(model_class)

            order_item = OrderItem.objects.create(
                order=order, content_type=content_type, object_id=product.id,
                quantity=item['quantity'], price=product.price * item['quantity']
            )
            total_price += order_item.price

    order.total_price = total_price
    order.save()

    request.session['cart'] = {}  # Xóa giỏ hàng sau khi đặt hàng
    return redirect('order_history')
