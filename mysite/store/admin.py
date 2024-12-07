from django.contrib import admin
from .models import Product, CartItem

# Register your models here.
# admin.site.register(Product)
admin.site.register(CartItem)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'gender', 'price', 'stock')
    list_filter = ('category', 'gender')
    search_fields = ('name', 'category')