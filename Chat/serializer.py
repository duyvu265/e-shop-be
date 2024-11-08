from rest_framework import serializers
from .models import ChatSession, Message, TypingStatus
from SiteUser.models import SiteUser

class ChatSessionSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(queryset=SiteUser.objects.all(), many=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'participants', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=SiteUser.objects.all())
    chat_session = serializers.PrimaryKeyRelatedField(queryset=ChatSession.objects.all())
    status = serializers.ChoiceField(choices=Message.STATUS_CHOICES, required=False)  # Thêm trạng thái tin nhắn

    class Meta:
        model = Message
        fields = ['id', 'chat_session', 'sender', 'message', 'timestamp', 'is_read', 'attachments', 'status']

class TypingStatusSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=SiteUser.objects.all())
    chat_session = serializers.PrimaryKeyRelatedField(queryset=ChatSession.objects.all())
    is_typing = serializers.BooleanField()

    class Meta:
        model = TypingStatus
        fields = ['user', 'chat_session', 'is_typing']
