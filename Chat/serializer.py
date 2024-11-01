from rest_framework import serializers
from .models import Chat

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'customer', 'seller', 'message', 'timestamp', 'is_read', 'attachments']
        read_only_fields = ['timestamp', 'customer']
