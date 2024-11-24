from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):

    def __str__(self):
            return self.name

    Category_choices = [
        ('shorts', 'Shorts'),
        ('shirts', 'Shirts')
    ]

    Gender_choices = [
        ('men', "Men's"),
        ('women', "Women's")
    ]

    name = models.CharField(max_length=200)
    #image = models.ImageField(upload_to='product_images/')
    sizes = models.JSONField()  # Example: ["S", "M", "L"]
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, choices=Gender_choices)
    category = models.CharField(max_length=10, choices=Category_choices)
    stock = models.PositiveIntegerField()


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size})"