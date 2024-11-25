from rest_framework import serializers
from .models import ChatSession, Message, TypingStatus, Notification
from django.contrib.auth.models import User
from SiteUser.models import SiteUser

class SiteUserSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(source='user.is_staff', read_only=True)

    class Meta:
        model = SiteUser
        fields = ['id', 'user', 'avatar', 'phone_number', 'user_type', 'is_admin']

class MessageSerializer(serializers.ModelSerializer):
    sender = SiteUserSerializer(read_only=True)  

    class Meta:
        model = Message
        fields = ['id', 'chat_session', 'sender', 'message', 'timestamp', 'is_read', 'is_sent', 'attachments', 'status']
        read_only_fields = ['id', 'timestamp']

class ChatSessionSerializer(serializers.ModelSerializer):
    participants = SiteUserSerializer(many=True, read_only=True) 

    class Meta:
        model = ChatSession
        fields = ['id', 'participants', 'created_at']
        read_only_fields = ['id', 'created_at']

class TypingStatusSerializer(serializers.ModelSerializer):
    user = SiteUserSerializer(read_only=True)  

    class Meta:
        model = TypingStatus
        fields = ['id', 'user', 'chat_session', 'is_typing']


class NotificationSerializer(serializers.ModelSerializer):
    user = SiteUserSerializer(read_only=True)  
    message = MessageSerializer(read_only=True)  

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'is_read', 'timestamp']
        read_only_fields = ['id', 'timestamp']
