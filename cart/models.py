from pymongo import MongoClient  # Import pymongo để truy xuất dữ liệu từ MongoDB
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from customer.models import Customer
from bson import ObjectId  # Import ObjectId để lưu ID từ MongoDB

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Lưu kiểu dữ liệu
    object_id = models.CharField(max_length=50)  # Lưu ID dưới dạng string (ObjectId từ MongoDB)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        client = MongoClient("mongodb://localhost:27017/")
        db = client['manh_project2']
        collection = db['book']  # Tên collection của Book trong MongoDB

        product = collection.find_one({"_id": ObjectId(self.object_id)})
        if product:
            return self.quantity * float(product['price'])  # Chuyển về float nếu cần
        return 0

    def __str__(self):
        return f"Cart for {self.customer.username} - Product ID: {self.object_id}"
