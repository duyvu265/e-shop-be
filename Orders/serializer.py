from rest_framework import serializers
from .models import OrderStatus

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ['id', 'status']  # Chọn các trường bạn muốn hiển thị

    def create(self, validated_data):
        """Tạo một trạng thái đơn hàng mới."""
        return OrderStatus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Cập nhật thông tin trạng thái đơn hàng."""
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

    def validate_status(self, value):
        """Kiểm tra trạng thái không được để trống."""
        if not value:
            raise serializers.ValidationError("Trạng thái không được để trống.")
        return value
