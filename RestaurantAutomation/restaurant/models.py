from django.db import models
from django.contrib.auth.models import AbstractUser
# models

class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=True) # True for customers, False for staff
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    validated = models.BooleanField(default=False)

    def __str__(self):
        return self.email

class Product(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='product_pics/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name