# cart/models.py
from django.db import models
from customer.models import Customer  # Import the custom Customer model
from book.models import Book

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from customer.models import Customer

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Store product type
    object_id = models.PositiveIntegerField()  # Store product ID
    product = GenericForeignKey('content_type', 'object_id')  # Generic relation
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

# class Cart(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     book = models.ForeignKey(Book, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"Cart for {self.customer.username} - {self.book.title}"