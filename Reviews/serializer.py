from rest_framework import serializers
from .models import Review
from SiteUser.models import SiteUser

class SiteUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username') 

    class Meta:
        model = SiteUser
        fields = ['id', 'username', 'avatar']

class ReviewSerializer(serializers.ModelSerializer):
    user = SiteUserSerializer(read_only=True) 

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
