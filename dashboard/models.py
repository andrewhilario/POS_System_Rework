from django.db import models
from cloudinary.models import CloudinaryField

# Import
import random
import string


# Create your models here.
class Store(models.Model):
    store_name = models.CharField(max_length=100)
    store_address = models.CharField(max_length=100)
    store_manager = models.CharField(max_length=100)
    store_slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    store_image = CloudinaryField("image")
    store_created = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.store_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100, null=True, blank=True)
    category_code = models.CharField(max_length=6, unique=True, null=True, blank=True)
    category_description = models.TextField(max_length=1000, blank=True)
    category_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category_created = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    product_name = models.CharField(max_length=100)
    product_slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    product_description = models.TextField(max_length=1000, blank=True)
    product_stock = models.IntegerField(blank=True, null=True)
    product_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    product_image = CloudinaryField("image")
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    product_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product_created = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.product_name


class Order(models.Model):
    order_id = models.CharField(max_length=100)
    order_date = models.DateTimeField(blank=True, null=True)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    order_store = models.ForeignKey(Store, on_delete=models.CASCADE)
    order_completed = models.BooleanField(default=False)
    order_void = models.BooleanField(default=False)
    order_created = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.order_id + " - " + self.order_store.store_name


class OrderItem(models.Model):
    order_item_id = models.CharField(max_length=100)
    order_item_order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    order_item_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_item_quantity = models.IntegerField()
    order_item_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    order_item_total = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    order_item_created = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.order_item_product.product_name
