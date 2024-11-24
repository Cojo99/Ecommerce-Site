from rest_framework import serializers
from .models import Product

#create serializer with classes
class ProductSerializer(serializers.ModelSerializer):
    #image = serializers.ImageField(max_length=None, use_url=True)
    class Meta:
        model = Product
        fields = ['id','name', 'sizes', 'gender', 'category', 'stock']   
    #image = models.ImageField(upload_to='product_images/')