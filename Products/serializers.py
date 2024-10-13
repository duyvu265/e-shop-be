from rest_framework import serializers
from .models import Product
from ProductsCategory.serializers import ProductCategorySerializer  

# Serializer cho sản phẩm
class ProductSerializer(serializers.ModelSerializer):  
    category = ProductCategorySerializer()  
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'product_image', 'created_at', 'updated_at', 'category']
