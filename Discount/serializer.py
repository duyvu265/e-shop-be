from rest_framework import serializers
from .models import Discount
import datetime

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'code', 'amount', 'expiration_date', 'is_active', 
                  'applicable_to', 'product', 'category', 'user_group', 'min_quantity', 'description']
    
    def create(self, validated_data):
        return Discount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.applicable_to = validated_data.get('applicable_to', instance.applicable_to)
        instance.product = validated_data.get('product', instance.product)
        instance.category = validated_data.get('category', instance.category)
        instance.user_group = validated_data.get('user_group', instance.user_group)
        instance.min_quantity = validated_data.get('min_quantity', instance.min_quantity)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

    def validate_code(self, value):
        if not value:
            raise serializers.ValidationError("Mã giảm giá không được để trống.")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Số tiền giảm giá phải lớn hơn 0.")
        return value

    def validate_expiration_date(self, value):
        if value <= datetime.date.today():
            raise serializers.ValidationError("Ngày hết hạn phải lớn hơn ngày hiện tại.")
        return value

    def validate_user_group(self, value):
        valid_groups = ['admin', 'super_admin', 'customer', 'manager', 'staff']
        if value not in valid_groups:
            raise serializers.ValidationError(f"Nhóm người dùng '{value}' không hợp lệ.")
        return value

    def validate_min_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Số lượng sản phẩm tối thiểu phải lớn hơn hoặc bằng 1.")
        return value
