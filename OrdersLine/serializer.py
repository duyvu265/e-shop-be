from rest_framework import serializers
from .models import OrderLine

class OrderLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLine
        fields = ['id', 'order', 'product_item', 'qty', 'price']  # Chọn các trường bạn muốn hiển thị

    def create(self, validated_data):
        """Tạo một dòng đơn hàng mới."""
        return OrderLine.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Cập nhật thông tin dòng đơn hàng."""
        instance.order = validated_data.get('order', instance.order)
        instance.product_item = validated_data.get('product_item', instance.product_item)
        instance.qty = validated_data.get('qty', instance.qty)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

    def validate_qty(self, value):
        """Kiểm tra số lượng đơn hàng không lớn hơn số lượng trong kho."""
        if value <= 0:
            raise serializers.ValidationError("Số lượng phải lớn hơn 0.")
        return value

    def validate(self, attrs):
        """Kiểm tra số lượng đơn hàng với kho."""
        product_item = attrs.get('product_item')
        qty = attrs.get('qty')
        
        if product_item and qty > product_item.qty_in_stock:
            raise serializers.ValidationError("Số lượng trong đơn hàng không thể lớn hơn số lượng trong kho.")
        
        return attrs
