from django.db import models
from django.contrib.auth.models import AbstractUser


#USER
class UserRole(models.TextChoices):
    GUEST = 'GUEST', 'Guest'
    USER = 'USER', 'User'
    STAFF = 'STAFF', 'Staff'
    ADMIN = 'ADMIN', 'Admin'

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.GUEST)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return self.email or self.username
    
#TABLE
class DiningTable(models.Model):
    qr = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f"Table {self.id}"

#CATEGORY
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
#PRODUCT
class Product(models.Model):
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="product_pics/", blank=True, null=True)

    class Meta:
    # Optional: Ensure product names are unique within a category
        unique_together = ("category", "name")
    def __str__(self):
        return self.name
    
#ORDER
class OrderStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    SERVED = 'SERVED', 'Served'
    COMPLETED = 'COMPLETED', 'Completed'
    CANCELLED = 'CANCELLED', 'Cancelled'

class Order(models.Model):
    user = models.ForeignKey(CustomUser, related_name="orders", on_delete=models.PROTECT)
    table = models.ForeignKey(DiningTable, related_name="orders", on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING, db_index=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # optional but recommended
    updated_at = models.DateTimeField(auto_now=True)      # optional but recommended

    # Many-to-many through table for order items
    products = models.ManyToManyField(Product, through="OrderProduct", related_name="orders")

    def __str__(self):
        return f"Order {self.id} by {self.user}"
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("order", "product")  # one line per product per order

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order_id})"
    
