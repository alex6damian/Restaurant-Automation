from django.test import TestCase
from django.db import IntegrityError
from .models import Category, Product, Order, CustomUser, DiningTable, OrderProduct

class DbSmokeTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="tester", email="tester@example.com", password="x")
        self.table = DiningTable.objects.create(qr="T-DB", capacity=2)

    def test_product_requires_category(self):
        cat = Category.objects.create(name="Drinks")
        prod = Product.objects.create(name="Water", price="1.00", category=cat)
        self.assertEqual(prod.category, cat)

    def test_product_name_unique_within_category(self):
        cat = Category.objects.create(name="Desserts")
        Product.objects.create(name="Cake", price="3.50", category=cat)
        with self.assertRaises(IntegrityError):
            Product.objects.create(name="Cake", price="3.50", category=cat)

    def test_order_product_unique_line_per_product(self):
        cat = Category.objects.create(name="Mains")
        prod = Product.objects.create(name="Burger", price="9.99", category=cat)
        order = Order.objects.create(user=self.user, table=self.table)
        OrderProduct.objects.create(order=order, product=prod, quantity=1)
        with self.assertRaises(IntegrityError):
            OrderProduct.objects.create(order=order, product=prod, quantity=2)