from rest_framework import serializers
from .models import ShopOrder
from SiteUser.models import SiteUser, Address, UserPaymentMethod
from Orders.models import OrderStatus

class SiteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteUser
        fields = ['id', 'user', 'avatar', 'phone_number']  # Thay đổi các trường này theo model của bạn

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'postal_code', 'country']  # Thay đổi các trường này theo model của bạn

class UserPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPaymentMethod
        fields = ['id', 'card_number', 'expiry_date', 'cvv']  # Thay đổi các trường này theo model của bạn

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ['id', 'status']  # Thay đổi các trường này theo model của bạn

class ShopOrderSerializer(serializers.ModelSerializer):
    site_user = SiteUserSerializer(read_only=True)
    shipping_address = AddressSerializer(read_only=True)
    payment_method = UserPaymentMethodSerializer(read_only=True)
    order_status = OrderStatusSerializer(read_only=True)

    class Meta:
        model = ShopOrder
        fields = ['id', 'site_user', 'order_date', 'payment_method', 'shipping_address', 'shipping_method', 'order_total', 'order_status']

    def create(self, validated_data):
        # Chỉ tạo đơn hàng mới nếu cần thiết
        return ShopOrder.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Cập nhật đơn hàng nếu cần thiết
        instance.shipping_method = validated_data.get('shipping_method', instance.shipping_method)
        instance.order_total = validated_data.get('order_total', instance.order_total)
        instance.order_status = validated_data.get('order_status', instance.order_status)
        instance.save()
        return instance
