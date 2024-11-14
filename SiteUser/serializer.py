from rest_framework import serializers
from django.contrib.auth.models import User
from .models import SiteUser, Address, UserPaymentMethod

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name','is_active']

class SiteUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SiteUser
        fields = ['user', 'avatar', 'phone_number','liked_products','user_type']
