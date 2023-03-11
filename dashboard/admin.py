from django.contrib import admin
from .models import Store, Category, Product, Order, OrderItem
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'product_store')
    list_filter = ('product_name', 'product_price', 'product_store')
    search_fields = ('product_name', 'product_price', 'product_store')
    list_per_page = 10

class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'store_address', 'store_manager')
    list_filter = ('store_name', 'store_address', 'store_manager')
    search_fields = ('store_name', 'store_address', 'store_manager')
    list_per_page = 10

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_store')
    list_filter = ('category_name', 'category_store')
    search_fields = ('category_name', 'category_store')
    list_per_page = 10

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_date', 'order_total', 'order_store')
    list_filter = ('order_id', 'order_date', 'order_total', 'order_store')
    search_fields = ('order_id', 'order_date', 'order_total', 'order_store')
    list_per_page = 10

admin.site.register(Store, StoreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product , ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
