from rest_framework import serializers
from .models import ProductItem

class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = ['id', 'product', 'SKU', 'qty_in_stock', 'price', 'created_at', 'updated_at', 'color', 'size']  # Chọn các trường bạn muốn hiển thị

    def create(self, validated_data):
        """Tạo một sản phẩm cụ thể mới."""
        return ProductItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Cập nhật thông tin sản phẩm cụ thể."""
        instance.product = validated_data.get('product', instance.product)
        instance.SKU = validated_data.get('SKU', instance.SKU)
        instance.qty_in_stock = validated_data.get('qty_in_stock', instance.qty_in_stock)
        instance.price = validated_data.get('price', instance.price)
        instance.color = validated_data.get('color', instance.color)
        instance.size = validated_data.get('size', instance.size)
        instance.save()
        return instance
