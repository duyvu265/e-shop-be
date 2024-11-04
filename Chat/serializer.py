from rest_framework import serializers
from .models import ChatSession, Message
from SiteUser.models import SiteUser

class ChatSessionSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=SiteUser.objects.all(), many=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'participants', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=SiteUser.objects.all())
    chat_session = serializers.PrimaryKeyRelatedField(queryset=ChatSession.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'chat_session', 'sender', 'message', 'timestamp', 'is_read', 'attachments']
