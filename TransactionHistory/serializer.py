from rest_framework import serializers
from .models import TransactionHistory
from SiteUser.models import SiteUser
from ShopOrder.models import ShopOrder

class SiteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteUser
        fields = ['id', 'user', 'avatar', 'phone_number']

class ShopOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopOrder
        fields = ['id', 'order_details', 'total_amount', 'order_date']  # Thay đổi các trường này theo model của bạn

class TransactionHistorySerializer(serializers.ModelSerializer):
    site_user = SiteUserSerializer(read_only=True)
    order = ShopOrderSerializer(read_only=True)

    class Meta:
        model = TransactionHistory
        fields = ['site_user', 'order', 'transaction_date', 'amount', 'payment_status']
