from rest_framework import serializers
from .models import Discount
import datetime

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'code', 'amount', 'expiration_date', 'is_active']  # Chọn các trường bạn muốn hiển thị

    def create(self, validated_data):
        """Tạo một mã giảm giá mới."""
        return Discount.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Cập nhật thông tin mã giảm giá."""
        instance.code = validated_data.get('code', instance.code)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.expiration_date = validated_data.get('expiration_date', instance.expiration_date)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

    def validate_code(self, value):
        """Kiểm tra mã giảm giá không được để trống và có độ dài hợp lệ."""
        if not value:
            raise serializers.ValidationError("Mã giảm giá không được để trống.")
        return value

    def validate_amount(self, value):
        """Kiểm tra số tiền giảm giá không được nhỏ hơn hoặc bằng 0."""
        if value <= 0:
            raise serializers.ValidationError("Số tiền giảm giá phải lớn hơn 0.")
        return value

    def validate_expiration_date(self, value):
        """Kiểm tra ngày hết hạn phải lớn hơn ngày hiện tại."""
        if value <= datetime.date.today():
            raise serializers.ValidationError("Ngày hết hạn phải lớn hơn ngày hiện tại.")
        return value
