from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Cart
# from book.models import Book
from order.models import Order, OrderItem
from book.models import Book
from clothes.models import Clothe
from phone.models import Phone
from shoes.models import Shoe
from customer.models import Customer

def add_to_cart(request, product_id, product_type):
    customer = request.user  # Directly assign request.user

    # Get the product model using ContentType
    content_type = get_object_or_404(ContentType, model=product_type)
    product = get_object_or_404(content_type.model_class(), id=product_id)

    # Get or create the cart item
    cart_item, created = Cart.objects.get_or_create(
        customer=customer, 
        content_type=content_type, 
        object_id=product_id
    )

    # Increase quantity
    # cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_detail')

def cart_detail(request):
    cart_items = Cart.objects.filter(customer=request.user)
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items})

def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.quantity += 1
    cart_item.save()
    
    # Cập nhật tổng giá trị đơn hàng
    cart_item.total_price = cart_item.quantity * cart_item.product.price

    return redirect('cart_detail')

def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        
        # Cập nhật tổng giá trị đơn hàng
        cart_item.total_price = cart_item.quantity * cart_item.product.price
    else:
        cart_item.delete()

    return redirect('cart_detail')

def place_order(request):
    customer = request.user
    cart_items = Cart.objects.filter(customer=customer)

    if not cart_items.exists():
        return redirect('cart_detail')  # Nếu giỏ hàng trống, quay lại trang giỏ hàng

    # Tạo đơn hàng mới
    order = Order.objects.create(user=customer, total_price=0)
    total_price = 0

    for cart_item in cart_items:
        product = cart_item.content_type.get_object_for_this_type(id=cart_item.object_id)  # Lấy sản phẩm thực tế
        content_type = cart_item.content_type  # Lấy ContentType

        order_item = OrderItem.objects.create(
            order=order,
            content_type=content_type,
            object_id=product.id,
            quantity=cart_item.quantity,
            price=cart_item.quantity * product.price
        )
        total_price += order_item.price

    # Cập nhật tổng giá trị đơn hàng
    order.total_price = total_price
    order.save()

    # Xóa giỏ hàng sau khi đặt hàng
    cart_items.delete()

    return redirect('order_history')


def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    order_data = []  # Danh sách chứa dữ liệu đầy đủ của mỗi đơn hàng
    
    for order in orders:
        items = []  # Danh sách chứa dữ liệu đầy đủ của mỗi sản phẩm trong đơn hàng
        
        for item in order.items.all():
            product = item.content_type.get_object_for_this_type(id=item.object_id)

            # Kiểm tra loại sản phẩm để lấy đúng thuộc tính tên
            if isinstance(product, Book):
                product_name = product.title
            else:
                product_name = getattr(product, 'name', 'Unknown')

            items.append({
                "quantity": item.quantity,
                "product_name": product_name,
                "price": item.price
            })

        order_data.append({
            "id": order.id,
            "created_at": order.created_at,
            "total_price": order.total_price,
            "status": order.status,
            "items": items  # Gửi danh sách sản phẩm đã xử lý
        })

    return render(request, 'order/order_history.html', {"orders": order_data})

def checkout(request):
    customer = request.user
    cart_items = Cart.objects.filter(customer=customer)  # Lấy giỏ hàng từ DB

    processed_cart_items = []  # Danh sách mới để chứa dữ liệu đầy đủ

    # Tính tổng giá
    total_price = 0
    for item in cart_items:
        product = item.content_type.get_object_for_this_type(id=item.object_id)
        
        # Kiểm tra nếu là sách thì lấy `title`, còn lại lấy `name`
        if isinstance(product, Book):
            product_name = product.title
        else:
            product_name = getattr(product, 'name', 'Unknown')

        processed_cart_items.append({
            "name": product_name,
            "quantity": item.quantity,
            "price": product.price,
            "total_price": item.quantity * product.price
        })

        total_price += item.quantity * product.price

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # ✅ Chuyển giỏ hàng sang đơn hàng
        order = Order.objects.create(user=customer, total_price=total_price)

        for item in cart_items:
            product = item.content_type.get_object_for_this_type(id=item.object_id)
            OrderItem.objects.create(
                order=order,
                content_type=item.content_type,
                object_id=product.id,
                quantity=item.quantity,
                price=item.quantity * product.price
            )

        # ✅ Xóa giỏ hàng sau khi đặt hàng
        cart_items.delete()

        return render(request, 'order/thankyou.html')

    return render(request, 'order/checkout.html', {'cart_items': processed_cart_items, 'total_price': total_price})




