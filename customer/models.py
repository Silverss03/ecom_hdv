# customer/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Customer(AbstractUser):  # Subclass AbstractUser to extend the User model
    # Add any additional fields you want for the customer
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    # Add other fields that are specific to your customer

    def __str__(self):
        return self.username