from rest_framework import serializers
from .models import ShippingMethod

class ShippingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingMethod
        fields = ['id', 'name', 'cost']  # Chọn các trường bạn muốn hiển thị

    def create(self, validated_data):
        """Tạo một phương thức vận chuyển mới."""
        return ShippingMethod.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Cập nhật thông tin phương thức vận chuyển."""
        instance.name = validated_data.get('name', instance.name)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.save()
        return instance
