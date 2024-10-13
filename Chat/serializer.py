from rest_framework import serializers
from .models import Chat
from SiteUser.serializer import SiteUserSerializer  # Giả định bạn đã có SiteUserSerializer

class ChatSerializer(serializers.ModelSerializer):
    customer = SiteUserSerializer()  # Serializer cho người dùng là khách hàng
    seller = SiteUserSerializer()    # Serializer cho người dùng là người bán

    class Meta:
        model = Chat
        fields = ['customer', 'seller', 'message', 'timestamp']
