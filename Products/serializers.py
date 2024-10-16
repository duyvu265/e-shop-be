from rest_framework import serializers
from .models import Product, ProductImage
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['url']  
class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()  
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'quantity', 'images']
    def get_images(self, obj):
        return {f'image{i+1}': img.url for i, img in enumerate(obj.images.all())}
