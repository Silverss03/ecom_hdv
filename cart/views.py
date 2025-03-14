from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Cart
from order.models import Order, OrderItem
from pymongo import MongoClient
from bson import ObjectId
from customer.models import Customer

def add_to_cart(request, product_id, product_type):
    customer = request.user
    content_type = get_object_or_404(ContentType, model=product_type)

    # Kết nối với MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client['manh_project2']
    collection = db['book']

    try:
        product_id_int = int(product_id)  # Convert to int if using 'id'
        product = collection.find_one({"id": product_id_int})  # Query using 'id'

    except (ValueError, TypeError):
        return redirect('cart_detail')

    if not product:
        return redirect('cart_detail')

    # **Ensure object_id is always stored as a STRING**
    cart_item, created = Cart.objects.get_or_create(
        customer=customer, 
        content_type=content_type, 
        object_id=str(product['_id'])  # 🔹 Store ObjectId as string
    )

    cart_item.save()
    return redirect('cart_detail')

def cart_detail(request):
    client = MongoClient("mongodb://localhost:27017/")
    db = client['manh_project2']
    collection = db['book']

    cart_items = Cart.objects.filter(customer=request.user)

    processed_cart_items = []
    for item in cart_items:
        try:
            product = collection.find_one({"_id": ObjectId(item.object_id)})
        except Exception as e:
            print(f"Error fetching product {item.object_id}: {e}")
            product = None

        if product:
            processed_cart_items.append({
                "id": item.id,
                "name": product.get("title", "Unknown"),  # ✅ Thêm tên sách
                "image": product.get("image", ""),  # ✅ Thêm đường dẫn hình ảnh
                "quantity": item.quantity,
                "price": float(product.get("price", 0)),
                "total_price": item.quantity * float(product.get("price", 0))
            })

    return render(request, 'cart/cart_detail.html', {'cart_items': processed_cart_items})

def checkout(request):
    customer = request.user
    cart_items = Cart.objects.filter(customer=customer)

    client = MongoClient("mongodb://localhost:27017/")
    db = client['manh_project2']
    collection = db['book']

    processed_cart_items = []
    total_price = 0

    for item in cart_items:
        product = collection.find_one({"_id": ObjectId(item.object_id)}) # 🔹 Tìm theo `id`
        if product:
            processed_cart_items.append({
                "id": item.id,
                "name": product.get("title", "Unknown"),  # ✅ Thêm tên sách
                "image": product.get("image", ""),  # ✅ Thêm đường dẫn hình ảnh
                "quantity": item.quantity,
                "price": float(product.get("price", 0)),
                "total_price": item.quantity * float(product.get("price", 0))
            })
            total_price += item.quantity * float(product["price"])

    if request.method == 'POST':
        order = Order.objects.create(user=customer, total_price=total_price)
        for item in cart_items:
            product = collection.find_one({"_id": ObjectId(item.object_id)})    # 🔹 Tìm theo `id`
            if product:
                OrderItem.objects.create(
                    order=order,
                    product_id=str(item.object_id),  # Chuyển ObjectId thành chuỗi
                    product_name=product["title"],  # Lưu tên sản phẩm
                    quantity=item.quantity,
                    price=item.quantity * float(product["price"])
                )

        for item in cart_items:
            item.delete()
        return render(request, 'order/thankyou.html')

    return render(request, 'order/checkout.html', {'cart_items': processed_cart_items, 'total_price': total_price})

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



def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    client = MongoClient("mongodb://localhost:27017/")
    db = client['manh_project2']
    collection = db['book']

    order_data = []  # Danh sách chứa dữ liệu đầy đủ của mỗi đơn hàng

    for order in orders:
        items = []  # Danh sách chứa dữ liệu đầy đủ của mỗi sản phẩm trong đơn hàng

        for item in order.items.all():
            product = collection.find_one({"_id": ObjectId(item.product_id)})  # 🔹 Tìm theo `id`
            product_name = product["title"] if product else "Unknown"

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