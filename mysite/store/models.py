from django.db import models

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